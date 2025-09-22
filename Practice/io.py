import os
import shutil
from pathlib import Path

path = "C:/Users/bstea/OneDrive/Desktop/secret.txt"
path2 = "C:/Users/bstea/OneDrive/Desktop/SecretStuff"
path3 = "C:/Users/bstea/OneDrive/Desktop/SecretStuff2"
with open(path, 'w') as file:
    file.write("Hello Ben")

if not os.path.exists(path2):
    os.mkdir(path2)
if not os.path.exists(path3):
    os.mkdir(path3)

if not os.path.exists(path2 + "/secret.txt"):
    shutil.move(path,"C:/Users/bstea/OneDrive/Desktop/SecretStuff")

# Loop through every item in the source folder
for file_name in os.listdir(path2):
    src = os.path.join(path2, file_name)
    dst = os.path.join(path3, file_name)

    # Copy only files (skip directories)
    if os.path.isfile(src):
        shutil.copy(src, dst)

# define a function that copies all files in a directory to another
def Copy_Files(src: str, dest: str):
    # cast to Path object
    src = Path(src)
    dst = Path(dest)

    # check directory exists
    if not src.exists():
        raise FileNotFoundError("Directory not found")

    # create destination and all necessary parent folders. Dont raise exception if already exists
    dst.mkdir(parents=True,exist_ok=True)

    # loop through src directory's files
    for file in src.rglob("*"):
        # remove the parent "fluff" from the destination path
        dstFilePath = dst / file.relative_to(src)
        # if file is a directory, make it in the destination
        if file.is_dir():
            dstFilePath.mkdir(parents=True,exist_ok=True)
        else:
            if dstFilePath.exists():
                print(f"WARNING. About to overwrite{file.name}")
            shutil.copy(file,dstFilePath)
