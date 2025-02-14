import { useState, useEffect } from 'react';
import type { ChatHistory } from '../types/chatHistory';

export function useChatHistories() {
  const [histories, setHistories] = useState<ChatHistory[]>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('chatHistories');
      return saved ? JSON.parse(saved) : [];
    }
    return [];
  });

  useEffect(() => {
    localStorage.setItem('chatHistories', JSON.stringify(histories));
  }, [histories]);

  return [histories, setHistories] as const;
} 