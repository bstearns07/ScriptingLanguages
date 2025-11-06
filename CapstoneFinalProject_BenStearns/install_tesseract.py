########################################################################################################################
# Title..............: Capstone Final Project - Ocular Recognition
# Author.............: Ben Stearns
# Date...............: 10-30-2025
# Purpose............: The purpose of this program is to:
#                       - Scan an image of a card
#                       - Extracts the text using OCR
# File Description...: checks to see if tesseract is installed. If not, it downloads it and adds to PATH
#######################################################################################################################

"""
tesseract_installer.py
----------------------------------
Checks if Tesseract OCR is installed on Windows.
If not, downloads and installs it automatically.
Prints an error message if installation fails.
"""

import os                   # to allow file management functionality
import shutil               # provides shell utilities for high-level file operations like copying, moving, removing
import subprocess           # python module for launching external commands/programs and interacting with them
import sys                  # so the script can exit with an error code using sys.exit()
import requests             # to perform a GET request to download the tesseract.exe file
from pathlib import Path    # to allow object-oriented management of filepaths

TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"    # represents the location to download tesseract
INSTALLER_PATH = Path("tesseract_installer.exe")                    # represents the path to run the tesseract installer

# represents the url for downloading the tesseract installer
INSTALLER_URL = "https://github.com/UB-Mannheim/tesseract/releases/latest/download/tesseract-ocr-w64-setup.exe"


def install_tesseract():
    """Download and install Tesseract silently on Windows."""
    print("⚠️  Tesseract not found. Attempting to install...")

    try:
        # Download installer
        print("⬇ Downloading Tesseract installer...")
        response = requests.get(INSTALLER_URL, stream=True, timeout=60)
        response.raise_for_status()

        with open(INSTALLER_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("✅ Download complete. Installing...")

        # Run silent installer
        subprocess.run(
            [str(INSTALLER_PATH), "/SILENT"],
            check=True
        )

        print("✅ Installation finished.")

        # Add to PATH for current session
        tesseract_dir = os.path.dirname(TESSERACT_EXE)
        os.environ["PATH"] += os.pathsep + tesseract_dir

        # Try adding permanently (non-fatal if fails)
        subprocess.run(
            f'setx PATH "%PATH%;{tesseract_dir}"',
            shell=True,
            check=False
        )

        print("✅ Added Tesseract to PATH.")
        return True

    except Exception as e:
        print(f"❌ Failed to install Tesseract: {e}")
        return False

    finally:
        # Clean up installer if it exists
        if INSTALLER_PATH.exists():
            INSTALLER_PATH.unlink(missing_ok=True)


def ensure_tesseract():
    """Ensure Tesseract is installed and return its path."""
    if shutil.which("tesseract"):
        print("✔ Tesseract found in PATH.")
        return shutil.which("tesseract")
    elif os.path.exists(TESSERACT_EXE):
        print("✔ Tesseract found at default location.")
        return TESSERACT_EXE
    else:
        success = install_tesseract()
        if success and os.path.exists(TESSERACT_EXE):
            print("🎉 Tesseract successfully installed!")
            return TESSERACT_EXE
        else:
            print("❌ Could not find or install Tesseract. Please install manually:")
            print("   https://github.com/UB-Mannheim/tesseract/wiki")
            return None


if __name__ == "__main__":
    path = ensure_tesseract()
    if path:
        print(f"Tesseract available at: {path}")
    else:
        sys.exit(1)
