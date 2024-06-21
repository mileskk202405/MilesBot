import array
import asyncio
import json

import websockets
from google.protobuf import json_format

from CmdKit import CmdKit
import src.pb_pb2 as pb


class WebSocketClient:
    def __init__(self, url, reconnect_interval=5):
        self.url = url
        self.reconnect_interval = reconnect_interval  # 重连间隔时间，单位为秒

    async def connect(self):
        try:
            self.ws = await websockets.connect(self.url)
            print(f"Connected to {self.url}")
        except Exception as e:
            print(f"Connection failed: {e}")
            await self.reconnect()

    async def send(self, message):
        if self.ws:
            await self.ws.send(message)
            print(f"Sent message: {message}")

    async def receive(self):
        if self.ws:
            try:
                message = await self.ws.recv()
                print(f"获取到的消息是: {message}")
                print("对消息进行反序列处理")
                messageData= pb.ExternalMessage().FromString(message)
                print(messageData)
                print("对validMsg进行反序显示成中文")
                print(messageData.validMsg)
                # chinese_string = messageData['validMsg'].decode('utf-8')
                # print(chinese_string)
                return message
            except websockets.exceptions.ConnectionClosed:
                print("Connection was closed by the server.")
                await self.reconnect()

    async def close(self):
        if self.ws:
            await self.ws.close()
            print("Connection closed")

    async def reconnect(self):
        while True:
            print(f"Attempting to reconnect in {self.reconnect_interval} seconds...")
            await asyncio.sleep(self.reconnect_interval)
            try:
                await self.connect()
                break  # 重连成功，跳出循环
            except Exception as e:
                print(f"Reconnection failed: {e}")

    async def run(self):
        await self.connect()
        await self.endMessage()
        try:
            while True:
                await self.receive()
        except Exception as e:
            print(f"An error occurred: {e}")
            await self.reconnect()  # 捕获异常时尝试重连
        finally:
            await self.close()

    #发送数据
    async def endMessage(self):
        data = {'key': 'value'}
        cmdMerge = CmdKit.merge(2, 1)

        msgData = pb.ExternalMessage()
        msgData.cmdCode = 1
        # msgData.protocolSwitch = 0
        msgData.cmdMerge = cmdMerge
        # msgData.responseStatus = {},
        # msgData.validMsg = "1".encode('utf-8'),
        # msgData.data = json.dumps(data).encode('utf-8')

        await self.send(msgData.SerializeToString())
