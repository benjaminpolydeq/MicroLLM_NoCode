from transformers import AutoModelForCausalLM

class ARSLMModel:
    def __init__(self, model_path, device="cpu"):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto"
        ).to(device)

    def forward(self, **inputs):
        return self.model(**inputs)