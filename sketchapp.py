import streamlit as st
import openai  
import requests  
import os  
from PIL import Image 

openai.api_key = '*YOUR OPENAI API KEY HERE*'

# set a directory to save DALL-E images to (parts of this taken from Github DALL-E tutorial and modified to fit my app)
image_dir = "images"
os.makedirs(image_dir, exist_ok=True)

# generate image based on prompt or image file or both
def generate_sketch(prompt, image_file, image_size):
    generation_response = None  # Initialize the variable to None
    
    image_urls = []
    
    # checks whether an image file has been uploaded
    if image_file is not None: 
        # reads content of uploaded image file
        img_bytes = image_file.read()
        # creates file path for uploaded image
        img_path = os.path.join(image_dir, "uploaded_image.png")
        with open(img_path, "wb") as f:
            # saves the uploaded image to disk at the specified path
            f.write(img_bytes)
        prompt += f"![prompt image]({img_path})"
    
    generation_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=image_size,
        response_format="url",
    )

    #saving the image (taken from Github DALL-E Tutorial)
    generated_image_name = "generated_image.png"  
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    generated_image_url = generation_response["data"][0]["url"]  
    generated_image = requests.get(generated_image_url).content  

    with open(generated_image_filepath, "wb") as f:
        f.write(generated_image)  

    return [Image.open(generated_image_filepath)]

def app():
    st.title("Industrial Design Style Sketch Generator")
    st.markdown("**Your prompt must be specific.** Please specify the type of sketch you want, in what style, color, background, line weight, and context.")
    st.markdown("A **strong example** would be: 'an industrial design style sketch of a cube with strong line weight in a grey marker render with a blue gradient background'")
    st.markdown("Using **both** the text prompt and the image prompt can help generate a better sketch. You will still be able to generate sketches with only a text prompt or an image prompt.")
    st.markdown("Happy sketching!")
    prompt = st.text_input("Enter a text prompt")
    image_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])
    image_size = st.selectbox("Image Size", ["256x256", "512x512", "1024x1024"])
   
    if st.button("Generate Sketches"):
        sketches = generate_sketch(prompt, image_file, image_size)
        for i, sketch in enumerate(sketches):
            st.image(sketch, caption=f"Generated Sketch {i+1}", use_column_width=True)

if __name__ == "__main__":
    app()
