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
    imageName: string;
    fileNames: string[];
    audioFileName : string;
    visualized_name: string;
  }