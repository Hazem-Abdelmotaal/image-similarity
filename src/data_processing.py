import os
import random
from functools import wraps
import pandas as pd
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input


def cache_pd(path):
    def real_cache_pd(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(path):
                return pd.read_pickle(path)

            output = func(*args, **kwargs)
            output.to_pickle(path)
            return output
        return wrapper
    return real_cache_pd


def filter_existing_rows(dataframe, directory):
    def row_exists(row):
        return os.path.exists(directory + row.id_0 + '.jpg') \
            and os.path.exists(directory + row.id_1 + '.jpg')

    exists = dataframe.apply(row_exists, axis=1)
    return dataframe[exists == True]


def generate_batch(true_set, false_set, batch_size=32):
    true_sample = true_set.sample(n=batch_size // 2)

    false_sample = pd.DataFrame()
    # for each true match find False match if possible
    for i, row in true_sample.iterrows():
        false_match = false_set[false_set['id_0'] == row['id_0']]
        if not false_match.empty:
            false_sample = false_sample.append(false_match.head(1))
        else:
            rand_row = false_set.sample()
            fake_row = row.copy()
            fake_row['match'] = False
            fake_row['id_1'] = rand_row['id_1'].values[0]
            false_sample = false_sample.append(pd.DataFrame([fake_row]))

    batch = pd.concat([true_sample, false_sample])
    return batch


def generate_batch_fast(true_set, false_set, batch_size=32):
    true_sample = true_set.sample(n=batch_size // 2)
    false_sample = false_set.sample(n=batch_size // 2)

    return pd.concat([true_sample, false_sample])


def generate_batch_fake(true_set, false_set, batch_size=32):
    true_sample = true_set.sample(n=batch_size // 2)
    false_sample = true_sample.copy()

    false_sample['match'] = False
    false_sample['id_1'] = false_sample['id_1'].transform(np.random.permutation)

    return pd.concat([true_sample, false_sample])


def id_to_jpg(img_id, directory):
    return img_to_array(load_img(directory + img_id + ".jpg"))


def row_to_img_pair(row, directory):
    img_0 = id_to_jpg(row['id_0'], directory)
    img_1 = id_to_jpg(row['id_1'], directory)

    label = 1 if row['match'] else 0

    return [img_0, img_1], label


def pair_augmentation(left, right):
    # - left right
    # - left_horizontal right
    # - left righ_horizontal
    new_left = [left, np.flip(left, axis=1), left]
    new_right = [right, right, np.flip(right, axis=1)]

    return new_left, new_right


def df_to_img_pair(dataframe, directory):
    images_a = []
    images_b = []
    labels = []

    for i, row in dataframe.iterrows():
        try:
            pair, label = row_to_img_pair(row, directory)
            aug_pairs = pair_augmentation(*pair)
            images_a += aug_pairs[0]
            images_b += aug_pairs[1]
            labels += [label] * len(aug_pairs[0])
        except:  # TODO: setexcetion type
            pass

    return [
        preprocess_input(np.array(images_a), mode='tf'),
        preprocess_input(np.array(images_b), mode='tf')], np.array(labels)
