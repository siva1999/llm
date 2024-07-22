from flask import Flask, render_template
from text_to_image import generate_image
import os

app = Flask(__name__)

# Read the story from a text file
def read_story():
    with open('story.txt', 'r') as file:
        story = file.read()
    return story

# Generate images for each segment of the story
def generate_images_for_story(story):
    segments = story.split('.')
    image_paths = []
    for i, segment in enumerate(segments):
        if segment.strip():
            image_path = f'static/images/image_{i}.png'
            generate_image(segment.strip(), image_path)
            image_paths.append(image_path)
    return segments, image_paths

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_story')
def generate_story_route():
    story = read_story()
    segments, image_paths = generate_images_for_story(story)
    return render_template('story.html', story_segments=segments, images=image_paths)

if __name__ == '__main__':
    os.makedirs('static/images', exist_ok=True)
    app.run(debug=True)
