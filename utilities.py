import os

def read_documents(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

import os

def get_system_username():
    try:
        user_name = os.getlogin()
    except Exception as e:
        user_name = 'Unknown User'
        print(f"Error getting system username: {e}")
    return user_name

# # Usage
# username = get_system_username()
# print(f"The system username is: {username}")
