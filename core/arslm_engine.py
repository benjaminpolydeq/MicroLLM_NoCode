# core/arslm_engine.py

from core.base_model.arslm.model import ARSLMModel

# ⚠️ chemin vers TON modèle
MODEL_PATH = "models/arslm"  # à adapter

_arslm_instance = None


def get_model():
    global _arslm_instance
    if _arslm_instance is None:
        _arslm_instance = ARSLMModel(MODEL_PATH)
    return _arslm_instance


def arslm_generate(prompt, max_tokens=256, temperature=0.7):
    model = get_model()
    return model.generate(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
