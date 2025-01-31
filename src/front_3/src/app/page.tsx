"use client";

import { useState } from "react";
import ExampleList from "./_components/ExampleList";
import SearchBar from "./_components/SearchBar";
import ChatList from "./_components/ChatList";
import Sidebar from "./_components/Sidebar";
import type { QAndA } from "./_types/question";
import ThemeToggle from "./_components/ThemeToggle";

export default function Home() {
  const [questionList, setQuestionList] = useState<QAndA[]>([]);
  const [showExampleList, setShowExampleList] = useState(true);

  const handleSubmit = async (formData: FormData) => {
    const 검색받은질문 = formData.get("search") as string;
    
    if (!검색받은질문?.trim()) return;

    const 질문리스트 = questionList.concat({
      question: 검색받은질문,
      answer: null,
    });

    setQuestionList(질문리스트);
    setShowExampleList(false);

    try {
      // API 호출 및 답변 처리 로직
      // 임시로 에러를 발생시켜 테스트
      const random = Math.random();
      if (random < 0.5) throw new Error("API Error");

      setTimeout(() => {
        setQuestionList(prev => 
          prev.map((qa, i) => 
            i === prev.length - 1 
              ? { ...qa, answer: "답변이에용~~ api 호출해서 진짜 답변으로 바꿔야해요!" }
              : qa
          )
        );
      }, 1000);
    } catch (error) {
      setQuestionList(prev => 
        prev.map((qa, i) => 
          i === prev.length - 1 
            ? { ...qa, error: true }
            : qa
        )
      );
    }
  };

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

    try {
      // API 호출 및 답변 처리 로직
      setTimeout(() => {
        setQuestionList(prev => 
          prev.map((qa, i) => 
            i === index 
              ? { ...qa, answer: "재시도 답변이에용~~ api 호출해서 진짜 답변으로 바꿔야해요!" }
              : qa
          )
        );
      }, 1000);
    } catch (error) {
      setQuestionList(prev => 
        prev.map((qa, i) => 
          i === index 
            ? { ...qa, error: true }
            : qa
        )
      );
    }
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