"""
飞书群机器人发送通知
"""
import json
from logging import Logger
import requests
import datetime


class FlybookRobotAlert():
    def __init__(self, webhook_url, logger=Logger("飞书通知")):
        self.webhook = webhook_url
        self.logger = logger

        self.headers = {'Content-Type': 'application/json; charset=UTF-8'}

    def post_to_robot(self, post_data):
        '''
        给飞书机器人发送请求
        :param data:
        :return:
        '''
        try:
            resp = requests.request(
                method="POST", url=self.webhook, data=post_data, headers=self.headers).json()
            if resp.get("StatusCode") == 0 and resp.get("msg") == "success":
                self.logger.info(f"飞书通知发送成功，msg={resp}")
            else:
                self.logger.warning(f"飞书通知发送失败,{resp}")
        except Exception as e:
            self.logger.warning("飞书通知发送异常")
            self.logger.warning(e)
            pass

    def send_message(self, date, acc, traf):
        # 飞书通知标题
        robot_headers = 'cdn用量报告'
        field_list = [
            {
                "is_short": False,
                "text": {
                    "tag": "lark_md",
                    "content": f"**请求数**：<font color=\"green\">{{}}</font>   **次**\n".format(acc)
                }
            },
            {
                "is_short": False,
                "text": {
                    "tag": "lark_md",
                    "content": f"**流量**：<font color=\"green\">{{:.2f}}</font>    **MB**\n".format(traf / 1e6)
                }
            }
        ]

        elements = [
            {
                "tag": "div",
                "text": {
                    "content": date.strftime("%Y年%m月%d日"),
                    "tag": "lark_md"
                }
            },
            {
                "tag": "div",
                "fields": field_list
            }
        ]

        card = json.dumps({
            "config": {
                "wide_screen_mode": True
            },
            "elements": elements,
            "header": {
                "template": "blue",
                "title": {
                    "content": robot_headers,
                    "tag": "plain_text"
                }
            }
        })

        msg_body = json.dumps({"msg_type": "interactive", "card": card})
        self.post_to_robot(msg_body)
        # {'StatusCode': 0, 'StatusMessage': 'success', 'code': 0, 'data': {}, 'msg': 'success'}
        return


if __name__ == '__main__':
    a = FlybookRobotAlert(
        "https://open.feishu.cn/open-apis/bot/v2/hook/51b9e4d8-10d7-4772-b175-4b94d5f2d734")
    a.send_message(datetime.date.today(), 1860, 34372421)
