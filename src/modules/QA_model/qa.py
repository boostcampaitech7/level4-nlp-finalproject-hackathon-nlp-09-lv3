import os
import glob
import requests
import pandas as pd
from openai import OpenAI

from dotenv import load_dotenv

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

try:
    import nltk
    from nltk.tokenize import word_tokenize
except ImportError:
    nltk = None
    word_tokenize = None


import torch
import requests
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

load_dotenv()



###############################################
# 1) CSV 로드 & RAG Data 생성
###############################################

def load_csv_data_from_dirs(base_dir: str) -> pd.DataFrame:
    """
    base_dir 아래의 모든 *.csv 파일을 찾아 하나의 DataFrame으로 합칩니다.
    """
    csv_files = glob.glob(os.path.join(base_dir, "**", "*.csv"), recursive=True)
    all_df_list = []
    for csv_path in csv_files:
        try:
            df = pd.read_csv(csv_path, keep_default_na=False)
            df["__csv_path__"] = csv_path
            all_df_list.append(df)
        except Exception as e:
            print(f"[WARN] CSV 로드 오류: {csv_path}, {e}")
    if not all_df_list:
        return pd.DataFrame()
    return pd.concat(all_df_list, ignore_index=True)


def build_rag_data(df: pd.DataFrame) -> list:
    """
    CSV에서 RAG 용( id, type, summary, original_content )을 추려 list[dict]로 변환.
    """
    rag_data = []
    for idx, row in df.iterrows():
        item = {
            "id": row.get("id", f"row_{idx}"),
            "type": row.get("type", ""),
            # 이미지 부분은 사용하지 않으므로 제외/주석
            # "image_path": row.get("image_route", ""),
            "summary": row.get("summary", ""),
            "original_content": row.get("original_content", ""),
        }
        rag_data.append(item)
    return rag_data


###############################################
# 2) RAG 검색 (간단 / BM25)
###############################################

def simple_rag_search(question: str, data_list: list, top_k=3):
    q_tokens = question.lower().split()
    scored = []
    for item in data_list:
        text = f"{item['summary']} {item['original_content']}".lower()
        score = 0
        for t in q_tokens:
            if t in text:
                score += 1
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    top_items = [it for sc, it in scored[:top_k] if sc > 0]
    return top_items


