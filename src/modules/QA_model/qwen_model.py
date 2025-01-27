from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from QA_model.base_model import BaseModel

class QwenModel(BaseModel):
    def __init__(self, model_name="Qwen/Qwen2.5-7B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32 if torch.cuda.is_available() else torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

    def answering(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
