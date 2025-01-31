import torch
from unsloth import FastLanguageModel
from QA_model.base_model import BaseModel


class Qwen32BModel(BaseModel):
    def __init__(self):
        # Load the Gemma 27B model
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name="unsloth/DeepSeek-R1-Distill-Qwen-32B-bnb-4bit",
            max_seq_length=2048,
            dtype=None,  # Automatically picks float16 for A100/H100, float32 for CPU
            load_in_4bit=True,  # Load with 4-bit quantization
        )
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        FastLanguageModel.for_inference(self.model)
    
    def answering(self, prompt:str):
        inputs = self.tokenizer([prompt], return_tensors = "pt").to("cuda")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=256,
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        answer = answer[answer.find('</think>')+10:]
        return answer

        

