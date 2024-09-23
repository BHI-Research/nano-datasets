### Videos: nano-kinetics

Kinetics is a series of large-scale datasets commonly used for action recognition in videos. They consist of hundreds of thousands of video clips sourced from YouTube, each labeled with one of hundreds of action classes. These datasets are widely used for training and evaluating video models in the field of deep learning.

To create a reduced version of one of these Kinetics datasets, you don't need to download the dataset from external sources or register on any website. Upon downloading or cloning this GitHub repository, you will have access to the necessary folders (k400, k600, k700), each of which contains the following files:
- train.csv: Contains the video IDs and their corresponding class labels for the training set.
- val.csv: Contains the video IDs and their corresponding class labels for the validation set.
- map-k[number]-class.csv: Maps the class labels to their corresponding class indices.

These files are used by the script to select videos for creating the reduced dataset. You can define the parameter num_videos to specify how many videos to take from  class. Once you run the script, it will create a folder in the destination directory and save the specified number of videos. Additionally, the script will generate a CSV file, containing the complete path of each video and the class number. 


### Requirements
- yt-dlp
- pandas
- os
- moviepy

NOTE: No dependencies installation required.


### How to run

To run the script create_nano.py in the nano-dataset folder, use the following parameters:

- save_dir:
    - type: directory (string).
    - Description: Directory where the generated nano-dataset will be saved.
    - [REQUIRED]

- dataset:
    - Type: string.
    - Description: Dataset to select videos from (k400 | k600 | k700).
    - [REQUIRED]

- video_type: 
    - Type: string
    - Description: Type of videos to include (train | validation).
    - [REQUIRED]

- num_classes: 
    - Type: number (int)
    - Description: Number of classes to include in the nano-dataset. If not specified, all classes will be included.
    - [OPTIONAL]

- videos_per_class:
    - Type: number (int)
    - Description: Number of videos to include per class. If not specified, all videos for each class will be included.
    - [OPTIONAL]


### Examples

This are some uses examples.

Input
```bash
python create_nano.py --help
```

Output
```bash
usage: create_nano.py [-h] --save_dir SAVE_DIR --dataset {k400,k600,k700} --video_type {train,val} [--num_classes NUM_CLASSES] [--videos_per_class VIDEOS_PER_CLASS]

Generate a nano-dataset from the selected dataset.

options:
  -h, --help            show this help message and exit
  --save_dir SAVE_DIR   Directory where the nano-dataset will be saved
  --dataset {k400,k600,k700}   Dataset to select videos from (k400 | k600 | k700)
  --video_type {train,val}     Type of videos to include (train | val)
  --num_classes NUM_CLASSES    Number of classes to include in the nano-dataset
  --videos_per_class VIDEOS_PER_CLASS  Number of videos to include per class
```


Input
```bash
python create_nano.py --save_dir ./nano-dataset/ --dataset k400 --video_type train --num_classes 5 --videos_per_class 10
```

Output
```bash
[youtube] Extracting URL: https://www.youtube.com/watch?v=p1VKQa4N-hg
[youtube] p1VKQa4N-hg: Downloading webpage
[youtube] p1VKQa4N-hg: Downloading ios player API JSON
[youtube] p1VKQa4N-hg: Downloading web creator player API JSON
[youtube] p1VKQa4N-hg: Downloading player a9d81eca
[youtube] p1VKQa4N-hg: Downloading m3u8 information
[info] p1VKQa4N-hg: Downloading 1 format(s): 18
[download] Destination: p1VKQa4N-hg.mp4
[download] 100% of   11.41MiB in 00:00:01 at 6.01MiB/s
Moviepy - Building video /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4.
MoviePy - Writing audio in abseiling_0TEMP_MPY_wvf_snd.mp3
MoviePy - Done.                                                                                                                                                       
Moviepy - Writing video /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4

Moviepy - Done !                                                                                                                                                      
Moviepy - video ready /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4
Video downloaded and saved in: /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4
...
```
In this example, the script copies 10 videos from 5 classes of the Kinetics-400 training dataset and saves them into the nano-datasets/nano-dataset folder. A CSV file with the video paths and class indices is generated in the destination directory.
