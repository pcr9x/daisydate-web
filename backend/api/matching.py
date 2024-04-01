from fastapi import APIRouter, HTTPException
from zodb_utils import get_zodb_storage
from models.chatting import ChatMessage
from models.users import UserLikeRequest
from api.users import root
import transaction, uuid

router = APIRouter()

chatting_storage = "chatting.fs"
chatting = get_zodb_storage(chatting_storage)


def user_screening(current_user):
    pref_age = current_user.preferences.age
    filtered_user = [
        p
        for p in root.values()
        if (pref_age[0] <= p.age <= pref_age[1]
        and current_user.preferences.gender == p.gender
        and current_user.preferences.relationship_goals == p.relationship_goals
        and p.id not in current_user.matches
        and p.id not in current_user.liked
        and p.id not in current_user.daisied
        and p.id != current_user.id)
        or current_user.id in p.liked
    ]

    sorted_user = []
    for user in filtered_user:
        if user.id in current_user.daisied:
            sorted_user.insert(0, user)
        else:
            sorted_user.append(user)

    return sorted_user


def isMatch(currentUser, otherUser):
    return (currentUser in root[otherUser].liked) or (currentUser in root[otherUser].daisied)

def createChatRoom(user1, user2):
    chatID = str(uuid.uuid4())
    chatting[chatID] = ChatMessage(chatID, user1, user2)
    root[user1].matches.append(user2)
    root[user2].matches.append(user1)
    return {"chatID": chatID}

@router.post("/suggested/{other_user_id}/like")
async def like_user(user: UserLikeRequest, other_user_id: str):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if user.current_user_id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")

    root[user.current_user_id].liked.append(other_user_id)

    # Check if the other user has already liked the current user
    if isMatch(user.current_user_id, other_user_id):
        createChatRoom(user.current_user_id, other_user_id)

    transaction.commit()
    return {"message": "Like sent successfully"}


@router.post("/suggested/{other_user_id}/daisy")
async def daisy_user(user: UserLikeRequest, other_user_id: str):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if user.current_user_id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")

    if root[user.current_user_id].daisies < 100:
        raise HTTPException(status_code=403, detail="Not enough daisies")

    root[user.current_user_id].daisied.append(other_user_id)
    root[user.current_user_id].daisies -= 100

    if isMatch(user.current_user_id, other_user_id):
        createChatRoom(user.current_user_id, other_user_id)

    transaction.commit()
    return {"message": "Daisy sent successfully"}


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
