import logging
import time
from queue import Empty
from threading import Thread

from wcferry import Wcf, WxMsg


class Bot:
    def __init__(self, wcf: Wcf) -> None:
        self.wcf = wcf
        self.wxid = self.wcf.get_self_wxid()
        self.LOG = logging.getLogger("Bot")


    def onMsg(self, msg: WxMsg) -> int:
        try:
            print(msg)  # 打印信息
        except Exception as e:
            print(e)

        return 0

    def enableRecvMsg(self) -> None:
        self.wcf.enable_recv_msg(self.onMsg)

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    self.LOG.info(msg)
                    print(msg)
                    # self.processMsg(msg)
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    self.LOG.error(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()



    def keepRunningAndBlockProcess(self) -> None:
        """
        保持机器人运行，不让进程退出
        """
        while True:
            time.sleep(1)
