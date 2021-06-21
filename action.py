import os
import sys
from cloud189app import *
from extends import *


def push_msg(log):
    msg = ""
    DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK").strip() if os.getenv("DINGTALK_WEBHOOK") is not None else ""
    DINGTALK_SECRET = os.getenv("DINGTALK_SECRET").strip() if os.getenv("DINGTALK_SECRET") is not None else ""
    PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN").strip() if os.getenv("PUSHPLUS_TOKEN") is not None else ""

    if len(DINGTALK_WEBHOOK) > 0 and len(DINGTALK_SECRET) > 0:
        r = dingTalkPush.push_text(log, DINGTALK_WEBHOOK, DINGTALK_SECRET)
        msg += "\n钉钉推送: " + r
    if len(PUSHPLUS_TOKEN) > 0:
        r = pushPlusPush.push_text(log, PUSHPLUS_TOKEN)
        msg += "\nPushPlus推送: " + r

    return msg


def main(user: str, pwd: str):
    log = ""
    try:
        print_msg()
        # log 变量记录消息推送内容
        log += print_msg(hide_username(user) + ":", True)
        cloud = Client(user, pwd)
        log += print_msg(cloud.msg)
        if not cloud.isLogin:
            exit(-1)
        cloud.sign()
        log += print_msg(cloud.msg)
        cloud.draw()
        log += print_msg(cloud.msg)
    except Exception:
        log += print_msg("任务执行失败, 请重试!")
    finally:
        print_msg(push_msg(log))


def hide_username(name: str) -> str:
    u_len = len(name)
    fill_len = int(u_len * 0.3) + 1
    b_index = int((u_len - fill_len) / 2)
    e_index = u_len - fill_len - b_index
    return name[:b_index] + "*" * fill_len + name[-e_index:]


def print_msg(msg: str = "", isFirstLine: bool = False) -> str:
    if isFirstLine or msg == "":
        indent = ""
    else:
        indent = " " * 4
        msg = msg.replace("\n", "\n" + indent)
    msg = indent + msg + "\n"

    print(msg, end='')
    return msg


if __name__ == '__main__':
    # 参数格式: 账号----密码
    if len(sys.argv) == 2 and len(sys.argv[1].split("----")) == 2:
        username = sys.argv[1].split("----")[0]
        password = sys.argv[1].split("----")[1]
    else:
        username = input("请输入账号: ")
        password = input("请输入登录密码: ")
    username = username.strip()
    password = password.strip()

    main(username, password)
