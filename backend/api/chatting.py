from fastapi import APIRouter, HTTPException, Request
from models.chatting import Message
from api.matching import chatting
import transaction
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="../frontend/pages")


@router.post("/messages/{chat_id}")
async def send_message(chat_id: str, message: Message):
    # Check if the chat exists
    chat = chatting.get(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Check if the sender is part of the chat
    sender_id = message.senderID
    if sender_id not in [chat.userID1, chat.userID2]:
        raise HTTPException(status_code=403, detail="Sender not part of the chat")

    # Determine the recipient ID
    recipient_id = chat.userID1 if sender_id == chat.userID2 else chat.userID2

    # Add the message to the chat
    chat.add_new_message(message)

    # Save the updated chat
    chatting[chat_id] = chat
    transaction.commit()

    return {"message": "Message sent successfully"}


@router.get("/messages/{chat_id}")
async def get_messages(chat_id: str):
    chat = chatting.get(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat.message


@router.get("/messages/{user_id}/all")
async def getAllChatIdByUser(user_id: str):
    chat_ids = []
    for key, value in chatting.items():
        if value.userID1 == user_id or value.userID2 == user_id:
            chat_ids.append(key)
    return {"chat_ids": chat_ids}


@router.get("/messages/all/test/test")
async def get_all_chat_id():
    return list(chatting.values())


def get_all_chats(user_id: str):
    results = []
    for c in chatting:
        chat = chatting[c]
        if chat.userID1 == user_id or chat.userID2 == user_id:
            results.append(chat)
    print(results)
    return results


@router.get("/messages/{user_id}")
async def index(user_id: str, request: Request):
    if user_id == "all":
        return chatting
    data = get_all_chats(user_id)
    return templates.TemplateResponse(
        "chat-page.html", {"request": request, "data": data}
    )
