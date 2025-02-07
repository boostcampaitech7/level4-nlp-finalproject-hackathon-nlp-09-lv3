import pandas as pd
import requests
from glob import glob
import pdfplumber
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
load_dotenv()

# pdf문서와 페이지, 좌표가 주어지면, 해당하는 부분을 잘라 폴더에 페이지 번호_element id_image.png로 저장합니다.

def crop_and_save(BASE_DIR, route, page_num, coords, id, dpi=500, scale = 15):
    os.makedirs(BASE_DIR, exist_ok = True)
    with pdfplumber.open(route) as pdf:
        page = pdf.pages[page_num-1]
    dir_route = f"{BASE_DIR}/{route.split('/')[-1][:-4]}"
    save_route = dir_route + f'/page_{page_num}_id_{id}_image.png'
    os.makedirs(dir_route, exist_ok=True)
    page_width = page.width
    page_height = page.height

    # 상대 좌표를 절대 픽셀 좌표로 변환 후 y스케일 살짝 조정 (그래프 이름이 위아래에 붙는경우가 있음)
    x0 = coords[0]['x'] * page_width
    y0 = max(0, coords[0]['y'] * page_height - scale)
    x1 = coords[2]['x'] * page_width
    y1 = min(page_height, coords[2]['y'] * page_height + scale)

    # 크롭 박스가 페이지를 벗어나지 않도록 보정
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(page_width, x1)
    y1 = min(page_height, y1)

    # 크롭 영역 정의
    crop_box = (x0, y0, x1, y1)
    page = page.crop(crop_box).to_image(resolution = dpi)
    page.save(save_route)

    return save_route