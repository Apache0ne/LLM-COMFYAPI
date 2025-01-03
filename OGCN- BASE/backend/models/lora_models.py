import os

class LoraModels:
    def __init__(self, models_file):
        self.models_file = models_file
        self.models = self.load_models()

    def load_models(self):
        models = {'SDXL': [], 'SD': [], 'FLUX': []}
        current_category = None

        if os.path.exists(self.models_file):
            with open(self.models_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_category = line[1:-1]
                    elif line and current_category:
                        models[current_category].append(line)

        return models

    def get_models(self):
        return self.models

    def get_models_by_category(self, category):
        return self.models.get(category, [])