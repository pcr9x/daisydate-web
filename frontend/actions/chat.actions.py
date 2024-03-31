from js import document
import requests

def populate_chat_bar(user_id):
    chat_bar = document.getElementByID("chat-bar")
    response = requests.get("http://localhost:8000/messages/{user_id}")
    data = response.json()
    print(data)
