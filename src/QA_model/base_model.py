class BaseModel:
    def answering(self, prompt: str) -> str:
        """
        주어진 프롬프트에 대해 모델의 답변을 반환하는 메서드.
        모든 하위 클래스는 이 메서드를 구현해야 한다.
        """
        raise NotImplementedError("하위 클래스 모델은 반드시 이걸 상속받아야 함")
