import type { ClosedQueryResponse } from '../../types/dto/closedQueryService'; 
import type { QAndA } from '../../types/question';
import { closedDomainApi } from '../chatApi';

const BASE_URL = '/static/output';


export const parseClosedApiResponse = (
  response: ClosedQueryResponse, 
  question: string
): QAndA => {
  const { answer, pdfFileNames, audioFileNames } = response; // 추가된 필드 반영
  console.log(answer)
  console.log(pdfFileNames)
  console.log(audioFileNames)
  // [생성된 이미지 이름] 을 기준으로 분리
  const [context, remainingText = ''] = answer.split('[생성된 이미지 이름]');

  // 이미지 이름과 출처 분리
  const [imageNameSection, sourceSection = ''] = remainingText.split('[정보 출처]');


  const imageName = imageNameSection
    .split('\n')  // 줄바꿈 기준 분리
    .map(name => name.trim())
    .filter(name => name.length > 0)
    .map(path => {
      console.log('처리 전 경로:', path); // 디버깅용
      const fileName = path.split('/').pop() || '';
      const parsedfileName = fileName.slice(2, fileName.length)
      const newPath = `./static/output/${parsedfileName}`;
      console.log('처리 후 경로:', newPath); // 디버깅용
      return newPath;
    }).at(0) || '';  // 첫 번째 요소 가져옴, 없으면 빈 문자열

  console.log('최종 imageName:', imageName); // 디버깅용

  const fileNames = pdfFileNames.map(name => `${BASE_URL}/${name}`); // PDF 파일 변환

  const audioFileName = audioFileNames.at(0) || ''; // 첫 번째 오디오 파일 선택

  return {
    question,
    answer: context.trim(),
    context: '',
    error: false,
    imageName,
    fileNames,
    audioFileName
  };
};
