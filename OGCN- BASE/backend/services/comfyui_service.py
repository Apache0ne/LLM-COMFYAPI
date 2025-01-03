import json

class ComfyUIService:
    def __init__(self, api_url):
        self.api_url = api_url
        self.workflows = self.load_workflows()

    def load_workflows(self):
        with open('workflows.json', 'r') as f:
            return json.load(f)

    def create_workflow(self, workflow_id, selected_model, selected_lora, improved_prompt):
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        workflow = self.workflows[workflow_id].copy()

        # Replace placeholders in the workflow with actual values
        workflow["4"]["inputs"]["ckpt_name"] = selected_model
        workflow["6"]["inputs"]["text"] = improved_prompt
        workflow["7"]["inputs"]["text"] = "text, watermark"

        if selected_lora and selected_lora.lower() != 'none':
            workflow["17"] = {
                "inputs": {
                    "lora_name": selected_lora,
                    "strength_model": 1,
                    "strength_clip": 1,
                    "model": ["4", 0],
                    "clip": ["4", 1]
                },
                "class_type": "LoraLoader",
            }
            workflow["3"]["inputs"]["model"] = ["17", 0]
            workflow["6"]["inputs"]["clip"] = ["17", 1]
            workflow["7"]["inputs"]["clip"] = ["17", 1]

        return workflow
