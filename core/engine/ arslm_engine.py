from core.base_model.arslm.model import ARSLMModel

MODEL_PATH = "models/arslm"
_model = None

def load_model():
    global _model
    if _model is None:
        _model = ARSLMModel(MODEL_PATH)
    return _model

def generate_text(prompt: str, max_tokens: int=256, temperature: float=0.7) -> str:
    model = load_model()
    return model.generate(prompt=prompt, max_tokens=max_tokens, temperature=temperature)