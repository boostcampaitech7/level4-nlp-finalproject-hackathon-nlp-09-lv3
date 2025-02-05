import { useState } from 'react';
import type { ChatHistory } from '../types/chatHistory';

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
            <h2 className="text-lg font-semibold text-[var(--foreground)]">대화 기록</h2>
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

          <div className="space-y-2">
            {histories.map((history) => (
              <div
                key={history.id}
                className="p-3 rounded-lg bg-[var(--background)] hover:bg-gray-700/50 cursor-pointer transition-colors"
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
        </div>
      </div>
    </div>
  );
} 