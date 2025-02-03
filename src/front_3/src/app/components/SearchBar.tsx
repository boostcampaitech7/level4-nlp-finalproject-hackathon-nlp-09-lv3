// const SearchBar = ({
//     handleSubmit,
//   }: {
//     handleSubmit: (formData: FormData) => void;
//   }) => {
//     return (
//       <form className="py-5 px-3" action={handleSubmit}>
//         <label
//           htmlFor="search"
//           className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
//         >
//           Search
//         </label>
//         <div className="relative">
//           <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
//             <svg
//               className="w-4 h-4 text-gray-500 dark:text-gray-400"
//               aria-hidden="true"
//               xmlns="http://www.w3.org/2000/svg"
//               fill="none"
//               viewBox="0 0 20 20"
//             >
//               <path
//                 stroke="currentColor"
//                 strokeLinecap="round"
//                 strokeLinejoin="round"
//                 strokeWidth="2"
//                 d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
//               />
//             </svg>
//           </div>
//           <input
//             type="search"
//             id="search"
//             name="search"
//             className="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
//             placeholder="FinBuddy에게 물어보세요!"
//             required
//           />
//           <button
//             type="submit"
//             className="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
//           >
//             검색
//           </button>
//         </div>
//       </form>
//     );
//   };
  
//   export default SearchBar;


const SearchBar = ({ handleSubmit }: { handleSubmit: (formData: FormData) => void }) => {
  return (
    <form 
      className="fixed bottom-12 left-1/2 transform -translate-x-1/2 w-[80%] max-w-3xl" 
      action={handleSubmit}
      onSubmit={(e) => {
        const textarea = e.currentTarget.querySelector('textarea');
        if (textarea) {
          setTimeout(() => {
            textarea.style.height = 'auto';
          }, 0);
        }
      }}
    >
      <div className="relative bg-white p-4 rounded-xl shadow-lg">
        <textarea
          id="search"
          name="search"
          className="block w-full resize-none p-3 text-sm text-gray-900 bg-white border-none rounded-lg focus:ring-0 focus:outline-none pr-12"
          placeholder="FinBuddy에게 물어보세요!"
          rows={1}
          onInput={(e) => {
            e.currentTarget.style.height = "auto";
            e.currentTarget.style.height = `${e.currentTarget.scrollHeight}px`;
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              e.currentTarget.form?.requestSubmit();
            }
          }}
          required
        />
        <button
          type="submit"
          className="absolute right-6 bottom-6 p-1 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="검색"
        >
          <svg
            className="w-5 h-5 text-gray-900"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M22 2L11 13" />
            <path d="M22 2L15 22L11 13L2 9L22 2Z" />
          </svg>
        </button>
      </div>
    </form>
  );
};

export default SearchBar;
