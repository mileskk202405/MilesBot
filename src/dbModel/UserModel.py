import json

from mongoengine import Document, StringField, IntField, ReferenceField, ListField
from mongoengine import connect
from dbModel.MessageModel import Message

connect('milesDB', host='mongodb://localhost:27017/milesDB')


class User(Document):
    wxId= StringField(required=True,uniuque=True)
    name= StringField(required=False)
    age= IntField(required=False)
    message= ListField(ReferenceField(Message))


    # 转化成子典
    def toDict(self):
        j = self.to_json()
        dc = json.loads(j)
        del dc['_id']
        return dc


    # 根据wxid获取用户,不存在则创建
    def getByWxid(self,wxId:str):
        user = User.objects(wxId=wxId).first()
        if not user:
            user = User(wxId=wxId)
            user.save()
        return user