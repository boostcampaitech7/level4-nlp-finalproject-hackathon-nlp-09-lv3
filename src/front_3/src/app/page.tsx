"use client";

import { useState } from "react";
import { useMutateQueryApi } from "./store/useClosedQueryApi";// API 훅 임포트
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import ExampleList from "./components/ExampleList";
import SearchBar from "./components/SearchBar";
import ChatList from "./components/ChatList";
import Sidebar from "./components/Sidebar";
import type { QAndA } from "./types/question";
import ThemeToggle from "./components/ThemeToggle";


export default function Home() {
  const queryClient = new QueryClient();// QueryClient 생성
  const [questionList, setQuestionList] = useState<QAndA[]>([]);
  const [showExampleList, setShowExampleList] = useState(true); 
  return (
    <QueryClientProvider client={queryClient}> 
      <HomeContent 
        questionList={questionList}
        setQuestionList={setQuestionList}
        showExampleList={showExampleList}
        setShowExampleList={setShowExampleList}
      />
    </QueryClientProvider>
  );
}

function HomeContent({ questionList, setQuestionList, showExampleList, setShowExampleList }) {
  // useMutateQueryApi 훅을 사용해 mutation 객체 가져오기
  const mutation = useMutateQueryApi();

  //응답받는 로직
  const handleSubmit = async (formData: FormData) => {
    const submittedQuestion = formData.get("search") as string;
    
    if (!submittedQuestion?.trim()) return;

    const questionLists = questionList.concat({
      question: submittedQuestion,
      answer: null,
    });

    setQuestionList(questionLists);
    setShowExampleList(false);

    try {
      // API 호출 및 답변 처리 로직
      // 임시로 에러를 발생시켜 테스트
      // const random = Math.random();
      // if (random < 0.5) throw new Error("API Error");

      // API 요청을 mutation.mutate로 처리
      mutation.mutate(
        { query: submittedQuestion },
        {
          onSuccess: (data) => {
          // API 요청 성공 시 응답 데이터 처리
            setQuestionList(prev => 
            prev.map((qa, i) => 
              i === prev.length - 1 
                ? { ...qa, answer: data.answer, context: data.context }
                : qa
          )
        );
      }, 
          onError: (error) => {
            // API 요청 실패 시 처리
            setQuestionList(prev => 
              prev.map((qa, i) => 
                i === prev.length - 1 ? { ...qa, error: true }: qa
              )
            );
            console.error("API 요청 실패:", error);
          },
        }
      );
    } catch (error) {
      // 에러 처리
      setQuestionList(prev =>
        prev.map((qa, i) =>
          i === prev.length - 1 ? { ...qa, error: true } : qa
        )
      );
    }
  };

  //재시도 로직
  const handleRetry = async (index: number) => {
    const question = questionList[index].question;
    
    // 재시도할 질문의 error와 answer 초기화
    setQuestionList(prev => 
      prev.map((qa, i) => 
        i === index 
          ? { ...qa, error: false, answer: null }
          : qa
      )
    );

    // try {
    //   // handleSubmit을 호출하여 질문 재전송
    //   const formData = new FormData();
    //   formData.append("search", question);  // 기존 질문으로 FormData 준비
      
      // // handleSubmit을 재호출
      // await handleSubmit(formData);
      // API 호출 및 답변 처리 로직
      // setTimeout(() => {
      //   setQuestionList(prev => 
      //     prev.map((qa, i) => 
      //       i === index 
      //         ? { ...qa, answer: "재시도 답변이에용~~ api 호출해서 진짜 답변으로 바꿔야해요!" }
      //         : qa
      //     )
      //   );
      // }, 1000);
    
    //  catch (error) {
    //   setQuestionList(prev => 
    //     prev.map((qa, i) => 
    //       i === index ? { ...qa, error: true }: qa
    //     )
    //   );
    // }
  };

  return (
    <div className="flex flex-col min-h-screen bg-[var(--background)]">
      <ThemeToggle />
      {showExampleList && (
        <div className="flex-1 flex flex-col items-center justify-center">
          {/* 로고 섹션 */}
          <div className="text-center mb-16">
            <h1 className="text-4xl font-bold text-[var(--foreground)] mb-4">FinBuddy</h1>
            <img 
              width="64" 
              height="64" 
              src="https://img.icons8.com/pastel-glyph/64/1A1919/dog-jump--v1.png"
              alt="dog-jump--v1"
              className="mx-auto dark:invert"
            />
          </div>

          {/* 예시 목록 섹션 */}
          <div className="w-full max-w-4xl mx-auto px-4">
            <ExampleList 
              questionList={questionList} 
              setQuestionList={setQuestionList}
              setShowExampleList={setShowExampleList}
            />
          </div>
        </div>
      )}

      {/* 채팅 리스트 */}
      {questionList.length > 0 && (
        <ChatList 
          questionList={questionList} 
          onRetry={handleRetry}
        />
      )}

      {/* Sidebar */}
      <Sidebar 
        setQuestionList={setQuestionList}
        setShowExampleList={setShowExampleList}
        showExampleList={showExampleList}
      />

      {/* SearchBar */}
      <div className="w-full max-w-4xl mx-auto px-4">
        <SearchBar handleSubmit={handleSubmit} />
      </div>
    </div>

  );
}