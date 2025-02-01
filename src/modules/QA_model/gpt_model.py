import os
from openai import OpenAI
from QA_model.base_model import BaseModel
from dotenv import load_dotenv
load_dotenv()

class GPTModel(BaseModel):
    def __init__(self, model_name="gpt-4o"):
        self.api_key = os.environ['OPENAI_API_KEY']
        if not self.api_key:
            raise ValueError("환경 변수 'OPENAI_API_KEY'가 설정되지 않았습니다.")
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model_name

    def answering(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "당신은 참고문서들을 활용하여 질문에 대한 답변을 제공하는 주식 전문가입니다."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=512,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"API 호출 실패: {e}"
