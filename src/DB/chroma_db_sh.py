import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import chromadb

# Chroma 클라이언트 초기화
client = chromadb.Client()  # 더 이상 Settings를 명시적으로 전달하지 않음

# 컬렉션 생성 또는 가져오기
collection_name = "text_data"
collection = client.get_or_create_collection(name=collection_name)

# CSV 파일 경로
csv_file = r"C:\Users\seohy\Desktop\boostcamp_AITech\LabQ\level4-nlp-finalproject-hackathon-nlp-09-lv3\datas\CJ제일배당_교보증권(2024.11.13)\CJ제일배당_교보증권(2024.11.13).csv"  # 사용자가 업로드한 파일 경로

# CSV 데이터 읽기
df = pd.read_csv(csv_file)

# 텍스트 데이터 준비
text_data = df['summary'].fillna('') if 'summary' in df.columns else df['original_content'].fillna('')

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=300)  # 최대 300개의 차원으로 제한
embeddings = vectorizer.fit_transform(text_data).toarray()

# Chroma DB에 데이터 저장
for index, embedding in enumerate(embeddings):
    document_id = str(df.loc[index, 'id'])  # 고유 ID
    metadata = df.loc[index].to_dict()  # 메타데이터로 저장
    
    collection.add(
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[document_id]
    )

print(f"데이터 {len(df)}개가 Chroma DB에 저장되었습니다.")


def search_similar_documents(query, collection, vectorizer):
    # 쿼리 문장 벡터화
    query_vector = vectorizer.transform([query]).toarray()  # 쿼리 문장을 벡터로 변환
    
    # 저장된 임베딩 벡터의 차원과 일치하도록 query_vector를 맞춥니다.
    if query_vector.shape[1] != 300:
        print(f"쿼리 벡터 차원이 다릅니다: {query_vector.shape[1]}")
        return
    
    # Chroma DB에서 유사도 검색
    results = collection.query(query_embeddings=query_vector.tolist(), n_results=5)
    
    # 검색된 문서 출력
    print(f"쿼리: {query}\n")
    
    if not results['documents']:
        print("검색된 문서가 없습니다.")
        return
    
    print(len(results))
    print(results)

# 검색할 쿼리 문장
query_text = 'CJ제일제당의 시가총액'

# Chroma DB에서 유사한 문서 검색
search_similar_documents(query_text, collection, vectorizer)
