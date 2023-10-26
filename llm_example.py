import tkinter as tk
import openai
import os

from fuzzywuzzy import process

# Initialize OpenAI API client
openai.api_key = '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'

# Knowledge base dictionary
knowledge_base = {
    "python": "Python is a high-level, general-purpose programming language.",
    # ... add other knowledge base entries as needed
}


def get_knowledge_base_response(query):
    # Using fuzzy string matching to find the most relevant entry
    best_match, score = process.extractOne(query, knowledge_base.keys())
    if score > 80:  # You can adjust the threshold
        return knowledge_base[best_match]
    return None  # If no good match is found


# List to store all messages for context
messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Create the main window
window = tk.Tk()
window.title("Chat with GPT-3.5-turbo")
window.geometry("500x500")

# Create widgets
chat_history = tk.Text(window, width=60, height=30)
chat_history.pack()

user_input = tk.Entry(window, width=60)
user_input.pack()


def send_message():
    message = user_input.get()
    if message:
        user_input.delete(0, tk.END)  # Clear the entry field
        chat_history.insert(tk.END, f"\nUser: {message}\n")
        messages.append({"role": "user", "content": message})

        # Check the knowledge base first
        kb_response = get_knowledge_base_response(message)
        if kb_response:
            chat_history.insert(tk.END, f"Bot: {kb_response}\n")
        else:
            # If no knowledge base response, send message to GPT-3.5-turbo
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            chat_message = response['choices'][0]['message']['content']
            chat_history.insert(tk.END, f"Bot: {chat_message}\n")
            messages.append({"role": "assistant", "content": chat_message})


send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Run the Tkinter event loop
if __name__ == "__main__":
    window.mainloop()
