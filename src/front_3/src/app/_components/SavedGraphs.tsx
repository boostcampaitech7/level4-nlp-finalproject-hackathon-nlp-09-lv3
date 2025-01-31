interface SavedGraphsProps {
  onClose: () => void;
}

const SavedGraphs = ({ onClose }: SavedGraphsProps) => {
  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-[var(--foreground)]">저장된 그래프</h2>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-200 rounded-full dark:hover:bg-gray-700"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
      
      {/* 여기에 저장된 그래프 목록을 추가할 수 있습니다 */}
      <div className="space-y-4">
        <p className="text-[var(--foreground)]">아직 저장된 그래프가 없습니다.</p>
      </div>
    </div>
  );
};

export default SavedGraphs; 