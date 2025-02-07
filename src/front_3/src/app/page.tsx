"use client";

import { useState, useRef, Dispatch, SetStateAction } from "react";
import { useClosedQueryApi } from "./store/useClosedQueryApi";// API 훅 임포트
//import { closedQueryClient } from "./store/closedQueryClient";// API 훅 임포트
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import ExampleList from "./components/ExampleList";
import SearchBar from "./components/SearchBar";
import ChatList from "./components/ChatList";
import ThemeToggle from "./components/ThemeToggle";
import ChatHistoryMenu from './components/ChatHistoryMenu';
import type { ChatHistory } from './types/chatHistory';
import { parseApiResponse } from './api/parsers/chatParser';
import type { QAndA } from "./types/question";

export const closedQueryClient = new QueryClient();

function HomeContent() {
  const [questionList, setQuestionList] = useState<QAndA[]>([]);
  const [showExampleList, setShowExampleList] = useState(true);
  const [histories, setHistories] = useState<ChatHistory[]>([]);
  const [domain, setDomain] = useState<'open' | 'close' | null>(null);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [loadingIndex, setLoadingIndex] = useState<number | null>(null);
  
  const searchBarRef = useRef<{ setText: (text: string) => void } | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const { mutate, isPending }  = useClosedQueryApi(); // mutation 객체 사용

  const handleExampleClick = (example: string) => {
    const formData = new FormData();
    formData.append('search', example);
    handleSubmit(formData);
  };

  const handleSubmit = async (formData: FormData) => {
    const submittedQuestion = formData.get("search") as string;
    
    if (!submittedQuestion?.trim()) return;

    const newQuestion = {
      question: submittedQuestion,
      answer: null,
    };

    let newId: string | null = null;

    if (!currentChatId) {
      newId = Date.now().toString();
      setCurrentChatId(newId);
      const newHistory: ChatHistory = {
        id: newId,
        title: submittedQuestion,
        messages: [newQuestion],
        createdAt: new Date(),
      };
      setHistories(prev => [newHistory, ...prev]);
      setQuestionList([newQuestion]);
    } else {
      const updatedQuestionList = [...questionList, newQuestion];
      setQuestionList(updatedQuestionList);
      updateCurrentChat(updatedQuestionList);
    }
    
    setShowExampleList(false);

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    abortControllerRef.current = new AbortController();

    try {
      const result = await mutate(submittedQuestion); // mutate 호출하여 API 요청
      console.log("API 응답 결과:", result);

      // API 응답 파싱 및 상태 업데이트
      const updatedQuestion = {
        ...newQuestion,
        answer: result.answer,
        error: false
      };

      const updatedList = questionList.length > 0 
        ? [...questionList, updatedQuestion]
        : [updatedQuestion];

        setQuestionList(prev => [...prev, updatedQuestion]);
        console.log("업데이트된 questionList:", [...questionList, updatedQuestion]);
      
      // 현재 대화 또는 새 대화 업데이트
      if (currentChatId) {
        updateCurrentChat([...questionList, updatedQuestion]);
      } else if (newId) {
        setHistories(prev => prev.map(history => 
          history.id === newId
            ? { ...history, messages: updatedList }
            : history
        ));
      }
    } catch (error) {
      console.error("API 요청 실패:", error);
      
      // 에러 상태 업데이트
      const errorQuestion = {
        ...newQuestion,
        error: true
      };

      const updatedList = questionList.length > 0
        ? [...questionList, errorQuestion]
        : [errorQuestion];

      setQuestionList(updatedList);
      
      // 현재 대화 또는 새 대화의 에러 상태 업데이트
      if (currentChatId) {
        updateCurrentChat(updatedList);
      } else if (newId) {
        setHistories(prev => prev.map(history =>
          history.id === newId
            ? { ...history, messages: updatedList }
            : history
        ));
      }
    }
  };

  // 새로운 대화 시작 시 현재 대화 저장
  const saveCurrentChat = () => {
    if (questionList.length > 0) {
      // 현재 대화가 이미 저장되어 있는지 확인
      const isAlreadySaved = histories.some(history => 
        history.messages.length === questionList.length && 
        history.messages[0].question === questionList[0].question &&
        history.messages[history.messages.length - 1].question === 
        questionList[questionList.length - 1].question
      );

      if (!isAlreadySaved) {
        const newHistory: ChatHistory = {
          id: Date.now().toString(),
          title: questionList[0].question,
          messages: [...questionList],
          createdAt: new Date(),
        };
        setHistories(prev => [newHistory, ...prev]);
      }
    }
  };

  // 새로운 대화 시작
  const handleNewChat = () => {
    if (currentChatId) {
      saveCurrentChat();
    }
    setCurrentChatId(null);
    setQuestionList([]);
    setShowExampleList(true);
  };

  // 저장된 대화 선택
  const handleSelectHistory = (history: ChatHistory) => {
    if (currentChatId && currentChatId !== history.id) {
      saveCurrentChat();
    }
    setCurrentChatId(history.id);
    setQuestionList(history.messages);
    setShowExampleList(false);
  };

  // 대화 내용이 업데이트될 때마다 histories 업데이트
  const updateCurrentChat = (newQuestionList: QAndA[]) => {
    if (currentChatId) {
      setHistories(prev => prev.map(history => 
        history.id === currentChatId
          ? {
              ...history,
              messages: newQuestionList,
              // 마지막 메시지가 변경된 경우에만 title 업데이트
              title: history.messages[0].question
            }
          : history
      ));
    }
  };

  const handleAbort = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  };

  //재시도 로직
  const handleRetry = async (index: number) => {
    const question = questionList[index].question;
    // if (!question) return;
    
    // setLoadingIndex(index);

    // try {
    //   const result = await mutation.mutateAsync({ query: question });
      
    //   const updatedList = questionList.map((qa, i) => 
    //     i === index 
    //       ? { 
    //           ...qa, 
    //           answer: result.answer, 
    //           context: result.context,
    //           imageNames: result.imageNames,
    //           fileNames: result.filenames,
    //           error: false 
    //         } 
    //       : qa
    //   );
      
    //   setQuestionList(updatedList);
    //   if (currentChatId) {
    //     updateCurrentChat(updatedList);
    //   }
    // } catch (error) {
    //   console.error("API 요청 실패:", error);
    //   const updatedList = questionList.map((qa, i) => 
    //     i === index 
    //       ? { ...qa, error: true } 
    //       : qa
    //   );
    //   setQuestionList(updatedList);
    //   if (currentChatId) {
    //     updateCurrentChat(updatedList);
    //   }
    // } finally {
    //   setLoadingIndex(null);
    // }
  };

  // 대화 삭제 핸들러
  const handleDeleteHistory = (id: string) => {
    setHistories(prev => prev.filter(history => history.id !== id));
    if (currentChatId === id) {
      setCurrentChatId(null);
      setQuestionList([]);
      setShowExampleList(true);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-[var(--background)]">
      <ThemeToggle />
      <ChatHistoryMenu
        histories={histories}
        onSelectHistory={handleSelectHistory}
        onDeleteHistory={handleDeleteHistory}
        onNewChat={handleNewChat}
      />

      {showExampleList ? (
        <ExampleList onExampleClick={handleExampleClick} />
      ) : (
        <ChatList 
          questionList={questionList} 
          onRetry={handleRetry}
          isLoading={isPending}  // isLoading은 mutation의 isPending 상태로 변경
          //isLoading={loadingIndex !== null}
          loadingIndex={loadingIndex}
        />
      )}

      <div className="w-full max-w-4xl mx-auto px-4">
        <SearchBar 
          ref={searchBarRef}
          handleSubmit={handleSubmit}
          domain={domain}
          setDomain={setDomain}
          isLoading={isPending}
          onAbort={handleAbort}
        />
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <QueryClientProvider client={closedQueryClient}>
      <HomeContent />
    </QueryClientProvider>
  );
}