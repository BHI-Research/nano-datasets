import os
import shutil
import random
import argparse
import csv

def copy_random_files(source_directory, destination_directory, n, class_count, random_class_selection=False):
    all_classes = [d for d in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, d))]
    
    if random_class_selection:
        selected_classes = random.sample(all_classes, min(class_count, len(all_classes)))
    else:
        selected_classes = all_classes[:class_count]

    image_paths_csv = os.path.join(destination_directory, "image_paths.csv")
    class_mapping_csv = os.path.join(destination_directory, "class_mapping.csv")

    with open(image_paths_csv, 'w', newline='') as img_csv, open(class_mapping_csv, 'w', newline='') as class_csv:
        img_writer = csv.writer(img_csv)
        class_writer = csv.writer(class_csv)

        img_writer.writerow(["Image Path", "Class"])
        class_writer.writerow(["Class ID", "Class Name"])

        for class_id, class_name in enumerate(selected_classes):
            class_path = os.path.join(source_directory, class_name)
            destination_path = os.path.join(destination_directory, class_name)
            os.makedirs(destination_path, exist_ok=True)

            files = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
            selected_files = random.sample(files, min(n, len(files)) if n else len(files))

            class_writer.writerow([class_id, class_name])

            for file in selected_files:
                source_file_path = os.path.join(class_path, file)
                destination_file_path = os.path.join(destination_path, file)
                shutil.copy2(source_file_path, destination_file_path)
                img_writer.writerow([destination_file_path, class_name])

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy random files and generate class files.')
    
    parser.add_argument('--src', type=str, help='Source directory with train or val images', required=True)
    parser.add_argument('--dest', type=str, help='Destination directory to save the generated classes', required=True)
    parser.add_argument('--classes', type=int, help='Number of classes to select', required=True)
    parser.add_argument('--images', type=int, help='Number of images to copy per class', required=False)
    parser.add_argument('--randomly', type=str, choices=['S', 'N'], default='N', help='Randomly select classes (S/N)', required=False)

    args = parser.parse_args()

    source_directory = args.src
    destination_directory = args.dest
    class_count = args.classes
    image_count = args.images
    random_class_selection = (args.randomly == 'S')

    if args.class_associations:
        class_associated_filepath = args.class_associations
    else:
        class_associated_filepath = None

    copy_random_files(source_directory, destination_directory, image_count, class_count, random_class_selection)
