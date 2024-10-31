
import glob
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

####################
# Code by Debugverse
# https://www.youtube.com/@DebugVerseTutorials
####################

load_dotenv()


API_KEY = os.getenv("GENAI_API_KEY")

genai.configure(api_key=API_KEY)

instruction = "You are shown an image. your job is to respond with a json object describing the image with two words. you must only use the keys: image1, image2. for example {\"image1\": \"cute\", \"image2\": \"cat\"} do not use articles or dots, only simple words"


model = genai.GenerativeModel("gemini-1.5-flash")


def run(image_name):
    # main program logic
    try:
        imgfile = genai.upload_file(image_file)
        result = model.generate_content(
            [imgfile, "\n\n", instruction]
        )

        image_description = json.loads(result.text)
        new_filename = f"{image_description["image1"]}_{
            image_description["image2"]}.jpg"

        os.rename(image_name, new_filename)
        print(f"File renamed to: {new_filename}")

    except json.JSONDecodeError as e:
        print(f"error decoding JSON: {e}")
    except KeyError as e:
        print(f"Missing key in JSON: {e}")
    except OSError as e:
        print(f"Error renaming file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


image_extensions = ("*.jpg", "*.jpeg", "*.png")
image_files = []

for extension in image_extensions:
    image_files.extend(glob.glob(extension))

print(f"Found {len(image_files)} image files.")


for image_file in image_files:
    run(image_file)
