from fastapi import APIRouter, HTTPException
from models.users import UserLikeRequest
from api.users import root
from api.suggested import createChatRoom, isMatch
import transaction

router = APIRouter()

pref_age = (18, 100)
pref_height = "Open to all"


@router.post("/discover/search")
def adjust_preferences(pref: dict):
    global pref_age, pref_height
    pref_age = pref["age"]
    pref_height = pref["height"]

    return {"message": "Preferences updated successfully"}


@router.get("/discover")
def user_screening(current_user_id: dict):
    global pref_age, pref_height
    current_user = root.get(current_user_id["current_user_id"])

    # Filter users based on age
    filtered_age = [p for p in root.values() if pref_age[0] <= p.age <= pref_age[1]]

    # Extract user ids from filtered_age
    filtered_age_ids = {user.id for user in filtered_age}

    # Filter users based on height
    if pref_height == "Open to all":
        filtered_height = root.values()  # No filtering based on height
    else:
        filtered_height = [
            p for p in root.values() if pref_height[0] <= p.height <= pref_height[1]
        ]

    # Extract user ids from filtered_height
    filtered_height_ids = {user.id for user in filtered_height}

    # Filter users based on gender
    filtered_gender = [
        p
        for p in root.values()
        if current_user.preferences.gender == "Everyone"
        or current_user.preferences.gender == p.gender
    ]

    # Extract user ids from filtered_gender
    filtered_gender_ids = {user.id for user in filtered_gender}

    # Get the intersection of user ids
    filtered_user_ids = filtered_age_ids.intersection(
        filtered_gender_ids, filtered_height_ids
    )

    # Filter the original list of users based on the intersection of ids
    filtered_user = [user for user in root.values() if user.id in filtered_user_ids]
    for user in filtered_user:
        if (
            user.id in current_user.matches
            or user.id in current_user.liked
            or user.id in current_user.daisied
        ):
            filtered_user.remove(user)

    return filtered_user


@router.post("/discover/{other_user_id}/daisy")
async def daisy_user(user: UserLikeRequest, other_user_id: str):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if user.current_user_id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")

    if root[user.current_user_id].daisies < 100:
        raise HTTPException(status_code=403, detail="Not enough daisies")

    root[user.current_user_id].daisied.append(other_user_id)
    root[user.current_user_id].daisies -= 200

    if isMatch(user.current_user_id, other_user_id):
        createChatRoom(user.current_user_id, other_user_id)
        root[user.current_user_id].daisy.remove(other_user_id)
        root[other_user_id].daisy.remove(user.current_user_id)

    transaction.commit()
    return {"message": "Daisy sent successfully"}
