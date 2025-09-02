from PIL import Image, ImageEnhance, ImageFilter
import os

path = "images"
pathOut = "editedImages"

for filename in os.listdir(path):
    img = Image.open(f"{path}/{filename}")
    editedImg = img.filter(ImageFilter.SHARPEN)
    newName = os.path.splitext(filename)[0]
    editedImg.save(f"{pathOut}/{newName}_edited.png")