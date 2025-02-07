import type { ClosedQueryResponse } from '../../types/dto/closedQueryService'; 
import type { QAndA } from '../../types/question';

const BASE_URL = '/static/output';


export const parseApiResponse = (
  response: ClosedQueryResponse, 
  question: string
): QAndA => {
  const { answer } = response;  // response에서 answer 추출
  
  // [생성된 이미지 이름] 을 기준으로 분리
  const [context, remainingText = ''] = answer.split('[생성된 이미지 이름]');
  
  // 이미지 이름과 출처 분리
  const [imageNameSection, sourceSection = ''] = remainingText.split('[정보 출처]');
  
  console.log('원본 이미지 섹션:', imageNameSection); // 디버깅용

  const imageName = imageNameSection
    .split('\n')  // 줄바꿈으로 분리 (쉼표가 아님)
    .map(name => name.trim())
    .filter(name => name.length > 0)
    .map(path => {
      console.log('처리 전 경로:', path); // 디버깅용
      const fileName = path.split('/').pop() || '';
      const newPath = `/static/output/${fileName}`;
      console.log('처리 후 경로:', newPath); // 디버깅용
      return newPath;
    }).at(0) || '';  // 첫 번째 요소를 가져옴, 없으면 빈 문자열

  console.log('최종 imageName:', imageName); // 디버깅용

  const fileNames = sourceSection
    .split('\n')
    .map(name => name.trim())
    .filter(name => name.length > 0)
    .map(path => `${BASE_URL}/${path}`);

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
