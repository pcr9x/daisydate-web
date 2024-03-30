from fastapi import APIRouter, HTTPException
from datetime import datetime
from zodb_utils import get_zodb_storage
from models.chatting import ChatMessage
from models.users import UserLikeRequest
from api.users import root
import transaction, uuid

router = APIRouter()

chatting_storage = "chatting.fs"
chatting = get_zodb_storage(chatting_storage)


def user_screening(user):
    pref_age = user.preferences.age
    filtered_user = [
        p
        for p in root.values()
        if pref_age[0] <= p.age <= pref_age[1]
        and user.preferences.gender == p.gender
        and user.preferences.relationship_goals == p.relationship_goals
    ]
    return filtered_user


@router.post("/suggested/{other_user_id}/like")
async def like_user(user: UserLikeRequest, other_user_id: str):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if user.current_user_id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")

    root[user.current_user_id].liked.append(other_user_id)

    # Check if the other user has already liked the current user
    if user.current_user_id in root[other_user_id].liked:
        # They are a match
        chatID = str(uuid.uuid4())
        chatting[chatID] = ChatMessage(chatID, user.current_user_id, other_user_id)
        root[user.current_user_id].matches.append(other_user_id)
        root[other_user_id].matches.append(user.current_user_id)
        transaction.commit()
        return {"chatID": chatID}
    else:
        transaction.commit()
        return {"chatID": None}


# @router.post("/messages/{chatID}")
# async def send_message(chatID: str, sender_id: str, message: str):
#     if chatID not in root:
#         raise HTTPException(status_code=404, detail="Message key not found")

#     sender = root.get(sender_id)
#     if sender is None:
#         raise HTTPException(status_code=404, detail="Sender not found")

#     recipient_id = chatID.replace(sender_id, "")
#     recipient = root.get(recipient_id)
#     if recipient is None:
#         raise HTTPException(status_code=404, detail="Recipient not found")

#     # Prepare message metadata
#     timestamp = datetime.now().isoformat()

#     # Store the message in the sender's sent messages
#     sender_sent_messages = root.get(sender_id, {}).setdefault("sent_messages", [])
#     sender_sent_messages.append(
#         {"timestamp": timestamp, "recipient_id": recipient_id, "message": message}
#     )

#     # Store the message in the recipient's received messages
#     recipient_received_messages = root.get(recipient_id, {}).setdefault(
#         "received_messages", []
#     )
#     recipient_received_messages.append(
#         {"timestamp": timestamp, "sender_id": sender_id, "message": message}
#     )

#     return {"message": "Message sent successfully"}
