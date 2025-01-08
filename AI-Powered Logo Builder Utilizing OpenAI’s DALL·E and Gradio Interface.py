import os
import openai
import requests 
import gradio as gr

openai.api_key = "" #Enter your API_KEY here 

def generate_logo(prompt, style="minimalist", color_scheme="blue and white", dimensions="1024x1024"):
    try:
        
        detailed_prompt = f"{prompt}, in a {style} style, with a {color_scheme} color scheme"
        
        
        print(f"Generating logo with prompt: {detailed_prompt}")

        
        response = openai.Image.create(
            prompt=detailed_prompt,
            n=4,  
            size=dimensions
        )

        
        os.makedirs("logos", exist_ok=True)

        
        image_paths = []
        preview_images = []
        for i, img_data in enumerate(response['data']):
            img_url = img_data['url']
            filename = f"logo_{i + 1}.png"
            filepath = os.path.join("logos", filename)

      
            with open(filepath, "wb") as f:
                f.write(requests.get(img_url).content)

            image_paths.append(filepath)
            preview_images.append(filepath)

        return preview_images, image_paths

    except Exception as e:
        
        print(f"Error occurred: {e}")
        return [], [], f"Error: {e}"

interface = gr.Interface(
    fn=generate_logo,
    inputs=[
        gr.Textbox(label="Logo Description", placeholder="e.g., 'Modern tech company logo'"),
        gr.Radio(["minimalist", "abstract", "vintage", "futuristic"], label="Style", value="minimalist"),
        gr.Dropdown(
            [
                "blue and white", 
                "black and gold", 
                "red and black", 
                "green and white", 
                "purple and silver",
                "orange and teal", 
                "pink and gray", 
                "yellow and black", 
                "turquoise and coral", 
                "navy and cream", 
                "emerald and gold"
            ],
            label="Color Scheme",
            value="blue and white"
        ),
        gr.Radio(["256x256", "512x512", "1024x1024"], label="Dimensions", value="1024x1024")
    ],
    outputs=[
        gr.Gallery(label="Generated Logos"),  # Gallery for displaying the generated logos
        gr.File(label="Download All Logos")  # Allow download of the logos
    ],
    title="Enhanced AI Logo Builder",
    description=(
        "Generate unique logos by describing your vision. Choose from various styles, color schemes, "
        "and dimensions. Outputs include a gallery for preview and downloadable logos."
    ),
    theme="default",
    allow_flagging="never"
)

if __name__ == "__main__":
    interface.launch()
