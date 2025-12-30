from peft import PeftModel

class LoRAManager:
    def load(self, base_model, lora_path):
        return PeftModel.from_pretrained(base_model, lora_path)