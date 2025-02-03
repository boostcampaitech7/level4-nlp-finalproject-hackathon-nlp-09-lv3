import { useEffect, useRef } from "react";
import type { QAndA } from "../types/question";

interface ChatListProps {
  questionList: QAndA[];
  onRetry?: (index: number) => void;
}

const ChatList = ({ questionList, onRetry }: ChatListProps) => {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [questionList]);

  return (
    <div className="flex-1 w-full max-w-3xl mx-auto overflow-y-auto px-4 pb-40 mt-8">
      <div className="space-y-6">
        {questionList.map(({ question, answer, error }, index) => (
          <div key={index} className="flex flex-col space-y-4">
            {/* 사용자 질문 */}
            <div className="flex justify-end">
              <div className="bg-[var(--chat-user)] text-[var(--chat-text)] p-4 rounded-lg max-w-[80%]">
                {question}
              </div>
            </div>

            {/* AI 답변 */}
            <div className="flex items-center space-x-2">
              <div className="flex-shrink-0 w-6 h-6">
                <img 
                  width="24" 
                  height="24" 
                  src="https://img.icons8.com/material/24/737373/speech-bubble-with-dots.png" 
                  alt="speech-bubble-with-dots"
                />
              </div>
              <div className="bg-[var(--chat-ai)] text-[var(--chat-text)] p-4 rounded-lg max-w-[80%]">
                {error ? (
                  <div className="flex items-center space-x-2">
                    <span className="text-red-500">오류가 발생했습니다. 다시 시도해주세요.</span>
                    <button 
                      onClick={() => onRetry?.(index)}
                      className="p-1 hover:bg-gray-200 rounded-full dark:hover:bg-gray-700"
                    >
                      <svg
                        className="w-5 h-5 text-red-500"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                        />
                      </svg>
                    </button>
                  </div>
                ) : answer ? (
                  answer
                ) : (
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200" />
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div ref={chatEndRef} />
    </div>
  );
};

export default ChatList;
