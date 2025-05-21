# This program creates a nano-dataset with a set number of videos per class.
# For this, it uses a CSV file of an original dataset to download the videos using their IDs.

from yt_dlp import YoutubeDL
from moviepy.video.io.VideoFileClip import VideoFileClip
import csv
import pandas as pd
import os
import argparse
import json

"""
Create or update a .csv file with the video paths and their corresponding labels.

Args:
    path (str): Path to the specific video.
    label (str): Specific label for the video.
    labels (dict): Dictionary containing all the labels.
    csv_path (str): Path where the CSV file will be saved.
"""


def save_video_paths(path, label, labels, csv_path):
    directory = os.path.dirname(csv_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    new_data = {
        'Video Path': [path],
        'class': [labels[label]]
    }
    new_df = pd.DataFrame(new_data)

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path, sep=' ', header=None, names=['Video Path', 'class'])
        df_updated = pd.concat([df_existing, new_df]).drop_duplicates(subset=['Video Path', 'class'],
                                                                      keep='first').reset_index(drop=True)
    else:
        df_updated = new_df

    df_updated.to_csv(csv_path, sep=' ', header=False, index=False)


"""
    Creates or updates a JSON file with the provided checkpoint data.

    Args:
    checkpoint_data (dict): Dictionary containing the checkpoint data to be saved.
    path (str): Path where the JSON file will be saved.
"""


def checkpoint_creator(checkpoint_data, path):
    with open(path, 'w') as file:
        json.dump(checkpoint_data, file, indent=4)


"""
    Reads and returns the checkpoint data from a JSON file.

    Args:
    path (str): Path of the JSON file to be read.

    Returns:
    dict: Dictionary containing the checkpoint data if the file exists.
    None: If the file does not exist.
"""


def checkpoint_reader(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r') as file:
        data = json.load(file)
    return data


"""
    Reads a CSV file and creates a dictionary mapping unique labels to indices.

    Args:
    csv_name (str): Path of the CSV file to be read.

    Returns:
    dict: Dictionary where keys are unique labels from the CSV and values are their corresponding indices.
"""


def get_dictionary(csv_name):
    labels = {}
    with open(csv_name, mode='r', newline='') as file:
        reader = csv.reader(file)
        index_label = 0
        for row in reader:
            label = row[0]
            if label not in labels:
                labels[label] = index_label
                index_label += 1
    return labels


"""
    Downloads a YouTube video and extracts a subclip.

     Args:
    url (str): Video URL.
    start_time (int): Start time of the subclip in seconds.
    end_time (int): End time of the subclip in seconds.
    output_path (str): Path where the video will be saved.
"""


def download_youtube_video(url, start_time, end_time, output_path, cookies=None):
    video_path = None
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
    }
    if cookies is not None:
        ydl_opts['cookies'] = cookies
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)

        with VideoFileClip(video_path) as video:
            video_duration = video.duration
            if end_time > video_duration:
                print(
                    f"Error: El tiempo de fin {end_time} excede la duración del video ({video_duration}). Omitiendo video.")
                return None

            output_path = output_path.replace(" ", "-")
            video_r = video.subclip(start_time, end_time)
            video_r.write_videofile(output_path, codec="libx264")
            print(f"Video downloaded and saved in: {output_path}")
            return output_path
    except Exception as e:
        print(f"Error downloading video from {url}: {e}")
        return None
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)


'''
    Check if a video was downloaded

    Args:
        output_path_base (str): root path
        final_label (str): video path
        count (int): number of video

    Returns: 
        True or False
'''


def is_video_downloaded(output_path_base, final_label, count):
    output_path = os.path.join(output_path_base, f"{final_label}_{count}.mp4")
    return os.path.exists(output_path)


"""
    Creates a nano-dataset by downloading a specified number of videos per class.

    Args:
    csv_name (str): CSV file from which the video IDs are obtained.
    n_videos (int): Amount of videos per class.
    n_class (int): Amount of classes
    directory_path (str): Path where the dataset will be created.
    new_csv_name (str): Name of the output nano CSV file.
"""


