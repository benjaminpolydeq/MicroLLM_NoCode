from pathlib import Path

TEMPLATE_DIR = Path("nocode/templates")

def list_templates():
    return [f.stem for f in TEMPLATE_DIR.glob("*.txt")]

def load_template(name):
    return (TEMPLATE_DIR / f"{name}.txt").read_text(encoding="utf-8")

def render_template(template, user_input, history=""):
    return template.replace("{{user_input}}", user_input)\
                   .replace("{{history}}", history)