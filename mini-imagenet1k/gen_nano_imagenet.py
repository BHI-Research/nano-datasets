"""
Script to create mini datasets based from imagenetmini dataset. Usage:

python main.py --help

Parameters:
--n : Number of images for each class.
--src : Source of imagenetmini dataset.
--dest : Destination of new dataset.
--class_fp : Path of file that asociates classe with folder names.

Imagenetmini must be download from:
https://www.kaggle.com/datasets/ifigotin/imagenetmini-1000
"""

import os
import shutil
import random
import argparse

def copy_random_files(source_directory, destination_directory, n):
    for dir_path, _, files in os.walk(source_directory):
        if not files:
            continue
        
        # Select N random files
        selected_files = random.sample(files, min(n, len(files)))
        
        # Create the destination directory path
        destination_path = os.path.join(destination_directory, os.path.basename(dir_path))
        os.makedirs(destination_path, exist_ok=True)

        # Copy the selected files to the destination directory
        for file in selected_files:
            source_file_path = os.path.join(dir_path, file)
            destination_file_path = os.path.join(destination_path, file)
            shutil.copy2(source_file_path, destination_file_path)
            print(f'Copied: {source_file_path} -> {destination_file_path}')

def convert_class_associated_file_to_dict(class_associated_filepath):
    classes = {}

    with open(class_associated_filepath) as file:
        lines = file.readlines()

    for line in lines:
        line = line[:-1]  # Remove \n
        line = line.split("\t")
        classes[line[0]] = line[1]

    return classes

def generate_class_files(destination_directory, destination_file, class_associated_filepath):
    if class_associated_filepath is not None:
        classes = convert_class_associated_file_to_dict(class_associated_filepath)

    for dir_path, _, files in os.walk(destination_directory):
        if not files:
            continue

        folder = os.path.basename(dir_path)
        # Get folder name (class associated)

        for file in files:
            _, file_ext = os.path.splitext(file)
            # Get file extension

            if file_ext.lower() in [".jpeg", ".png", ".gif"]:
                # Image file extension

                if class_associated_filepath is not None:
                    line = f"{os.path.join(dir_path, file)} {classes[folder]}\n"
                else:
                    line = f"{os.path.join(dir_path, file)} {folder}\n"
                # Use file with classes if exists
                # Otherwise uses folders name

                destination_file.write(line)

# Usage example
destination_directory = "./imagenetmini/images/"
class_associated_filepath = None
dest_filepath = os.path.join(destination_directory, "imagenetmini-classes.txt")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy random files and generate class files.')
    parser.add_argument('--src', type=str, help='Source directory to copy files from', required=True)
    parser.add_argument('--dest', type=str, help='Destination directory to copy files to', required=False)
    parser.add_argument('--n', type=int, help='Number of files to copy per folder', required=True)
    parser.add_argument('--class_fp', type=str, help='Path to the class associated file', required=False)

    args = parser.parse_args()

    if args.dest:
        dest_filepath = os.path.join(args.dest, "imagenetmini-classes.txt")

    if args.src:
        source_directory = args.src

    if args.class_fp:
        class_associated_filepath = args.class_fp

    copy_random_files(source_directory, destination_directory, args.n)

    with open(dest_filepath, 'w') as dest_file:
        generate_class_files(destination_directory, dest_file, class_associated_filepath)