def dataset_creator(csv_name, n_videos, n_class, directory_path, new_csv_name, cookies=None):
    base_url = "https://www.youtube.com/watch?v="
    root = os.path.dirname(os.path.abspath(__file__))

    if directory_path == '':
        output_path_base = os.path.join(root, 'downloads')
    elif root not in directory_path:
        output_path_base = os.path.join(root, directory_path)
    else:
        output_path_base = directory_path

    if not os.path.exists(output_path_base):
        os.makedirs(output_path_base)

    checkpoint_path = os.path.join(output_path_base, 'checkpoint.json')
    checkpoint_data = checkpoint_reader(checkpoint_path)

    if checkpoint_data is None:
        checkpoint_data = {
            'current_label': None,
            'count': 0,
            'video_id': None
        }

    labels = get_dictionary(csv_name)
    label_keys = list(labels.keys())

    if n_class is not None:
        label_keys = label_keys[:n_class]

    current_label = checkpoint_data['current_label']
    if current_label is None:
        current_label = label_keys[0]

    count = checkpoint_data['count']
    video_id = checkpoint_data['video_id']

    with open(csv_name, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

        while True:
            for row in rows:
                try:
                    label, current_video_id, start, end = row[0], row[1], int(row[2]), int(row[3])
                except ValueError as ve:
                    print(f"Invalid time format in CSV for row: {row}. Skipping...")
                    continue

                if current_label != label:
                    continue

                if video_id and current_video_id != video_id:
                    continue

                if is_video_downloaded(output_path_base, label.replace(" ", "-"), count):
                    count += 1
                    continue

                if count >= n_videos:
                    count = 0
                    next_label_index = label_keys.index(current_label) + 1
                    if next_label_index >= len(label_keys):
                        os.remove(checkpoint_path)
                        print("Dataset download complete.")
                        return
                    current_label = label_keys[next_label_index]
                    checkpoint_data = {
                        'current_label': current_label,
                        'count': count,
                        'video_id': None
                    }
                    checkpoint_creator(checkpoint_data, checkpoint_path)
                    break

                final_label = label.replace(" ", "-")
                video_url = base_url + current_video_id
                output_path = os.path.join(output_path_base, f"{final_label}_{count}.mp4")
                try:
                    checkpoint_data = {
                        'current_label': current_label,
                        'count': count,
                        'video_id': current_video_id
                    }
                    checkpoint_creator(checkpoint_data, checkpoint_path)

                    video_downloaded = download_youtube_video(video_url, start, end, output_path, cookies=cookies)

                    if video_downloaded:
                        csv_path = os.path.join(output_path_base, new_csv_name)
                        save_video_paths(output_path, label, labels, csv_path)
                        count += 1
                        video_id = None
                    else:
                        print(f"Retrying video for class {current_label}...")
                        continue

                except Exception as e:
                    print(f"Error downloading video: {e}")
                    continue

            if count < n_videos:
                print(f"Not enough videos for class {current_label}. Retrying...")
            else:
                video_id = None
                current_label = label_keys[label_keys.index(current_label) + 1]
                count = 0
                checkpoint_creator(checkpoint_data, checkpoint_path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate a nano-dataset from the selected dataset.')
    parser.add_argument('--save_dir', type=str, help='Directory where the nano-dataset will be saved', required=False)
    parser.add_argument('--dataset', type=str, choices=['k400', 'k600', 'k700'],
                        help='Dataset to select videos from (k400 | k600 | k700)', required=False)
    parser.add_argument('--video_type', type=str, choices=['train', 'val'],
                        help='Type of videos to include (train | val)', required=False)
    parser.add_argument('--num_classes', type=int, help='Number of classes to include in the nano-dataset',
                        required=False)
    parser.add_argument('--videos_per_class', type=int, help='Number of videos to include per class', required=False)
    parser.add_argument('--cookies', type=str, help='Ruta al archivo de cookies para yt-dlp', required=False)

    args = parser.parse_args()

    try:
        directory_path = args.save_dir
        dataset_s     = args.dataset
        video_type    = args.video_type
        n_classes     = args.num_classes       if args.num_classes       is not None else 1000
        n_videos      = args.videos_per_class  if args.videos_per_class  is not None else 1000
        cookies       = args.cookies

        if directory_path != '' and not os.path.exists(directory_path):
            os.makedirs(directory_path)

        new_csv_name = f'nano-{video_type}.csv'

        # === FIX: resolver ruta del CSV relativa a donde está este script ===
        import os
        script_dir    = os.path.dirname(os.path.abspath(__file__))
        directory_csv = os.path.join(script_dir, dataset_s, f"{video_type}.csv")

        dataset_creator(
            directory_csv,
            n_videos,
            n_classes,
            directory_path,
            new_csv_name,
            cookies=cookies
        )

    except AttributeError:
        print("Wrong data type.")
    except Exception as e:
        print(f'An error has occurred: {e}')
