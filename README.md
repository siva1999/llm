# Fine Tuning LLM For Story Generation

In this project, I developed a custom dataset derived from an existing dataset using the Spacy NLP model to extract characters, objects, locations, vehicles, professions, and emotions from the stories. 

Dataset before :

![image](https://github.com/user-attachments/assets/5c2f15dc-8fd6-4f3c-a40b-ff0fb7b4d823)


Dataset after custom creation :

![image](https://github.com/user-attachments/assets/44fda2e4-796d-4871-a9e4-3bd0c0c287b6)


## Results

Before Fine Tuning :

![image](https://github.com/user-attachments/assets/7f555319-7152-49df-87e0-7d437c5978f6)


After Fine Tuning :

![image](https://github.com/user-attachments/assets/e5eccf53-641a-400b-b877-5a05fad485d2)


I then fine-tuned the Google FLAN-T5 Large (783M parameters) language model using this custom dataset.

Fine tuned model is uploaded in the Huggingface : https://huggingface.co/siva1999/flan-t5-story-gen


### Model Sample Output :


Simple Generator : https://github.com/siva1999/llm/blob/main/app/streamlit_output_simple.pdf

Advanced Generator : https://github.com/siva1999/llm/blob/main/app/streamlit_output_advanced.pdf

Custom Prompt Generator : https://github.com/siva1999/llm/blob/main/app/streamlit_output_own_prompt.pdf



