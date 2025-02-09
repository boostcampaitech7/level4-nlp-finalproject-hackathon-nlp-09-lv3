import os
import sys
from tqdm import tqdm
from utils import get_pdf_routes
project_root = os.getcwd()
sys.path.append(project_root + '/modules')

from modules.pdf_parsing.make_md_and_summaries import make_md
from modules.pdf_parsing.upstage_parser import parsing
def pdf_to_md_and_csv(BASE_DIR = './datas'):
    temp = BASE_DIR
    BASE_DIR = './modules/datas'
    pdfs = get_pdf_routes(BASE_DIR)
    BASE_DIR = temp
    results = []

    for pdf in tqdm(pdfs, desc = 'pdf 문서 파싱중..'):
        elements = parsing(BASE_DIR = BASE_DIR, route = pdf)['elements']
        result = make_md(BASE_DIR = BASE_DIR, route = pdf, elements = elements,)
        results.append(result)

if __name__ == 'main':
    pdf_to_md_and_csv()