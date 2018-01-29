import os

RAW_IMAGES = './data/raw-images'
IMAGES = './data/images'
TMP_IMAGES = './data/raw-tmp-images'


def files_in(directory):
  files = {}
  for filename in os.listdir(directory):
    name_split = filename.split('.')
    if len(name_split >= 2)
      image_id = name_split[0]
      files[image_id] = filename

  return files

def images():
  raw_images = files_in(RAW_IMAGES)
  transformed_images = files_in(IMAGES)

  for key in raw_images:
    if key not in transformed_images:
      yield raw_images[key]

if __name__ == '__main__':
  from multiprocessing import Pool

  def link(image):
    print('Link: ' + image)
    os.symlink(RAW_IMAGES + '/' + image, TMP_IMAGES + '/' + image)

  p = Pool(8)
  print('Start')
  p.map(link, images())
  print('Done')
