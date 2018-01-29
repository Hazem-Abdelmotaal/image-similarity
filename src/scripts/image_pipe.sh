#!/bin/bash

# download images to ./data/raw-images/
python ./csv_image_downloader.py

# filter resized images (./data/raw-tmp-images/)
python ./images_to_resize.py

# resize and save to ./data/images/
./resize_and_fill.sh

# remove links
find ./data/raw-tmp-images/ -type l -name "*" -print0 | xargs -0 rm
