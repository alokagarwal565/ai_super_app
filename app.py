# app.py
from flask import Flask, render_template, request, jsonify
import replicate
import requests
import os

app = Flask(__name__)

def download_image(image_url, filename):
    response = requests.get(image_url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print("FAILURE!!!!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data['prompt']
    hf_lora = data['hf_lora']

    input_data = {
        "prompt": prompt,
        "hf_lora": hf_lora
    }

    output = replicate.run(
        "lucataco/flux-dev-lora:091495765fa5ef2725a175a57b276ec30dc9d39c22d30410f2ede68a3eab66b3",
        input=input_data
    )

    # Get the list of predictions and select the most recent one
    predictions = replicate.predictions.list()

    if predictions.results:
        latest_prediction = predictions.results[0]
        output_url = latest_prediction.output[0] if latest_prediction.output else None
        
        if output_url:
            download_image(output_url, "static/output.jpg")
            return jsonify({"status": "success", "image_url": "static/output.jpg"})
    
    return jsonify({"status": "error", "message": "No predictions available."})

if __name__ == '__main__':
    app.run(debug=True)