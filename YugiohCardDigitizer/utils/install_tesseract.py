######################################################################################################################
# Project...............: Yugioh Card Library
# Author................: Ben Stearns
# Date..................: 12-4-25
# Project Description...: This application creates a digital database library for storing and managing Yugioh cards
# File Description......: checks to see if tesseract is installed. If not, it downloads it and adds to PATH non-silently
#######################################################################################################################
import ctypes
import os                   # for checking whether tesseract.exe already exists on the host system
import shutil               # for checking if tesseract exists in the system PATH
import subprocess           # used to run the tesseract installer as a process
import sys                  # used for exiting the program if the installation fails
import time                 # for animating the "still installing" spinner
from pathlib import Path    # to allow object-oriented file management

# define script variables for representing the path to the installer and download location for tesseract.exe
TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"    # represents the location to download tesseract
INSTALLER_PATH = Path("tesseract-installer.exe") # represents the path to run the tesseract installer

def ensure_tesseract():
    # check if tesseract is already in PATH. If found, return the absolute path the executable for printing
    if shutil.which("tesseract"): # searches system PATH
        print("✔ Tesseract found in PATH.")
        return shutil.which("tesseract")
    # check that tesseract exists at the expected installation location. If so, returns it's filepath
    elif os.path.exists(TESSERACT_EXE):
        print("✔ Tesseract found at default location.")
        return TESSERACT_EXE
    # if tesseract is not found, attempt to install it and store if it was successful
    else:
        return None
