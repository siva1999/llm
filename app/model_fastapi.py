from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import base64
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

app = FastAPI()

# Load Stable Diffusion model for image generation
pipe = StableDiffusionPipeline.from_pretrained('CompVis/stable-diffusion-v1-4')
pipe = pipe.to("cuda")

# Load fine-tuned T5 model and tokenizer for story generation

# Load from huggingface

tokenizer = AutoTokenizer.from_pretrained("siva1999/flan-t5-story-gen")
model = AutoModelForSeq2SeqLM.from_pretrained("siva1999/flan-t5-story-gen")

# Load from a folder

#model_path = '../model/fine-tuned-t5'
#tokenizer = AutoTokenizer.from_pretrained(model_path)
#model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to("cuda")

text2text_generator = pipeline('text2text-generation', model=model, tokenizer=tokenizer, device=0)

class StoryRequest(BaseModel):
    keywords: List[str]
    emotion: str
    userpref: str

class EnhancedStoryRequest(BaseModel):
    keywords: List[str]
    emotion: str
    userpref: str
    num_characters: int
    characters: List[dict]
    desc_caption: str

class CustomPromptRequest(BaseModel):
    prompt: str

class StoryImageRequest(BaseModel):
    story: str
    max_segments: int = 5

class ImageResponse(BaseModel):
    image: str
    text: str

class StoryResponse(BaseModel):
    images: List[ImageResponse]

def break_story_into_segments(story, max_segments=5):
    sentences = story.split('. ')
    total_sentences = len(sentences)
    sentences_per_segment = total_sentences // max_segments + (total_sentences % max_segments > 0)
    segments = []
    current_segment = []
    for i, sentence in enumerate(sentences):
        current_segment.append(sentence)
        if (i + 1) % sentences_per_segment == 0 or (i + 1) == total_sentences:
            segments.append('. '.join(current_segment).strip())
            current_segment = []
    return segments

def generate_image(prompt):
    image = pipe(prompt).images[0]
    return image

@app.post("/generate-story-images/", response_model=StoryResponse)
async def generate_story_images(story_request: StoryImageRequest):
    try:
        story = story_request.story
        max_segments = story_request.max_segments
        segments = break_story_into_segments(story, max_segments)
        images = []
        for segment in segments:
            prompt = f"Illustrate: {segment}"
            image = generate_image(prompt)
            img_io = io.BytesIO()
            image.save(img_io, 'PNG')
            img_io.seek(0)
            img_str = base64.b64encode(img_io.getvalue()).decode('utf-8')
            images.append(ImageResponse(image=img_str, text=segment))
        return StoryResponse(images=images)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_story")
def generate_story(request: StoryRequest):
    prompt = (
        f"Generate a complete story that evokes a {request.emotion} emotion. The story should feature a "
        f"{request.keywords[0]}, a {request.keywords[1]}, and a {request.keywords[2]}. "
        f"Additionally, incorporate elements of {request.userpref} to enhance the narrative. "
        f"Ensure the {request.userpref} aspects are seamlessly integrated and contribute to the overall {request.emotion} tone of the story."
    )
    try:
        generated_story = text2text_generator(prompt, max_length=512, do_sample=True, top_p=0.95, num_return_sequences=1)
        return {"story": generated_story[0]['generated_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_enhanced_story")
def generate_enhanced_story(request: EnhancedStoryRequest):
    char_details = "; ".join([f"{char['name']}, a {char['profession']}" for char in request.characters])
    prompt = (
        f"Generate a complete story that evokes a {request.emotion} emotion. The story should feature a {request.keywords[0]}, a {request.keywords[1]}, and {request.keywords[2]}. "
        f"Additionally, incorporate elements of {request.userpref} to enhance the narrative. "
        f"Ensure the {request.userpref} aspects are seamlessly integrated and contribute to the overall {request.emotion} tone of the story. "
        f"The story should include {request.num_characters} characters: {char_details}. "
        f"Description: {request.desc_caption}"
    )
    try:
        generated_story = text2text_generator(prompt, max_length=512, do_sample=True, top_p=0.95, num_return_sequences=1)
        return {"story": generated_story[0]['generated_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_custom_story")
def generate_custom_story(request: CustomPromptRequest):
    try:
        generated_story = text2text_generator(request.prompt, max_length=512, do_sample=True, top_p=0.95, num_return_sequences=1)
        return {"story": generated_story[0]['generated_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
