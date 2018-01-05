from __future__ import print_function
import csv
import urllib
import os
import time


def csv_images(csv_path):
  with open(csv_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=';')
    for row in csv_reader:
      yield {'id': row['id_0'], 'url': row['img_0']}
      yield {'id': row['id_1'], 'url': row['img_1']}


def save_image(image, directory):
  try:
    filename = directory + '/' + image['id']
    if not (os.path.isfile(filename + '.png') or os.path.isfile(filename + '.jpeg')):
      _, h = urllib.urlretrieve(image['url'], filename)
      f_type = h['Content-Type'].split('/')[1]

      if 'html' in f_type:
        os.remove(filename)
      else:
        os.rename(filename, filename + '.' + f_type)
        print('Image saved: ' + filename + '.' + f_type)
    else:
      print('next')
  except Exception as e:
    print("Could not download url: " + image['url'])
    print(e)


def save_images(images, directory):
  vissited = set()
  for i,image in enumerate(images):
    print(i, end=': ')
    if image['id'] not in vissited:
      save_image(image, dst)
      vissited.add(image['id'])
    else:
      print('vissited')


if __name__ == '__main__':
  images = csv_images('./data/image_pairs.csv')
  dst = './data/raw-images'

  save_images(images, dst)

