import json
import logging
import time
from queue import Empty
from threading import Thread
import xml.etree.ElementTree as ET

from wcferry import Wcf, WxMsg
from LlmChat import chat


class Bot:
    def __init__(self, wcf: Wcf) -> None:
        self.wcf = wcf
        self.wxid = self.wcf.get_self_wxid()
        self.LOG = logging.getLogger("Bot")
        self.chat = chat()


    def processMsg(self, msg: WxMsg) -> None:
        """当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
        此处可进行自定义发送的内容,如通过 msg.content 关键字自动获取当前天气信息，并发送到对应的群组@发送者
        群号：msg.roomid  微信ID：msg.sender  消息内容：msg.content
        content = "xx天气信息为："
        receivers = msg.roomid
        self.sendTextMsg(content, receivers, msg.sender)
        """
        print("接收到消息")
        print(json.dumps(msg.__dict__))

        # 群聊消息
        if msg.from_group():
            # 如果在群里被 @
            # if msg.roomid not in self.config.GROUPS:  # 不在配置的响应的群列表里，忽略
            #     return

            # if msg.is_at(self.wxid):  # 被@
            #     # self.toAt(msg)
            #     print("在"+msg.roomid+"群里被" +msg.sender + "@")
            #
            # else:  # 其他消息
            #     # self.toChengyu(msg)
            #     print("在"+msg.roomid+"群里" +msg.sender + "说：" + msg.content)

            return  # 处理完群聊信息，后面就不需要处理了

        # 非群聊信息，按消息类型进行处理
        if msg.type == 37:  # 好友请求
            self.autoAcceptFriendRequest(msg)

        elif msg.type == 10000:  # 系统信息
            # self.sayHiToNewFriend(msg)
            print("系统消息")

        elif msg.type == 0x01:  # 文本消息
            # 让配置加载更灵活，自己可以更新配置。也可以利用定时任务更新。
            if msg.from_self():
                if msg.content == "^更新$":
                    # self.config.reload()
                    self.LOG.info("已更新")
            else:
                self.toChitchat(msg)  # 闲聊
        elif msg.type == 0x03:  # 图片消息
            print("图片消息")

    # 通过队列的方式打开接收消息
    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    self.LOG.info(msg)
                    self.processMsg(msg)
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    self.LOG.error(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()


    # 同意好友请求
    def autoAcceptFriendRequest(self, msg: WxMsg) -> None:
        try:
            xml = ET.fromstring(msg.content)
            v3 = xml.attrib["encryptusername"]
            v4 = xml.attrib["ticket"]
            scene = int(xml.attrib["scene"])
            self.wcf.accept_new_friend(v3, v4, scene)

        except Exception as e:
            self.LOG.error(f"同意好友出错：{e}")




    # 和用户交互信息
    def toChitchat(self, msg: WxMsg) -> bool:
        """闲聊，接入 ChatGPT
        """
        rsp = self.chat.textMessageHandle(msg)
        if rsp:
            if msg.from_group():
                self.sendTextMsg(rsp, msg.roomid, msg.sender)
            else:
                self.sendTextMsg(rsp, msg.sender)

            return True
        else:
            self.LOG.error(f"我的大脑罢工了，请你稍后再来找我吧，我要睡一觉。")
            return False


    # 发送消息给用户
    def sendTextMsg(self, msg: str, receiver: str, at_list: str = "") -> None:
        """ 发送消息
        :param msg: 消息字符串
        :param receiver: 接收人wxid或者群id
        :param at_list: 要@的wxid, @所有人的wxid为：notify@all
        """
        # msg 中需要有 @ 名单中一样数量的 @
        ats = ""
        if at_list:
            if at_list == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = at_list.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f" @{self.wcf.get_alias_in_chatroom(wxid, receiver)}"

        # {msg}{ats} 表示要发送的消息内容后面紧跟@，例如 北京天气情况为：xxx @张三
        if ats == "":
            self.LOG.info(f"To {receiver}: {msg}")
            self.wcf.send_text(f"{msg}", receiver, at_list)
        else:
            self.LOG.info(f"To {receiver}: {ats}\r{msg}")
            self.wcf.send_text(f"{ats}\n\n{msg}", receiver, at_list)

    # 发送图片消息给用户
    def sengImageMsg(self, path: str, receiver: str) -> None:
        self.wcf.send_image(path, receiver)


    # 保持机器人运行，不让进程退出
    def keepRunningAndBlockProcess(self) -> None:
        """
        保持机器人运行，不让进程退出
        """
        while True:
            time.sleep(1)
