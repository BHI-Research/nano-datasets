# nano-datasets

Create custom subsets of big public datasets. A complement of [nano-datasets](https://github.com/BHI-Research/nano-datasets). Supported datasets are [Kinetics-400/600/700](https://github.com/cvdfoundation/kinetics-dataset), [Something-Something-v2](https://developer.qualcomm.com/software/ai-datasets/something-something), and [ImageNet-1K](https://www.image-net.org/download.php).

## Setup

```bash
(base) conda create -n nano-datasets python=3.11
(base) conda activate nano-datasets
(nano-datasets) pip install -r requirements.txt
```

## Run

### Images: mini-imagenet

To create a reduced version of imagenet1k, start downloading it in your local pc. Download it from [here](https://www.image-net.org/download.php) (required to register in website).

After that, run script gen_nano_imagenet.py in mini-imagetnet folder, with this parameters:

```bash
# empty arguments
(nano-datasets) python .\gen_nano_imagenet.py
  gen_nano_imagenet.py: error: the following arguments are required: --src, --n

usage: gen_nano_imagenet.py [-h] --src SRC [--dest DEST] --n N [--class_fp CLASS_FP]
Copy random files and generate class files.

options:
  -h, --help           show this help message and exit
  --src SRC            Source directory to copy files from
  --dest DEST          Destination directory to copy files to
  --n N                Number of files to copy per folder
  --class_fp CLASS_FP  Path to the class associated file
```

Script will save  a custom  dataset in the destination folder.

## Videos

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

## ssv2

To create a minimal dataset from ssv2 original dataset, start downloading ssv2 on your local pc. You can download it from [here](https://developer.qualcomm.com/software/ai-datasets/something-something).

After it, run refer_by_classes.py in ssv2 folder, with this parameters:

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

Script will save a custom dataset in the destination folder.
