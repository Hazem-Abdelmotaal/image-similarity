#!/bin/bash
# https://www.imagemagick.org/Usage/basics/#mogrify

src='./data/raw-images'
dst='./data/images'

magick mogrify -resize 32x32 -background "#fff" -extent 32x32 \
-gravity center -format jpg -path $dst $src/*.jpeg

magick mogrify -resize 32x32 -background "#fff" -extent 32x32 \
-gravity center -format jpg -path $dst .$src/*.png
