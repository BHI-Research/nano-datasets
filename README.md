# nano-datasets

Create custom subsets of big public datasets. A complement of [nano-datasets](https://github.com/BHI-Research/nano-datasets). Supported datasets are [Kinetics-400/600/700](https://github.com/cvdfoundation/kinetics-dataset), [Something-Something-v2](https://developer.qualcomm.com/software/ai-datasets/something-something), and [ImageNet-1K](https://www.image-net.org/download.php).

## Setup

```bash
(base) conda create -n nano-datasets python=3.11
(base) conda activate nano-datasets
(nano-datasets) pip install -r requirements.txt
```

### Images: mini-ImageNet

ImageNet-1K is one of the most influential datasets in the development of deep learning. It contains 1.28 million images organized into 1,000 different classes and has historically been used to train and evaluate image classification models. Although ImageNet is primarily a static image dataset, its influence extends to learning video representations, as many pre-trained models on ImageNet have been adapted and used as a basis for video tasks.

To create a reduced version of ImageNet-1K, start by downloading it to your local PC. You can download it from here (registration required). Once downloaded, this script will allow you to create a mini-dataset by selecting a number of images (images) from a specified number of classes (classes). The images will be copied to a destination folder, organized by class. The script also generates two CSV files: one with the image paths and associated class names, and another mapping the class names to class indices if needed.

Requirements
 - os
 - shutil
 - random
 - argparse
 - csv

Note: No additional dependencies need to be installed, as all required modules are part of the Python standard library.

#### How to run
To run the script gen_nano_imagenet.py, located in the mini-imagenet folder, the following parameters are required:

 - --src:
   - Type: Directory (string). Directory where the ImageNet-1K dataset is located (train or val). [REQUIRED].
 - --dest:
   - Type: Directory (string). Directory where the mini-ImageNet-1K dataset and the CSV files will be saved. [REQUIRED].
 - --classes:
   - Type: Integer. The number of classes to include in the mini-dataset. [REQUIRED].
 - --images:
   - Type: Integer. The number of images to copy from each selected class. If not specified, all images from each selected class will be copied. [OPTIONAL].
 - --randomly:
   - Type: String (S/N). Whether to select the classes randomly. Defaults to 'N' (no). [OPTIONAL].

#### Output
The script generates two CSV files:

 - image_paths.csv: Contains the complete file paths of the images and the corresponding class names.
 - class_mapping.csv: Contains the mapping of class indices to class names.

#### Examples
These are some usage examples:

Example 1: Help command
```bash
python gen_nano_imagenet.py --help
```
Output:

```bash
usage: gen_nano_imagenet.py [-h] --src SRC --dest DEST --classes CLASSES [--images IMAGES] [--randomly {S,N}]
Copy random files and generate class files.

options:
  -h, --help                                   Show this help message and exit.
  --src SRC                                    Source directory with train or val images.
  --dest DEST                                  Destination directory to save the mini-dataset.
  --classes CLASSES                            Number of classes to select.
  --images IMAGES                              Number of images to copy per class.
  --randomly {S,N}                             Randomly select classes (S/N). Defaults to N.
Example 2: Select specific number of classes and images per class
```
```bash
python gen_nano_imagenet.py --src ./imagenet-mini/ --dest ./mini_imagenet/ --classes 10 --images 5 --randomly S
```
Output:

```bash
Copied: ./imagenet-mini/train/n01440764/n01440764_1775.JPEG -> ./mini_imagenet/n01440764/n01440764_1775.JPEG
Copied: ./imagenet-mini/train/n01440764/n01440764_10845.JPEG -> ./mini_imagenet/n01440764/n01440764_10845.JPEG
Copied: ./imagenet-mini/train/n01443537/n01443537_19366.JPEG -> ./mini_imagenet/n01443537/n01443537_19366.JPEG
Copied: ./imagenet-mini/train/n01443537/n01443537_18160.JPEG -> ./mini_imagenet/n01443537/n01443537_18160.JPEG
...
```
This will copy 5 random images from each of 10 randomly selected classes into the destination folder and create the corresponding CSV files. The CSV files will be located in the destination directory.

### Videos: nano-kinetics

Kinetics is a series of large-scale datasets commonly used for action recognition in videos. They consist of hundreds of thousands of video clips sourced from YouTube, each labeled with one of hundreds of action classes. These datasets are widely used for training and evaluating video models in the field of deep learning.

To create a reduced version of one of these Kinetics datasets, you don't need to download the dataset from external sources or register on any website. Upon downloading or cloning this GitHub repository, you will have access to the necessary folders (k400, k600, k700), each of which contains the following files:
- train.csv: Contains the video IDs and their corresponding class labels for the training set.
- val.csv: Contains the video IDs and their corresponding class labels for the validation set.
- map-k[number]-class.csv: Maps the class labels to their corresponding class indices.

These files are used by the script to select videos for creating the reduced dataset. You can define the parameter num_videos to specify how many videos to take from  class. Once you run the script, it will create a folder in the destination directory and save the specified number of videos. Additionally, the script will generate a CSV file, containing the complete path of each video and the class number. If needed, another parameter map_file can be used to associate each class name with an specific index.

### Requirements
- yt-dlp
- pandas
- os
- moviepy
NOTE: No dependencies installation required.

### How to run

To run the script create_nano.py in the nano-dataset folder, use the following parameters:

- save_dir:
    - Type: directory (string).
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

- map_file:
    - Type: File path (string).
    - Description: Path to a CSV file that maps each class label to a class number.
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
usage: create_nano.py [-h] --save_dir SAVE_DIR --dataset {k400,k600,k700} --video_type {train,val} --map_file MAP_FILE [--num_classes NUM_CLASSES] [--videos_per_class VIDEOS_PER_CLASS]

Generate a nano-dataset from the selected dataset.

options:
  -h, --help            show this help message and exit
  --save_dir SAVE_DIR   Directory where the nano-dataset will be saved
  --dataset {k400,k600,k700}   Dataset to select videos from (k400 | k600 | k700)
  --video_type {train,val}     Type of videos to include (train | val)
  --map_file MAP_FILE   Path to the class mapping file
  --num_classes NUM_CLASSES    Number of classes to include in the nano-dataset
  --videos_per_class VIDEOS_PER_CLASS  Number of videos to include per class
```


Input
```bash
python create_nano.py --save_dir ./nano-dataset/ --dataset k400 --video_type train --map_file ./class_mapping.csv --num_classes 5 --videos_per_class 10
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
1. **`--src`**  
   - Type: String (directory path)  
   - Description: The source directory where the SSV2 answers file (`test-answers.csv`) is located.  
   - Example: `--src ./labels/test-answers.csv`

2. **`--n`**  
   - Type: Integer  
   - Description: The number of videos to take from each class. This will limit the number of videos copied for each class in the dataset.  
   - Example: `--n 5`

3. **`--labels_src`**  
   - Type: String (directory path)  
   - Description: Path to the `labels.json` file, which contains the mappings between class names and class IDs.  
   - Example: `--labels_src ./labels/labels.json`

#### Optional Parameters:

1. **`--dest`**  
   - Type: String (directory path)  
   - Description: The destination directory where the new dataset will be saved. If this parameter is not provided, the dataset will be saved in the current working directory.  
   - Example: `--dest ./my-dataset/`

2. **`--videos_src`**  
   - Type: String (directory path)  
   - Description: The directory containing the downloaded SSV2 videos. If this parameter is provided, the script will generate a CSV file with the absolute paths to the videos. If not provided, the script will create a CSV file with relative paths from the SSV2 answers file.  
   - Example: `--videos_src /path/to/downloaded/videos/`

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
