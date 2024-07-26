# Fine Tuning LLM For Story Generation

In this project, I developed a custom dataset derived from an existing dataset using the Spacy NLP model to extract characters, objects, locations, vehicles, professions, and emotions from the stories. 

Dataset before :

![image](https://github.com/user-attachments/assets/5c2f15dc-8fd6-4f3c-a40b-ff0fb7b4d823)


Dataset after custom creation :

![image](https://github.com/user-attachments/assets/44fda2e4-796d-4871-a9e4-3bd0c0c287b6)


## How to Run the Story generator 

1. clone the repo 
2. go to the folder llm/app
3. run the fast API in one terminal
4. run the streamlit in another terminal

For Generating images for storytelling we need a high power GPU

1. go to the notebook : https://github.com/siva1999/llm/blob/main/storytelling/text_to_image.ipynb , run it in google collab under a GPU. this will run a fastAPI service.
2. the notebook will give a ngork public ip , paste it in : https://github.com/siva1999/llm/blob/main/app/streamlit_with_image.py  (line no : 171)
3. run the fast API 
4. run the streamlit

### Model Sample Output :


Simple Generator : https://github.com/siva1999/llm/blob/main/app/streamlit_output_simple.pdf

Advanced Generator : https://github.com/siva1999/llm/blob/main/app/streamlit_output_advanced.pdf

Custom Prompt Generator : https://github.com/siva1999/llm/blob/main/app/streamlit_output_own_prompt.pdf

Generated images with story : https://github.com/siva1999/llm/blob/main/app/generated_story_with%20image.pdf

## Results

Before Fine Tuning :

![image](https://github.com/user-attachments/assets/7f555319-7152-49df-87e0-7d437c5978f6)


After Fine Tuning :

![image](https://github.com/user-attachments/assets/e5eccf53-641a-400b-b877-5a05fad485d2)


I then fine-tuned the Google FLAN-T5 Large (783M parameters) language model using this custom dataset.

Fine tuned model is uploaded in the Huggingface : https://huggingface.co/siva1999/flan-t5-story-gen






