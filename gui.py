import threading
import tkinter as tk
from tkinter import scrolledtext, ttk


class ChatGUI:
    def __init__(self, model):
        # self.name = uname
        self.window = tk.Tk()
        self.window.title(f"Chat with {model}")
        self.window.geometry("600x600")

        style = ttk.Style(self.window)
        # ('aqua', 'clam', 'alt', 'default', 'classic')
        try:
            style.theme_use('aqua')
        except tk.TclError:
            style.theme_use('clam')  # Experiment with different themes
        except Exception as e:
            print(f'New Error: {e}')

        # Customize button style
        style.configure('TButton', font=('Arial', 12), background='blue', foreground='white')

        self.top_frame = ttk.Frame(self.window)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame = ttk.Frame(self.window)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.chat_history = scrolledtext.ScrolledText(self.top_frame, wrap=tk.WORD, state='disabled',
                                                      font=("Arial", 14))
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = ttk.Entry(self.bottom_frame, font=("Arial", 14))
        self.user_input.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.send_button = ttk.Button(self.bottom_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10)

        # Loading label (consider replacing with an animated GIF or custom canvas)
        self.loading_label = ttk.Label(self.bottom_frame, text="Processing...", foreground="blue")

        self.chat_history.tag_configure('user', foreground="cyan")
        self.chat_history.tag_configure('bot', foreground="green")

        self.window.bind('<Return>', lambda event: self.send_message())

        self.user_input.focus_set()

    def send_message(self):
        user_message = self.get_user_input()
        if user_message:
            self.update_chat_history(f"User: {user_message}\n", 'user')  # Immediate display of user message
            self.loading_label.pack(side=tk.RIGHT, padx=10)  # Show loading indicator
            threading.Thread(target=self.process_message, args=(user_message,)).start()

    def set_send_message_action(self, action):
        self.send_message = action
        self.send_button.config(command=self.send_message)
        self.window.bind('<Return>', lambda event: self.send_message())

    def process_message(self, user_message):
        # Update chat history in the main thread with the bot's response
        self.window.after(0, lambda: self.update_chat_history(f"Bot: {user_message}\n", 'bot'))
        self.window.after(0, self.loading_label.pack_forget)  # Hide loading indicator

    def update_chat_history(self, message, tag) -> None:
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message, tag)
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def get_user_input(self):
        message = self.user_input.get()
        self.user_input.delete(0, tk.END)
        return message

    def run(self):
        self.window.mainloop()
