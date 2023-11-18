import re
import tkinter as tk
from tkinter import scrolledtext
import openai
import os
import configparser
from fuzzywuzzy import process, fuzz

# Load API key from configuration file
config = configparser.ConfigParser()
config.read('config.ini')
user = config['openai']['api_key']

os.environ['OPEN_AI_KEY'] = user
openai.api_key = os.getenv("OPEN_AI_KEY")

# Knowledge base dictionary
knowledge_base = {
    "python": "Python is a high-level, general-purpose programming language.",
    "who are you": "I am a beautiful lady who dances in the rain with my circuits!"
    # ... add other knowledge base entries as needed
}

# Read documents into a dictionary
def read_documents(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Adjust this if your files have different extensions
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

# Replace with your folder path
document_knowledge_base = read_documents('docs')

def list_document_names(document_knowledge_base):
    return list(document_knowledge_base.keys())

# Search within documents
def search_documents(query, document_knowledge_base):
    best_match, best_score = None, 0
    for filename, content in document_knowledge_base.items():
        score = fuzz.partial_ratio(query.lower(), content.lower())
        if score > best_score:
            best_match, best_score = content, score
    if best_score > 60:  # Adjust the threshold as needed
        return best_match
    return None

# Modified get_knowledge_base_response function
def get_knowledge_base_response(query):
    # Check predefined knowledge base
    print(f'query: {query}')
    tokens = query.lower().split()
    regex = re.compile('[^a-zA-Z0-9 ]')
    response = regex.sub('', query)
    for key in knowledge_base.keys():
        key_tokens = key.split()
        length = len(key_tokens)
        print([i for i, j in zip(response, key_tokens) if i == j])

    kb_response = knowledge_base.get(response.lower())
    print(f'kb_response: {kb_response}')
    if kb_response:
        return kb_response, "Predefined Knowledge Base"

    # Check document knowledge base
    doc_response = search_documents(query, document_knowledge_base)
    if doc_response:
        return doc_response, "Document Knowledge Base"

    return None, None

# List to store all messages for context
messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Create the main window
window = tk.Tk()
window.title("Chat with GPT-3.5-turbo")
window.geometry("600x600")

# Create frames
top_frame = tk.Frame(window)
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create scrolled text widget for chat history
chat_history = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, state='disabled', font=("Arial", 14))
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create entry widget for user input
user_input = tk.Entry(bottom_frame, font=("Arial", 14))
user_input.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

# Send message function with enhancements
def send_message():
    message = user_input.get()
    if message:
        user_input.delete(0, tk.END)  # Clear the entry field
        chat_history.configure(state='normal')
        chat_history.insert(tk.END, f"User: {message}\n", 'user')
        chat_history.insert(tk.END, "Bot is typing...\n", 'loading')
        chat_history.configure(state='disabled')
        messages.append({"role": "user", "content": message})
        # Check if user asks about documents in the knowledge base
        if "what documents" in message.lower() and "knowledge base" in message.lower():
            document_list = list_document_names(document_knowledge_base)
            response_message = "Here are the documents in your knowledge base:\n" + "\n".join(document_list)
            chat_history.configure(state='normal')
            chat_history.delete("end-2l", "end-1l")  # Remove the loading message
            chat_history.insert(tk.END, f"Bot: {response_message}\n", 'bot')
            chat_history.configure(state='disabled')
        else:
            # Check the knowledge base first
            print(f'message: {message}')
            kb_response, source = get_knowledge_base_response(message)
            if kb_response:
                response_message = f"{kb_response}"
                chat_history.configure(state='normal')
                chat_history.delete("end-2l", "end-1l")  # Remove the loading message
                chat_history.insert(tk.END, f"Bot: {response_message}\n", 'bot')
                chat_history.configure(state='disabled')
                if source:
                    print(f"Response sourced from: {source}")  # Logging the source
            else:
                # If no knowledge base response, send message to GPT-3.5-turbo
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )
                    chat_message = response['choices'][0]['message']['content']
                    chat_history.configure(state='normal')
                    chat_history.delete("end-2l", "end-1l")  # Remove the loading message
                    chat_history.insert(tk.END, f"Bot: {chat_message}\n", 'bot')
                    chat_history.configure(state='disabled')
                    messages.append({"role": "assistant", "content": chat_message})
                except Exception as e:
                    print(f"Error: {e}")
                    chat_history.configure(state='normal')
                    chat_history.delete("end-2l", "end-1l")  # Remove the loading message
                    chat_history.insert(tk.END, "Bot: Error in processing your request.\n", 'bot')
                    chat_history.configure(state='disabled')

        # Auto-scroll to the end
        chat_history.see(tk.END)

# Configure tag for user messages
chat_history.tag_configure('user', foreground="cyan")
chat_history.tag_configure('bot', foreground="green")
chat_history.tag_configure('loading', foreground="gray")

# Create send button
send_button = tk.Button(bottom_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10)

# Bind the Enter key to send message
window.bind('<Return>', lambda event: send_message())

# Set focus to input field
user_input.focus_set()

# Run the Tkinter event loop
if __name__ == "__main__":
    window.mainloop()
