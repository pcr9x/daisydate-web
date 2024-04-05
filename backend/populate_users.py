from models.users import UserInfo
import transaction, uuid
from api.auth import root
from datetime import datetime
from passlib.context import CryptContext
from api.suggested import createChatRoom

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user1 = UserInfo(
    name="Petch",
    email="lnwpetchza@gmail.com",
    password=pwd_context.hash("petch1234"),
    date_of_birth=datetime.strptime("2004-07-06", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-07-06", "%Y-%m-%d")).days // 365,
    photos=["assets/petch.jpg"],
    gender="Male",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a software engineering student.",
        "relationship_goals": "Long-term",
        "height": 185,
        "school": "KMITL",
    },
    preferences={
        "age": (18, 24),
        "gender": "Female",
    },
)

user2 = UserInfo(
    name="Capt",
    email="lnwcaptza@gmail.com",
    password=pwd_context.hash("capt1234"),
    date_of_birth=datetime.strptime("2004-02-28", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-02-28", "%Y-%m-%d")).days // 365,
    photos=["assets/capt.jpg"],
    gender="Other",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I love Ferrari.",
        "relationship_goals": "Short-term",
        "height": 200,
        "school": "KMITL",
    },
    preferences={"age": (19, 26)},
)

user3 = UserInfo(
    name="Wit",
    email="lnwwitza@gmail.com",
    password=pwd_context.hash("wit1234"),
    date_of_birth=datetime.strptime("2004-07-06", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-07-06", "%Y-%m-%d")).days // 365,
    photos=["assets/wit.jpg"],
    gender="Prefer not to say",
    detail={
        "bio": "I love SEP.",
        "relationship_goals": "Casual",
        "height": 180,
        "school": "KMITL",
    },
    id=str(uuid.uuid4()),
)

user4 = UserInfo(
    name="Minji",
    email="kimminji@gmail.com",
    password=pwd_context.hash("minji1234"),
    date_of_birth=datetime.strptime("2004-05-07", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-05-07", "%Y-%m-%d")).days // 365,
    photos=["assets/minji.jpeg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a member of NewJeans.",
        "relationship_goals": "Long-term",
        "height": 169,
        "school": "Chulalongkorn University",
    },
)

user5 = UserInfo(
    name="Yunjin",
    email="huhyunjin@gmail.com",
    password=pwd_context.hash("yunjin1234"),
    date_of_birth=datetime.strptime("2001-10-08", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2001-10-08", "%Y-%m-%d")).days // 365,
    photos=["assets/yunjin.jpg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a member of LE SSERAFIM.",
        "relationship_goals": "New friends",
        "height": 172,
        "school": "Srinakarinwirot University"
    }
)

user6 = UserInfo(
    name="IU",
    email="leejieun@gmail.com",
    password=pwd_context.hash("iu1234"),
    date_of_birth=datetime.strptime("1993-05-16", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("1993-05-16", "%Y-%m-%d")).days // 365,
    photos=["assets/iu.jpg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a singer.",
        "relationship_goals": "Just chatting",
        "height": 162,
        "school": "Chulalongkorn University",
    },
)

user7 = UserInfo(
    name="Chaewon",
    email="kimchaewon@gmail.com",
    password=pwd_context.hash("chaewon1234"),
    date_of_birth=datetime.strptime("2000-08-01", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2000-08-01", "%Y-%m-%d")).days // 365,
    photos=["assets/chaewon.jpg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a member of LE SSERAFIM.",
        "relationship_goals": "Long-term",
        "height": 164,
        "school": "Mahidol University",
    },
)

user8 = UserInfo(
    name="Wonyoung",
    email="jangwonyoung@gmail.com",
    password=pwd_context.hash("wonyoung1234"),
    date_of_birth=datetime.strptime("2004-08-31", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-08-31", "%Y-%m-%d")).days // 365,
    photos=["assets/wonyoung.jpg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a member of IVE.",
        "relationship_goals": "New friends",
        "height": 173,
        "school": "Srinakarinwirot University",
    },
)

user9 = UserInfo(
    name="Sakura",
    email="miyawakisakura@gmail.com",
    password=pwd_context.hash("sakura1234"),
    date_of_birth=datetime.strptime("1998-03-19", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("1998-03-19", "%Y-%m-%d")).days // 365,
    photos=["assets/sakura.jpeg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a member of LE SSERAFIM.",
        "relationship_goals": "Open to all",
        "height": 163,
        "school": "UTCC",
    },
)

user10 = UserInfo(
    name="Hanni",
    email="phamhanni@gmail.com",
    password=pwd_context.hash("hanni1234"),
    date_of_birth=datetime.strptime("2004-10-06", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-10-06", "%Y-%m-%d")).days // 365,
    photos=["assets/hanni.jpg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a member of NewJeans.",
        "relationship_goals": "Casual",
        "height": 162,
        "school": "Kasetsart University",
    },
)

user11 = UserInfo(
    name="Jennie",
    email="kimjennie@gmail.com",
    password=pwd_context.hash("jennie1234"),
    date_of_birth=datetime.strptime("1996-01-16", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("1996-01-16", "%Y-%m-%d")).days // 365,
    photos=["assets/jennie.jpg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a singer, actress, and model under OA (ODD ATELIER) Entertainment.",
        "relationship_goals": "Short-term",
        "height": 163,
        "school": "Srinakarinwirot University",
    },
)

user12 = UserInfo(
    name="Yujin",
    email="anyujin@gmail.com",
    password=pwd_context.hash("yujin1234"),
    date_of_birth=datetime.strptime("2003-09-01", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2003-09-01", "%Y-%m-%d")).days // 365,
    photos=["assets/yujin.jpg"],
    gender="Female",
    id=str(uuid.uuid4()),
    detail={
        "bio": "I'm a member of IVE.",
        "relationship_goals": "Casual",
        "height": 173,
        "school": "Thammasat University",
    },
)


root[user1.id] = user1
root[user2.id] = user2
root[user3.id] = user3
root[user4.id] = user4
root[user5.id] = user5
root[user6.id] = user6
root[user7.id] = user7
root[user8.id] = user8
root[user9.id] = user9
root[user10.id] = user10
root[user11.id] = user11
root[user12.id] = user12

createChatRoom(user1.id, user10.id)

transaction.commit()
