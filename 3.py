#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time
import urllib
import json,re
import hashlib
import base64,os

url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting'
na=r'C:\Users\Administrator\Desktop\pytes\3\{}.jpg'
api_key = 'd79ce1e440a3e096523eb718758ba967'
param = {"language": "en", "location": "true"}
x_appid = '5b52937a'
x_time = str(int(time.time()))
x_param1 = base64.b64encode(json.dumps(param).replace(' ', '').encode())

x_param=x_param1.decode()
www=api_key+ x_time + x_param
r1=re.compile(r'"content":"(.*?)"')

x_checksum = hashlib.md5(www.encode()).hexdigest()
def main(i):
    if not os.path.exists(na.format(i)):
        return
    f = open(na.format(i), 'rb')
    file_content = f.read()
    f.close()
    base64_image = base64.b64encode(file_content)

    x1={'image': base64_image}
    body = urllib.parse.urlencode(x1)
    
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    result = requests.post(url,headers=x_header,data=x1)
    result = result.text.split()
    #req=urllib.request.Request(url = url, data = body.encode('utf-8'),
                               #headers = x_header, method = 'POST')
    #result = urllib.request.urlopen(req).read()
    s=re.search(r1,result[0]).group(1)
    print (result,s)
    if s:
        os.rename(na.format(i),na.format(s))



if __name__ == '__main__':
    for i in range(73,102):
        main(i) 
