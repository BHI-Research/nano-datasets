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
Copiar código
python gen_nano_imagenet.py --help
```
Output:

```bash
Copiar código
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
Copiar código
python gen_nano_imagenet.py --src ./imagenet-mini/ --dest ./mini_imagenet/ --classes 10 --images 5 --randomly S
```
Output:

```bash
Copiar código
Copied: ./imagenet-mini/train/n01440764/n01440764_1775.JPEG -> ./mini_imagenet/n01440764/n01440764_1775.JPEG
Copied: ./imagenet-mini/train/n01440764/n01440764_10845.JPEG -> ./mini_imagenet/n01440764/n01440764_10845.JPEG
Copied: ./imagenet-mini/train/n01443537/n01443537_19366.JPEG -> ./mini_imagenet/n01443537/n01443537_19366.JPEG
Copied: ./imagenet-mini/train/n01443537/n01443537_18160.JPEG -> ./mini_imagenet/n01443537/n01443537_18160.JPEG
...
```
This will copy 5 random images from each of 10 randomly selected classes into the destination folder and create the corresponding CSV files. The CSV files will be located in the destination directory.

### Videos: nano-kinetics

Kinetics is a series of video datasets that have been instrumental in action recognition research. Kinetics-400 was the first release, which includes approximately 400 classes of human actions, with 400-1150 videos per class, captured from YouTube videos. Later versions, Kinetics-600 and Kinetics-700, expanded the number of classes and videos, reaching up to 700 classes in the latest release.


To ensure a smooth data preparation process, please follow these steps carefully:

***the create_nano.py script:***

Ensure that you have the `create_nano.py` script ready for execution.

### ***the folders k400, k600, and k700:***

Obtain the `k400, k600, and k700 folders`, which contain the necessary datasets. Make sure these folders are correctly named and contain all the required data files.

***Place all files in the same directory:***

Organize your working directory by placing the create_nano.py script and the k400, k600, and k700 folders together in the same directory. This setup is crucial for the script to locate and process the files efficiently.

***Run the create_nano.py script:***

Execute the create_nano.py script `python create_nano.py`. During execution, the script will prompt you with three questions:

`- Directory where you want to save the videos (if you want to use this same directory press enter): "C:\Users\nano-dataset\Nueva-carpeta"
`

`- Name of .csv file: train.csv`

`- Number of videos per class: 1`

Make sure to provide accurate and complete responses to these prompts to ensure successful execution.

```bash
(nano-datasets)  python create_nano.py
Directory where you want to save the videos (if you want to use this same directory press enter): 
Name of .csv file: my-dataset.csv
Number of videos per class: 5
```

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
