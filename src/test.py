from dbModel.UserModel import User
from dbModel.MessageModel import Message

userModel = User()

user = userModel.getByWxid("wxid_91mel5i1nx6l1")
messageModel = Message()
# messageModel.wxId = '222'
# messageModel.content = '你好2'
# messageModel.type = 1
# messageModel.isRead = 0
# messageModel.isSend = 0
# messageModel.direction = 0
# messageModel.msgId = 2
#
# messageModel.save()
# print(messageModel.wxId)
#
# user.message.append(messageModel)
# user.save()
print(user.wxId)

chatLogList = Message.getList(user.wxId,10)
messages = []
for chatLog in chatLogList:
    if chatLog.direction == 0:
        messages.append({
            "role": "user",
            "content": chatLog.content
        })
    else:
        messages.append({
            "role": "assistant",
            "content": chatLog.content
        })
messages.reverse()
print(messages)
