# nano-datasets

Create custom subsets of big public datasets. A complement of [nano-jepa](https://github.com/BHI-Research/nano-jepa).

Supported datasets are:

* [Kinetics-400/600/700](https://github.com/cvdfoundation/kinetics-dataset)
* [Something-Something-v2](https://developer.qualcomm.com/software/ai-datasets/something-something)
* [ImageNet-1K](https://www.image-net.org/download.php).

## Setup

```bash
(base) conda create -n nano-datasets python=3.11
(base) conda activate nano-datasets
(nano-datasets) pip install -r requirements.txt
```

## Run

### Videos: nano-kinetics (k400, k600, k700)

To create a reduced version of one of these Kinetics datasets, you don't need to download the dataset from external sources or register on any website. All information is in his repository, see folders k400, k600, and k700. Each directory which contains the following files:

* train.csv: Contains the video IDs and their corresponding class labels for the training set.
* val.csv: Contains the video IDs and their corresponding class labels for the validation set.
* map-k[number]-class.csv: Maps the class labels to their corresponding class indices.

#### General Use

```bash
(nano-datasets) python create_nano.py --help
usage: create_nano.py [-h] --save_dir SAVE_DIR --dataset {k400,k600,k700} --video_type {train,val} [--num_classes NUM_CLASSES] [--videos_per_class VIDEOS_PER_CLASS] [--cookies COOKIES_FILE]

Generate a nano-dataset from the selected dataset.

options:
  -h, --help            show this help message and exit
  --save_dir SAVE_DIR   Directory where the nano-dataset will be saved
  --dataset {k400,k600,k700}   Dataset to select videos from (k400 | k600 | k700)
  --video_type {train,val}     Type of videos to include (train | val)
  --num_classes NUM_CLASSES    Number of classes to include in the nano-dataset
  --videos_per_class VIDEOS_PER_CLASS   Number of videos to include per class
  --cookies COOKIES_FILE   File with cookies from youtube
```

#### Example

In this example, the script copies 10 videos from 5 classes of the Kinetics-400 training dataset and saves them into the nano-dataset-k400-5c-10v folder. A CSV file with the video paths and class indices is generated in the destination directory.

```bash
(nano-datasets) python create_nano.py --save_dir ./nano-dataset-k400-5c-10v/ --dataset k400 --video_type train --num_classes 5 --videos_per_class 10

[youtube] Extracting URL: https://www.youtube.com/watch?v=p1VKQa4N-hg
[youtube] p1VKQa4N-hg: Downloading webpage
[youtube] p1VKQa4N-hg: Downloading ios player API JSON
[youtube] p1VKQa4N-hg: Downloading web creator player API JSON
[youtube] p1VKQa4N-hg: Downloading player a9d81eca
[youtube] p1VKQa4N-hg: Downloading m3u8 information
[info] p1VKQa4N-hg: Downloading 1 format(s): 18
[download] Destination: p1VKQa4N-hg.mp4
[download] 100% of   11.41MiB in 00:00:01 at 6.01MiB/s
Moviepy - Building video /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4.
MoviePy - Writing audio in abseiling_0TEMP_MPY_wvf_snd.mp3
MoviePy - Done.                                                                                                                                                       
Moviepy - Writing video /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4

Moviepy - Done !                                                                                                                                                      
Moviepy - video ready /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4
Video downloaded and saved in: /home/user/Desktop/nano-datasets/nano-dataset/abseiling_0.mp4
...
```

Notes:

* If you don't enter [num_classes] all classes will be downloaded.
* If you don't enter [videos_per_class] all videos per class will be downloaded.

### Videos: nano-ssv2 (Something-to-Something v2)

To create a minimal dataset from ssv2 original dataset, start downloading ssv2 on your local pc. You can download it from [here](https://www.qualcomm.com/developer/software/something-something-v-2-dataset/downloads). From the downloaded dataset, we define a parameter 'n', which is the number of videos to take from each class. After running the script, it will create a CSV file, with each file complete path, and the class name. The script **does not use videos downloaded path**. It uses a relative path, obtained from the ssv2 answers file. If you want a final model dataset file, you can use the 'videos_src' parameter. In this way, you give the script downloaded videos path.

#### General Use

```bash
(nano-datasets) cd ssv2
(nano-datasets) python refer_by_classes.py --help

usage: refer_by_classes.py [-h] --src SRC [--dest DEST] --n N --labels_src LABELS_SRC [--videos_src VIDEOS_SRC]

Copy random files and generate class files.

options:
  -h, --help            show this help message and exit
  --src SRC             Source directory to get answers file from
  --dest DEST           Destination directory to create json file
  --n N                 Number of videos to take from each class
  --labels_src LABELS_SRC
                        Destination directory of labels file
  --videos_src VIDEOS_SRC
                        Destination directory of videos
```

#### Examples

```bash
(nano-datasets) cd ssv2
(nano-datasets) python .\refer_by_classes.py --src .\labels\test-answers.csv --dest . --n 2 --label s_src .\labels\labels.json

208583.webm 42
186174.webm 42
50058.webm 144
150115.webm 144
...
```

```bash
(nano-datasets) cd ssv2
(nano-datasets) python .\refer_by_classes.py --src .\labels\test-answers.csv --dest . --n 2 --label s_src .\labels\labels.json --videos_src "...\dataset-20bn\20bn\20bn-something-something-v2"
...\dataset-20bn\20bn\20bn-something-something-v2\208583.webm 42
...\dataset-20bn\20bn\20bn-something-something-v2\186174.webm 42
...\dataset-20bn\20bn\20bn-something-something-v2\50058.webm 144
...\dataset-20bn\20bn\20bn-something-something-v2\150115.webm 144
```

Script will save a custom dataset in the destination folder.

### Images: mini-imagenet

To create a reduced version of ImageNet-1k, start downloading it in your local pc. Download it from [here](https://www.kaggle.com/datasets/ifigotin/imagenetmini-1000) (required to register on the website first). From the downloaded dataset, we define a parameter 'n', which is the number of images to take from each class. After running the script, it will create a folder for each class in a destination directory, and save 'n' images from each class in them. Finally, script will create a CSV file, with each file complete path, and the class name. If it is required, another parameter 'class_fp' could be used, to associate each class name with an index. In that case, final CSV will contain each file complete path, with class index.

#### General Use

```bash
(nano-datasets) cd mini-imagenet1k
(nano-datasets) python gen_nano_imagenet.py --help

usage: gen_nano_imagenet.py [-h] --src SRC [--dest DEST] --n N [--class_fp CLASS_FP]
Copy random files and generate class files.

options:
  -h, --help           show this help message and exit
  --src SRC            Source directory to copy files from
  --dest DEST          Destination directory to copy files to
  --n N                Number of files to copy per folder
  --class_fp CLASS_FP  Path to the class associated file
```

#### Example

```bash
(nano-datasets) python .\gen_nano_imagenet.py --src .\imagenet-mini\train --dest . --n 2

Copied: .\imagenet-mini\train\n01440764\n01440764_1775.JPEG -> ./imagenetmini/train/n01440764\n01440764_1775.JPEG
Copied: .\imagenet-mini\train\n01440764\n01440764_10845.JPEG -> ./imagenetmini/train/n01440764\n01440764_10845.JPEG
Copied: .\imagenet-mini\train\n01443537\n01443537_19366.JPEG -> ./imagenetmini/train/n01443537\n01443537_19366.JPEG
Copied: .\imagenet-mini\train\n01443537\n01443537_18160.JPEG -> ./imagenetmini/train/n01443537\n01443537_18160.JPEG
...
```

Script will save a custom dataset in the destination folder.

## Cite

If you use this tool. Cite us using the following info:

```
@inproceedings{ermantraut2020resolucion,
  title={nano-JEPA: Democratizing Video Understanding with Personal Computer},
  author={Adrian Rostagno and Javier Iparraguirre and Joel Ermantraut and Lucas Tobio and Segundo Foissac and Santiago Aggio and Guillermo Friedrich},
  booktitle={XXV WASI – Workshop Agentes y Sistemas Inteligentes, CACIC},
  year={2024}
}
```
