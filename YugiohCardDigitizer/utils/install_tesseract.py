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

def require_admin():
    """Re-launch the script with admin privileges if not already elevated."""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        # Relaunch with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join(sys.argv),
            None,
            1
        )
        sys.exit()  # Exit original (non-admin) process

# defines a function to install the tesseract program if it isn't found on the host system
def install_tesseract():
    print("Tesseract not found. Attempting to install from local installer...")

    # define a safety statement that returns false that the installer file isn't present just in case
    if not INSTALLER_PATH.exists():
        print(f" Installer not found: {INSTALLER_PATH}")
        return False

    # attempt to run the installer to install tesseract
    try:
        print("⚙ Running installer... Please wait.\n")

        # Launch installer non-blocking, send log info to a file, and silence terminal output
        process = subprocess.Popen(
            [
                str(INSTALLER_PATH),
                "/VERYSILENT",
                "/SUPPRESSMSGBOXES",
                "/NORESTART",
                "/LOG=install_log.txt"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Spinner indicator for simulating the process is still running
        spinner = ["⠙","⠸","⠼","⠴","⠦","⠇"] # the frames of the spinner
        i = 0 # for tracking which frame the spinner is one
        print("   Installing Tesseract...\n")

        # define a loop that runs as long as the installer is still running that prints the spinner
        while process.poll() is None:
            print(f"   {spinner[i % len(spinner)]} Still installing...", end="\r") # cycles through spinner list
            i += 1 # increment to next frame of spinner
            time.sleep(0.15) # pause a little between iterations for smooth animation

        # Once the process is done, check if it returned an error code. If so, display an error occurred. Return false
        if process.returncode != 0:
            print("\n Installer exited with an error.")
            return False

        # otherwise display the installer finished successfully
        print("\n✅ Installer completed successfully.")

        # Add Tesseract to PATH by appending it's folder to environment variable
        tesseract_dir = os.path.dirname(TESSERACT_EXE)
        subprocess.run(
            f'setx PATH "%PATH%;{tesseract_dir}"',
            shell=True, # allows running the Windows setx command
            check=False # prevents throwing errors even if PATH was already updated
        )

        # display tesseract was successfully added to PATH
        print("✅ Added Tesseract to PATH.")
        return True

    # catch all other exception that may occur and return false
    except Exception as e:
        print(f"Failed to install Tesseract: {e}")
        return False

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
        success = install_tesseract()

        # if the installation was successful and tesseract is at the expected location, print success and return path
        if success and os.path.exists(TESSERACT_EXE):
            print("🎉 Tesseract successfully installed!")
            return TESSERACT_EXE
        # if installation was not successful, print the failure and return nothing
        else:
            print("  Could not find or install Tesseract. Please install manually:")
            print("   https://github.com/UB-Mannheim/tesseract/wiki")
            return None

# driver that runs the script if ran directly
if __name__ == "__main__":
    # auto-elevate to admin before anything else
    #require_admin()

    # check if tesseract is already on the host system, install if needed, and return it's filepath
    path = ensure_tesseract()

    # if the filepath returned successfully, print its path. Otherwise, exit the program
    if path:
        print(f"Tesseract available at: {path}")
    else:
        sys.exit(1)