import React from 'react';
import type { Dispatch, SetStateAction } from "react";
import type { QAndA } from "../types/question";

// const Example = ({
//   text,
//   questionList,
//   setQuestionList,
// }: {
//   text: string;
//   questionList: QAndA[];
//   setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
// }) => {
//   const handleClick = () => {
//     const a = questionList.concat([{ question: text, answer: "" }]);

//     setQuestionList(a);
//   };

//   return (
//     <li
//       className="bg-gray-200 w-1/2 text-gray-900 m-1 p-2 rounded-md cursor-pointer"
//       onClick={handleClick}
//     >
//       {text}
//     </li>
//   );
// };

// export default function ExampleList({
//   questionList,
//   setQuestionList,
// }: {
//   questionList: QAndA[];
//   setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
// }) {
//   const exampleList = [
//     ["네이버의 2025년 전망은 어때?", "랩큐의 2025년 엽업 계획에 대해 말해줘"],
//     ["카카오의 2024년 2분기 수익률을 알려줘.", "한화가 새로 시작한 사업이 있어?"],
//   ];

//   return (
//     <ul className="w-screen mx-auto justify-center">
//       {exampleList.map((example, index) => (
//         <ul key={index} className="flex">
//           {example.map((text, index) => (
//             <Example
//               key={index}
//               text={text}
//               questionList={questionList}
//               setQuestionList={setQuestionList}
//             />
//           ))}
//         </ul>
//       ))}
//     </ul>
//   );
// }

interface ExampleListProps {
  onExampleClick: (example: string) => void;
}

const ExampleList: React.FC<ExampleListProps> = ({ onExampleClick }) => {
  const examples = [
    "네이버의 2025년 전망은 어때?",
    "랩큐의 2025년 사업 계획을 알려줘",
    "카카오의 2024년 2분기 수익률을 알려줘.",
    "한화가 새로 시작한 사업이 있어?"
  ];

  return (
    <div className="w-full max-w-4xl px-4">
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold mb-4 text-[var(--foreground)]">FinBuddy</h1>
        <img 
          src="/kong.png"
          alt="FinBuddy Logo"
          className="w-16 h-16 mx-auto"
        />
      </div>
      <div className="grid grid-cols-2 gap-4 max-w-4xl w-full px-4">
        {examples.map((example, index) => (
          <button
            key={index}
            onClick={() => onExampleClick(example)}
            className="p-6 text-center rounded-lg bg-[var(--example-box)] hover:bg-gray-700/50 transition-colors"
          >
            <p className="text-[var(--foreground)]">{example}</p>
          </button>
        ))}
      </div>
    </div>
  );
};

export default ExampleList;


