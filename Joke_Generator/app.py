from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = ''  # Replace with secure storage (e.g., .env)
GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' + API_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-joke', methods=['POST'])
def generate_joke():
    # Get topic from request, default to empty string
    topic = request.json.get('topic', '')
    # Construct prompt based on topic
    prompt = f"Tell me a funny joke about {topic}." if topic else "Tell me a random funny joke."
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 1.0,  # Increase randomness
            "maxOutputTokens": 200  # Limit response length
        }
    }
    try:
        response = requests.post(GEMINI_URL, json=data)
        response.raise_for_status()
        response_json = response.json()
        print("API Response:", response_json)
        joke = response_json['candidates'][0]['content']['parts'][0]['text']
        return jsonify({'joke': joke})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except (KeyError, IndexError) as e:
        return jsonify({'error': f'Unexpected API response format: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)