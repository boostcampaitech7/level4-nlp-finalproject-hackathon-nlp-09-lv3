"use client";

import { useState, useRef, Dispatch, SetStateAction } from "react";
import { useMutateQueryApi } from "./store/useClosedQueryApi";// API 훅 임포트
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import ExampleList from "./components/ExampleList";
import SearchBar from "./components/SearchBar";
import ChatList from "./components/ChatList";
import Sidebar from "./components/Sidebar";
import type { QAndA } from "./types/question";
import ThemeToggle from "./components/ThemeToggle";
import ChatHistoryMenu from './components/ChatHistoryMenu';
import type { ChatHistory } from './types/chatHistory';

interface HomeContentProps {
  questionList: QAndA[];
  setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
  showExampleList: boolean;
  setShowExampleList: Dispatch<SetStateAction<boolean>>;
  histories: ChatHistory[];
  setHistories: Dispatch<SetStateAction<ChatHistory[]>>;
}

export default function Home() {
  const queryClient = new QueryClient();// QueryClient 생성
  const [questionList, setQuestionList] = useState<QAndA[]>([]);
  const [showExampleList, setShowExampleList] = useState(true); 
  const [histories, setHistories] = useState<ChatHistory[]>([]);
  return (
    <QueryClientProvider client={queryClient}> 
      <HomeContent 
        questionList={questionList}
        setQuestionList={setQuestionList}
        showExampleList={showExampleList}
        setShowExampleList={setShowExampleList}
        histories={histories}
        setHistories={setHistories}
      />
    </QueryClientProvider>
  );
}

function HomeContent({ 
  questionList, 
  setQuestionList, 
  showExampleList, 
  setShowExampleList,
  histories,
  setHistories
}: HomeContentProps) {
  const searchBarRef = useRef<{ setText: (text: string) => void } | null>(null);
  const [domain, setDomain] = useState<'open' | 'close'>('close');
  const mutation = useMutateQueryApi();
  const abortControllerRef = useRef<AbortController | null>(null);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  
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

  const handleSubmit = async (formData: FormData) => {
    const submittedQuestion = formData.get("search") as string;
    
    if (!submittedQuestion?.trim()) return;

    // 먼저 새 질문을 목록에 추가
    const newQuestion = {
      question: submittedQuestion,
      answer: null,
    };

    let newId: string | null = null;  // newId를 함수 스코프로 이동

    // 새로운 대화인 경우
    if (!currentChatId) {
      newId = Date.now().toString();  // newId 할당
      setCurrentChatId(newId);
      // histories에 새 대화 추가
      const newHistory: ChatHistory = {
        id: newId,
        title: submittedQuestion,
        messages: [newQuestion],
        createdAt: new Date(),
      };
      setHistories(prev => [newHistory, ...prev]);
      // questionList 업데이트
      setQuestionList([newQuestion]);
    } else {
      // 기존 대화 업데이트
      const updatedQuestionList = [...questionList, newQuestion];
      setQuestionList(updatedQuestionList);
      updateCurrentChat(updatedQuestionList);
    }
    
    setShowExampleList(false);

    // 이전 요청이 있다면 중단
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // 새로운 AbortController 생성
    abortControllerRef.current = new AbortController();

    try {
      mutation.mutate(
        { query: submittedQuestion },
        {
          onSuccess: (data) => {
            const updatedList = [...questionList, { ...newQuestion, answer: data.answer, context: data.context }];
            setQuestionList(updatedList);
            
            if (currentChatId) {
              updateCurrentChat(updatedList);
            } else if (newId) {  // newId가 존재할 때만 실행
              setHistories(prev => prev.map(history => 
                history.id === newId
                  ? { ...history, messages: updatedList }
                  : history
              ));
            }
          },
          onError: (error) => {
            console.error("API 요청 실패:", error);
            const updatedList = [...questionList, { ...newQuestion, error: true }];
            setQuestionList(updatedList);
            
            if (currentChatId) {
              updateCurrentChat(updatedList);
            } else if (newId) {  // newId가 존재할 때만 실행
              setHistories(prev => prev.map(history =>
                history.id === newId
                  ? { ...history, messages: updatedList }
                  : history
              ));
            }
          },
        }
      );
    } catch (error) {
      if ((error as Error).name === 'AbortError') {
        console.log('Request aborted');
      } else {
        console.error('Error:', error);
        const updatedList = [...questionList, { ...newQuestion, error: true }];
        setQuestionList(updatedList);
        
        if (currentChatId) {
          updateCurrentChat(updatedList);
        } else if (newId) {  // newId가 존재할 때만 실행
          setHistories(prev => prev.map(history =>
            history.id === newId
              ? { ...history, messages: updatedList }
              : history
          ));
        }
      }
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
              setShowExampleList={setShowExampleList}
              searchBarRef={searchBarRef}
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
        setQuestionList={handleNewChat}
        setShowExampleList={setShowExampleList}
        showExampleList={showExampleList}
      />

      {/* SearchBar */}
      <div className="w-full max-w-4xl mx-auto px-4">
        <SearchBar 
          ref={searchBarRef} 
          handleSubmit={handleSubmit}
          domain={domain}
          setDomain={setDomain}
          isLoading={mutation.isPending}
          onAbort={handleAbort}
        />
      </div>
    </div>

  );
}