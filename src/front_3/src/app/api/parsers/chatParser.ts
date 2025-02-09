// import type { ClosedQueryResponse } from '../../types/dto/closedQueryService'; 
// import type { QAndA } from '../../types/question';
// import { closedDomainApi } from '../chatApi';

// const BASE_URL = '/static/output';


// export const parseClosedApiResponse = (
//   response: ClosedQueryResponse, 
//   question: string
// ): QAndA => {
//   const { answer, pdfFileNames, audioFileNames } = response; // 추가된 필드 반영
//   console.log(answer)
//   console.log(pdfFileNames)
//   console.log(audioFileNames)
//   // [생성된 이미지 이름] 을 기준으로 분리
//   const [context, remainingText = ''] = answer.split('[생성된 이미지 이름]');

//   // 이미지 이름과 출처 분리
//   const [imageNameSection, sourceSection = ''] = remainingText.split('[정보 출처]');


//   const imageName = imageNameSection
//     .split('\n')  // 줄바꿈 기준 분리
//     .map(name => name.trim())
//     .filter(name => name.length > 0)
//     .map(path => {
//       console.log('처리 전 경로:', path); // 디버깅용
//       const fileName = path.split('/').pop() || '';
//       const parsedfileName = fileName.slice(2, fileName.length)
//       console.log('추출된 이미지 이름:', parsedfileName); // 디버깅용
//       const newPath = `./static/output/${parsedfileName}`;
//       console.log('처리 후 경로:', newPath); // 디버깅용
//       return newPath;
//     }).at(0) || '';  // 첫 번째 요소 가져옴, 없으면 빈 문자열

//   console.log('최종 imageName:', imageName); // 디버깅용

//   const fileNames = pdfFileNames.map(name => `${BASE_URL}/${name}`); // PDF 파일 변환

//   const audioFileName = audioFileNames.at(0) || ''; // 첫 번째 오디오 파일 선택

//   return {
//     question,
//     answer: context.trim(),
//     context: '',
//     error: false,
//     imageName,
//     fileNames,
//     audioFileName
//   };
// };

// 뭔가 처리가 좀 복잡하게 하는것 같아서 좀더 간편하게 정규표현식으로 자르도록 수정
import type { ClosedQueryResponse } from '../../types/dto/closedQueryService'; 
import type { QAndA } from '../../types/question';

const IMAGE_BASE_URL = '/static/output';
const PDF_BASE_URL = '/static/pdfs';
const TTS_BASE_URL = '/static/tts';

export const parseClosedApiResponse = (
  response: ClosedQueryResponse, 
  question: string
): QAndA => {
  // pdfFileNames와 audioFileNames가 없을 경우 기본값을 빈 배열로 지정
  const { answer, pdfFileNames = [], audioFileNames = [] } = response;
  console.log('응답:', answer);
  console.log('PDF 파일:', pdfFileNames);
  console.log('오디오 파일:', audioFileNames);

  // 정규표현식으로 대괄호 안의 .png 파일명을 추출합니다.
  const bracketMatch = answer.match(/\[([^\]]+\.png)\]/);
  let imageFileName = bracketMatch ? bracketMatch[1].trim() : '';
  if (!imageFileName) {
    // 예외적으로 "- 생성된 이미지 이름:" 뒤의 파일명을 시도
    const fallbackMatch = answer.match(/-+\s*생성된\s+이미지\s+이름:\s*([^\s]+)/);
    if (fallbackMatch) {
      imageFileName = fallbackMatch[1].trim();
    }
  }
  const imageName = imageFileName ? `${IMAGE_BASE_URL}/${imageFileName}` : '';
  

  // 선택적으로, 이미지 태그로 노출되지 않도록 답변 텍스트에서 제거할 수 있습니다.
  const cleanedAnswer = answer.replace(/\[([^\]]+\.png)\]/, '').trim();

  // PDF 파일: 응답에 포함된 경로에서 파일명만 추출하여 PDF_BASE_URL과 결합
  const fileNames = pdfFileNames.map(name => {
    const baseName = name.split('/').pop(); // 디렉토리 경로 제거
    return `${PDF_BASE_URL}/${baseName}`;
  });

  // 오디오 파일: 첫 번째 요소의 파일명만 추출하여 TTS_BASE_URL과 결합
  let audioFileNameFinal = '';
  if (typeof audioFileNames === 'string') {
    audioFileNameFinal = `${TTS_BASE_URL}/${audioFileNames.split('/').pop()}`;
  } else if (Array.isArray(audioFileNames) && audioFileNames.length > 0) {
    const firstAudio = audioFileNames[0] as string;
    audioFileNameFinal = `${TTS_BASE_URL}/${firstAudio.split('/').pop()}`;
  }


  console.log('실제 참조하는 이미지 파일 :', imageName);
  console.log('실제 참조하는 PDF 파일:', fileNames);
  console.log('실제 참조하는 오디오 파일:', audioFileNameFinal);
    
  return {
    question,
    answer: cleanedAnswer,
    context: '',
    error: false,
    imageName,
    fileNames,
    audioFileName: audioFileNameFinal
  };
};
