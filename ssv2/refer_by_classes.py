"""
This script creates a new csv file, with N number of video listed,
for each class of ssv2 available classes.
"""

import json
import os.path
import argparse

SSV2_SEPARATOR = ";"
OWN_CSV_SEPARATOR = " "

def create_class_sorted_dict(test_results_file):
    """
    This function reads test results csv file, and sorts video by class.
    """
    sorted_by_class_dict = dict()

    with open(test_results_file, "r") as file_handle:
        for line in file_handle:
            line = line.rstrip("\n")
            line = line.split(SSV2_SEPARATOR)
            id = line[0]
            classname = line[1]

            if classname in sorted_by_class_dict.keys():
                sorted_by_class_dict[classname].append(id)
            else:
                sorted_by_class_dict[classname] = [id]

    return sorted_by_class_dict

def gen_csv_of_n_video_for_class(class_dict, n):
    """
    This function generates a csv from a dict, where each class has N videos.
    """
    csv_content = ""

    for key in class_dict.keys():
        videos = class_dict[key][:n]
        # N videos of class

        for video in videos:
            csv_content += f"{video}{SSV2_SEPARATOR}{key}\n"
    # Assign n video of class to new dict

    return csv_content

def convert_csv_to_model_file(csv_file, labels_file, videos_dest=None):
    labels_file = json.load(open(labels_file, "r"))

    new_csv_content = ""
    for line in csv_file.split("\n"):
        line = line.rstrip("\n")
        line = line.split(SSV2_SEPARATOR)
        try:
            id = line[0]
            classname = line[1]
        except:
            pass
            # last line \n

        if len(id) == 0:
            continue
            # cases of blank ids

        class_id = labels_file[classname]
        if videos_dest != None:
            new_line = f"{os.path.join(videos_dest, id)}.webm{OWN_CSV_SEPARATOR}{class_id}"
        else:
            new_line = f"{id}.webm{OWN_CSV_SEPARATOR}{class_id}"

        print(new_line)
        new_csv_content += new_line + "\n"
    return new_csv_content

def main():
    parser = argparse.ArgumentParser(description='Copy random files and generate class files.')
    parser.add_argument('--src', type=str, help='Source directory to get answers file from', required=True)
    parser.add_argument('--dest', type=str, help='Destination directory to create json file', required=False)
    parser.add_argument('--n', type=int, help='Number of videos to take from each class', required=True)
    parser.add_argument('--labels_src', type=str, help='Destination directory of labels file', required=True)
    parser.add_argument('--videos_src', type=str, help='Destination directory of videos', required=False)

    args = parser.parse_args()

    if args.src:
        test_results_file = args.src
    else:
        test_results_file = "test-answers.csv"

    if args.dest:
        dest_filepath = os.path.join(args.dest, "videos_sorted_by_class.json")
    else:
        dest_filepath = "videos_sorted_by_class.json"

    class_dict = create_class_sorted_dict(test_results_file)

    with open(dest_filepath, "w") as json_file:
        json.dump(class_dict, json_file, indent=4)
    # Save as JSON file

    if args.n:
        csv_content = gen_csv_of_n_video_for_class(class_dict, args.n)

    if args.labels_src:
        labels_file = args.labels_src
    else:
        labels_file = "labels.json"

    labels = json.load(open(labels_file, "r"))

    if args.videos_src:
        # If we have source video directory, we can convert csv file
        # to a useful model file, adding absolute directory for each video
        csv_content = convert_csv_to_model_file(csv_content, labels_file, args.videos_src)
    else:
        print("To create model dataset src file, use videos_src command argument to locate dataset videos.")

    # After, save csv file
    with open("class_dict.csv", "w") as csv_file:
        csv_content = convert_csv_to_model_file(csv_content, labels_file)
        csv_file.write(csv_content)

if __name__ == '__main__':
    main()
