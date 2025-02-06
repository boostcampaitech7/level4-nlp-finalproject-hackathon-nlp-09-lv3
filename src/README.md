
# SRC 구성
소스코드의 구성은 다음과 같습니다.

## backends
> 정량, 정성평가를 위한 api endpoint api 및 응답/답변 schema, 라우터, 미들웨어가 지정돼 있습니다.
파이프라인 코드를 활용하여 front로부터 받아온 query를 활용하여 답변을 내부 엔진에서 제작하여 제출합니다.

## front
> front잘모름 

## modules
> 프로젝트가 동작하기 위한 소스코드들이 첨부돼 있습니다.
### 1. pdf_parsing
pdf_parsing 폴더에 총 4가지 py 파일이 들어가 있습니다.

sample.ipynb에 코드 사용에 대한 흐름이 작성돼 있습니다.
1. cropper.py
> pdf, 페이지, 좌표를 입력받아 BASE_DIR로 지정된 폴더에 테이블, 그래프 이미지를 저장합니다.
2. make_md_and_summaries.py
> summarizer_for_rag.py에 선언된 summarize 함수들을 바탕으로 pdf의 내용들을 마크다운으로 저장합니다.
테이블 사진은 마크다운으로 바뀌어 md파일에 삽입되고, 그래프는 이미지의 경로를 삽입하여 볼 수 있도록 합니다.
이후, csv파일 형태로 각 그래프, 테이블, Documents들의 요약문을 저장합니다.
3. summarizer_for_rag.py
> 그래프와 테이블, Document를 받아 내용을 200자 이내로 요약합니다.
그래프와 테이블에는 gpt 4o-mini를 사용하며, Document의 요약에는 gpt 4o-mini와 HyperclovaX중 하나를 사용합니다.
4. upstage_parser.py
> pdf를 받아 pdf의 내용을 요소별로 파싱합니다. 그래프, 테이블, Document 등이 파싱됩니다.
파싱된 내용들은 json의 형태로 지정한 BASE_DIR에 저장됩니다.

### 2. embedding_models
embedding_models 폴더는 총 4가지 py 파일이 들어가 있습니다.
타 모델 대비 약 10%정도 성능이 앞섰기에 프로젝트에 사용되는 모델은 navercloud embedding모델입니다.(topk5 85%)
1. navercloud_embedding.py
> navercloud의 임베딩v2모델을 사용하여 입력받은 text를 1024의 float vector로 반환합니다.
2. kf_deberta_embedding.py
> 카카오뱅크의 금융 특화 임베딩 모델입니다.
3. kure_embedding.py
> bge-m3 기반 고려대학교의 금융 특화 임베딩 모델입니다.
4. openai_embedding.py
>openai의 LLM기반 임베딩 모델입니다.

### 3. evaluation
evaluation 폴더에는 3가지 py 파일이 들어가 있습니다.
1. __init__.py
> import를 편하게 하기 위해 __init__.py를 추가하였습니다.
2. GPT_evaluation.py
> query, retrieved_contexts, ground_truth_answer, generated_answer을 받아 G-eval 점수를 공지된 기준에 따라 평가합니다. retrieval score와 generation score을 각각 측정합니다.
3. retrieval_evaluation.py
> retrieval과 eval_dataset을 받아 eval_dataset에 대한 retrieval의 acc를 print합니다.

### 4. retrievals
retrieval에는 총 5가지 py파일이 들어가 있습니다.
성능 평가 결과, bm25와 dpr의 ensemble retriever이 가장 성능이 좋아 이를 사용합니다.
1. __init__.py
> import를 편하게 하기 위해 __init__.py를 추가하였습니다.
bm25, dpr, ensemble의 이름으로 선언할 수 있습니다.
2. BM25_retrieval.py
> kiwi tokenizer를 사용하는 BM25 retrieval입니다. Documents를 입력으로 받습니다.
3. Dense_passage_retrieval.py
> 생성된 db를 받아 DPR을 반환합니다.
4. LLM_retrieval.py
> 주어진 문서들(약 10~20개) 중, LLM이 직접 기준에 따라 선택하도록 합니다.
5. Ensemble_retrieval.py
> etrievals, topk, weights, search_type을 인자로 받아 Sparse retrieval과 Dense retrieval을 합쳐서 결과를 내는 Ensemble retrieval을 반환합니다.
search type은 다음과 같습니다.
- "similarity" : 유사도 중시 (default 값)
- "mmr" Maximum Marginal Relevance : 다양성 중시
- "similarity_score_threshold" : 유사도 중시 + 사용자 임계값 반영
- "hybrid" : 하이브리드 ("similarity"와 "mmr"을 함께 사용하여 순위 산정)


