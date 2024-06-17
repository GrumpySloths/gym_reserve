import json
import time
import requests
import base64

class YdmVerify(object):
    _custom_url = "http://api.jfbym.com/api/YmServer/customApi"
    _token = "pkS8cetVsEBWEQ960rtCIRAA0moXn0qudg3XjQzqdbE"
    _headers = {
        'Content-Type': 'application/json'
    }
    def common_verify(self, image, verify_type="10110"):

        payload = {
            "image": base64.b64encode(image).decode(),
            "token": self._token,
            "type": verify_type
        }
        # print(payload)
        resp = requests.post(self._custom_url, headers=self._headers, data=json.dumps(payload))
        # print(resp.text)
        return resp.json()['data']['data']
    def slide_verify(self, slide_image, background_image, verify_type="20101"):
        # 滑块类型
        # 通用双图滑块  20111
        payload = {
            "slide_image": base64.b64encode(slide_image).decode(),
            "background_image": base64.b64encode(background_image).decode(),
            "token": self._token,
            "type": verify_type
        }
        resp = requests.post(self._custom_url, headers=self._headers, data=json.dumps(payload))
        print(resp.text)
        return resp.json()['data']['data']

#创建一个YdmVerify实例
ydm = YdmVerify()

# url = 'https://cas.sysu.edu.cn/cas/captcha.jsp'
# response = requests.get(url)
# jsp_content = response.content
#加载 captcha.png
with open('captcha.png', 'rb') as f:
    jsp_content = f.read()
info=ydm.common_verify(jsp_content)
print(info)
# print(jsp_content)
