import type { Dispatch, SetStateAction } from "react";
import type { QAndA } from "../_types/question";

const Example = ({
  text,
  questionList,
  setQuestionList,
}: {
  text: string;
  questionList: QAndA[];
  setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
}) => {
  const handleClick = () => {
    const a = questionList.concat([{ question: text, answer: "" }]);

    setQuestionList(a);
  };

  return (
    <li
      className="bg-gray-200 w-1/2 text-gray-900 m-1 p-2 rounded-md cursor-pointer"
      onClick={handleClick}
    >
      {text}
    </li>
  );
};

export default function ExampleList({
  questionList,
  setQuestionList,
}: {
  questionList: QAndA[];
  setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
}) {
  const exampleList = [
    ["네이버의 2025년 전망은 어때?", "랩큐의 2025년 엽업 계획에 대해 말해줘"],
    ["어쩌고", "저쩌고"],
  ];

  return (
    <ul className="w-screen mx-auto justify-center">
      {exampleList.map((example, index) => (
        <ul key={index} className="flex">
          {example.map((text, index) => (
            <Example
              key={index}
              text={text}
              questionList={questionList}
              setQuestionList={setQuestionList}
            />
          ))}
        </ul>
      ))}
    </ul>
  );
}