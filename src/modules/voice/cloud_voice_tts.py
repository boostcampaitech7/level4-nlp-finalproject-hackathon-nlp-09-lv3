
from dotenv import load_dotenv
load_dotenv()
import os
import sys
import urllib.request
import re
def tts(text, cnt, save_dir):
    text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", text)

    client_id = os.environ['NAVER_CLOUD_VOICE_KEY']
    client_secret = os.environ['NAVER_CLOUD_VOICE_SECRET']
    data = "speaker=nara_call&volume=0&speed=-2&pitch=0&format=mp3&text=" + text
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    save_dir = f'{save_dir}/voice_{cnt}.mp3'
    if(rescode==200):
        response_body = response.read()
        with open(save_dir, 'wb') as f:
            f.write(response_body)
        return save_dir
        
    else:
        print("Error Code:" + rescode)
        return None