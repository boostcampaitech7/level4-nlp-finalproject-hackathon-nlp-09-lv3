import os
import pandas as pd
from .summarizer_for_rag import image_summarization, table_summarization, text_summarization, text_summarization_Hyperclova
from .cropper import crop_and_save
from bs4 import BeautifulSoup

def make_md(BASE_DIR, route, elements,  model = 'hyperclova'):
    if model == 'gpt-4o-mini':
        text_summarizer = text_summarization
    elif model == 'hyperclova':
        text_summarizer = text_summarization_Hyperclova
    else:
        raise ValueError("text summarizer로 'gpt-4o-mini'나 'hyperclova' 둘 중 하나를 선택하세요.")

    file_name = route.split('/')[-1][:-4]
    md_file = f'{BASE_DIR}/{file_name}/{file_name}.md'
    dir_route = f'{BASE_DIR}/{file_name}'
    os.makedirs(dir_route, exist_ok=True)
    company_name = route.split('/')[-1].split('_')[0]
    investment = route.split('/')[-1].split('_')[1][:-4]
    # images = ['table', 'figure'] 이미지로 저장되는 category들
    summaries = []
    # result['elements']를 순회하며 처리
    for item in elements:
        element_id = item['id']
        with open(md_file, 'a', encoding='utf-8') as md:
            if item['category'] == 'figure' or item['category'] == 'chart' :
                try:
                    # 이미지 루트를 반환하는 crop_and_save 함수 호출
                    image_route = crop_and_save(BASE_DIR, route, item['page'], item['coordinates'], item['id'])
                    # 이미지 경로를 Markdown 형식으로 추가
                    md.write(f"![{item['category']}]({image_route.split('/')[-1]})\n\n\n")
                    summary = image_summarization(image_route, company_name, investment)
                    summaries.append(
                        {'id' : element_id,
                        'type' : item['category'],
                        'image_route' : image_route,
                        'dir_route' : dir_route,
                        'file_name' : route.split('/')[-1],
                        'original_content' : None,
                        'page' : item['page'],
                        'investment' : investment,
                        'company_name' : company_name,
                        'table' : None,
                        'summary' : summary,
                        }
                    )
                except:
                    print('에러발생:', item)

            elif item['category'] == 'table':
                try:
                    image_route = crop_and_save(BASE_DIR, route, item['page'], item['coordinates'], item['id'])
                    # 이미지 경로를 Markdown 형식으로 추가
                    # md.write(f"![{item['category']}]({image_route.split('/')[-1]})\n\n\n")
                    summary = table_summarization(image_route, company_name, investment)
                    table_md = summary[:summary.rfind('|')+1]
                    md.write(f"{table_md}\n\n\n")
                    summary = summary[summary.rfind('|')+1:]
                    summaries.append(
                        {'id' : element_id,
                        'type' : item['category'],
                        'image_route' : image_route,
                        'dir_route' : dir_route,
                        'file_name' : route.split('/')[-1],
                        'original_content' : None,
                        'page' : item['page'],
                        'investment' : investment,
                        'company_name' : company_name,
                        'table' : table_md,
                        'summary' : summary,

                        }
                    )
                except:
                    print('에러발생:', item)
            else:
                try:
                    # 이미지가 아닌 경우 html 콘텐츠를 추가
                    html_content = item['content'].get('html', '')
                    if len(html_content)> 100:
                        summary = text_summarizer(html_content, company_name, investment)
                        summaries.append(
                            {'id' : element_id,
                            'type' : item['category'],
                            'iamge_route' : None,
                            'dir_route' : dir_route,
                            'file_name' : route.split('/')[-1],
                            'original_content' : html_content,
                            'page' : item['page'],
                            'investment' : investment,
                            'company_name' : company_name,
                            'table' : None,
                            'summary' : summary,
                            }
                        )
                        md.write(f"{html_content}\n\n\n")
                    else:
                        md.write(f"{html_content}\n\n\n")
                except:
                    print('에러발생:', item)
    result = pd.DataFrame(summaries)
    csv_route = os.path.join(dir_route, file_name + '.csv')
    result['summary'] = result['summary'].apply(lambda x: x[x.find(':')+1:].lstrip())

    def html_to_content(html):
        if not isinstance(html, str):  # 입력이 문자열이 아닌 경우
            return ""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=" ", strip=True)

    result['original_content'] = result['original_content'].apply(html_to_content)
    result.to_csv(csv_route, index = False)
    return result