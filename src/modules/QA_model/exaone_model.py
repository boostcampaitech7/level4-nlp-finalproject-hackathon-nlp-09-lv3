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
        messages = [
            {"role": "system", 
            "content": """You are EXAONE model from LG AI Research, a helpful assistant. 
            사용자의 지시에 맞게 질문에 답하세요."""},
            {"role": "user", "content": prompt}
        ]
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        )
        outputs = self.model.generate(
                    input_ids.to('cuda'),
                    max_new_tokens=512,
                    eos_token_id=self.tokenizer.eos_token_id,
                    do_sample=False
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens = True, )
        answer = answer[answer.find('[|assistant|]')+13:]
        return answer
