import { useEffect, useRef } from "react";
import type { QAndA } from "../types/question";

interface ChatListProps {
  questionList: QAndA[];
  onRetry: (index: number) => void;
  isLoading?: boolean;
  loadingIndex?: number;
}

const ChatList = ({ questionList, onRetry, isLoading, loadingIndex }: ChatListProps) => {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [questionList]);

  return (
    <div className="flex-1 overflow-y-auto pt-8 pb-32">
      <div className="max-w-4xl mx-auto px-4">
        {questionList.map((qa, index) => (
          <div key={index} className="mb-8">
            {/* 사용자 질문 */}
            <div className="flex items-start gap-3 mb-8 justify-end">
              <div className="flex-1 flex justify-end">
                <div className="bg-[var(--example-box)] rounded-lg p-4 inline-block max-w-[80%]">
                  <p className="text-[var(--foreground)]">{qa.question}</p>
                </div>
              </div>
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
                <svg
                  className="w-5 h-5 text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
            </div>

            {/* AI 답변 */}
            {(qa.answer !== null || qa.error || (isLoading && loadingIndex === index)) && (
              <div className="flex items-start gap-3 pr-11">
                <div className="flex-shrink-0 w-8 h-8 rounded-full overflow-hidden">
                  <img 
                    src="https://img.icons8.com/pastel-glyph/64/1A1919/dog-jump--v1.png"
                    alt="AI Assistant"
                    className="w-full h-full object-cover dark:invert"
                  />
                </div>
                <div className="flex-1">
                  {isLoading && loadingIndex === index ? (
                    <div className="bg-[var(--example-box)] rounded-lg p-4 inline-block">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '200ms' }}></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '400ms' }}></div>
                      </div>
                    </div>
                  ) : qa.error ? (
                    <div className="bg-red-50 dark:bg-red-900/30 rounded-lg p-4 inline-block max-w-[90%]">
                      <p className="text-red-600 dark:text-red-400">
                        죄송합니다. 오류가 발생했습니다.
                      </p>
                      <button
                        onClick={() => onRetry(index)}
                        className="mt-2 text-red-600 dark:text-red-400 text-sm hover:underline"
                      >
                        다시 시도하기
                      </button>
                    </div>
                  ) : (
                    <div className="bg-[var(--example-box)] rounded-lg p-4 inline-block max-w-[90%]">
                      <p className="text-[var(--foreground)] whitespace-pre-wrap">
                        {qa.answer}
                      </p>
                      {qa.context && (
                        <div className="mt-2 text-sm text-gray-500">
                          <p>참고 문서: {qa.context}</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      <div ref={chatEndRef} />
    </div>
  );
};

export default ChatList;