### 5. utils 
데이터를 불러오는 등 잡다한 함수들이 지정돼 있는 폴더입니다.
1. __init__.py
> import를 편하게 하기 위해 __init__.py를 추가하였습니다.
2. utils.py
> paragraph 데이터만 가져오는 함수(정량평가용), 모든 데이터를 가져오는 함수(정성평가용), 문서들을 Document 타입으로 변환하는 함수가 선언돼 있습니다.

### 6. DB
사용하는 DB를 선언하는 .py파일로 이루어져 있습니다.
현재는 Chromadb만 구현돼 있습니다.
1. Chromadb.py
> add_docs(documents) 함수를 통해 db에 데이터들을 삽입합니다.
이때, List:[Document] 형태로 건네주어야 데이터를 삽입할 수 있습니다.
네이버 클라우드 임베딩 모델을 사용하기에 많은 request를 한번에 요청할 경우, 오류가 발생하므로 배치로 나눈 뒤 배치마다 10초의 딜레이를 주었습니다.
verify_db()를 통해 DB내의 문서 수를 확인하고, DPR 생성을 위한 db객체를 받을 수 있습니다.

### 7. making_datas
Validation dataset의 제작을 위한 코드들이 담긴 폴더입니다.
1. make_validation_dataset.py
> Retrieval, Generation Evaluation을 위한 QA 데이터셋을 GPT를 사용해 제작합니다.

### 8. QA_model
QA_model에는 총 8가지 py 파일로 구성돼 있습니다.
1. __init__.py
> 다양한 모델들의 임포트를 편리하게 수행하도록 작성된 초기화 스크립트입니다.
2. base_model.py
> 모델의 answering 상속을 위해 지정된 class입니다.
3. exaone_model.py
> LGAI의 엑사원 8B모델입니다.
4. gpt_model.py
> gpt 4o mini 또는 gpt 4o를 지정하여 사용할 수 있는 모델입니다.
5. hyperclova_model.py
> 네이버클라우드의 하이퍼클로바 모델입니다.
6. qwen_model.py
> qwen 2.5 7B 모델입니다.
7. qwen14b.py
> deepseek R1으로부터 knowledge distillation 된 qwen 2.5 14B 모델입니다.
8. qwen32b.py
> deepseek R1으로부터 knowledge distillation 된 qwen 2.5 32B 모델입니다.

### 9. Finbuddy
Finbuddy에는 정성평가를 위한 Agent가 구현돼 있습니다.
Finbuddy의 구조는 다음과 같습니다.
- __init__.py
- context_crew.py : 본문을 받아 처리하는 에이전트입니다.
- image_crew.py : 이미지를 받아 처리하는 에이전트입니다.
- news_search_crew.py : 뉴스 기사를 검색하여 질문에 대답하는 에이전트입니다.
- table_crew.py : 테이블을 받아 처리하는 에이전트입니다.
- final_crew.py : 각 에이전트의 답변을 종합하여 질문에 대한 대답을 생성하는 에이전트입니다.
- config
    - agent들의 yaml파일
    - task들의 yaml파일
- tools
    - __init__.py : tool들을 임포트하기 편리하도록 초기화하는 스크립트입니다.
    - code_executetool.py : Agent가 생성한 코드를 실행하는 도구입니다.
    - naver_news_search.py : 네이버의 뉴스 기사 검색 API를 활용하여 최신 뉴스를 검색하는 도구입니다.
    - urls_to_context.py : 입력받은 url에 방문하여 내용을 가져오는 도구입니다.

### 10. Pipeline
Pipeline 폴더에는 정량, 정성평가를 위한 파이프라인들이 형성돼 있습니다.
1. __init__.py
> 임포트를 편리하기 수행하기 위한 초기화 스크립트입니다.
2. Pipe_for_eval.py
> 정량평가를 위한 파이프라인입니다. 질문을 받아 평가에 필요한 context들과 answer을 출력합니다.
3. Pipe_for_service.py
> 정성평가를 위한 Agent 파이프라인입니다. 질문을 받아 적절한 Agent에게 분배하여 답변을 출력합니다.

# 준비물
> env 파일이 필요합니다. 현재 사용된 api는 총 4가지입니다.
- OPENAI_API_KEY
- UPSTAGE_API_KEY
- HyperclovaX_API_KEY
- HyperclovaX_PRIVATE_KEY
- NAVERCLOUD_EMBEDDING_KEY
- NAVERCLOUD_EMBEDDING_PRIMARY_KEY
- NAVER_API_CLIENT_ID
- NAVER_API_CLIENT_SECRET
