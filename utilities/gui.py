import threading
import tkinter as tk
from tkinter import scrolledtext, ttk


class ChatGUI:
    """
    A class to create and manage the Graphical User Interface for the chat application.

    Attributes:
        window (tk.Tk): The main window of the application.
        top_frame (ttk.Frame): The top frame of the window, containing the chat history.
        bottom_frame (ttk.Frame): The bottom frame of the window, containing input and send button.
        chat_history (scrolledtext.ScrolledText): The text area to display chat history.
        user_input (ttk.Entry): The entry widget for user input.
        send_button (ttk.Button): The button to send messages.
        loading_label (ttk.Label): A label to indicate processing of messages.
    """

    def __init__(self, model):
        """
        Initializes the ChatGUI with a specified model.

        Args:
            model (str): The name of the model to be used for chatting.
        """
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
        self._flashing_after_id = None

    def show_loading_indicator(self):
        """ Show the loading indicator. """
        self.loading_label.config(foreground="red", text="Processing...")
        self.loading_label.pack(side=tk.RIGHT, padx=10)  # Make sure the label is packed
        self._flash_loading_label()

    def hide_loading_indicator(self):
        """ Hide the loading indicator. """
        if self._flashing_after_id is not None:
            self.loading_label.after_cancel(self._flashing_after_id)
        self.loading_label.pack_forget()

    def _flash_loading_label(self):
        """ Create a flashing effect for the loading label. """
        current_color = self.loading_label.cget("foreground")
        next_color = "white" if current_color == "red" else "red"
        self.loading_label.config(foreground=next_color)
        # Schedule the next color change
        self._flashing_after_id = self.loading_label.after(500, self._flash_loading_label)

    def send_message(self):
        """
        Retrieves user input and initiates the process of sending a message.
        """
        user_message = self.get_user_input()
        if user_message:
            self.update_chat_history(f"User: {user_message}\n", 'user')  # Immediate display of user message
            self.loading_label.pack(side=tk.RIGHT, padx=10)  # Show loading indicator
            threading.Thread(target=self.process_message, args=(user_message,)).start()

    def set_send_message_action(self, action):
        """
        Sets the action to be performed when the send button is clicked or Enter is pressed.

        Args:
            action (function): The function to be called when a message is sent.
        """
        self.send_message = action
        self.send_button.config(command=self.send_message)
        self.window.bind('<Return>', lambda event: self.send_message())

    def process_message(self, user_message):
        """
        Processes the user message and updates the chat history.

        Args:
            user_message (str): The message entered by the user.
        """
        # Update chat history in the main thread with the bot's response
        self.window.after(0, lambda: self.update_chat_history(f"Bot: {user_message}\n", 'bot'))
        self.window.after(0, self.loading_label.pack_forget)  # Hide loading indicator

    def update_chat_history(self, message, tag) -> None:
        """
        Updates the chat history text area with a new message.

        Args:
            message (str): The message to be added to the chat history.
            tag (str): The tag ('user' or 'bot') indicating the sender of the message.
        """
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message, tag)
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def get_user_input(self):
        """
        Retrieves the message entered by the user in the input field.

        Returns:
            str: The message entered by the user.
        """
        message = self.user_input.get()
        self.user_input.delete(0, tk.END)
        return message

    def run(self):
        """
        Starts the main loop of the application, displaying the GUI.
        """
        self.window.mainloop()
