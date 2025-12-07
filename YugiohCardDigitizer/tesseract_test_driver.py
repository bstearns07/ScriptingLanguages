######################################################################################################################
# Project...............: Yugioh Card Library
# Author................: Ben Stearns
# Date..................: 12-4-25
# Project Description...: This application creates a digital database library for storing and managing Yugioh cards
# File Description......: defines a function to run the tesseract program on all image files in the samples directory
#######################################################################################################################
# REQUIRED: Download tesseract here => https://github.com/UB-Mannheim/tesseract/wiki

# imports
import os
from tesseract import process_yugioh_card

# defines the directory to search for images in
images_dir = "samples"  # represents the directory containing the images to scan

# defines a function that loops through all images in the scan directory and attempt to extra card data from them
def main():
    for file in os.listdir(images_dir):
        image_filepath = os.path.join(images_dir, file)     # defines the full filepath to the image
        result = process_yugioh_card(image_filepath)
        print(result)

if __name__ == "__main__":
    main()
