from models import users
from ZODB.FileStorage import FileStorage
import transaction, uuid
from api.users import root
from pydantic import EmailStr
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user1 = users.UserInfo(
    name="Petch",
    email="lnwpetchza@gmail.com",
    password=pwd_context.hash("petch1234"),
    date_of_birth=datetime.strptime("2004-07-06", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-07-06", "%Y-%m-%d")).days // 365,
    photos=["assets/petch.jpg"],
    gender="Man",
    id=str(uuid.uuid4()),
)

user2 = users.UserInfo(
    name="Capt",
    email="lnwcaptza@gmail.com",
    password=pwd_context.hash("capt1234"),
    date_of_birth=datetime.strptime("2004-02-28", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-02-28", "%Y-%m-%d")).days // 365,
    photos=["assets/capt.jpg"],
    gender="Man",
    id=str(uuid.uuid4()),
)

user3 = users.UserInfo(
    name="Wit",
    email="lnwwitza@gmail.com",
    password=pwd_context.hash("wit1234"),
    date_of_birth=datetime.strptime("2004-07-06", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-07-06", "%Y-%m-%d")).days // 365,
    photos=["assets/wit.jpg"],
    gender="Man",
    id=str(uuid.uuid4()),
)

user4 = users.UserInfo(
    name="Minji",
    email="kimminji@gmail.com",
    password=pwd_context.hash("minji1234"),
    date_of_birth=datetime.strptime("2004-05-07", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-05-07", "%Y-%m-%d")).days // 365,
    photos=["assets/minji.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user5 = users.UserInfo(
    name="Yunjin",
    email="huhyunjin@gmail.com",
    password=pwd_context.hash("yunjin1234"),
    date_of_birth=datetime.strptime("2001-10-08", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2001-10-08", "%Y-%m-%d")).days // 365,
    photos=["assets/yunjin.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user6 = users.UserInfo(
    name="IU",
    email="leejieun@gmail.com",
    password=pwd_context.hash("iu1234"),
    date_of_birth=datetime.strptime("1993-05-16", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("1993-05-16", "%Y-%m-%d")).days // 365,
    photos=["assets/iu.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user7 = users.UserInfo(
    name="Chaewon",
    email="kimchaewon@gmail.com",
    password=pwd_context.hash("chaewon1234"),
    date_of_birth=datetime.strptime("2000-08-01", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2000-08-01", "%Y-%m-%d")).days // 365,
    photos=["assets/chaewon.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user8 = users.UserInfo(
    name="Wonyoung",
    email="jangwonyoung@gmail.com",
    password=pwd_context.hash("wonyoung1234"),
    date_of_birth=datetime.strptime("2008-08-31", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2008-08-31", "%Y-%m-%d")).days // 365,
    photos=["assets/wonyoung.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user9 = users.UserInfo(
    name="Sakura",
    email="miyawakisakura@gmail.com",
    password=pwd_context.hash("sakura1234"),
    date_of_birth=datetime.strptime("1998-03-19", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("1998-03-19", "%Y-%m-%d")).days // 365,
    photos=["assets/sakura.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user10 = users.UserInfo(
    name="Hanni",
    email="phamhanni@gmail.com",
    password=pwd_context.hash("hanni1234"),
    date_of_birth=datetime.strptime("2004-10-06", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2004-10-06", "%Y-%m-%d")).days // 365,
    photos=["assets/hanni.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user11 = users.UserInfo(
    name="Jennie",
    email="kimjennie@gmail.com",
    password=pwd_context.hash("jennie1234"),
    date_of_birth=datetime.strptime("1996-01-16", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("1996-01-16", "%Y-%m-%d")).days // 365,
    photos=["assets/jennie"],
    gender="Woman",
    id=str(uuid.uuid4()),
)

user12 = users.UserInfo(
    name="Yujin",
    email="anyujin@gmail.com",
    password=pwd_context.hash("yujin1234"),
    date_of_birth=datetime.strptime("2003-09-01", "%Y-%m-%d"),
    age=(datetime.now() - datetime.strptime("2003-09-01", "%Y-%m-%d")).days // 365,
    photos=["assets/yujin.jpg"],
    gender="Woman",
    id=str(uuid.uuid4()),
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

transaction.commit()