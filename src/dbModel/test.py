from UserModel import User
from MessageModel import Message


userModel = User()
user = userModel.getByWxid('222')
# print(user)
#
MessageModel = Message()
# MessageModel.wxId = '222'
# MessageModel.content = '你好2'
# MessageModel.type = 1
# MessageModel.isRead = 0
# MessageModel.isSend = 0
# MessageModel.direction = 0
#
# MessageModel.save()
#
# user.message.append(MessageModel)
# user.save()

messageList = MessageModel.getList(user.wxId,10)
for message in messageList:
    print(message.time)
    print(message.content)

# print(messageList)
