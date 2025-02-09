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
            <div className="flex items-start gap-3 mb-8 justify-end pl-11">
              <div className="flex-1 flex justify-end">
                <div className="bg-[var(--example-box)] rounded-lg p-4 inline-block max-w-[80%]">
                  <p className="text-[var(--foreground)]">{qa.question}</p>
                </div>
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center ml-3">
                  <svg 
                    className="w-5 h-5 text-gray-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
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
            </div>

            {/* AI 답변 */}
            {(qa.answer || qa.error || (isLoading && loadingIndex === index)) && (
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
                    <div className="bg-[var(--example-box)] rounded-lg p-4">
                      <div className="flex items-center gap-2">
                        {[0, 200, 400].map((delay) => (
                          <div
                            key={delay}
                            className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                            style={{ animationDelay: `${delay}ms` }}
                          />
                        ))}
                      </div>
                    </div>
                  ) : qa.error ? (
                    <div className="bg-red-50 dark:bg-red-900/30 rounded-lg p-4">
                      <p className="text-red-600 dark:text-red-400">
                        죄송합니다. 오류가 발생했습니다.
                      </p>
                      <button
                        onClick={() => onRetry(index)}
                        className="mt-2 text-red-600 dark:text-red-400 text-sm hover:underline"
                        type="button"
                      >
                        다시 시도하기
                      </button>
                    </div>
                  ) : (
                    <div className="bg-[var(--example-box)] rounded-lg p-4">
                      <p className="text-[var(--foreground)]">{qa.answer}</p>
                      {qa.imageName?.length > 0 && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                          {qa.imageName.map((imgUrl, idx) => (
                            <img 
                              key={idx}
                              src={imgUrl}
                              alt={`생성된 이미지 ${idx + 1}`}
                              className="w-full rounded-lg shadow-md"
                            />
                          ))}
                        </div>
                      )}
                      {qa.fileNames?.length > 0 && (
                        <div className="mt-4 space-y-2">
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                            참고 문서:
                          </p>
                          {qa.fileNames.map((fileUrl, idx) => (
                            <a
                              key={idx}
                              href={fileUrl}
                              download
                              className="block text-blue-600 dark:text-blue-400 hover:underline"
                            >
                              {decodeURIComponent(fileUrl.split('/').pop() || '')}
                            </a>
                          ))}
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
