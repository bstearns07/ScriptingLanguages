import os
import shutil

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