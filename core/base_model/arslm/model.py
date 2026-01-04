import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ARSLMModel:
    def __init__(self, model_path="gpt2", device="cpu"):
        """
        Load real ARSLM model (can be Micro, Small, Medium, Large)
        """
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=temperature
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
