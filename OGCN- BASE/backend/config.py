import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    COMFYUI_API_URL = 'http://127.0.0.1:8189/api'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Default LLM configuration
    LLM_CONFIG = {
        'choice': 'ollama',
        'model': 'llama3.2',
        'api_key': None,
        'api_url': 'http://localhost:11434'  # Ensure this is set correctly
    }

    @staticmethod
    def load_checkpoint_models():
        models_file = os.path.join(os.path.dirname(__file__), 'CKPmodels.txt')
        models = {'SDXL': [], 'SD': [], 'FLUX': []}
        current_category = None

        if os.path.exists(models_file):
            with open(models_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_category = line[1:-1]
                    elif line and current_category:
                        models[current_category].append(line)

        return models

    CHECKPOINT_MODELS = load_checkpoint_models()

    @staticmethod
    def load_lora_models():
        models_file = os.path.join(os.path.dirname(__file__), 'Lmodels.txt')
        models = {'SDXL': [], 'SD': [], 'FLUX': []}
        current_category = None

        if os.path.exists(models_file):
            with open(models_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_category = line[1:-1]
                    elif line and current_category:
                        models[current_category].append(line)

        return models

    LORA_MODELS = load_lora_models()