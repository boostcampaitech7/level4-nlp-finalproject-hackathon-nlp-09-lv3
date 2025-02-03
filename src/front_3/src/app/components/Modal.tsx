interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
}

const Modal = ({ isOpen, onClose, onConfirm }: ModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-[#404040] rounded-xl p-6 w-[400px] mx-4">
        <div className="text-white text-center mb-6">
          <p>새로운 대화를 시작하면 지금까지 진행한 대화가</p>
          <p>모두 사라집니다.</p>
        </div>
        <div className="flex justify-center space-x-3">
          <button
            onClick={onConfirm}
            className="px-6 py-2.5 bg-[#4CAF50] text-white rounded-lg hover:bg-[#45a049] transition"
          >
            새로운 대화 시작
          </button>
          <button
            onClick={onClose}
            className="px-6 py-2.5 bg-[#666666] text-white rounded-lg hover:bg-[#777777] transition"
          >
            취소
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal; 