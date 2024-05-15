from flask import Flask, request, jsonify
from pathlib import Path
from openai import OpenAI
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

cloudinary.config( 
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_API_KEY'), 
  api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

app = Flask(__name__)

@app.route('/texttospeach', methods=['POST'])
def shorten_url():
    data = request.json
    if 'text_quotes' in data:
        print(data)
        original_url = data['text_quotes']
        speech_file_path = Path(__file__).parent / "speech.mp3"

        voice_type="alloy"
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        if 'voice_type' in data and data["voice_type"].lower() in voices:
            voice_type = data["voice_type"].lower()

        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice_type,
            input=original_url
        )

        response.stream_to_file(speech_file_path)

        # Upload speech file to Cloudinary
        result = upload(speech_file_path, resource_type="video")

        # Get the URL of the uploaded file from Cloudinary
        speech_url, options = cloudinary_url(result['public_id'], resource_type="video")

        print(speech_url)
        
        return speech_url, 200
    else:
        return "No text provided in request body", 400

if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    app.run('0.0.0.0', debug=True, port=8100)
