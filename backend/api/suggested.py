from fastapi import APIRouter, HTTPException
from zodb_utils import get_zodb_storage
from models.chatting import ChatMessage
from models.users import UserLikeRequest
from api.users import root
import transaction, uuid

router = APIRouter()

chatting_storage = "chatting.fs"
chatting = get_zodb_storage(chatting_storage)

# CAPT- DONE
@router.get("/suggested")
def user_screening(current_user_id: dict):
    current_user = root.get(current_user_id["current_user_id"])
    pref_age = current_user.preferences.age

    # Filter users based on age
    filtered_age = [p for p in root.values() if pref_age[0] <= p.age <= pref_age[1]]

    # Extract user ids from filtered_age
    filtered_age_ids = {user.id for user in filtered_age}

    # Filter users based on gender
    filtered_gender = [
        p
        for p in root.values()
        if current_user.preferences.gender == "Everyone"
        or current_user.preferences.gender == p.gender
    ]

    # Extract user ids from filtered_gender
    filtered_gender_ids = {user.id for user in filtered_gender}

    # Filter users based on relationship goals
    filtered_relationship_goals = [
        p
        for p in root.values()
        if current_user.preferences.relationship_goals == "Open to all"
        or current_user.preferences.relationship_goals is None
        or current_user.preferences.relationship_goals == p.relationship_goals
    ]

    # Extract user ids from filtered_relationship_goals
    filtered_relationship_goals_ids = {user.id for user in filtered_relationship_goals}

    # Get the intersection of user ids
    filtered_user_ids = filtered_age_ids.intersection(
        filtered_gender_ids, filtered_relationship_goals_ids
    )

    # Filter the original list of users based on the intersection of ids
    filtered_user = [user for user in root.values() if user.id in filtered_user_ids]
    for user in filtered_user:
        if user.id in current_user.matches or user.id in current_user.liked or user.id in current_user.daisied:
            filtered_user.remove(user)

    # Sort filtered_user based on current user's daisied list
    sorted_user = sorted(
        filtered_user,
        key=lambda user: (
            current_user.daisied.index(user.id)
            if user.id in current_user.daisied
            else float("inf")
        ),
    )

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
    root[user.current_user_id].daisies += 25

    # Check if the other user has already liked the current user
    if isMatch(user.current_user_id, other_user_id):
        createChatRoom(user.current_user_id, other_user_id)
        root[user.current_user_id].liked.remove(other_user_id)
        root[other_user_id].liked.remove(user.current_user_id)

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
        root[user.current_user_id].daisy.remove(other_user_id)
        root[other_user_id].daisy.remove(user.current_user_id)

    transaction.commit()
    return {"message": "Daisy sent successfully"}
