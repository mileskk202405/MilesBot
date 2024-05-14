from wcferry import Wcf
from wxBot import Bot





wcf = Wcf(debug=True)
bot = Bot(wcf)
if (wcf.is_login()):
     # 获取当前登录账号的ID
    print(wcf.get_self_wxid())

    bot.LOG.info(f"WeChatRobot成功启动···")
    bot.enableReceivingMsg()

    bot.keepRunningAndBlockProcess()