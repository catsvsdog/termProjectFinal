from rembg import remove
from PIL import Image
from cmu_graphics import CMUImage
import os

def loadImage(inputPath, output_dir):
    result = []
    # loop through images in inputPath
    for i, item in enumerate(os.listdir(inputPath)):
        if item.lower().endswith(('.png', 'jpg', '.jpeg', '.gif', '.img')):
            image_path = os.path.join(inputPath, item)
            try:
                input_image = Image.open(image_path)
                print("loading image: ", item)
                output_image = remove(input_image)
                output_path = os.path.join(output_dir)
                base, ext = os.path.splitext(item)
                # replace .png extension
                new_file_name = base + '.png'
                new_file_path_name = output_path + new_file_name
                # save the image with new file extension to new location
                output_image.save(new_file_path_name)
                output_path = CMUImage((output_image))  #turn into cmu image
                print("output path: ", output_path)
                result.append(output_path)
                print(f"Save to : {output_path}")
            except Exception as e:
                print(f"Error process {item}: {e}")
    return result
