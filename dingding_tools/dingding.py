import json
import time

import requests
import sys
import os
import urllib.request

APPKEY = 'dingsc8zhhijvzhghhv6'
APPSECRET = 'jMJ1U_obfjUxkHPUUs4KR2xG6CuaDEOwr1rT3AlETXrhSXrHhox2EysJ1VAZeU5r'
DING_TALK_TOKEN_URL = 'https://api.dingtalk.com/gettoken?appkey=%s&appsecret=%s'
CONTENT_TYPE = 'application/json'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
MY_DING_ROBOT_HEADERS = ''
MY_DING_ROBOT_URL = ''
MY_DING_ROBOT_TEL = ''
DING_TALK_PROCESS_URL = 'https://oapi.dingtalk.com/topapi/processinstance/list?access_token=%s'
PROCESS_CODE = ''
START_TIME = ''
access_token = '1c65658a32f132f681ef9db781ad9d9d'
PROCESS_CODE = 'PROC-F74A0CE2-74E9-4E43-A8F0-D07C8BCE7F9D'


class DingdingUtils(object):
    """钉钉操作类"""

    _appkey = APPKEY
    _appsecret = APPSECRET
    _tokenUrl = DING_TALK_TOKEN_URL
    _robotHeaders = MY_DING_ROBOT_HEADERS
    _robotUrl = MY_DING_ROBOT_URL
    _robotTel = MY_DING_ROBOT_TEL
    _processUrl = DING_TALK_PROCESS_URL

    # 获取钉钉审批Token
    def getDingToken(self):
        headers = {
            'Content-Type': CONTENT_TYPE,
            'User-Agent': USER_AGENT
        }
        url = self._tokenUrl % (self._appkey, self._appsecret)
        req = urllib.request.Request(url, headers=headers)
        result = urllib.request.urlopen(req)
        access_token = json.loads(result.read())
        if access_token["errcode"] == 0:
            return access_token["access_token"]
        else:
            self.sendMsgRobot("0-钉钉操作:获取Token失败:" + access_token["errmsg"])
            return None

    def get_process_code(self, code_name: str) -> str:
        """
        根据OA名称获取process_code
        :param code_name: OA名称
        :return: dict['process_code']
        """
        headers = {
            'Content-Type': CONTENT_TYPE,
            'User-Agent': USER_AGENT
        }
        # data = {"name": '下单'}
        data = {"name": code_name}

        data1 = json.dumps(data).encode(encoding='UTF8')
        url = f'https://oapi.dingtalk.com/topapi/process/get_by_name?access_token={self.getDingToken()}'
        req = urllib.request.Request(url, headers=headers, data=data1)
        result_text = urllib.request.urlopen(req)
        process_code = json.loads(result_text.read())
        # print(process_code)

        if process_code["errcode"] == 0:
            return process_code["process_code"]
        else:
            self.sendMsgRobot("0-钉钉操作:获取process_code失败:" + process_code["errmsg"])
            return None

    # 获取单个审批内容
    def getDingProcessContent(self, process_code, start_time):
        headers = {
            'Content-Type': CONTENT_TYPE,
            'User-Agent': USER_AGENT
        }
        data = {
            'process_code': process_code,
            'start_time': start_time
        }
        accesstoken = self.getDingToken()
        # print(f'accesstoken:{accesstoken}')
        if accesstoken is not None:
            data1 = json.dumps(data).encode(encoding='UTF8')
            processUrl = self._processUrl % (accesstoken)
            req = urllib.request.Request(processUrl, headers=headers, data=data1)
            result = urllib.request.urlopen(req)
            data_list = json.loads(result.read())
            # print(data_list)
            return data_list
        else:
            self.sendMsgRobot("0-钉钉操作:获取Token失败:" + accesstoken["errmsg"])

    # 钉钉机器人发送文本消息
    def sendMsgRobot(self, msg):
        robotHeaders = self._robotHeaders
        robotUrl = self._robotUrl
        json_text = {
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "at": {
                "atMobiles": [
                    self._robotTel
                ],
                "isAtAll": False
            }
        }
        requests.post(robotUrl, json.dumps(json_text), headers=robotHeaders).content

    @staticmethod
    def get_start_time(time_str: str = "2022-10-20 00:00:00"):
        # time_str = "2016-05-05 20:28:54"
        # 转换成时间数组
        # start_time = time.gmtime()
        time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        # print(time_array)
        # 转换成时间戳
        timestamp = int(time.mktime(time_array))
        # print(f"{time_str}-->>>>>{timestamp}")
        return timestamp


#
testDing = DingdingUtils()
# print(testDing.getDingToken())
# print(testDing.getDingProcessContent(PROCESS_CODE, start_time))
process_code = testDing.get_process_code('下单')
start_time = testDing.get_start_time()
res = testDing.getDingProcessContent(process_code, 1666195200000)
print(f'res{res},{type(res)}')
print(res['result']['list'])
lis = res['result']['list']
for i in lis:
    print(i)
    for item in i.items():
        if item[0] == 'form_component_values':
            print(item[1])
            for jj in item[1]:
                print(jj)
