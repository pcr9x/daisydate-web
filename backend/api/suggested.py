from fastapi import APIRouter, HTTPException, status, Depends
from zodb_utils import get_zodb_storage
from models.chatting import ChatMessage
from models.users import UserPreferences, UserInfo
from api.auth import root
from api.account import get_current_user
from collections import deque
import transaction, uuid

router = APIRouter()

chatting_storage = "chatting.fs"
chatting = get_zodb_storage(chatting_storage)

# CAPT- DONE
@router.get("/suggested")
async def user_screening(current_user: UserInfo = Depends(get_current_user)):
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
    filtered_user = [
        user
        for user in root.values()
        if user.id in filtered_user_ids
        and user.id not in current_user.matches
        and user.id not in current_user.liked
        and user.id not in current_user.daisied
        and user.id not in current_user.disliked
        and user.id != current_user.id
    ]

    for p in root.values():
        if current_user.id in p.daisied and p.id not in filtered_user_ids:
            filtered_user.append(p)

    # Sort filtered_user based on other user's daisied list
    sorted_user = []
    for p in filtered_user:
        if current_user.id in p.daisied:
            sorted_user.insert(0, p)
        else:
            sorted_user.append(p)

    return sorted_user


@router.put("/suggested/preferences")
async def adjust_pref(
    pref: UserPreferences, current_user: UserInfo = Depends(get_current_user)
):
    user_id = current_user.id
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    current_user.preferences = pref

    root[user_id] = current_user
    transaction.commit()
    return {"message": "User's preferences updated successfully"}


def isMatch(currentUser, otherUser):
    return (currentUser in root[otherUser].liked) or (currentUser in root[otherUser].daisied)

def createChatRoom(user1, user2):
    chatID = str(uuid.uuid4())
    chatting[chatID] = ChatMessage(chatID=chatID, userID1=user1, userID2=user2)
    u1 = root[user1]
    u2 = root[user2]
    u1.matches.append(u2)
    u2.matches.append(u1)
    root[user1] = u1
    root[user2] = u2
    return {"chatID": chatID}


@router.post("/suggested/{other_user_id}/like")
async def like_user(
    other_user_id: str, current_user: UserInfo = Depends(get_current_user)
):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if current_user.id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")
    
    current_user.liked.append(other_user_id)
    current_user.daisies += 25

    root[current_user.id] = current_user

    # Check if the other user has already liked the current user
    if isMatch(current_user.id, other_user_id):
        createChatRoom(current_user.id, other_user_id)
        root[current_user.id].liked.remove(other_user_id)
        root[other_user_id].liked.remove(current_user.id)

    transaction.commit()
    return {"message": "Like sent successfully"}


@router.post("/suggested/{other_user_id}/daisy")
async def daisy_user(
    other_user_id: str, current_user: UserInfo = Depends(get_current_user)
):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if current_user.id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")

    if root[current_user.id].daisies < 100:
        raise HTTPException(status_code=403, detail="Not enough daisies")
    
    current_user.daisied.append(other_user_id)
    current_user.daisies -= 100

    root[current_user.id] = current_user

    if isMatch(current_user.id, other_user_id):
        createChatRoom(current_user.id, other_user_id)
        root[current_user.id].daisy.remove(other_user_id)
        root[other_user_id].daisy.remove(current_user.id)

    transaction.commit()
    return {"message": "Daisy sent successfully"}


@router.post("/suggested/{other_user_id}/dislike")
async def dislike_user(
    other_user_id: str, current_user: UserInfo = Depends(get_current_user)
):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if current_user.id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")

    current_user.disliked.append(other_user_id)

    root[current_user.id] = current_user
    transaction.commit()
    return {"message": "Dislike sent successfully"}
