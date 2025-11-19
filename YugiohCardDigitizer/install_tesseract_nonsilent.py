import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import requests

TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"    # represents the location to download tesseract
INSTALLER_PATH = Path("tesseract_installer.exe")                    # represents the path to run the tesseract installer

# represents the url for downloading the tesseract installer
INSTALLER_URL = "https://github.com/tesseract-ocr/tesseract/releases/download/5.5.1/tesseract-ocr-w64-setup-5.5.1.XXXX.exe"

def install_tesseract():
    """Download and install Tesseract with progress reporting."""
    print("⚠️  Tesseract not found. Attempting to install...")

    try:
        # --- DOWNLOAD WITH PROGRESS ---
        print("⬇ Downloading Tesseract installer...")
        response = requests.get(INSTALLER_URL, stream=True, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 8192

        with open(INSTALLER_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"   Download progress: {percent:5.1f}% ({downloaded // 1024} KB)", end="\r")

        print("\n✅ Download complete. Installing...")

        # --- INSTALL WITH PERIODIC STATUS ---
        print("⚙ Running installer... this can take a minute.")

        process = subprocess.Popen(
            [str(INSTALLER_PATH), "/SILENT", "/LOG=install_log.txt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Polling loop
        while True:
            ret = process.poll()
            if ret is not None:
                break

            print("   ⏳ Still installing...", end="\r")
            time.sleep(2)

        if process.returncode != 0:
            raise RuntimeError("Installer returned an error code.")

        print("✅ Installation finished.")

        # Add to PATH
        tesseract_dir = os.path.dirname(TESSERACT_EXE)
        os.environ["PATH"] += os.pathsep + tesseract_dir

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