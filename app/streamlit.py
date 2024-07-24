import streamlit as st
import requests

# Set the page configuration
st.set_page_config(
    page_title="LLM Based Story Generator",  # Title that appears on the tab
    page_icon="📖",  # Optional: add an icon
    layout="wide",  # Optional: set the layout
    initial_sidebar_state="expanded"  # Optional: set the initial sidebar state
)

st.title("LLM Based Story Generator")

# Sidebar for window selection
window_option = st.sidebar.selectbox("Choose a window", ("Simple Generator", "Advanced Generator", "Create My Own Prompt"))

if window_option == "Simple Generator":
    st.header("Simple Generator")
    
    # Input fields for user
    keywords = st.text_input("Enter keywords (comma separated)", "prince, frog, trees")
    emotion = st.text_input("Enter the desired emotion", "happy")
    userpref = st.text_input("Enter user preference", "history")

    if st.button("Generate Story"):
        with st.spinner("Generating your story....."):
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
            response = requests.post("http://127.0.0.1:8000/generate_story", json=payload)
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
        with st.spinner("Generating your story....."):
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
            response = requests.post("http://127.0.0.1:8000/generate_enhanced_story", json=payload)
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
        with st.spinner("Generating your story....."):
            progress_bar = st.progress(0)

            # Preparing the request
            progress_bar.progress(10)
            payload = {"prompt": custom_prompt}
            progress_bar.progress(30)

            # Sending the request to the server
            response = requests.post("http://127.0.0.1:8000/generate_custom_story", json=payload)
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
