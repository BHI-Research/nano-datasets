# nano-datasets

Create custom subsets of big public datasets. A complement of [nano-datasets](https://github.com/BHI-Research/nano-datasets). Supported datasets are [Kinetics-400/600/700](https://github.com/cvdfoundation/kinetics-dataset), [Something-Something-v2](https://developer.qualcomm.com/software/ai-datasets/something-something), and [ImageNet-1K](https://www.image-net.org/download.php).

## Setup

```bash
(base) conda create -n nano-datasets python=3.11
(base) conda activate nano-datasets
(nano-datasets) pip install -r requirements.txt
```

### Images: mini-imagenet

ImageNet-1K is one of the most influential datasets in the development of deep learning. It contains 1.28 million images organized into 1,000 different classes, and has historically been used to train and evaluate image classification models. Although ImageNet is primarily a static image dataset, its influence extends to learning video representations, as many pre-trained models on ImageNet have been adapted and used as a basis for video tasks.

To create a reduced version of ImageNet-1k, start downloading it in your local pc. Download it from [here](https://www.kaggle.com/datasets/ifigotin/imagenetmini-1000) (required to register in website first). From downloaded dataset, we define a parameter 'n', which is the number
of images to take from each class. After run script, it will create a folder for each class on a destination directory, and save 'n' images
from each class in them. Finally, script will create a CSV file, with each file complete path, and the class name. If it is required, another
parameter 'class_fp' could be use, to associate each class name with an index. In that case, final CSV will contain each file complete path,
with class index.

#### Requirements
 - os
 - shutil
 - random
 - argparse

NOTE: No dependencies installation required.

#### How to run

To run script 'gen_nano_imagenet.py' in mini-imagenet folder, this parameters are required:

 - src:
   - type: directory, string. Directory where to locate ImageNet-1k downloaded dataset. [REQUIRED].
 - dest:
   - type: directory, string. Directory where to save mini-ImageNet-1k generated dataset. [NOT REQUIRED].
 - n:
   - type: number. Number of files from each class to copy to new dataset destination folder. [REQUIRED].
 - class_fp:
   - type: string. File path to associate each class name with an index. [NOT REQUIRED].

#### Examples

This are some uses examples.

Input
```bash
python gen_nano_imagenet.py --help
```
Output
```bash
usage: gen_nano_imagenet.py [-h] --src SRC [--dest DEST] --n N [--class_fp CLASS_FP]
Copy random files and generate class files.

options:
  -h, --help           show this help message and exit
  --src SRC            Source directory to copy files from
  --dest DEST          Destination directory to copy files to
  --n N                Number of files to copy per folder
  --class_fp CLASS_FP  Path to the class associated file
```

Input
```bash
python .\gen_nano_imagenet.py --src .\imagenet-mini\train --dest . --n 2
```
Output
```bash
Copied: .\imagenet-mini\train\n01440764\n01440764_1775.JPEG -> ./imagenetmini/train/n01440764\n01440764_1775.JPEG
Copied: .\imagenet-mini\train\n01440764\n01440764_10845.JPEG -> ./imagenetmini/train/n01440764\n01440764_10845.JPEG
Copied: .\imagenet-mini\train\n01443537\n01443537_19366.JPEG -> ./imagenetmini/train/n01443537\n01443537_19366.JPEG
Copied: .\imagenet-mini\train\n01443537\n01443537_18160.JPEG -> ./imagenetmini/train/n01443537\n01443537_18160.JPEG
...
```

Script will save a custom dataset in the destination folder.


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


### Videos: nano-ssv2 (Something-to-Something v2)

Something-Something-v2 is a dataset specifically designed for interactive action recognition, where emphasis is placed on human interactions with everyday objects. It contains over 220,000 short videos divided into 174 action classes, such as “Push something up” or “Move something to the right”. This dataset is particularly valuable for research into complex interaction modelling and has been used to explore learning approaches beyond the classification of simple actions.

To create a minimal dataset from ssv2 original dataset, start downloading ssv2 on your local pc. You can download it from [here](https://www.qualcomm.com/developer/software/something-something-v-2-dataset/downloads). From downloaded dataset, we define a parameter 'n', which is the number of videos to take from each class. After run script, it will create a CSV file, with each file complete path, and the class name. To create that file script **does not use videos downloaded path**. It uses relative path, obtained from ssv2 answers file. It you want a final model dataset file, you can use 'videos_src' parameter. With it, you give script downloaded videos path, and dataset CSV is created using them instead of relative paths.

#### Requirements
 - json
 - os
 - argparse

NOTE: No dependencies installation required.

#### How to run

To run 'refer_by_classes.py' in ssv2 folder, this parameters are required:
 - src:
   - type: directory, string. Directory where to locate ssv2 answers file. [REQUIRED].
 - dest:
   - type: directory, string. Directory where to save ssv2 generated dataset. [NOT REQUIRED].
 - n:
   - type: number. Number of files from each class to copy to new dataset file. [REQUIRED].
 - labels_src:
   - type: directory, string. Path to labels.json file. [REQUIRED].
 - videos_src:
   - type: directory, string. Downloaded videos folder path to complete CSV file with absolute path. [NOT REQUIRED].

Input
```bash
python refer_by_classes.py --help
```
Output
```bash
usage: refer_by_classes.py [-h] --src SRC [--dest DEST] --n N --labels_src LABELS_SRC [--videos_src VIDEOS_SRC]

Copy random files and generate class files.

options:
  -h, --help            show this help message and exit
  --src SRC             Source directory to get answers file from
  --dest DEST           Destination directory to create json file
  --n N                 Number of videos to take from each class
  --labels_src LABELS_SRC
                        Destination directory of labels file
  --videos_src VIDEOS_SRC
                        Destination directory of videos
```
Input
```bash
python .\refer_by_classes.py --src .\labels\test-answers.csv --dest . --n 2 --label
s_src .\labels\labels.json
```
Output
```bash
208583.webm 42
186174.webm 42
50058.webm 144
150115.webm 144
...
```
Input
```bash
python .\refer_by_classes.py --src .\labels\test-answers.csv --dest . --n 2 --label
s_src .\labels\labels.json --videos_src "...\dataset-20bn\20bn\20bn-something-something-v2"
```
Output
```bash
...\dataset-20bn\20bn\20bn-something-something-v2\208583.webm 42
...\dataset-20bn\20bn\20bn-something-something-v2\186174.webm 42
...\dataset-20bn\20bn\20bn-something-something-v2\50058.webm 144
...\dataset-20bn\20bn\20bn-something-something-v2\150115.webm 144
```

Script will save a custom dataset in the destination folder.
