# oraganizes files

import os
import shutil
def organize_files(directory):
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documents': ['.pdf', '.docx', '.txt', '.pptx', '.xlsx'],
        'Audio': ['.mp3', '.wav', '.aac', '.flac'],
        'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
        'Archives': ['.zip', '.tar', '.rar', '.gz'],
        'Others': []
    }
    for folder in file_types.keys():
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            continue
        moved = False
        for folder, extensions in file_types.items():
            if any(filename.endswith(ext) for ext in extensions):
                shutil.move(file_path, os.path.join(directory, folder,
                filename))
                moved = True
                break
        if not moved:
            shutil.move(file_path, os.path.join(directory, 'Others',
            filename))
if __name__ == "__main__":
    # Replace 'your_directory_path' with the actual path to the directory you want to organize
    organize_files('test')
