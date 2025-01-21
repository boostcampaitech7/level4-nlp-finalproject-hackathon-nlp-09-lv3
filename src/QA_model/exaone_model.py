from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from QA_model.base_model import BaseModel

class ExaoneModel(BaseModel):
    def __init__(self, model_name="LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )

    def answering(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            eos_token_id=self.tokenizer.eos_token_id,
            do_sample=False
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
