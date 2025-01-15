
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


# 준비물
1. .env 파일이 필요합니다.
   1. upsage api key
   2. navercloud api key
   3. navercloud private key
   4. openai api key