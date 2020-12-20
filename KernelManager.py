import csv
import random
from datetime import timedelta, date

import aiml
import pandas as pd

class KernelManager:
    def __init__(self):
        self.kernel = aiml.Kernel()
        self.kernel.learn("std-startup.xml")
        self.kernel.respond("load aiml b")
        self.complaints_filename = "complaints.csv"
        self.bookings_df = self.load_bookings("bookings.csv")
        self.cached_date = None

    def handle_kernel_response(self, text):
        resp = self.kernel.respond(text)
        if self.is_special_command(resp):
            resp = self.handle_command(resp)
        return resp

    def handle_command(self, text):
        prefix, command, args = self.split_command(text)
        display_msg = prefix+"\n" if prefix else ""
        if command == 'save complaint':
            display_msg += self.save_complaint(args)
        if command == 'book visit':
            display_msg += self.book_visit(args)
        if command == 'propose date':
            display_msg += self.propose_date(args)

        return display_msg

    def save_complaint(self, args):
        name, reason = args
        self.insert_complaint(name, reason)
        return f"Skarga zostala zapisana.\n Pracownik: {name}, Powod: {reason}"

    def insert_complaint(self, name, reason):
        with open(self.complaints_filename, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([name, reason])

    def book_visit(self, args):
        assert self.cached_date, "Data nie zostala wybrana"
        client_name, barber_name = args
        barber_name = self.to_proper_name(barber_name)
        self.insert_booking(self.cached_date, barber_name, client_name)
        return f"Zostales umowiony.\n Fryzjer: {barber_name}, na dzien: {self.cached_date}.\n Dziekujemy za zlozenie rezerwacji"

    def insert_booking(self, cached_date, barber_name, client_name):
        self.bookings_df.loc[len(self.bookings_df)] = [cached_date, barber_name, client_name]
        self.bookings_df.to_csv("bookings.csv", sep=';')

    def propose_date(self, args):
        barber_name = self.to_proper_name(args[0])
        self.cached_date = self.get_random_free_date(barber_name)
        return f"Proponuje termin {self.cached_date}, dobrze?"

    def get_random_free_date(self, barber_name, span_days=14):
        taken = self.bookings_df[self.bookings_df['barber'] == barber_name]['date'].dt.date
        today = date.today()
        taken_14days = taken[(taken>today) & (taken <= today + timedelta(days=span_days))].values
        if len(taken_14days) >= span_days-1:
            return self.get_random_free_date(barber_name, span_days=span_days*2)
        rnd = random.randint(1, span_days)
        new_date = (today + timedelta(days=rnd))
        while new_date in taken:
            rnd = random.randint(1, span_days)
            new_date = (today + timedelta(days=rnd))
        return new_date

    @staticmethod
    def load_bookings(filename):
        return pd.read_csv(filename, delimiter=';', index_col=0, parse_dates=['date'], header=0)

    @staticmethod
    def is_special_command(text) -> bool:
        return '[' in text

    @staticmethod
    def split_command(text: str) -> tuple:
        # command like "some text to display [command name] command | args | separated"
        prefix, rest = text.split('[')
        command, args = rest.split(']')
        args = KernelManager.split_args(args)
        return prefix, command, args

    @staticmethod
    def split_args(args: str) -> list:
        result = []
        for arg in args.split('|'):
            result.append(arg.strip(" "))
        return result

    @staticmethod
    def to_proper_name(txt):
        txt = txt.upper()
        if "KAS" in txt:
            return "KASIA"
        elif "ADAM" in txt:
            return "ADAM"
        elif "MAR" in txt:
            return "MAREK"
        elif "ANET" in txt:
            return "ANETA"
        else:
            return "UNKNOWN"



