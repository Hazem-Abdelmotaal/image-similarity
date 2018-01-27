#!/bin/bash
# https://www.imagemagick.org/Usage/basics/#mogrify

dst='./data/images'

size='64x64'

echo "jpg -> jpg"
magick mogrify -resize $size -background "#fff" -extent $size \
-gravity center -format jpg -path $dst './data/raw-images/*.jpg'

echo "jpeg -> jpg"
magick mogrify -resize $size -background "#fff" -extent $size \
-gravity center -format jpg -path $dst './data/raw-images/*.jpeg'

echo "png -> jpg"
magick mogrify -resize $size -background "#fff" -extent $size \
-gravity center -format jpg -path $dst './data/raw-images/*.png'

