from flask import Flask, request, send_file, render_template

# import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from diffusers.utils import DIFFUSERS_CACHE

import io
import os

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=os.environ["HF_TOKEN"],
                                               local_files_only=os.path.exists(DIFFUSERS_CACHE)).to("cuda")

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')


@ app.route('/', defaults={'path': ''})
def index(path):
    return render_template('index.html')


@ app.route('/generate', methods=["POST"])
def generate():
    prompt = request.json["prompt"]
    with autocast("cuda"):
        image = pipe(prompt)["sample"][0]
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == '__main__':
    app.run()
