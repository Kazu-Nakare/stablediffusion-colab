from flask import Flask, request, jsonify, render_template

# import torch
from diffusers import StableDiffusionPipeline
from diffusers.utils import DIFFUSERS_CACHE

import os

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token="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",
                                               local_files_only=os.path.exists(DIFFUSERS_CACHE)).to("cuda")

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')


@app.route('/', defaults={'path': ''})
def index(path):
    return render_template('index.html')


@app.route('/test', methods=["POST"])
def test():
    result = {'data': request.json["title"] + request.json["content"]}
    return jsonify(result), 200


if __name__ == '__main__':
    app.run()
