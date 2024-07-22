import streamlit as st
import requests

st.title("Story Generator")

# Input fields for user
keywords = st.text_input("Enter keywords (comma separated)", "dog, sun, beach")
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
