"use client";

import { useState, useRef, Dispatch, SetStateAction } from "react";
import { useClosedQueryApi } from "./store/useClosedQueryApi";// API 훅 임포트
import { useOpenQueryApi } from "./store/useOpenQueryApi";// API 훅 임포트
import { useQueryApi } from "./store/useQueryApi";
//import { closedQueryClient } from "./store/closedQueryClient";// API 훅 임포트
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import ExampleList from "./components/ExampleList";
import SearchBar from "./components/SearchBar";
import ChatList from "./components/ChatList";
import ThemeToggle from "./components/ThemeToggle";
import ChatHistoryMenu from './components/ChatHistoryMenu';
import type { ChatHistory } from './types/chatHistory';
import { parseClosedApiResponse } from './api/parsers/chatParser';
import type { QAndA } from "./types/question";

export const closedQueryClient = new QueryClient();

function HomeContent() {
  const [questionList, setQuestionList] = useState<QAndA[]>([]);
  const [showExampleList, setShowExampleList] = useState(true);
  const [histories, setHistories] = useState<ChatHistory[]>([]);
  const [domain, setDomain] = useState<'open' | 'close' | null>(null);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [loadingIndex, setLoadingIndex] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  
  const searchBarRef = useRef<{ setText: (text: string) => void } | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const { mutate: mutateClosed, isPending: isPendingClosed, mutateAsync: mutateAsyncClosed } = useClosedQueryApi();
  const { isPending: isPendingOpen, mutateAsync: mutateAsyncOpen } = useOpenQueryApi();
  const { isPending: isPendingQuery, mutateAsync: mutateAsyncQuery } = useQueryApi();
  

  const handleExampleClick = (example: string) => {
    setShowExampleList(false);  // 예시 질문 클릭 시에도 목록 숨김
    const formData = new FormData();
    formData.append('search', example);
    handleSubmit(formData);
  };

  const handleSubmit = async (formData: FormData) => {
    const submittedQuestion = formData.get("search") as string;
    
    if (!submittedQuestion?.trim()) return;


    // 예시 질문 목록을 강제로 숨김
    setShowExampleList(false);

    // 입력 필드 초기화
    if (searchBarRef.current) {
      searchBarRef.current.setText('');
    }

    const newQuestion = {
      question: submittedQuestion,
      answer: null,
    };


    // 새 질문을 한 번만 추가
    const updatedQuestionList = [...questionList, newQuestion];
    setQuestionList(updatedQuestionList);

    if (!currentChatId) {
      const newId = Date.now().toString();
      setCurrentChatId(newId);
      const newHistory: ChatHistory = {
        id: newId,
        title: submittedQuestion,
        messages: [newQuestion],
        createdAt: new Date(),
      };
      setHistories(prev => [newHistory, ...prev]);
    } else {
      updateCurrentChat(updatedQuestionList);
    }


    setLoadingIndex(questionList.length);
    try {
      let result;
    
      // domain에 따라 다른 API를 호출
      if (domain === null) {
        result = await mutateAsyncQuery(submittedQuestion); // query API 호출
        console.log("query API 응답 결과:", result);
      } else if (domain === 'close') {
        result = await mutateAsyncClosed(submittedQuestion); // closed API 호출
        console.log("closed API 응답 결과:", result);
      } else if (domain === 'open') {
        result = await mutateAsyncOpen(submittedQuestion); // open API 호출
        console.log("open API 응답 결과:", result);
      }

      // 🔹 API 응답을 parseClosedApiResponse로 변환
      const parsedResponse = parseClosedApiResponse(result, submittedQuestion);

      // 새로운 질문 객체 업데이트
      const updatedQuestion = {
        ...newQuestion,
        answer: parsedResponse.answer,
        error: false,
        imageName: parsedResponse.imageName, // 이미지 정보
        fileNames: parsedResponse.fileNames,  // PDF 정보
        audioFileName: parsedResponse.audioFileName, // TTS 오디오 파일 정보 // 출처 정보 추가
        visualized_name: parsedResponse.visualized_name,
      };

      // 마지막 질문만 업데이트
      setQuestionList(prev => prev.map((q, i) => 
        i === prev.length - 1 ? updatedQuestion : q
      ));

      if (currentChatId) {
        const finalQuestionList = questionList.map((q, i) => 
          i === questionList.length - 1 ? updatedQuestion : q
        );
        updateCurrentChat(finalQuestionList);
      }

    } catch (error) {
      console.error("API 요청 실패:", error);
      const errorQuestion = {
        ...newQuestion,
        error: true
      };
      setQuestionList(prev => prev.map((q, i) => 
        i === prev.length - 1 ? errorQuestion : q
      ));
    } finally {
      setLoadingIndex(null);
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

      <div className="flex-1 flex flex-col overflow-y-auto">
        {questionList.length > 0 ? (
          <ChatList 
            questionList={questionList} 
            onRetry={handleRetry}
            isLoading={domain === 'close' ? isPendingClosed : 
                      domain === 'open' ? isPendingOpen : 
                      isPendingQuery}
            loadingIndex={loadingIndex}
          />
        ) : showExampleList ? (
          <div className="flex-1 flex items-center justify-center">
            <ExampleList onExampleClick={handleExampleClick} />
          </div>
        ) : null}
      </div>

      <div className="w-full max-w-4xl mx-auto px-4">
        <SearchBar 
          ref={searchBarRef}
          handleSubmit={handleSubmit}
          domain={domain}
          setDomain={setDomain}
          isLoading={domain === 'close' ? isPendingClosed : 
                    domain === 'open' ? isPendingOpen : 
                    isPendingQuery}
          setLoading={setLoading}
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