def bm25_rag_search(question: str, data_list: list, top_k=3):
    if BM25Okapi is None or nltk is None or word_tokenize is None:
        return simple_rag_search(question, data_list, top_k=top_k)

    corpus = [f"{it['summary']} {it['original_content']}" for it in data_list]
    tokenized_corpus = [word_tokenize(doc.lower()) for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    q_tokens = word_tokenize(question.lower())
    scores = bm25.get_scores(q_tokens)
    scored = list(zip(scores, data_list))
    scored.sort(key=lambda x: x[0], reverse=True)
    top_items = [it for sc, it in scored[:top_k] if sc > 0]
    return top_items


def rag_search(question: str, data_list: list, top_k=3, use_bm25=False):
    if use_bm25:
        return bm25_rag_search(question, data_list, top_k=top_k)
    else:
        return simple_rag_search(question, data_list, top_k=top_k)


###############################################
# 3) GPT-4o-mini API 예시 (선택)
###############################################


def call_openai_api(prompt):
    """
    OpenAI API를 호출하여 GPT 모델로부터 응답을 얻는 함수.
    """
    api_key = os.environ['OPENAI_API_KEY']
    if not api_key:
        return "API 키가 설정되지 않았습니다. 환경 변수 'OPENAI_API_KEY'를 설정하세요."
    client = OpenAI(api_key=api_key)
    # OpenAI API 키 설정
    try:
        # GPT-4 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 Retreived 된 문서 내용을 정리하여 설명해줍니다."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API 호출 실패: {e}"


###############################################
# 4) 모델 초기화
###############################################

def init_model(model_name: str):
    """
    model_name에 따라:
      - "Qwen/Qwen2.5-7B-Instruct"
      - "LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct"
      - "GPT-4o-mini" (예시 API)
    식으로 분기해 로드(또는 API 사용)를 결정.
    반환: {"mode": "qwen"|"exaone"|"api", "tokenizer":..., "model":...} 등
    """
    if model_name == "GPT-4o-mini":
        # API만 호출
        return {
            "mode": "api",
            "api_name": "gpt4o-mini"
        }

    elif "Qwen" in model_name:
        # Qwen 모델 로드
        print(f"Loading Qwen model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            device_map="auto",
            trust_remote_code=True
        )
        return {
            "mode": "qwen",
            "model_name": model_name,
            "tokenizer": tokenizer,
            "model": model
        }

    elif "EXAONE" in model_name:
        # EXAONE 모델 로드
        print(f"Loading EXAONE model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )
        return {
            "mode": "exaone",
            "model_name": model_name,
            "tokenizer": tokenizer,
            "model": model
        }
    else:
        # 그 외 모델 (단순 CAusalLM)
        print(f"Loading generic HF model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )
        return {
            "mode": "generic",
            "model_name": model_name,
            "tokenizer": tokenizer,
            "model": model
        }


###############################################
# 5) RAG + 모델로 질의에 답변
###############################################

def answer_question(
    question: str,
    data_list: list,
    model_handle: dict,
    top_k=3,
    use_bm25=False
):
    # 1) RAG 검색
    relevant_items = rag_search(question, data_list, top_k=top_k, use_bm25=use_bm25)
    if not relevant_items:
        return f"[질문] {question}\n[답변] 관련된 자료를 찾지 못했습니다."

    # 2) RAG context 구성
    context_parts = []
    for item in relevant_items:
        if item["summary"]:
            context_parts.append(item["summary"])
        elif item["original_content"]:
            context_parts.append(item["original_content"])
    context_text = "\n".join(context_parts)

    # 여기서는 단순히 "system"과 "user"를 구성 (Qwen, EXAONE에서 조금씩 포맷이 다름)
    # 실제로는 모델 별 template를 약간 달리 적용해야 합니다.

    # 대화 내용:
    system_msg = ""
    if model_handle["mode"] == "qwen":
        system_msg = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
    elif model_handle["mode"] == "exaone":
        system_msg = "You are EXAONE model from LG AI Research, a helpful assistant."
    else:
        system_msg = "You are a helpful assistant."

    prompt_user = (
        f"Here is some context from CSV:\n{context_text}\n"
        f"Question: {question}\n"
        f"Please answer using the above context."
    )

    ###############################################
    #  (A) GPT-4o-mini API 모드
    ###############################################
    if model_handle["mode"] == "api":
        # 단순히 system+user를 이어붙인 뒤 API 호출 예시
        # (실제 API 규격에 맞추어 JSON body를 구성해야 한다면 수정)
        combined_prompt = f"[System]\n{system_msg}\n[User]\n{prompt_user}\n[Assistant]"
        return call_openai_api(combined_prompt)

    ###############################################
    #  (B) Qwen
    ###############################################
    if model_handle["mode"] == "qwen":
        tokenizer = model_handle["tokenizer"]
        model = model_handle["model"]

        # Qwen은 messages를 이용해 apply_chat_template 호출
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt_user},
        ]
        text_for_model = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text_for_model], return_tensors="pt").to(model.device)

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            # do_sample=True, top_p=0.9, temperature=0.8 등 필요시 추가
        )
        # Qwen에서는 input prompt 길이만큼 잘라내는 작업(예: 아래) 권장
        generated_ids = [
            out[len(inp):] for inp, out in zip(model_inputs.input_ids, generated_ids)
        ]

        answer_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return f"[질문]\n{question}\n\n[답변]\n{answer_text}"

    ###############################################
    #  (C) EXAONE
    ###############################################
    if model_handle["mode"] == "exaone":
        tokenizer = model_handle["tokenizer"]
        model = model_handle["model"]

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt_user},
        ]
        out = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        )

        # 반환값이 dict인지 tensor인지 분기
        if isinstance(out, dict):
            out = {k: v.to(model.device) for k, v in out.items()}
        elif isinstance(out, torch.Tensor):
            out = {"input_ids": out.to(model.device)}
        else:
            raise ValueError(f"Unknown type returned from apply_chat_template: {type(out)}")

        output = model.generate(
            **out,
            max_new_tokens=512,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=False,
        )
        # 결과 디코딩
        answer_text = tokenizer.decode(output[0], skip_special_tokens=True)

        # **필요 없는 텍스트 제거** (추가된 부분)
        if "[|assistant|]" in answer_text:
            answer_text = answer_text.split("[|assistant|]")[-1].strip()

        return answer_text

    ###############################################
    #  (D) 기타 generic 모델
    ###############################################
    tokenizer = model_handle["tokenizer"]
    model = model_handle["model"]
    # 간단히 system+user를 이어붙인 뒤, generate
    combined_prompt = f"[System]\n{system_msg}\n[User]\n{prompt_user}\n[Assistant]"
    inputs = tokenizer(combined_prompt, return_tensors="pt").to(model.device)
    gen_out = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False
    )
    result_text = tokenizer.decode(gen_out[0], skip_special_tokens=True)
    # 필요 시 prompt만큼 잘라낸다
    if result_text.startswith(combined_prompt):
        result_text = result_text[len(combined_prompt):].strip()
    return f"[질문]\n{question}\n\n[답변]\n{result_text}"


###############################################
# 메인 실행 테스트
###############################################
if __name__ == "__main__":
    if nltk is not None:
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass

    # 1) 데이터 로드
    base_dir = "/data/jung/src/datas"  # 예시
    df_all = load_csv_data_from_dirs(base_dir)
    rag_data = build_rag_data(df_all)

    # 2) 모델 초기화 (Qwen, EXAONE, GPT-4o-mini 등)
    # model_handle = init_model("Qwen/Qwen2.5-7B-Instruct")
    # model_handle = init_model("LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct")
    model_handle = init_model("GPT-4o-mini")  # 예시

    # 3) 질문 & 답변
    user_question = "크래프톤의 발행 주식 수는?"
    answer = answer_question(
        question=user_question,
        data_list=rag_data,
        model_handle=model_handle,
        top_k=3,
        use_bm25=False
    )
    print(answer)