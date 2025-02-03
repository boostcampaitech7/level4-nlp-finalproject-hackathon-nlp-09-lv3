import { useState } from "react";
import { Dispatch, SetStateAction } from "react";
import type { QAndA } from "../types/question";
import Modal from "./Modal";
import SavedGraphs from "./SavedGraphs";

interface SidebarProps {
  setQuestionList: Dispatch<SetStateAction<QAndA[]>>;
  setShowExampleList: Dispatch<SetStateAction<boolean>>;
  showExampleList: boolean;
}

const Sidebar = ({ setQuestionList, setShowExampleList, showExampleList }: SidebarProps) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [showGraphs, setShowGraphs] = useState(false);

  const handleNewChat = () => {
    setIsModalOpen(true);
  };

  const handleConfirmNewChat = () => {
    setQuestionList([]);
    setShowExampleList(true);
    setIsModalOpen(false);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const toggleGraphs = () => {
    setShowGraphs(!showGraphs);
  };

  if (showExampleList) {
    return null;
  }

  return (
    <>
      <div className="fixed left-4 bottom-24 flex flex-col space-y-4">
        <button
          onClick={toggleGraphs}
          className="flex items-center space-x-2 text-white bg-[#2C2C2C] px-4 py-2 rounded-lg hover:bg-[#3C3C3C] transition"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <span>저장된 그래프</span>
        </button>

        <button
          onClick={handleNewChat}
          className="flex items-center space-x-2 text-white bg-[#2C2C2C] px-4 py-2 rounded-lg hover:bg-[#3C3C3C] transition"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          <span>새로운 대화</span>
        </button>
      </div>

      {showGraphs && (
        <div className="fixed right-0 top-0 h-full w-80 bg-[var(--background)] shadow-lg transform transition-transform duration-300 ease-in-out">
          <SavedGraphs onClose={() => setShowGraphs(false)} />
        </div>
      )}

      <Modal 
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onConfirm={handleConfirmNewChat}
      />
    </>
  );
};

export default Sidebar; 