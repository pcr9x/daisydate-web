from api.users import root
from populate_users import user1, user2
import api.matching as apiMatching
import transaction

#NOT WORKING
root[user1.id].liked.append(user2.id)
root[user2.id].liked.append(user1.id)

apiMatching.createChatRoom(user2.id, user1.id)

transaction.commit()
