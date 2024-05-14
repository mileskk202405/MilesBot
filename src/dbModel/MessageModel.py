import datetime
import json

from mongoengine import Document, StringField, IntField, DateTimeField,LongField

from mongoengine import connect

connect('milesDB', host='mongodb://localhost:27017/milesDB')

class Message(Document):
    wxId= StringField(required=True)    # 微信id
    content= StringField(required=True)     # 内容
    type= IntField(required=True)      # 1:文本 3:图片 4:语音 5:视频
    time=  DateTimeField(default=datetime.datetime.utcnow)      # 时间戳
    isRead= IntField(required=True)      # 0:未读 1:已读
    isSend= IntField(required=True)     # 0:未发送 1:已发送
    direction= IntField(required=True)      # 0:接收 1:发送
    msgId= LongField(required=True)     # 消息id
    # 转化成子典
    def toDict(self):
        j = self.to_json()
        dc = json.loads(j)
        del dc['_id']
        return dc



    # 根据wxid查询消息记录
    def getList(self,wxId:str,limit:int=10):
        return Message.objects(wxId=wxId).order_by('-time').limit(limit)