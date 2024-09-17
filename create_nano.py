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
    Crea o actualiza un archivo .csv con las rutas de los videos y sus etiquetas correspondientes.

    Args:
    path (str): Ruta del video específico.
    label (str): Etiqueta específica del video.
    labels (dict): Diccionario que contiene todas las etiquetas.
    csv_path (str): Ruta donde se guardará el archivo CSV.
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
        df_updated = pd.concat([df_existing, new_df]).drop_duplicates(subset=['Video Path', 'class'], keep='first').reset_index(drop=True)
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

def download_youtube_video(url, start_time, end_time, output_path):
    video_path = None
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)

        # Verifica la duración del video antes de extraer el subclip
        with VideoFileClip(video_path) as video:
            video_duration = video.duration
            if end_time > video_duration:
                print(f"Error: El tiempo de fin {end_time} excede la duración del video ({video_duration}). Omitiendo video.")
                return None

            output_path = output_path.replace(" ", "-")
            video_recortado = video.subclip(start_time, end_time)
            video_recortado.write_videofile(output_path, codec="libx264")
            print(f"Video downloaded and saved in: {output_path}")
            return output_path
    except Exception as e:
        print(f"Error downloading video from {url}: {e}")
        return None
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)


def is_video_downloaded(output_path_base, final_label, count):
    output_path = os.path.join(output_path_base, f"{final_label}_{count}.mp4")
    return os.path.exists(output_path)


"""
    Creates a nano-dataset by downloading a specified number of videos per class.

    Args:
    csv_name (str): CSV file from which the video IDs are obtained.
    n_videos (int): Number of videos per class.
    directory_path (str): Path where the dataset will be created.
    new_csv_name (str): Name of the output nano CSV file.
"""
def dataset_creator(csv_name, n_videos, directory_path, new_csv_name):
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
                    if next_label_index >= len(labels):
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

                    video_downloaded = download_youtube_video(video_url, start, end, output_path)

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
    parser = argparse.ArgumentParser(description='Copy random files and generate class files.')
    parser.add_argument('--src', type=str, help='Source file where to take video names', required=False)
    parser.add_argument('--dest', type=str, help='Destination directory to download files to', required=False)
    parser.add_argument('--n', type=int, help='Number of files to download per class', required=False)

    args = parser.parse_args()

    try:
        csv_name = ''
        if args.dest is None:
            directory_path = input("Directory where you want to save the videos (if you want to use this same directory press enter): ")
            csv_name = input("Name of .csv file: ")
        else:
            directory_path = args.dest

        if args.src != None:
            csv_name = args.src

        if not args.n:
            n_fragments = int(input("Number of videos per class: "))
        else:
            n_fragments = args.n

        if directory_path != '' and not os.path.exists(directory_path):
            os.makedirs(directory_path)

        new_csv_name = f'nano-{csv_name}'
        dataset_creator(csv_name, n_fragments, directory_path, new_csv_name)

    except AttributeError:
        print("Wrong data type.")
    except Exception as e:
        print(f'An error has occurred: {e}')
