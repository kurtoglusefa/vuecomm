import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import dotenv
import re

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

endpoint = "your_azure_oai_endpoint"
api_key = "your_azure_oai_key"
deployment = "your_azure_oai_deployment"

client = openai.AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)

system_message = {
    "role": "system",
    "content": "Sei un assistente virtuale chiamato Jonathan. Rispondi sempre nella stessa lingua della domanda dell'utente.",
}

def get_response(user_query):
    completion = client.chat.completions.create(
        model=deployment,
        temperature=0.5,
        max_tokens=1000,
        messages=[
            system_message,
            {
                "role": "user",
                "content": user_query,
            },
        ],
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": "your_azure_search_endpoint",
                        "index_name": "your_azure_search_index",
                        "authentication": {
                            "type": "api_key",
                            "key": "your_azure_search_key",
                        }
                    }
                }
            ],
        }
    )
    response_content = completion.choices[0].message.content
    cleaned_response_content = re.sub(r'\[doc\d+\]', '', response_content)
    formatted_response_content = cleaned_response_content.replace('\n', '<br>')
    return formatted_response_content

@app.route('/api/chat/send', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get('message')
    response = get_response(user_query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)