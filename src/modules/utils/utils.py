from langchain.schema import Document
import pandas as pd
import os
from glob import glob

def create_documents(df):
    documents = []
    for _, row in df.iterrows():
        metadata = row.to_dict()
        text = metadata.pop("summary") 
        documents.append(Document(page_content=text, metadata=metadata))
    return documents

def get_all_datas(BASE_DIR):
    csv_routes = glob(os.path.join(BASE_DIR, '*/*.csv'))
    df = pd.DataFrame()
    for route in csv_routes:
        d = pd.read_csv(route)
        df = pd.concat([df, d])
    df = df.reset_index(drop=True)
    # 정량평가를 위해, 그래프와 테이블을 제외하고 paragraph만 가져옵니다.
    return df

def get_only_paragraphs(BASE_DIR):
    csv_routes = glob(os.path.join(BASE_DIR, '*/*.csv'))
    df = pd.DataFrame()
    for route in csv_routes:
        d = pd.read_csv(route)
        df = pd.concat([df, d])
    df = df.reset_index(drop=True)
    # 정량평가를 위해, 그래프와 테이블을 제외하고 paragraph만 가져옵니다.
    df = df[df['type'] == 'paragraph']
    df = df.drop(df[df['original_content'].str.contains('@')].index).reset_index(drop = True)
    df = df.drop(df[df['original_content'].str.contains(r'자료:\s?', regex=True)]['original_content'].index).reset_index(drop= True)
    return df

def get_pdf_routes(BASE_DIR):
    pdf_routes = glob(os.path.join(BASE_DIR, '*/*.pdf'))
    return pdf_routes
