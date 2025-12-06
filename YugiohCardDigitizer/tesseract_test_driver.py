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
from preprossing import process_yugioh_card

# defines the directory to search for images in
images_dir = "samples"  # represents the directory containing the images to scan

# defines a function that loops through all images in the scan directory and attempt to extra card data from them
def main():
    for file in os.listdir(images_dir):
        image_filepath = os.path.join(images_dir, file)     # defines the full filepath to the image
        result = process_yugioh_card(image_filepath)
        print(result)
        # processed_image = preprocess_image(image_filepath)  # prepare the image for tesseract and store
        #
        # text = extract_text(processed_image)                # extract all text from the card
        # card = extract_card_info(text)  # use the extracted text to create a card
        # # image = Image.open(image_filepath)
        # # text = extract_text(image)
        # # card = extract_card_info(text)
        #
        # processed_image.save("tesseractImage.png") # to save the processed image to debug what tesseract sees
        #
        # # print the results
        # print("===Extracted Text===")
        # print(text)
        # print("===Image Information===")
        # print(card.name, card.attack, card.defense)
        # print(card.description)
        # print()

if __name__ == "__main__":
    main()
