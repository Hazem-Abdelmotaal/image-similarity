# image-similarity


docker run -v $PWD:/tmp/working \
-v /Volumes/macHDD/Documents/img-sim:/Volumes/macHDD/Documents/img-sim \
-w=/tmp/working -p 8888:8888 --rm -it \
kaggle/python jupyter notebook --no-browser --ip="0.0.0.0" --notebook-dir=/tmp/working --allow-root
