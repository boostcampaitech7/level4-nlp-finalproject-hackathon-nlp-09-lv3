'use client';

import { useState } from 'react';

export default function ChatBot() {
  const [messages, setMessages] = useState<{ user: string; bot: string }[]>([]);
  const [input, setInput] = useState('');

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

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow p-6 space-y-4">
        <h1 className="text-xl font-bold text-center">ChatBot</h1>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {messages.map((msg, idx) => (
            <div key={idx} className="space-y-1">
              <p className="text-blue-500">
                <strong>User:</strong> {msg.user}
              </p>
              <p className="text-gray-700">
                <strong>Bot:</strong> {msg.bot || 'Typing...'}
              </p>
            </div>
          ))}
        </div>
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            className="flex-1 border border-gray-300 rounded-lg p-2"
            placeholder="Type a message..."
          />
          <button
            onClick={sendMessage}
            className="bg-blue-500 text-white rounded-lg px-4 py-2"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
