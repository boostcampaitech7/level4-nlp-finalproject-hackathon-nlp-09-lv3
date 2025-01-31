'use client';

import { useState } from 'react';
import { TrashIcon, MagnifyingGlassIcon, CurrencyDollarIcon } from '@heroicons/react/24/solid'; // Heroicons에서 아이콘 import
import './styles.css'; // CSS 파일 import

export default function ChatBot() {
  const [messages, setMessages] = useState<{ user: string; bot: string }[]>([]);
  const [input, setInput] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false); // 팝업 상태 관리

  const recommendQuestions = [
    'How can I invest my savings?',
    'What is the best way to budget?',
    'Can you help me save for retirement?',
    'What are some good investment strategies?',
  ];

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');

    // 사용자 메시지 추가
    setMessages((prev) => [...prev, { user: userMessage, bot: '' }]);

    // API 호출
    const res = await fetch('/api/chatbot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage }),
    });
    const data = await res.json();

    // 봇 응답 추가
    setMessages((prev) =>
      prev.map((msg, idx) =>
        idx === prev.length - 1 ? { ...msg, bot: data.response } : msg
      )
    );
  };

  const clearChat = () => {
    setMessages([]);
    setIsModalOpen(false); // 팝업 닫기
  };

  const showModal = () => {
    setIsModalOpen(true); // 팝업 열기
  };

  const closeModal = () => {
    setIsModalOpen(false); // 팝업 닫기
  };

  const handleRecommendedQuestionClick = (question: string) => {
    setInput(question);
  };

  return (
    <div className="container">
      <div className="header">FinBuddy</div>
    
      {/* 메시지가 없을 때 로고 보여주기 */}
      {messages.length === 0 && (
        <div className="logo-container">
          <CurrencyDollarIcon className="logo-icon" />
          <p className="logo-text">FinBuddy</p>
        </div>
      )}

      {/* 추천 질문 버튼들 */}
      {!messages.length && (
        <div className="recommended-questions">
          {recommendQuestions.map((question, idx) => (
            <button
              key={idx}
              onClick={() => handleRecommendedQuestionClick(question)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              className="recommended-question-button"
            >
              {question}
            </button>
          ))}
        </div>
      )}

      <div className="chat-box">
        <div className="message-container">
          {messages.map((msg, idx) => (
            <div key={idx} style={{ marginBottom: '8px' }}>
              <p className="user-message">{msg.user}</p>
              <p className="bot-message">{msg.bot || 'Typing...'}</p>
            </div>
          ))}
        </div>

        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            className="input-field"
            placeholder="Type a message..."
          />
          <button onClick={sendMessage} className="send-button">
            <MagnifyingGlassIcon className="h-5 w-5 mr-2" />
            Send
          </button>
        </div>
      </div>

      {/* 채팅 초기화 버튼 */}
      <div className="clear-chat-container">
        <button onClick={showModal} className="clear-chat-button">
          <TrashIcon className="h-5 w-5 mr-2" />
          Clear Chat
        </button>
      </div>

      {/* 팝업 */}
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <p>지금까지 나눈 모든 채팅이 사라집니다.</p>
            <div className="modal-buttons">
              <button onClick={clearChat} className="modal-button confirm">
                초기화
              </button>
              <button onClick={closeModal} className="modal-button cancel">
                취소
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
