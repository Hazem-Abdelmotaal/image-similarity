#!/bin/bash
# https://www.imagemagick.org/Usage/basics/#mogrify

src='./data/tmp-images'
dst='./data/images'

size='64x64'

echo "jpg -> jpg"
magick mogrify -resize $size -background "#fff" -extent $size \
-gravity center -format jpg -path $dst "$src/*.jpg" &

echo "jpeg -> jpg"
magick mogrify -resize $size -background "#fff" -extent $size \
-gravity center -format jpg -path $dst "$src/*.jpeg" &

echo "png -> jpg"
magick mogrify -resize $size -background "#fff" -extent $size \
-gravity center -format jpg -path $dst "$src/*.png" &

wait
echo "finish"
