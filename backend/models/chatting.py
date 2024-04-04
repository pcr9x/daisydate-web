from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    senderID: str
    message: str
    timeStamp: datetime = Field(default_factory=datetime.now)


class ChatMessage(BaseModel):
    chatID: str
    userID1: str
    userID2: str
    message: list[Message] = []


class ChatResponse(BaseModel):
    otherUserProfile: str
    otherUserName: str
    latestMessage: str
    user_id: str
    chatID: str
    messages: list[Message]
