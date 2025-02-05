from pydantic import BaseModel
from openai import OpenAI
class ToolChoice(BaseModel):
    tool: str
    final_answer: str

class GPT_Router:
    def __init__(self):
        self.client = OpenAI()

    def answering(self, query:str)->str:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """당신은 Finbuddy의 RAG 시스템 사용 결정자입니다.
                주어지는 질문을 분석하여 가장 알맞는 시스템을 사용하도록 지시합니다.
                사용 가능한 시스템 : [최신 뉴스기사 검색, 내부 주식 리포트 RAG, 직접 답변]"""},
                {"role": "user", "content": f"""
                주어진 질문이 최신 내용에 대해 묻고 있다면 최신 뉴스기사를 검색하도록 지시하세요.
                주어진 질문이 기업에 대한 자세한 분석을 요구한다면 내부 주식 리포트 RAG를 사용하도록 지시하세요.
                만약 당신이 알고 있는 내용이라면 tool에서 직접 답변을 고르고 final_answer에 질문에 대한 대답을 입력하세요.
                어렵지 않은 질문이라면 직접 대답하세요.
                도구를 사용하는 경우, tool에 사용할 도구 이름을 입력한 뒤, final_answer에는 사용자 질문을 RAG 시스템이 잘 검색할 수 있도록 깔끔하게 다듬으세요.
                사용자 질문: {query}"""}
            ],
            response_format=ToolChoice,
            )

        answer = completion.choices[0].message.parsed

        return answer