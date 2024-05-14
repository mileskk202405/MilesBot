from wcferry import WxMsg

from kimi.kimiChat import kimiChat
from dbModel.UserModel import User
from dbModel.MessageModel import Message

class chat:
    def __init__(self) -> None:
        self.chat = kimiChat()
        self.userModel = User()
        self.messageModel = Message()



    # 文本信息处理
    def textMessageHandle(self, msg: WxMsg) -> None:
        # 保存接受到的用户消息
        self.saveMessage(msg.sender,msg.content, 1, 0, 0, msg.id)
        # 调用聊天机器人
        chatLogList = self.getChatLog(msg.sender)
        result = self.chat.chat(chatLogList)
        # 保存发送的消息
        self.saveMessage(msg.sender,result, 1, 1, 1, msg.id)
        # 返回给用户
        return result




    # 保存用户的消息
    def saveMessage(self, sender: str,content: str,type: int,direction: int,isSend:int,msgId: int) -> None:
        # 获取用户
        user = self.userModel.getByWxid(sender)
        messageModel = Message()
        messageModel.wxId =sender
        messageModel.content = content
        messageModel.type = type
        messageModel.isRead = 1
        messageModel.isSend = isSend
        messageModel.direction = direction
        messageModel.msgId = 2

        messageModel.save()

        user.message.append(messageModel)
        user.save()
        return user




    # 得到用户的聊天记录,取10条，并且做符合open AI的格式
    def getChatLog(self, wxid: str) -> []:
        chatLogList = self.messageModel.getList(wxid,10)
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
        my_list_reversed = []
        for i in range(len(messages)):
            my_list_reversed.append(messages[len(messages) - 1 - i])
        return my_list_reversed
