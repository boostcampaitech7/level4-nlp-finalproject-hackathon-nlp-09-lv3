import { useState, useEffect } from 'react';
import type { ChatHistory } from '../types/chatHistory';

interface Image {
  id: number;
  url: string;
  title: string;
}

interface ChatHistoryMenuProps {
  histories: ChatHistory[];
  onSelectHistory: (history: ChatHistory) => void;
  onDeleteHistory: (id: string) => void;
  onNewChat: () => void;
}

export default function ChatHistoryMenu({ 
  histories, 
  onSelectHistory, 
  onDeleteHistory,
  onNewChat 
}: ChatHistoryMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'chat' | 'images'| ''>('chat');

    // 이미지 목록과 로딩 상태를 위한 state 추가
    const [images, setImages] = useState<Image[]>([]);
    const [loadingImages, setLoadingImages] = useState(false);
  
    // activeTab이 images로 변경될 때 API 호출
    useEffect(() => {
      if (activeTab === 'images') {
        setLoadingImages(true);
        fetch('http://localhost:8000/api/for_service/getImages')
          .then(res => res.json())
          .then((data) => {
            // data.images가 undefined면 빈 배열([])로 대체
            setImages(data.images ?? []);
            setLoadingImages(false);
          })
          .catch(err => {
            console.error(err);
            setLoadingImages(false);
          });
      }
    }, [activeTab, ]);

  return (
    <div className="fixed top-4 left-4 z-50">
      {/* 햄버거 버튼 */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-lg hover:bg-gray-700/50 transition-colors"
        aria-label="메뉴 열기"
      >
        <svg
          className="w-6 h-6 text-[var(--foreground)]"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      {/* 사이드 메뉴 */}
      <div className={`fixed top-0 left-0 h-full w-64 bg-[var(--example-box)] shadow-lg transform transition-transform ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="p-4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-[var(--foreground)]">메뉴</h2>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 rounded-lg hover:bg-gray-700/50 transition-colors"
            >
              <svg
                className="w-5 h-5 text-[var(--foreground)]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {/* 탭 버튼 */}
          <div className="flex mb-4 border-b border-gray-700">
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex-1 py-2 text-sm font-medium ${
                activeTab === 'chat'
                  ? 'text-blue-500 border-b-2 border-blue-500'
                  : 'text-[var(--foreground)]'
              }`}
            >
              대화내역
            </button>
            <button
                  onClick={() => setActiveTab('images')}
                  className={`flex-1 py-2 text-sm font-medium ${
                    activeTab === 'images'
                      ? 'text-blue-500 border-b-2 border-blue-500'
                      : 'text-[var(--foreground)]'
                  }`}
                >
                  이미지 모아보기
                </button>
              </div>

              {activeTab === 'images' && (
                <div className="mt-4 flex justify-end">
                  <button
                    onClick={() => {
                      // activeTab을 빈 값으로 설정 후 잠시 후에 'images'로 다시 설정
                      setActiveTab('');
                      setTimeout(() => {
                        setActiveTab('images');
                      }, 100); // 100ms 정도 지연 후 'images'로 설정
                    }}
                    className="px-2 py-1 text-xs font-medium text-gray-700 bg-gray-300 rounded-md hover:bg-gray-400"
                  >
                    새로고침
                  </button>
                </div>
                )}

          {activeTab === 'chat' ? (
            <>
              {/* 새로운 대화 버튼 */}
              <button
                onClick={() => {
                  onNewChat();
                  setIsOpen(false);
                }}
                className="w-full mb-4 flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-[var(--foreground)] bg-[var(--background)] rounded-lg hover:bg-gray-700/50 transition-colors"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
                새로운 대화
              </button>

              {/* 대화 내역 목록 */}
              <div className="space-y-2">
                {histories.map((history) => (
                  <div
                    key={history.id}
                    className="p-3 rounded-lg hover:bg-gray-700/50 cursor-pointer"
                    onClick={() => {
                      onSelectHistory(history);
                      setIsOpen(false);
                    }}
                  >
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-[var(--foreground)] truncate">
                        {history.title}
                      </span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteHistory(history.id);
                        }}
                        className="p-1 rounded-full hover:bg-gray-600/50"
                      >
                        <svg
                          className="w-4 h-4 text-[var(--foreground)]"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                          />
                        </svg>
                      </button>
                    </div>
                    <span className="text-xs text-gray-400">
                      {new Date(history.createdAt).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            // 이미지 탭 내용
            <div className="py-4">
              {loadingImages ? (
                <p className="text-center text-[var(--foreground)]">이미지 로딩 중...</p>
              ) : images.length > 0 ? (
                <div className="grid grid-cols-1 gap-2">
                  {images.map((img, idx) => (
                    <img
                      key={idx}
                      src={img.url}
                      alt={img.title}
                      className="object-cover w-full h-auto rounded-lg"
                    />
                  ))}
                </div>
              ) : (
                <p className="text-center text-[var(--foreground)]">이미지가 없습니다.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 