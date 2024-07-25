import streamlit as st
import requests
import base64
from io import BytesIO

# Set the page configuration
st.set_page_config(
    page_title="LLM Based Story Generator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("LLM Based Story Generator")

# Sidebar for window selection
window_option = st.sidebar.selectbox("Choose a window", ("Simple Generator", "Advanced Generator", "Create My Own Prompt", "Generate Story Images"))

API_URL_BASE = "http://127.0.0.1:8000"  # Replace with your actual FastAPI base URL



def generate_download_link(content, filename, content_type):
    b64 = base64.b64encode(content).decode()
    href = f'<a href="data:{content_type};base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

if window_option == "Simple Generator":
    st.header("Simple Generator")
    
    # Input fields for user
    keywords = st.text_input("Enter keywords (comma separated)", "prince, frog, trees")
    emotion = st.text_input("Enter the desired emotion", "happy")
    userpref = st.text_input("Enter user preference", "history")

    if st.button("Generate Story"):
        with st.spinner("Generating your story..."):
            progress_bar = st.progress(0)

            # Preparing the request
            progress_bar.progress(10)
            keywords_list = [keyword.strip() for keyword in keywords.split(",")]
            payload = {
                "keywords": keywords_list,
                "emotion": emotion,
                "userpref": userpref
            }
            progress_bar.progress(30)

            # Sending the request to the server
            response = requests.post(f"{API_URL_BASE}/generate_story", json=payload)
            progress_bar.progress(50)

            # Processing the response
            if response.status_code == 200:
                progress_bar.progress(70)
                story = response.json()["story"]
                progress_bar.progress(90)
                st.text_area("Generated Story", story, height=300)
                progress_bar.progress(100)
                st.success("Story generated successfully!")
            else:
                st.error("Error generating story: " + response.text)

            # Reset progress bar for the next run
            progress_bar.empty()

elif window_option == "Advanced Generator":
    st.header("Advanced Generator")
    
    # Input fields for user
    keywords = st.text_input("Enter keywords (comma separated)", "prince, frog, trees")
    emotion = st.text_input("Enter the desired emotion", "happy")
    userpref = st.text_input("Enter user preference", "history")
    desc_caption = st.text_input("Enter a description caption", "A prince, a princess, and a historian venture into an enchanted forest filled with ancient trees to find a magical frog that holds a secret to happiness.")

    # Default characters
    default_characters = [
        {"name": "Prince Alexander", "profession": "ruler and scholar"},
        {"name": "Princess Isabella", "profession": "adventurous princess"},
        {"name": "Prince Edward", "profession": "historian and childhood friend"}
    ]

    # Input for number of characters
    num_characters = st.number_input("Enter number of characters", min_value=1, max_value=10, value=3)

    # Input fields for characters and professions with default values
    characters = []
    for i in range(num_characters):
        default_name = default_characters[i]["name"] if i < len(default_characters) else f"Character {i+1} Name"
        default_profession = default_characters[i]["profession"] if i < len(default_characters) else f"Character {i+1} Profession"
        char_name = st.text_input(f"Enter name for character {i+1}", default_name)
        char_profession = st.text_input(f"Enter profession for character {i+1}", default_profession)
        characters.append({"name": char_name, "profession": char_profession})

    if st.button("Generate Story"):
        with st.spinner("Generating your story..."):
            progress_bar = st.progress(0)

            # Preparing the request
            progress_bar.progress(10)
            keywords_list = [keyword.strip() for keyword in keywords.split(",")]
            payload = {
                "keywords": keywords_list,
                "emotion": emotion,
                "userpref": userpref,
                "num_characters": num_characters,
                "characters": characters,
                "desc_caption": desc_caption
            }
            progress_bar.progress(30)

            # Sending the request to the server
            response = requests.post(f"{API_URL_BASE}/generate_enhanced_story", json=payload)
            progress_bar.progress(50)

            # Processing the response
            if response.status_code == 200:
                progress_bar.progress(70)
                story = response.json()["story"]
                progress_bar.progress(90)
                st.text_area("Generated Story", story, height=300)
                progress_bar.progress(100)
                st.success("Story generated successfully!")
            else:
                st.error("Error generating story: " + response.text)

            # Reset progress bar for the next run
            progress_bar.empty()

elif window_option == "Create My Own Prompt":
    st.header("Create My Own Prompt")
    
    # Input field for custom prompt
    custom_prompt = st.text_area("Enter your custom prompt", "Generate a story that evokes a happy emotion. The story should feature a prince, a frog, and trees. Additionally, incorporate elements of history to enhance the narrative. Ensure the history aspects are seamlessly integrated and contribute to the overall happy tone of the story.")

    if st.button("Generate Story"):
        with st.spinner("Generating your story..."):
            progress_bar = st.progress(0)

            # Preparing the request
            progress_bar.progress(10)
            payload = {"prompt": custom_prompt}
            progress_bar.progress(30)

            # Sending the request to the server
            response = requests.post(f"{API_URL_BASE}/generate_custom_story", json=payload)
            progress_bar.progress(50)

            # Processing the response
            if response.status_code == 200:
                progress_bar.progress(70)
                story = response.json()["story"]
                progress_bar.progress(90)
                st.text_area("Generated Story", story, height=300)
                progress_bar.progress(100)
                st.success("Story generated successfully!")
            else:
                st.error("Error generating story: " + response.text)

            # Reset progress bar for the next run
            progress_bar.empty()

elif window_option == "Generate Story Images":
    st.header("Generate Story Images")
    story = st.text_area("Enter your story here:", height=200)

    if st.button("Generate"):
        if story:
            with st.spinner("Sending request to server..."):
                response = requests.post("https://4306-34-127-86-94.ngrok-free.app/generate", data={'story': story})
                if response.status_code == 200:
                    with st.spinner("Generating images and PDF..."):
                        response_data = response.json()
                        pdf_content = base64.b64decode(response_data['pdf'])

                        pdf_filename = "generated_story.pdf"
                        pdf_download_link = generate_download_link(pdf_content, pdf_filename, "application/pdf")
                        st.markdown(pdf_download_link, unsafe_allow_html=True)
                else:
                    st.error(f"Error generating images: {response.status_code} - {response.text}")
        else:
            st.error("Please enter a story.")