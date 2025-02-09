import React, { useRef, useImperativeHandle, forwardRef, useState, useEffect } from 'react';

interface SearchBarProps {
  handleSubmit: (formData: FormData) => void;
  domain: 'open' | 'close' | null;
  setDomain: (domain: 'open' | 'close' | null) => void;
  isLoading: boolean;
  setLoading: (loading: boolean) => void; // ✅ 추가됨
  onAbort: () => void;
}

const SearchBar = (
  { handleSubmit, domain, setDomain, isLoading, setLoading, onAbort }: SearchBarProps, 
  ref: React.ForwardedRef<{ setText: (text: string) => void }>
) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isInputEmpty, setIsInputEmpty] = useState(true);

  useImperativeHandle(ref, () => ({
    setText: (text: string) => {
      if (textareaRef.current) {
        textareaRef.current.value = text;
        textareaRef.current.style.height = "auto";
        textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        setIsInputEmpty(!text.trim());
      }
    }
  }));

  const handleInput = (e: React.FormEvent<HTMLTextAreaElement>) => {
    const textarea = e.currentTarget;
    // 높이 자동 조절
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
    
    // 입력값이 비어있거나 공백/줄바꿈만 있는지 확인
    setIsInputEmpty(!textarea.value.trim());
  };

  //추가됨
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!isInputEmpty && !isLoading) {
      const formData = new FormData(e.currentTarget);
      setLoading(true);
      handleSubmit(formData);
    }
  };
  /** ✅ domain 변경 시 자동으로 API 요청 */
  useEffect(() => {
    if (domain) {
      setLoading(true);
      const formData = new FormData();
      formData.append('domain', domain);
      handleSubmit(formData);
    }
  }, [domain, handleSubmit, setLoading]);

  return (
    <div className="fixed bottom-12 left-1/2 transform -translate-x-1/2 w-[80%] max-w-3xl">
      <form action={handleSubmit}>
        <div className="relative bg-[var(--example-box)] p-4 rounded-xl shadow-lg">
          <textarea
            ref={textareaRef}
            id="search"
            name="search"
            className="block w-full resize-none p-3 text-sm text-[var(--foreground)] bg-[var(--example-box)] border-none rounded-lg focus:ring-0 focus:outline-none pr-12 mb-2"
            placeholder="FinBuddy에게 물어보세요!"
            rows={1}
            onInput={handleInput}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!isInputEmpty && !isLoading) {
                  e.currentTarget.form?.requestSubmit();
                }
              }
            }}
            required
          />

          <div className="flex justify-between items-center">
            {/* 도메인 전환 버튼 */}
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setDomain(domain === 'close' ? null : 'close')}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  domain === 'close'
                    ? 'bg-gray-700 text-white'
                    : 'bg-[var(--example-box)] text-[var(--foreground)] border border-gray-600 hover:bg-gray-700/50'
                }`}
              >
                <div className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                  </svg>
                  Closed Domain
                </div>
              </button>
              <button
                type="button"
                onClick={() => setDomain(domain === 'open' ? null : 'open')}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  domain === 'open'
                    ? 'bg-gray-700 text-white'
                    : 'bg-[var(--example-box)] text-[var(--foreground)] border border-gray-600 hover:bg-gray-700/50'
                }`}
              >
                <div className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Open Domain
                </div>
              </button>
            </div>

            {/* 전송 버튼 */}
            <button
              type="submit"
              disabled={isInputEmpty || isLoading}
              className={`p-1 rounded-lg transition-colors ${
                isInputEmpty || isLoading
                  ? 'cursor-not-allowed opacity-50' 
                  : 'hover:bg-gray-700/50 cursor-pointer'
              }`}
              aria-label="검색"
            >
              {isLoading ? (
                <svg 
                  className="w-5 h-5 text-gray-400 animate-spin" 
                  xmlns="http://www.w3.org/2000/svg" 
                  fill="none" 
                  viewBox="0 0 24 24"
                >
                  <circle 
                    className="opacity-25" 
                    cx="12" 
                    cy="12" 
                    r="10" 
                    stroke="currentColor" 
                    strokeWidth="4"
                  />
                  <path 
                    className="opacity-75" 
                    fill="currentColor" 
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
              ) : (
                <svg
                  className={`w-5 h-5 ${
                    isInputEmpty ? 'text-gray-400' : 'text-[var(--foreground)]'
                  }`}
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M22 2L11 13" />
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default forwardRef(SearchBar);
