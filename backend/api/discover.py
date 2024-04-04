from fastapi import APIRouter, HTTPException, Depends
from models.users import UserInfo
from api.auth import root
from api.account import get_current_user
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
def user_screening(current_user: UserInfo = Depends(get_current_user)):
    global pref_age, pref_height

    filtered_age = [p for p in root.values() if pref_age[0] <= p.age <= pref_age[1]]

    filtered_age_ids = {user.id for user in filtered_age}

    if pref_height == "Open to all":
        filtered_height = root.values()
    else:
        filtered_height = [
            p for p in root.values() if pref_height[0] <= p.height <= pref_height[1]
        ]

    filtered_height_ids = {user.id for user in filtered_height}

    filtered_gender = [
        p
        for p in root.values()
        if current_user.preferences.gender == "Everyone"
        or current_user.preferences.gender == p.gender
    ]

    filtered_gender_ids = {user.id for user in filtered_gender}

    filtered_user_ids = filtered_age_ids.intersection(
        filtered_gender_ids, filtered_height_ids
    )

    filtered_user = [user for user in root.values() if user.id in filtered_user_ids]
    for user in filtered_user:
        if (
            user.id in current_user.matches
            or user.id in current_user.liked
            or user.id in current_user.daisied
            or user.id in current_user.disliked
            or current_user.id in user.liked
            or current_user.id in user.daisied
            or current_user.id in user.disliked
            or user.id == current_user.id
        ):
            filtered_user.remove(user)

    return filtered_user


@router.post("/discover/{other_user_id}/daisy")
async def daisy_user(
    other_user_id: str, current_user: UserInfo = Depends(get_current_user)
):
    if other_user_id not in root:
        raise HTTPException(status_code=404, detail="Other user not found")

    if current_user.id not in root:
        raise HTTPException(status_code=404, detail="Current user not found")

    if root[current_user.id].daisies < 200:
        raise HTTPException(status_code=403, detail="Not enough daisies")

    root[current_user.id].daisied.append(other_user_id)
    root[current_user.id].daisies -= 200

    if isMatch(current_user.id, other_user_id):
        createChatRoom(current_user.id, other_user_id)
        root[current_user.id].daisy.remove(other_user_id)
        root[other_user_id].daisy.remove(current_user.id)

    transaction.commit()
    return {"message": "Daisy sent successfully"}
