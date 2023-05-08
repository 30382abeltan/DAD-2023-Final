import streamlit as st
import openai  
import requests  
import os  
from PIL import Image 

openai.api_key = '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'

image_dir = "images"
os.makedirs(image_dir, exist_ok=True)

def generate_sketch(prompt, image_file):
    if image_file is not None:
        img_bytes = image_file.read()
        img_path = os.path.join(image_dir, "uploaded_image.png")
        with open(img_path, "wb") as f:
            f.write(img_bytes)
        prompt += f"![prompt image]({img_path})"
    
    generation_response = openai.Image.create(
        prompt=prompt,
        n=5,
        size="1024x1024",
        response_format="url",
    )
    generated_image_name = "generated_image.png"  
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    generated_image_url = generation_response["data"][0]["url"]  
    generated_image = requests.get(generated_image_url).content  

    with open(generated_image_filepath, "wb") as f:
        f.write(generated_image)  

    return Image.open(generated_image_filepath)


def app():
    st.title("Industrial Design Style Sketch Generator")
    prompt = st.text_input("Enter a text prompt")
    image_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])
    if st.button("Generate Sketch"):
        sketch = generate_sketch(prompt, image_file)
        st.image(sketch, caption="Generated Sketch", use_column_width=True)

if __name__ == "__main__":
    app()
