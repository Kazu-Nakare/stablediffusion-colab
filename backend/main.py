import os
import io
from flask import Flask, request, send_file, render_template

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from diffusers.utils import DIFFUSERS_CACHE

torch_device = "cuda" if torch.cuda.is_available() else "cpu"


pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1",
                                               ).to(torch_device)

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')


@ app.route('/', defaults={'path': ''})
def index(path):
    return render_template('index.html')


@ app.route('/generate', methods=["POST"])
def generate():
    prompt = request.json["prompt"]
    with autocast(torch_device):
        image = pipe(prompt)["images"][0]
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == '__main__':
    app.run()
