from tkinter import Tk, Frame, Scrollbar, Label, END, Text, VERTICAL

from KernelManager import KernelManager


class GUI:

    def __init__(self, root):
        self.root = root
        self.chat_view = None
        self.enter_text_widget = None
        self.join_button = None
        self.init_gui()
        self.kernel = KernelManager()

    def init_gui(self):
        self.root.title("ChatBot")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_chat_entry_box()

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='ABC Hair Salon ChatBot', font=("Bell mt", 14)).pack(side='top', anchor='w')
        self.chat_view = Text(frame, width=60, height=10, font=("Roboto", 12))
        scrollbar = Scrollbar(frame, command=self.chat_view.yview, orient=VERTICAL)
        self.chat_view.config(yscrollcommand=scrollbar.set)
        self.chat_view.bind('<KeyPress>', lambda e: 'break')
        self.chat_view.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Type your message:', font=("Roboto", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=1, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter)
        frame.pack(side='top')

    def on_enter(self, event):
        user_input = self.get_user_input()
        kernel_repsonse = self.kernel.handle_kernel_response(user_input)
        self.display_message(user_input, "user")
        self.display_message(kernel_repsonse, "bot")

    def get_user_input(self):
        return self.enter_text_widget.get(1.0, 'end').strip()

    def display_message(self, text, author):
        msg_formatted = f"{author}> {text}\n"
        self.chat_view.insert('end', msg_formatted)
        self.chat_view.yview(END)
        self.clear_enter_widget()
        return 'break'

    def clear_enter_widget(self):
        self.enter_text_widget.delete(1.0, 'end')

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
