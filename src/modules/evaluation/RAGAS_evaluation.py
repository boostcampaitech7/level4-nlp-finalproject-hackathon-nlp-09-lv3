import pandas as pd
from ragas import SingleTurnSample, EvaluationDataset
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# CSV 파일 로드
df = pd.read_csv("/data/ephemeral/home/level4-nlp-finalproject-hackathon-nlp-09-lv3/src/modules/datas/g_eval_result_GPT_prompt3.csv")

# 데이터 변환
samples = []
for _, row in df.iterrows():
    samples.append(
        SingleTurnSample(
            user_input=row["question"],
            retrieved_contexts=[row["context"]],  # 리스트 형태로 변환
            response=row["generated_answer"],
            reference=row["answer"]
        )
    )

# RAGAS 평가 데이터셋 생성
eval_dataset = EvaluationDataset(samples=samples)

# LLM 설정
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))

# 평가 지표 설정
metrics = [
    Faithfulness(llm=evaluator_llm),
    AnswerRelevancy(llm=evaluator_llm),
    ContextPrecision(llm=evaluator_llm),
    ContextRecall(llm=evaluator_llm),
]

# 평가 실행
results = evaluate(
    dataset=eval_dataset,
    metrics=metrics
)

# 평가 결과를 DataFrame으로 변환
df_results = results.to_pandas()
df_results.to_csv("/data/ephemeral/home/level4-nlp-finalproject-hackathon-nlp-09-lv3/src/modules/datas/RAGAS_evaluation_results.csv", index=False)  # CSV 파일로 저장
print("평가 결과 저장 완료: evaluation_results.csv")
