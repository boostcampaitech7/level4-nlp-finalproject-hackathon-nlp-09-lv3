import type { Dispatch, SetStateAction } from "react";
import type { QAndA } from "../_types/question";

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

const Example = ({
  text,
  questionList,
  setQuestionList,
  setShowExampleList,
}: {
  text: string;
  questionList: QAndA[];
  setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
  setShowExampleList: Dispatch<SetStateAction<boolean>>;
}) => {
  const handleClick = () => {
    const newList = questionList.concat([{ 
      question: text, 
      answer: "답변이에용~~ api 호출해서 진짜 답변으로 바꿔야해요!" 
    }]);
    
    setQuestionList(newList);
    setShowExampleList(false); // 예시 목록 숨기기
  };

  return (
    <div
      className="bg-[var(--example-box)] w-full h-20 flex items-center justify-center text-[var(--foreground)] p-4 rounded-lg cursor-pointer hover:bg-[var(--example-box-hover)] transition text-center"
      onClick={handleClick}
    >
      {text}
    </div>
  );
};

export default function ExampleList({
  questionList,
  setQuestionList,
  setShowExampleList,
}: {
  questionList: QAndA[];
  setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
  setShowExampleList: Dispatch<SetStateAction<boolean>>;
}) {
  const exampleList = [
    "네이버의 2025년 전망은 어때?",
    "랩큐의 2025년 사업 계획을 알려줘",
    "카카오의 2024년 2분기 수익률을 알려줘.",
    "한화가 새로 시작한 사업이 있어?",
  ];

  return (
    <div className="grid grid-cols-2 gap-4 w-full px-4">
      {exampleList.map((text, index) => (
        <Example 
          key={index} 
          text={text} 
          questionList={questionList} 
          setQuestionList={setQuestionList}
          setShowExampleList={setShowExampleList}
        />
      ))}
    </div>
  );
}


