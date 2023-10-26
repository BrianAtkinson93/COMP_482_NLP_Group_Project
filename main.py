import tkinter as tk
from tkinter import Scrollbar, Text


class ChatbotGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simple Chatbot GUI")
        self.geometry("400x500")

        self.text_widget = Text(self, wrap='word')
        self.text_widget.pack(expand=True, fill='both')
        self.text_widget.configure(state='disabled')

        self.entry_widget = tk.Entry(self)
        self.entry_widget.pack(fill='x')
        self.entry_widget.bind("<Return>", self.on_enter)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack()

    def on_enter(self, event):
        self.send_message()

    def send_message(self):
        user_message = self.entry_widget.get()
        self.entry_widget.delete(0, 'end')
        self.update_chat(f"You: {user_message}")

        # Here you would process the user_message with your LLM and get a response
        # For example: response = process_message_with_llm(user_message)
        response = "Chatbot: I am a simple chatbot."
        self.update_chat(response)

    def update_chat(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert('end', message + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.see('end')


if __name__ == "__main__":
    app = ChatbotGUI()
    app.mainloop()
