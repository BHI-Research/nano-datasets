# This program creates a nano-dataset with a set number of videos per class.
# For this, it uses a CSV file of an original dataset to download the videos using their IDs.

from yt_dlp import YoutubeDL #module to download videos
from moviepy.video.io.VideoFileClip import VideoFileClip
import csv
import pandas as pd
import os
import argparse
import json

 """
    Creates or updates a .csv file with video paths and their corresponding labels.

    Args:
    path (str): Path of the specific video.
    label (str): Specific label of the video.
    labels (dict): Dictionary containing all labels.
    csv_path (str): Path where the CSV will be saved.
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

        output_path = output_path.replace(" ", "-")
        with VideoFileClip(video_path) as video:
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
                label, current_video_id, start, end = row[0], row[1], int(row[2]), int(row[3])

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
            directory_path = input(
                "Directory where you want to save the videos (if you want to use this same directory press enter): ")
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy random files and generate class files.')
    parser.add_argument('--src', type=str, help='Source file where to take video names', required=False)
    parser.add_argument('--dest', type=str, help='Destination directory to download files to', required=False)
    parser.add_argument('--n', type=int, help='Number of files to download per class', required=False)

    args = parser.parse_args()

    try:
        csv_name = ''
        if args.dest is None:
            directory_path = input(
                "Directory where you want to save the videos (if you want to use this same directory press enter): ")
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

# 'abseiling': 0
#  'air drumming': 1
#  'answering questions': 2
#  'applauding': 3
#  'applying cream': 4
#  'archery': 5
#  'arm wrestling': 6
#  'arranging flowers': 7
#  'assembling computer': 8
#  'auctioning': 9
#  'baby waking up': 10
#  'baking cookies': 11
#  'balloon blowing': 12
#  'bandaging': 13
#  'barbequing': 14
#  'bartending': 15
#  'beatboxing': 16
#  'bee keeping': 17
#  'belly dancing': 18
#  'bench pressing': 19
#  'bending back': 20
#  'bending metal': 21
#  'biking through snow': 22
#  'blasting sand': 23
#  'blowing glass': 24
#  'blowing leaves': 25
#  'blowing nose': 26
#  'blowing out candles': 27
#  'bobsledding': 28
#  'bookbinding': 29
#  'bouncing on trampoline': 30
#  'bowling': 31
#  'braiding hair': 32
#  'breading or breadcrumbing': 33
#  'breakdancing': 34
#  'brush painting': 35
#  'brushing hair': 36
#  'brushing teeth': 37
#  'building cabinet': 38
#  'building shed': 39
#  'bungee jumping': 40
#  'busking': 41
#  'canoeing or kayaking': 42
#  'capoeira': 43
#  'carrying baby': 44
#  'cartwheeling': 45
#  'carving pumpkin': 46
#  'catching fish': 47
#  'catching or throwing baseball': 48
#  'catching or throwing frisbee': 49
#  'catching or throwing softball': 50
#  'celebrating': 51
#  'changing oil': 52
#  'changing wheel': 53
#  'checking tires': 54
#  'cheerleading': 55
#  'chopping wood': 56
#  'clapping': 57
#  'clay pottery making': 58
#  'clean and jerk': 59
#  'cleaning floor': 60
#  'cleaning gutters': 61
#  'cleaning pool': 62
#  'cleaning shoes': 63
#  'cleaning toilet': 64
#  'cleaning windows': 65
#  'climbing a rope': 66
#  'climbing ladder': 67
#  'climbing tree': 68
#  'contact juggling': 69
#  'cooking chicken': 70
#  'cooking egg': 71
#  'cooking on campfire': 72
#  'cooking sausages': 73
#  'counting money': 74
#  'country line dancing': 75
#  'cracking neck': 76
#  'crawling baby': 77
#  'crossing river': 78
#  'crying': 79
#  'curling hair': 80
#  'cutting nails': 81
#  'cutting pineapple': 82
#  'cutting watermelon': 83
#  'dancing ballet': 84
#  'dancing charleston': 85
#  'dancing gangnam style': 86
#  'dancing macarena': 87
#  'deadlifting': 88
#  'decorating the christmas tree': 89
#  'digging': 90
#  'dining': 91
#  'disc golfing': 92
#  'diving cliff': 93
#  'dodgeball': 94
#  'doing aerobics': 95
#  'doing laundry': 96
#  'doing nails': 97
#  'drawing': 98
#  'dribbling basketball': 99
#  'drinking': 100
#  'drinking beer': 101
#  'drinking shots': 102
#  'driving car': 103
#  'driving tractor': 104
#  'drop kicking': 105
#  'drumming fingers': 106
#  'dunking basketball': 107
#  'dying hair': 108
#  'eating burger': 109
#  'eating cake': 110
#  'eating carrots': 111
#  'eating chips': 112
#  'eating doughnuts': 113
#  'eating hotdog': 114
#  'eating ice cream': 115
#  'eating spaghetti': 116
#  'eating watermelon': 117
#  'egg hunting': 118
#  'exercising arm': 119
#  'exercising with an exercise ball': 120
#  'extinguishing fire': 121
#  'faceplanting': 122
#  'feeding birds': 123
#  'feeding fish': 124
#  'feeding goats': 125
#  'filling eyebrows': 126
#  'finger snapping': 127
#  'fixing hair': 128
#  'flipping pancake': 129
#  'flying kite': 130
#  'folding clothes': 131
#  'folding napkins': 132
#  'folding paper': 133
#  'front raises': 134
#  'frying vegetables': 135
#  'garbage collecting': 136
#  'gargling': 137
#  'getting a haircut': 138
#  'getting a tattoo': 139
#  'giving or receiving award': 140
#  'golf chipping': 141
#  'golf driving': 142
#  'golf putting': 143
#  'grinding meat': 144
#  'grooming dog': 145
#  'grooming horse': 146
#  'gymnastics tumbling': 147
#  'hammer throw': 148
#  'headbanging': 149
#  'headbutting': 150
#  'high jump': 151
#  'high kick': 152
#  'hitting baseball': 153
#  'hockey stop': 154
#  'holding snake': 155
#  'hopscotch': 156
#  'hoverboarding': 157
#  'hugging': 158
#  'hula hooping': 159
#  'hurdling': 160
#  'hurling (sport)': 161
#  'ice climbing': 162
#  'ice fishing': 163
#  'ice skating': 164
#  'ironing': 165
#  'javelin throw': 166
#  'jetskiing': 167
#  'jogging': 168
#  'juggling balls': 169
#  'juggling fire': 170
#  'juggling soccer ball': 171
#  'jumping into pool': 172
#  'jumpstyle dancing': 173
#  'kicking field goal': 174
#  'kicking soccer ball': 175
#  'kissing': 176
#  'kitesurfing': 177
#  'knitting': 178
#  'krumping': 179
#  'laughing': 180
#  'laying bricks': 181
#  'long jump': 182
#  'lunge': 183
#  'making a cake': 184
#  'making a sandwich': 185
#  'making bed': 186
#  'making jewelry': 187
#  'making pizza': 188
#  'making snowman': 189
#  'making sushi': 190
#  'making tea': 191
#  'marching': 192
#  'massaging back': 193
#  'massaging feet': 194
#  'massaging legs': 195
#  "massaging person's head": 196
#  'milking cow': 197
#  'mopping floor': 198
#  'motorcycling': 199
#  'moving furniture': 200
#  'mowing lawn': 201
#  'news anchoring': 202
#  'opening bottle': 203
#  'opening present': 204
#  'paragliding': 205
#  'parasailing': 206
#  'parkour': 207
#  'passing American football (in game)': 208
#  'passing American football (not in game)': 209
#  'peeling apples': 210
#  'peeling potatoes': 211
#  'petting animal (not cat)': 212
#  'petting cat': 213
#  'picking fruit': 214
#  'planting trees': 215
#  'plastering': 216
#  'playing accordion': 217
#  'playing badminton': 218
#  'playing bagpipes': 219
#  'playing basketball': 220
#  'playing bass guitar': 221
#  'playing cards': 222
#  'playing cello': 223
#  'playing chess': 224
#  'playing clarinet': 225
#  'playing controller': 226
#  'playing cricket': 227
#  'playing cymbals': 228
#  'playing didgeridoo': 229
#  'playing drums': 230
#  'playing flute': 231
#  'playing guitar': 232
#  'playing harmonica': 233
#  'playing harp': 234
#  'playing ice hockey': 235
#  'playing keyboard': 236
#  'playing kickball': 237
#  'playing monopoly': 238
#  'playing organ': 239
#  'playing paintball': 240
#  'playing piano': 241
#  'playing poker': 242
#  'playing recorder': 243
#  'playing saxophone': 244
#  'playing squash or racquetball': 245
#  'playing tennis': 246
#  'playing trombone': 247
#  'playing trumpet': 248
#  'playing ukulele': 249
#  'playing violin': 250
#  'playing volleyball': 251
#  'playing xylophone': 252
#  'pole vault': 253
#  'presenting weather forecast': 254
#  'pull ups': 255
#  'pumping fist': 256
#  'pumping gas': 257
#  'punching bag': 258
#  'punching person (boxing)': 259
#  'push up': 260
#  'pushing car': 261
#  'pushing cart': 262
#  'pushing wheelchair': 263
#  'reading book': 264
#  'reading newspaper': 265
#  'recording music': 266
#  'riding a bike': 267
#  'riding camel': 268
#  'riding elephant': 269
#  'riding mechanical bull': 270
#  'riding mountain bike': 271
#  'riding mule': 272
#  'riding or walking with horse': 273
#  'riding scooter': 274
#  'riding unicycle': 275
#  'ripping paper': 276
#  'robot dancing': 277
#  'rock climbing': 278
#  'rock scissors paper': 279
#  'roller skating': 280
#  'running on treadmill': 281
#  'sailing': 282
#  'salsa dancing': 283
#  'sanding floor': 284
#  'scrambling eggs': 285
#  'scuba diving': 286
#  'setting table': 287
#  'shaking hands': 288
#  'shaking head': 289
#  'sharpening knives': 290
#  'sharpening pencil': 291
#  'shaving head': 292
#  'shaving legs': 293
#  'shearing sheep': 294
#  'shining shoes': 295
#  'shooting basketball': 296
#  'shooting goal (soccer)': 297
#  'shot put': 298
#  'shoveling snow': 299
#  'shredding paper': 300
#  'shuffling cards': 301
#  'side kick': 302
#  'sign language interpreting': 303
#  'singing': 304
#  'situp': 305
#  'skateboarding': 306
#  'ski jumping': 307
#  'skiing (not slalom or crosscountry)': 308
#  'skiing crosscountry': 309
#  'skiing slalom': 310
#  'skipping rope': 311
#  'skydiving': 312
#  'slacklining': 313
#  'slapping': 314
#  'sled dog racing': 315
#  'smoking': 316
#  'smoking hookah': 317
#  'snatch weight lifting': 318
#  'sneezing': 319
#  'sniffing': 320
#  'snorkeling': 321
#  'snowboarding': 322
#  'snowkiting': 323
#  'snowmobiling': 324
#  'somersaulting': 325
#  'spinning poi': 326
#  'spray painting': 327
#  'spraying': 328
#  'springboard diving': 329
#  'squat': 330
#  'sticking tongue out': 331
#  'stomping grapes': 332
#  'stretching arm': 333
#  'stretching leg': 334
#  'strumming guitar': 335
#  'surfing crowd': 336
#  'surfing water': 337
#  'sweeping floor': 338
#  'swimming backstroke': 339
#  'swimming breast stroke': 340
#  'swimming butterfly stroke': 341
#  'swing dancing': 342
#  'swinging legs': 343
#  'swinging on something': 344
#  'sword fighting': 345
#  'tai chi': 346
#  'taking a shower': 347
#  'tango dancing': 348
#  'tap dancing': 349
#  'tapping guitar': 350
#  'tapping pen': 351
#  'tasting beer': 352
#  'tasting food': 353
#  'testifying': 354
#  'texting': 355
#  'throwing axe': 356
#  'throwing ball': 357
#  'throwing discus': 358
#  'tickling': 359
#  'tobogganing': 360
#  'tossing coin': 361
#  'tossing salad': 362
#  'training dog': 363
#  'trapezing': 364
#  'trimming or shaving beard': 365
#  'trimming trees': 366
#  'triple jump': 367
#  'tying bow tie': 368
#  'tying knot (not on a tie)': 369
#  'tying tie': 370
#  'unboxing': 371
#  'unloading truck': 372
#  'using computer': 373
#  'using remote controller (not gaming)': 374
#  'using segway': 375
#  'vault': 376
#  'waiting in line': 377
#  'walking the dog': 378
#  'washing dishes': 379
#  'washing feet': 380
#  'washing hair': 381
#  'washing hands': 382
#  'water skiing': 383
#  'water sliding': 384
#  'watering plants': 385
#  'waxing back': 386
#  'waxing chest': 387
#  'waxing eyebrows': 388
#  'waxing legs': 389
#  'weaving basket': 390
#  'welding': 391
#  'whistling': 392
#  'windsurfing': 393
#  'wrapping present': 394
#  'wrestling': 395
#  'writing': 396
#  'yawning': 397
#  'yoga': 398
#  'zumba': 399
