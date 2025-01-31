"use client";

import { useState } from "react";
import ExampleList from "./_components/ExampleList";
import SearchBar from "./_components/SearchBar";
import type { QAndA } from "./_types/question";


export default function Home() {
  const [questionList, setQuestionList] = useState<QAndA[]>([]);

  const handleSubmit = async (formData: FormData) => {
    const 검색받은질문 = formData.get("search") as string;

    const 질문리스트 = questionList.concat({
      question: 검색받은질문,
      answer: "답변이에용~~ api 호출해서 진짜 답변으로 바꿔야해요!",
    });

    setQuestionList(질문리스트);
  };

  return (
    <div className="flex flex-col">
      {questionList.length === 0 ? (
        <ExampleList
          questionList={questionList}
          setQuestionList={setQuestionList}
        />
      ) : (
        <div>
          {questionList.map(({ question, answer }, index) => (
            <ul key={index} className="flex flex-col">
              <li className="flex justify-end   p-4 mb-2 rounded">
                {question}
              </li>
              <li className="flex justify-start  p-4 mb-2 rounded">
                {answer.length === 0 ? (
                  <div className="px-4 py-2 text-xs font-medium leading-none text-center text-blue-800 bg-blue-200 rounded-full animate-pulse dark:bg-blue-900 dark:text-blue-200">
                    검색중...
                  </div>
                ) : (
                  answer
                )}
              </li>
            </ul>
          ))}
        </div>
      )}
      <SearchBar handleSubmit={handleSubmit} />
    </div>
  );
}