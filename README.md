# 네이버 부스트캠프 AI Tech 기업언계해커톤 랩큐 NLP 9조 - FinBuddy
</br>

## 증권사 자료 기반 주식 LLM 서비스 개발
증권사 보고서를 활용하여 LLM 응용 시 매우 중요한 RAG(Retrieval Augmented Generation) 기술을 탐구하여 최상의 답변을 하는 LLM 서비스를 구현
<br><br>
## 1. Overview
FinBuddy는 증권사 보고서를 활용한 LLM 기반 주식 정보 제공 서비스입니다. 최신 자연어처리(NLP) 기술과 RAG(Retrieval-Augmented Generation) 기법을 적용하여, 신뢰할 수 있는 금융 정보를 사용자에게 제공하는 것을 목표로 합니다.

### 주요 목표

- 증권사 보고서를 효율적으로 검색 및 활용하여 LLM 모델의 답변 정확도 향상
- RAG 기반 검색 시스템 구축 및 성능 최적화
- 사용자 질의에 대한 적절한 주식 투자 정보 제공

## 2. 프로젝트 구성

### ⏰ 개발 기간
- 2025년 1월 10일 ~ 2025년 2월 12일
- 부스트캠프 AI Tech NLP 트랙 20-24주차 

### 프로젝트 기획
<img width="1430" alt="스크린샷 2025-02-11 오후 4 12 22" src="https://github.com/user-attachments/assets/00783c2d-33ae-4735-9247-407ef5a52113" />
</br>
<img width="1428" alt="스크린샷 2025-02-11 오후 4 12 34" src="https://github.com/user-attachments/assets/695afc08-6f80-418a-8367-7258c7ac49bb" />
</br>
<img width="1429" alt="스크린샷 2025-02-11 오후 4 12 43" src="https://github.com/user-attachments/assets/649234e2-2716-43ba-9297-d9b7baf15476" />
</br>

### 역할 분담
<img width="1426" alt="스크린샷 2025-02-11 오후 4 12 50" src="https://github.com/user-attachments/assets/ba5c4765-5ed4-4bbd-8861-39eb55acd77f" />
</br>

### ✨ 분석 환경
- Upstage AI Stages 제공 NVIDIA V100 GPU Server 활용
- OS : Linux
- Language : Python, JavaScript
- Libraries(mainly used) : Pytorch, HuggingFace, FastAPI, React, LangChain, ChromaDB, etc.
<br>

### 🏗 기술 스택

- **LLM** : GPT-4o-mini, LG EXAONE, Qwen 등 모델 활용
- **RAG** : ChromaDB 기반 벡터 검색 및 문서 임베딩
- **데이터 전처리** : PDF 문서 파싱(Upstage) 및 요약 모델 적용
- **모델 학습 및 평가** : G-eval, RAGAS

<p>
<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=LangChain&logoColor=white">
<img src="https://img.shields.io/badge/CrewAI-FF5A50?style=for-the-badge&logo=CrewAI&logoColor=white">
</p>

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white">
</p>

<p>
<img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=white">
<img src="https://img.shields.io/badge/Next_js-000000?style=for-the-badge&logo=Next_js&logoColor=white">
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=TypeScript&logoColor=white">
<img src="https://img.shields.io/badge/Tailwind CSS-06B6D4?style=for-the-badge&logo=Tailwind CSS&logoColor=white">
</p>

<p>
<img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white">
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
</p>

### 서비스 아키텍처
<img width="1426" alt="스크린샷 2025-02-11 오후 4 10 37" src="https://github.com/user-attachments/assets/f0bbaac6-9cb7-43c0-94ed-c6dbf92042bd" />
</br>

### 2.1. 데이터 전처리
**제공 데이터**
<img width="1421" alt="스크린샷 2025-02-11 오후 4 13 47" src="https://github.com/user-attachments/assets/83f9e8c4-0ab1-42f1-a264-4d047a7cb5b0" />
</br>

**PDF Parsing**
<img width="1422" alt="스크린샷 2025-02-11 오후 4 13 19" src="https://github.com/user-attachments/assets/feef88f5-3433-4e6b-957a-b66db79d9383" />
</br>

### 2.2 AI Agent 구조
<img width="1424" alt="스크린샷 2025-02-11 오후 4 11 15" src="https://github.com/user-attachments/assets/a758fa7b-02c3-4cb0-8410-969107a57f62" />
</br>

### 2.3. 모델 학습 및 평가
<img width="1427" alt="스크린샷 2025-02-11 오후 4 11 00" src="https://github.com/user-attachments/assets/f448783e-a244-4cdc-9184-53527a25139e" />
</br>

### 2.4. Backend 개발
FastAPI를 이용한 REST API 구성
- Open domain : 네이버 뉴스 검색을 통한 최신 정보 확인 가능
- Closed domain : 제공된 데이터 기반 RAG
- query : Chat-GPT 4o mini API 연동


### 2.5. Frontend 개발
axios를 이용한 API 연동
리액트 훅을 이용한 페이지 변수 값 상태 관리

## 4. 프로젝트 결과

### 시연 영상
<div align="center">
<video src = "" controls></video>
</div>



## 5. Team
<table>
    <tbody>
        <tr>
            <td align="center">
                <a href="https://github.com/Kimyongari">
                    <img src="https://github.com/Kimyongari.png" width="100px;" alt=""/><br />
                    <sub><b>Kimyongari</b></sub>
                </a><br />
                <sub>김용준</sub>
            </td>
            <td align="center">
                <a href="https://github.com/Soobin-Park">
                    <img src="https://github.com/Soobin-Park.png" width="100px;" alt=""/><br />
                    <sub><b>Soobin-Park</b></sub>
                </a><br />
                <sub>박수빈</sub>
            </td>
            <td align="center">
                <a href="https://github.com/seohyeon0677">
                    <img src="https://github.com/seohyeon0677.png" width="100px;" alt=""/><br />
                    <sub><b>seohyeon0677</b></sub>
                </a><br />
                <sub>이서현</sub>
            </td>
            <td align="center">
                <a href="https://github.com/Aitoast">
                    <img src="https://github.com/Aitoast.png" width="100px;" alt=""/><br />
                    <sub><b>Aitoast</b></sub>
                </a><br />
                <sub>정석현</sub>
            </td>
            <td align="center">
                <a href="https://github.com/uzlnee">
                    <img src="https://github.com/uzlnee.png" width="100px;" alt=""/><br />
                    <sub><b>uzlnee</b></sub>
                </a><br />
                <sub>정유진</sub>
            </td>
        </tr>
    </tbody>
</table>
<br><br>

---

## Reference
- [ChromaDB](https://docs.trychroma.com/docs/overview/introduction)
- [LangChain](https://python.langchain.com/docs/get_started/introduction)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [GPT-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini)
- [LG EXAONE](https://exaone.lge.com/exaone-api)
- [Qwen](https://qwen.baidu.com/doc/index)
