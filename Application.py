from tkinter import Tk, Frame, Scrollbar, Label, END, Text, VERTICAL

from KernelManager import KernelManager


class GUI:

    def __init__(self, root):
        self.root = root
        self.chat_view = None
        self.enter_text_widget = None
        self.init_gui()
        self.kernel = KernelManager()

    def init_gui(self):
        self.root.title("ChatBot")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_chat_entry_box()

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='ABC Hair Salon ChatBot', font=("Bell mt", 14)).pack(side='top', anchor='w', padx=20, pady=5)
        self.chat_view = Text(frame, width=60, height=10, font=("Calibri", 12))
        self.chat_view.tag_configure("user", foreground="#6a8bc4")
        scrollbar = Scrollbar(frame, command=self.chat_view.yview, orient=VERTICAL)
        self.chat_view.config(yscrollcommand=scrollbar.set)
        self.chat_view.bind('<KeyPress>', lambda e: 'break')
        self.chat_view.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Type your message:', font=("Calibri", 12)).pack(side='top', anchor='w', padx=10, pady=0)
        self.enter_text_widget = Text(frame, width=60, height=1, font=("Calibri", 12))
        self.enter_text_widget.pack(side='left', padx=10, pady=5)
        self.enter_text_widget.bind('<Return>', self.on_enter)
        frame.pack(side='top')

    def on_enter(self, event):
        user_input = self.get_user_input()
        kernel_repsonse = self.kernel.handle_kernel_response(user_input)
        self.display_message(user_input, "user", True)
        self.display_message(kernel_repsonse, "bot")

    def get_user_input(self):
        return self.enter_text_widget.get(1.0, 'end').strip()

    def display_message(self, text, author, higlight=False):
        msg_formatted = f"{author}> {text}\n"
        start_ind = self.chat_view.index('insert')
        self.chat_view.insert('end', msg_formatted)
        if higlight:
            self.chat_view.tag_add("user", start_ind, start_ind.replace(".0", ".end"))
        self.chat_view.yview(END)
        self.clear_enter_widget()
        return 'break'

    def clear_enter_widget(self):
        self.enter_text_widget.delete(1.0, 'end')

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
