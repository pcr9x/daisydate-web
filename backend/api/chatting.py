from fastapi import APIRouter, HTTPException
from models.chatting import Message
from api.matching import chatting
import transaction

router = APIRouter()

@router.post("/messages/{chat_id}")
async def send_message(chat_id: str, message: Message):
    # Check if the chat exists
    chat = chatting.get(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Check if the sender is part of the chat
    sender_id = message.userID
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
