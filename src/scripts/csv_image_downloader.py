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


def files_in(directory):
  # def test(filename):
  #   for end in ['.png', '.jpg', '.jpeg', '.gif', '.html']:
  #     if filename.endswith(end):
  #       return True
  #   return False

  files = set()
  for filename in os.listdir(directory):
    # if test(filename):
    image_id = filename.split('.')[0]
    files.add(image_id)

  return files


def uniq_images(images):
  visited = set()
  for img in images:
    if img['id'] not in visited:
      visited.add(img['id'])
      yield img


def save_image(image, directory):
  try:
    filename = directory + '/' + image['id']
    _, h = urllib.urlretrieve(image['url'], filename)
    f_type = h['Content-Type'].split('/')[1]

    if 'html' in f_type:
      with open(filename, 'w') as the_file:
        the_file.write('')
      print('not found')
    else:
      os.rename(filename, filename + '.' + f_type)
      print('Image saved: ' + filename + '.' + f_type)
  except Exception as e:
    print("Could not download url: " + image['url'])
    print(e)


def images():
  raw_images = files_in('./data/raw-images')
  transformed_images = files_in('./data/images')
  downloaded_images = raw_images | transformed_images

  for img in uniq_images(csv_images('./data/image_pairs_filtered.csv')):
    if img['id'] not in downloaded_images:
      yield img


if __name__ == '__main__':
  from multiprocessing import Pool

  def save_images_to_dst(images):
    save_image(images, './data/raw-images')

  p = Pool(4)
  print('Start')
  p.map(save_images_to_dst, images())
  print('Done')
