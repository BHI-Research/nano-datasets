# original source: https://docs.voxel51.com/user_guide/dataset_zoo/datasets.html#kinetics-400

import fiftyone as fo
import fiftyone.zoo as foz

#
# Load 10 random samples from the validation split
#
# Only the required videos will be downloaded (if necessary)
#

dataset = foz.load_zoo_dataset(
    "kinetics-400",
    split="validation",
    max_samples=10,
    shuffle=True,
)

session = fo.launch_app(dataset)

#
# Load 10 samples from the validation split that
# contain the actions "springboard diving" and "surfing water"
#
# Videos that contain all `classes` will be prioritized first, followed
# by videos that contain at least one of the required `classes`. If
# there are not enough videos matching `classes` in the split to meet
# `max_samples`, only the available videos will be loaded.
#
# Videos will only be downloaded if necessary
#
# Subsequent partial loads of the validation split will never require
# downloading any videos
#

dataset = foz.load_zoo_dataset(
    "kinetics-400",
    split="validation",
    classes=["springboard diving", "surfing water"],
    max_samples=10,
)

session.dataset = dataset