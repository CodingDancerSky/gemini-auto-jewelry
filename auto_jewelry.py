def get_rgb_from_hexadecimal(color_rgb):
	if color_rgb[0] == '#':
		r = int(color_rgb[1:3], 16)
		g = int(color_rgb[3:5], 16)
		b = int(color_rgb[5:7], 16)
		return r, g, b
	else:
		r = int(color_rgb[0:2], 16)
		g = int(color_rgb[2:4], 16)
		b = int(color_rgb[4:6], 16)
		return r, g, b

### Show a dialog for inputing image
from tkinter.filedialog import askopenfilename

input_image_path = askopenfilename()
# print("Input image file: ", input_image_path)

jewelry_type = input('What is the type of jewelry you are looking for with this stone (ring, earring, necklace, bracelet or others)?\n') 

### Sumary of input
import google.generativeai as genai
import pathlib
import os
import time

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# identify stone from image
image_to_text_prompt = "Name of the jewelry stone in the picture in the least number of words (remove unnecessary symbols such as comma)."
image1 = {
    'mime_type': 'image/jpeg',
    'data': pathlib.Path(input_image_path).read_bytes()
}
stone_name_response = model.generate_content([image_to_text_prompt, image1])
stone_name = stone_name_response.text
print("Jewelry stone name is: ", stone_name)

stone_culture_prompt = f"Description the history and symbolic meaning of {stone_name} in one sentence."
stone_culture_response = model.generate_content(stone_culture_prompt)
stone_culture = stone_culture_response.text
print(stone_culture)

stone_poetry_prompt = f"descibe the jewelry stone {stone_name} in a short poetry"
stone_poetry_response = model.generate_content(stone_poetry_prompt)
stone_poetry = stone_poetry_response.text
print(f"Poetry of the stone {stone_name}: \n{stone_poetry}\n")

# get color of the stone
stone_color_prompt = f"What is the main color of the stone {stone_name} in two words?"
stone_color_response = model.generate_content(stone_color_prompt)
stone_color = stone_color_response.text
stone_color_rgb_prompt = f"What is the rgb of color {stone_color} into hexadecimal format, pick any one and return just one result"
stone_color_rgb_response = model.generate_content(stone_color_rgb_prompt)
stone_color_rgb = stone_color_rgb_response.text
r, g, b = get_rgb_from_hexadecimal(stone_color_rgb)
print(f"Color of the country is: {stone_color} {stone_color_rgb} ({r},{g},{b})\n")

### Generate image
from vertexai.preview.vision_models import ImageGenerationModel

image_prompt = f"please show a product image of {jewelry_type} jewelry build with the stone {stone_name} on a female model with face (jewelry in center of the picture)."
# print("Image prompt: ", image_prompt)

model = ImageGenerationModel.from_pretrained("imagegeneration@006")
images = model.generate_images(
	prompt=image_prompt,
    number_of_images=1,
    aspect_ratio= "4:3",
	)

images[0].save(location="./gen-img.png", include_generation_parameters=True)

### Add Text Font onto the Image and Display
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

image = Image.open('./gen-img.png')
image = image.resize((1200, 900), Image.BICUBIC)
image_draw = ImageDraw.Draw(image)
title_text_font = ImageFont.truetype(font='./font/RousseauDeco.ttf', size=130)
image_draw.text(
	xy = (50, 100),
	text = stone_name,
	align = 'left',
	font = title_text_font,
	fill = (r, g, b)
	)
desciption_text_font = ImageFont.truetype(font='./font/Roboto-Regular.ttf', size=30)
image_draw.text(
	xy = (57, 220),
	text = stone_poetry,
	align = 'left',
	font = desciption_text_font,
	fill = (255, 255, 255)
	)

watermark_text_font_1 = ImageFont.truetype(font='./font/Roboto-Regular.ttf', size=20)
image_draw.text(
	xy = (850, 850),
	text = "made by ",
	align = 'left',
	font = watermark_text_font_1,
	fill = (200, 200, 200)
	)
watermark_text_font_2 = ImageFont.truetype(font='./font/Roboto-Regular.ttf', size=32)
image_draw.text(
	xy = (935, 837),
	text = "Xiangzhu Long",
	align = 'left',
	font = watermark_text_font_2,
	fill = (200, 200, 200)
	)
timestampe = round(time.time() * 1000);
image.save(f"{stone_name}_jewelry_{timestampe}.png")
os.remove("./gen-img.png")
image.show()
