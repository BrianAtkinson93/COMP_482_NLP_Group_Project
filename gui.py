import tkinter as tk
from tkinter import scrolledtext


class ChatGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chat with GPT-3.5-turbo")
        self.window.geometry("600x600")

        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.chat_history = scrolledtext.ScrolledText(self.top_frame, wrap=tk.WORD, state='disabled',
                                                      font=("Arial", 14))
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Entry(self.bottom_frame, font=("Arial", 14))
        self.user_input.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.bottom_frame, text="Send")
        self.send_button.pack(side=tk.RIGHT, padx=10)

        self.chat_history.tag_configure('user', foreground="cyan")
        self.chat_history.tag_configure('bot', foreground="green")
        self.chat_history.tag_configure('loading', foreground="gray")

        # Placeholder for send_message method
        self.send_message = lambda: None
        self.window.bind('<Return>', lambda event: self.send_message())

        self.user_input.focus_set()

    def set_send_message_action(self, action):
        """

        :param action:
        :return:
        """
        self.send_message = action
        self.send_button.config(command=self.send_message)

    def update_chat_history(self, message, tag):
        """

        :param message:
        :param tag:
        :return:
        """
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message, tag)
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def get_user_input(self):
        """

        :return:
        """
        message = self.user_input.get()
        self.user_input.delete(0, tk.END)
        return message

    def run(self):
        """

        :return:
        """
        self.window.mainloop()
