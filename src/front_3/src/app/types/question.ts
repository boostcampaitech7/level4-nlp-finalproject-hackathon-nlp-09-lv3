// export interface QAndA {
//     question: string
//     answer: string | null
//     error?: boolean
// }

export interface QAndA {
    question: string;
    answer: string;
    context: string;
    error: boolean;
    imageNames: string[];
    fileNames: string[];
  }