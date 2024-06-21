# import json
# from websocket.CmdKit import CmdKit
#
# # 假设data是一个Python字典或列表
# data = {'key': 'value'}
#
# # 将data序列化为JSON格式的字符串
# json_string = json.dumps(data)
#
# # 将JSON字符串转换为bytes类型
# binary_data = json_string.encode('utf-8')
#
# print(binary_data)
#
# cmdMerge = CmdKit.merge(1, 2)
#
# print(cmdMerge)
#
# msg = {
#     "cmdCode": 1,
#     "protocolSwitch": 0,
#     "cmdMerge": cmdMerge,
#     "responseStatus": 0,
#     "validMsg": "",
#     "data": data
# }
# msg_string = json.dumps(msg)
# msg_data = msg_string.encode('utf-8')
#
# print(msg_data)
import array
import asyncio
import json

from websocket.WebSocketClient import WebSocketClient


async def start():
    url = "ws://192.168.31.66:12000/websocket"
    client = WebSocketClient(url, reconnect_interval=10)  # 重连间隔设置为10秒
    await client.run()
    # await client.endMessage()


# 使用示例
if __name__ == "__main__":
    asyncio.run(start())
