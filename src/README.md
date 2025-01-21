
# SRC 구성
소스코드의 구성은 다음과 같습니다.
## 1. pdf_parsing (담당자 : 용가리)
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

## 2. embedding_models (담당자 용가리, 정유진, 이서현)
embedding_models 폴더는 총 1가지 py 파일이 들어가 있습니다.
1. navercloud_embedding.py
> navercloud의 임베딩v2모델을 사용하여 입력받은 text를 1024의 float vector로 반환합니다.

## 3. evaluation
evaluation 폴더에는 3가지 py 파일이 들어가 있습니다.
1. __init__.py
> import를 편하게 하기 위해 __init__.py를 추가하였습니다.
2. GPT_evaluation.py
> query, retrieved_contexts, ground_truth_answer, generated_answer을 받아 G-eval 점수를 공지된 기준에 따라 평가합니다.
3. retrieval_evaluation.py
> retrieval과 eval_dataset을 받아 eval_dataset에 대한 retrieval의 acc를 print합니다.

## 4. retrievals
retrieval에는 총 4가지 py파일이 들어가 있습니다.
1. __init__.py
> import를 편하게 하기 위해 __init__.py를 추가하였습니다.
bm25, dpr, ensemble의 이름으로 선언할 수 있습니다.
2. BM25_retrieval.py
> kiwi tokenizer를 사용하는 BM25 retrieval입니다. Documents를 입력으로 받습니다.
3. Dense_passage_retrieval.py
> 생성된 db를 받아 DPR을 반환합니다.
4. Ensemble_retrieval.py
> etrievals, topk, weights, search_type을 인자로 받아 Sparse retrieval과 Dense retrieval을 합쳐서 결과를 내는 Ensemble retrieval을 반환합니다.
search type은 다음과 같습니다.
- "similarity" : 유사도 중시 (default 값)
- "mmr" Maximum Marginal Relevance : 다양성 중시
- "similarity_score_threshold" : 유사도 중시 + 사용자 임계값 반영
- "hybrid" : 하이브리드 ("similarity"와 "mmr"을 함께 사용하여 순위 산정)


## 5. utils 
데이터를 불러오는 등 잡다한 함수들이 지정돼 있는 폴더입니다.
1. __init__.py
> import를 편하게 하기 위해 __init__.py를 추가하였습니다.
2. utils.py
> paragraph 데이터만 가져오는 함수(정량평가용), 모든 데이터를 가져오는 함수(정성평가용), 문서들을 Document 타입으로 변환하는 함수가 선언돼 있습니다.

## 6. DB
사용하는 DB를 선언하는 .py파일로 이루어져 있습니다.
현재는 Chromadb만 구현돼 있습니다.
1. Chromadb.py
> add_docs(documents) 함수를 통해 db에 데이터들을 삽입합니다.
이때, List:[Document] 형태로 건네주어야 데이터를 삽입할 수 있습니다.
네이버 클라우드 임베딩 모델을 사용하기에 많은 request를 한번에 요청할 경우, 오류가 발생하므로 배치로 나눈 뒤 배치마다 10초의 딜레이를 주었습니다.
verify_db()를 통해 DB내의 문서 수를 확인하고, DPR 생성을 위한 db객체를 받을 수 있습니다.

# 준비물
> env 파일이 필요합니다. 현재 사용된 api는 총 4가지입니다.
- OPENAI_API_KEY
- UPSTAGE_API_KEY
- HyperclovaX_API_KEY
- HyperclovaX_PRIVATE_KEY
- NAVERCLOUD_EMBEDDING_KEY
- NAVERCLOUD_EMBEDDING_PRIMARY_KEY
