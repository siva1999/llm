from diffusers import StableDiffusionPipeline
import torch

model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe.to(device)

def generate_image(prompt, filename):
    image = pipe(prompt).images[0]
    image.save(filename)
