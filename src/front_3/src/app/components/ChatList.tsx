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

  // 현재 재생 중인 오디오 인스턴스를 저장하는 ref
  const currentAudioRef = useRef<{ audio: HTMLAudioElement; url: string } | null>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [questionList]);

  // TTS 오디오 재생/일시정지 토글 함수
  const playAudio = (audioUrl: string) => {
    // 만약 이미 재생 중인 오디오가 있고, 같은 파일이면 토글
    if (currentAudioRef.current && currentAudioRef.current.url === audioUrl) {
      if (!currentAudioRef.current.audio.paused) {
        currentAudioRef.current.audio.pause();
      } else {
        currentAudioRef.current.audio.play().catch(error => {
          console.error("오디오 재생 오류:", error);
        });
      }
      return;
    }
    // 다른 파일이거나 아직 오디오가 없다면, 이전 오디오가 있다면 정지
    if (currentAudioRef.current) {
      currentAudioRef.current.audio.pause();
    }
    const audio = new Audio(audioUrl);
    // 재생이 끝나면 ref 초기화
    audio.onended = () => {
      currentAudioRef.current = null;
    };
    currentAudioRef.current = { audio, url: audioUrl };
    audio.play().catch(error => {
      console.error("오디오 재생 오류:", error);
    });
  };

  // PDF 파일 다운로드용 함수 (아래에서 사용)
  // const downloadFile = (url: string) => {
  //   // 절대 URL을 생성하고 NFC 정규화를 적용합니다.
  //   const absoluteUrl = new URL(url, window.location.origin).href.normalize('NFC');
  //   console.log("다운로드 요청 URL:", absoluteUrl);
    
  //   fetch(absoluteUrl)
  //     .then((res) => {
  //       if (!res.ok) {
  //         throw new Error('네트워크 응답이 올바르지 않습니다.');
  //       }
  //       return res.blob();
  //     })
  //     .then((blob) => {
  //       const blobUrl = window.URL.createObjectURL(blob);
  //       const a = document.createElement("a");
  //       a.style.display = "none";
  //       a.href = blobUrl;
  //       // URL의 마지막 부분(파일명)을 디코딩해서 download 속성에 넣습니다.
  //       a.download = decodeURIComponent(url.split('/').pop() || "download.pdf");
  //       document.body.appendChild(a);
  //       a.click();
  //       window.URL.revokeObjectURL(blobUrl);
  //       a.remove();
  //     })
  //     .catch((err) => console.error("다운로드 실패:", err));
  // };
  

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
                      <pre className="text-[var(--foreground)] whitespace-pre-wrap">{qa.answer}</pre>
                      {qa.imageName && (
                          <div className="mt-2">
                            <img 
                              src={qa.imageName}
                              alt="생성된 이미지"
                              className="w-full rounded-lg shadow-md"
                            />
                          </div>
                        )}
                      {/* {qa.fileNames?.length > 0 && (
                        <div className="mt-4 space-y-2">
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                            참고 문서:
                          </p>
                          {qa.fileNames.map((fileUrl, idx) => (
                            <a
                              key={idx}
                              href={encodeURI(fileUrl)}
                              download
                              className="block text-blue-600 dark:text-blue-400 hover:underline"
                            >
                              {decodeURIComponent(fileUrl.split('/').pop() || '')}
                            </a>
                          ))}
                        </div>
                      )} */}
                      {qa.fileNames?.length > 0 && (
                        <div className="mt-4 space-y-2">
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                            참고 문서:
                          </p>
                          {qa.fileNames.map((fileUrl, idx) => {
                            const fileName = decodeURIComponent(fileUrl.split('/').pop() || 'download.pdf');
                            return (
                              <a
                                key={idx}
                                href={fileUrl}  // 원본 URL 그대로 사용
                                download={fileName}  // download 속성에 올바른 파일명 지정
                                className="block text-blue-600 dark:text-blue-400 hover:underline"
                              >
                                {fileName}
                              </a>
                            );
                          })}
                        </div>
                      )}
                      {qa.audioFileName && (
                        <div className="mt-4">
                          <button 
                            onClick={() => playAudio(qa.audioFileName)}
                            className="flex items-center space-x-2 p-2 bg-gray-100 rounded hover:bg-gray-200"
                          >
                            <img 
                              src="/audio.png" 
                              alt="Play Audio" 
                              className="w-6 h-6"
                            />
                            <span className="text-sm text-gray-700">Play Audio</span>
                          </button>
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