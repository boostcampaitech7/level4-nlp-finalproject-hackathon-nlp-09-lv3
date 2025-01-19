import pandas as pd
from glob import glob
import os
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm

routes = glob('datas/*/*.csv')
load_dotenv()

df = pd.DataFrame()
for route in routes:
    df = pd.concat([df, pd.read_csv(route)])

print(df.head(1))

paragraphs = df[df['type'] == 'paragraph']
paragraphs = paragraphs.reset_index(drop = True)
def html_to_content(html):
    if not isinstance(html, str):  # 입력이 문자열이 아닌 경우
        return ""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=" ", strip=True)

paragraphs['original_content'] = paragraphs['original_content'].apply(html_to_content)
paragraphs['len'] = paragraphs['original_content'].apply(lambda x :len(x))
source = paragraphs[paragraphs['len'] > 100][['original_content', 'company_name', 'investment']].reset_index(drop = True)

def make_validation_data(original_content, company_name, investment):
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system", 
                "content": """당신은 QA 데이터셋 제작자입니다. 주어진 정보를 바탕으로 질문과 답변을 제작하세요.
                        질문은 실제 사용자가 할 수 있는 질문으로 만드세요.
                        질문은 100자 미만으로 제작하세요.
                        반드시 단답형이 아닌 어려운 주관식 문제를 제작하세요.
                        
                        [예시 1]
                        질문: CJ제일제당의 2025년 매출액은 얼마로 예상되나요?
                        답변: CJ제일제당의 2025년 매출액은 31,077.2 십억 원입니다

                        [예시 2]
                        질문: 2024년 7월에 예상한 LG화학의 양극재 2024년 4분기 판매량과 판가 전망은 어떻게 됐었나요?
                        답변: 2024년 7월에 예상된 LG화학의 2024년 4분기 양극재 판매량과 판가 전망은 다음과 같았습니다:
                            - 판매량: 전분기와 유사한 수준으로 유지될 것으로 예상
                            - 판가: 전분기 대비 10% 하락이 전망됨

                        [예시 3]
                        질문: SK하이닉스의 2024년 분기별 예상 세전 계속사업이익은?
                        답변: SK하이닉스의 2024년 분기별 예상 세전 계속사업이익은 아래와 같습니다:
                            - 1분기: 2,373억 원
                            - 2분기: 5,052억 원
                            - 3분기: 6,879억 원
                            - 4분기 (예상): 7,060억 원
                            - 연간 (예상): 21,364억 원

                        [예시 4]
                        질문: SK하이닉스는 HBM CAPA가 거의 다 Sold Out된 상황에서, 2025년 추가적인 수요에 어떻게 대응할 계획인가요?
                        답변: SK하이닉스는 2025년 추가적인 수요에 대응하기 위해 다음과 같은 계획을 진행 중입니다:
                            - TSV CAPA 확대: 작년 대비 2배 이상 늘리는 작업이 순조롭게 진행되고 있음.
                            - HBM3E 생산 확대: 예상보다 빠르게 증가하는 HBM3E 수요에 대응하기 위해 레거시 기술을 선단 공정으로 전환하여 생산 능력을 최대한 집중할 계획.
                            - 한계 인식: 당초 계획 대비 증가된 물량을 모두 소화하는 데에는 한계가 있을 수 있다는 점도 고려하고 있음.
                        결론: SK하이닉스는 생산 능력 확대와 기술 전환을 통해 추가적인 수요에 대응하고자 하지만, 공급 여력의 한계를 인지하고 있는 상황입니다.
                        """
            },
            {
                "role": "user", 
                "content": f"""
                회사 이름 : {company_name}
                리포트 작성 기관 : {investment}

                [원문]
                {original_content}

                [출력 형식]
                질문 : [원문을 읽고 풀이할 수 있는 어려운 질문]
                답변 : [질문에 대한 답변]
                """
            }
        ],
        temperature=0.0,
    )

    qa = response.choices[0].message.content
    return qa

def extract_qa(qa_text):
    if qa_text is None:
        return None, None
    
    try:
        parts = qa_text.split('답변:', 1)
        
        if len(parts) != 2:
            return None, None
        
        question_part, answer = parts
        
        # '질문:' 제거
        question = question_part.replace('질문:', '').strip()
        answer = answer.strip()
        
        return question, answer
    except:
        return None, None

results = []

for idx in tqdm(range(len(source))):
    context = source.loc[idx]['original_content']
    company = source.loc[idx]['company_name']
    investment = source.loc[idx]['investment']

    qa = make_validation_data(context, company, investment)
    question, answer = extract_qa(qa)
    
    results.append({
        'company_name': company,
        'investment': investment,
        'context': context,
        'question': question,
        'answer': answer
    })

    print("회사명:", results[-1]['company_name'])
    print("\n질문:", results[-1]['question'])
    print("\n답변:", results[-1]['answer'])
    print("\n원문:", results[-1]['context'])
    print("\n작성기관:", results[-1]['investment'])

result_df = pd.DataFrame(results)
result_df.to_csv('qa_validation_dataset_2.csv', index=False, encoding='utf-8-sig')
print("Dataset has been saved to 'qa_validation_dataset_2.csv'")