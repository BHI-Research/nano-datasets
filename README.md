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
python .\gen_nano_imagenet.py --src .\imagenet-mini\ --dest . --n 2
```
Output
```bash
Copied: .\imagenet-mini\train\n01440764\n01440764_1775.JPEG -> ./imagenetmini/images/n01440764\n01440764_1775.JPEG
Copied: .\imagenet-mini\train\n01440764\n01440764_10845.JPEG -> ./imagenetmini/images/n01440764\n01440764_10845.JPEG
Copied: .\imagenet-mini\train\n01443537\n01443537_19366.JPEG -> ./imagenetmini/images/n01443537\n01443537_19366.JPEG
Copied: .\imagenet-mini\train\n01443537\n01443537_18160.JPEG -> ./imagenetmini/images/n01443537\n01443537_18160.JPEG
...
```

Script will save a custom dataset in the destination folder.

### Videos: nano-kinetics

```bash
(nano-datasets)  python create_nano.py
Directory where you want to save the videos (if you want to use this same directory press enter): 
Name of .csv file: my-dataset.csv
Number of videos per class: 5
An error has occurred: [Errno 2] No such file or directory: 'my-dataset.csv'
(nano-datasets)
```

To ensure a smooth data preparation process, please follow these steps carefully:

***[Download the create_nano.py script:](https://github.com/BHI-Research/nano-datasets/blob/main/create_nano.py)***

Ensure that you have the `create_nano.py` script ready for execution. You can find the script in the provided repository or download it directly from the given link.

### ***[[Download the folders k400, k600, and k700:]](https://github.com/BHI-Research/nano-datasets/tree/main/k400)***

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
 - videos_src:
   - type: directory, string. Downloaded videos folder path to complete CSV file with absolute path. [NOT REQUIRED].

Input
```bash
python refer_by_classes.py --help
```
Output
```bash
usage: refer_by_classes.py [-h] [--src SRC] [--dest DEST] [--n N] [--videos_src VIDEOS_SRC]

Copy random files and generate class files.

options:
  -h, --help            show this help message and exit
  --src SRC             Source directory to get answers file from
  --dest DEST           Destination directory to create json file
  --n N                 Number of videos to take from each class
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