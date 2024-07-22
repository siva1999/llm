from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

class StoryRequest(BaseModel):
    keywords: list
    emotion: str
    userpref: str

# Initialize FastAPI
app = FastAPI()

# Load the fine-tuned model and tokenizer
model_path = '../model/fine-tuned-t5'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Create a pipeline for text generation
text2text_generator = pipeline('text2text-generation', model=model, tokenizer=tokenizer)

@app.post("/generate_story")
def generate_story(request: StoryRequest):
    prompt = (
        f"Generate a story that evokes a {request.emotion} emotion. The story should feature a "
        f"{request.keywords[0]}, a {request.keywords[1]}, and a {request.keywords[2]}. "
        f"Additionally, incorporate elements of {request.userpref} to enhance the narrative. "
        f"Ensure the {request.userpref} aspects are seamlessly integrated and contribute to the overall {request.emotion} tone of the story."
    )
    try:
        generated_story = text2text_generator(prompt, max_length=512, do_sample=True, top_p=0.95, num_return_sequences=1)
        return {"story": generated_story[0]['generated_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
