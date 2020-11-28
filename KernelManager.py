import aiml
class KernelManager:
    def __init__(self):
        self.kernel = aiml.Kernel()
        self.kernel.learn("std-startup.xml")
        self.kernel.respond("load aiml b")

    def handle_kernel_response(self, text):
        resp = self.kernel.respond(text)
        if self.is_special_command(resp):
            resp = self.handle_command(resp)
        return resp

    def is_special_command(self, text):
        return text[0] == '['

    def split_args(self, args):
        result = []
        for arg in args.split('|'):
            result.append(arg.strip(" "))
        return result

    def handle_command(self, text):
        command, args = text[1:].split(']')
        display_msg = ""
        if command == 'save complaint':
            name, reason = self.split_args(args)
            entry = {"table": "complaints", "name": name, "reason": reason}
            print(entry)
            display_msg = f"Skarga zostala zapisana.\n Pracownik: {name}, Powod: {reason}"
        if command == 'save client':
            name, surname = self.split_args(args)
            name = name.strip()
            surname = surname.strip()
            entry = {"table": "clients", "name": name, "surname": surname}
            print(entry)
            display_msg = f"Zostales zapisany.\nImie: {name}, Nazwisko: {surname}"
        if command == 'book visit':
            client_name, barber_name, date = self.split_args(args)
            entry = {"table": "bookings", "client_name": client_name, "barber_name": barber_name, "date": date}
            print(entry)
            display_msg = f"Zostales umowiony.\n Fryzjer: {barber_name}, na date: {date}"
        if command == 'check visit':
            barber_name = args.strip()
            # choose randomly a free day
            # print(entry)
            # display_msg = f"Zostales zapisany.\nImie: {name}, Nazwisko: {surname}"
        return display_msg