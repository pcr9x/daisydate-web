from datetime import datetime
from pydantic import BaseModel, Field
import persistent

class Message(BaseModel):
    UserID: str
    message: str
    timeStamp: datetime = Field(default_factory=datetime.now)

class ChatMessageModel(BaseModel):
    chatID: int
    userID1: str
    userID2: str
    message: list[Message]


class ChatMessage(persistent.Persistent):
    def __init__(self, chatID: str, userID1: str, userID2: str):
        self.chatID = chatID
        self.userID1 = userID1
        self.userID2 = userID2
        self.message: list[Message] = []

    def add_new_message(self, message: Message):
        self.message.append(message)