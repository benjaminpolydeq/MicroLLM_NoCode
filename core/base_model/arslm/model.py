import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ARSLMModel:
    def __init__(self, model_path: str, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if self.device=="cuda" else torch.float32
        ).to(self.device)
        self.model.eval()

    @torch.no_grad()
    def generate(self, prompt: str, max_tokens: int=256, temperature: float=0.7, top_p: float=0.9) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            eos_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
