from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from config import Config
import requests
from services.comfyui_service import ComfyUIService
from services.llm_service import LLMService
from utils.http_client import HTTPClient
from utils.html_utils import escape_html
import logging
from groq import Groq
from prompts import system_prompt_rpg, system_prompt_image, system_prompt_choices

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)

comfyui_service = ComfyUIService(app.config['COMFYUI_API_URL'])
llm_service = LLMService(app.config['LLM_CONFIG'])
http_client = HTTPClient()

#logging.basicConfig(level=logging.DEBUG)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(list(app.config['CHECKPOINT_MODELS'].keys()))

@app.route('/api/models', methods=['GET'])
def get_models_and_loras():
    category = request.args.get('category')
    return jsonify({
        'models': app.config['CHECKPOINT_MODELS'].get(category, []),
        'loras': app.config['LORA_MODELS'].get(category, [])
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    original_prompt = data['prompt']
    category = data['category']
    selected_model = data['model']
    selected_lora = data.get('lora', '')
    workflow_id = data.get('workflow_id', 'workflow1')  # Default to 'workflow1' if not provided

    # Ensure LLM service is properly configured
    if 'LLM_CONFIG' not in app.config or not app.config['LLM_CONFIG'].get('choice'):
        #app.logger.warning("LLM not configured. Using original prompt.")
        #app.logger.debug(f"LLM Config: {app.config['LLM_CONFIG']}")
        improved_prompt_rpg = original_prompt
        improved_prompt_image = original_prompt
        game_choices = "No game choices available."
    else:
        try:
            improved_prompt_rpg = llm_service.improve_prompt(original_prompt, system_prompt_rpg)
            improved_prompt_image = llm_service.improve_prompt(improved_prompt_rpg, system_prompt_image)
            game_choices = llm_service.improve_prompt(improved_prompt_rpg, system_prompt_choices)
            #app.logger.debug(f"Improved prompt: {improved_prompt}")
        except Exception as e:
            #app.logger.error(f"Error improving prompt: {str(e)}")
            improved_prompt_rpg = original_prompt
            improved_prompt_image = original_prompt
            game_choices = "No game choices available."

    workflow = comfyui_service.create_workflow(workflow_id, selected_model, selected_lora, improved_prompt_image)
    #app.logger.debug(f"Generated workflow: {workflow}")

    try:
        response = http_client.post(app.config['COMFYUI_API_URL'] + "/prompt", json={"prompt": workflow})
        if response is None:
            #logging.error("Failed to post workflow to ComfyUI API")
            return jsonify({'error': 'Failed to post workflow to ComfyUI API'}), 500
        if response.status_code == 200:
            prompt_id = response.json()['prompt_id']
            #logging.debug(f"Received prompt_id: {prompt_id}")
            
            while True:
                try:
                    history_response = http_client.get(f"{app.config['COMFYUI_API_URL']}/history/{prompt_id}")
                    if history_response is None:
                        #logging.error(f"Failed to fetch history for prompt_id: {prompt_id}")
                        return jsonify({'error': 'Failed to fetch image generation history'}), 500
                    if history_response.status_code == 200:
                        history = history_response.json()
                        #logging.debug(f"History response: {history}")
                        if prompt_id in history:
                            output_images = history[prompt_id]['outputs']
                            if output_images:
                                image_data = output_images['13']['images'][0]
                                image_url = f"{app.config['COMFYUI_API_URL']}/view?filename={image_data['filename']}"
                                #logging.debug(f"Image URL: {image_url}")

                                image_response = http_client.get(image_url)
                                if image_response is None:
                                    #logging.error(f"Failed to fetch image for prompt_id: {prompt_id}")
                                    return jsonify({'error': 'Failed to fetch image'}), 500
                                if image_response.status_code == 200:
                                    # Sanitize prompts for use in headers
                                    safe_original_prompt = escape_html(original_prompt).replace('\n', ' ').replace('\r', '')
                                    safe_improved_prompt_rpg = escape_html(improved_prompt_rpg).replace('\n', ' ').replace('\r', '')
                                    safe_improved_prompt_image = escape_html(improved_prompt_image).replace('\n', ' ').replace('\r', '')
                                    safe_game_choices = escape_html(game_choices).replace('\n', ' ').replace('\r', '')
                                    
                                    return Response(
                                        image_response.content,
                                        mimetype=image_response.headers['Content-Type'],
                                        headers={
                                            'X-Original-Prompt': safe_original_prompt,
                                            'X-Improved-Prompt-RPG': safe_improved_prompt_rpg,
                                            'X-Improved-Prompt-Image': safe_improved_prompt_image,
                                            'X-Game-Choices': safe_game_choices,
                                            'Access-Control-Expose-Headers': 'X-Original-Prompt, X-Improved-Prompt-RPG, X-Improved-Prompt-Image, X-Game-Choices',
                                            'Content-Type': 'image/png'  # Set the correct content type for the image
                                        }
                                    )
                except requests.exceptions.RequestException as e:
                    #logging.error(f"Request exception while fetching history: {e}")
                    return jsonify({'error': 'Failed to fetch image generation history'}), 500
    except requests.exceptions.ConnectionError:
        #logging.error(f"Connection error while posting workflow: {e}")
        return jsonify({'error': 'Unable to connect to ComfyUI API. Make sure it\'s running.'}), 503

    return jsonify({'error': 'Failed to generate image'}), 500

@app.route('/api/setup', methods=['POST'])
def save_setup():
    data = request.json
    llm_choice = data['llmChoice']
    if llm_choice == 'cerebras':
        app.config['LLM_CONFIG'] = {
            'choice': llm_choice,
            'model': data.get('modelName'),
            'api_key': data.get('apiKey'),
            'api_url': None  # No API URL required for Cerebras
        }
    elif llm_choice == 'groq':
        groq_model = data.get('groqModel')
        if not groq_model:
            return jsonify({'error': 'groqModel is required for Groq LLM choice'}), 400
        app.config['LLM_CONFIG'] = {
            'choice': llm_choice,
            'model': groq_model,
            'api_key': data.get('apiKey'),
            'api_url': 'https://api.groq.com/openai/v1'  # Hardcoded API URL for Groq
        }
    elif llm_choice == 'sambanova':
        app.config['LLM_CONFIG'] = {
            'choice': llm_choice,
            'model': data.get('modelName'),
            'api_key': data.get('apiKey'),
            'api_url': 'https://api.sambanova.ai/v1'  # Hardcoded API URL for Sambanova
        }
    else:
        app.config['LLM_CONFIG'] = {
            'choice': llm_choice,
            'model': data.get('ollamaModel') or data.get('modelName'),
            'api_key': data.get('apiKey'),
            'api_url': data.get('apiUrl', 'http://localhost:11434')  # Default to the correct URL if not provided
        }
    llm_service.update_config(app.config['LLM_CONFIG'])
    #app.logger.debug(f"Updated LLM Config: {app.config['LLM_CONFIG']}")
    return jsonify({'message': 'Setup saved successfully'})

@app.route('/api/setup', methods=['GET'])
def get_setup():
    setup_config = app.config.get('LLM_CONFIG', {'choice': None})
    #app.logger.debug(f"Retrieved LLM Config: {setup_config}")
    return jsonify(setup_config)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
