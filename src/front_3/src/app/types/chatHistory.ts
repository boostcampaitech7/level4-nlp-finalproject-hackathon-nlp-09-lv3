import type { QAndA } from "./question";

export interface ChatHistory {
  id: string;
  title: string;
  messages: QAndA[];
  createdAt: Date;
}