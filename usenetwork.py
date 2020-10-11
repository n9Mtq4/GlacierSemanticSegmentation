import numpy as np
import glob
import os
import sys
import json
from pathlib import Path
from PIL import Image

# disable GPU
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import tensorflow as tf
import tensorflow.keras as keras


MODEL_NAME = "model"

IN_DIR = Path("./netin")
OUT_DIR = Path("./netout")
LOAD_SIZE = 64

BAND_DIRS = sorted(list(IN_DIR.glob("B*")))

MAX_X = 255


def read_fname(fname):
    bands = np.asarray([np.array(Image.open(band_dir / fname)) for band_dir in BAND_DIRS]) / MAX_X
    mchannel = np.dstack(bands)
    return mchannel


def rgb_transform(ds):
#     return np.flip(ds, 3)  # Bands 2, 3, 4 -> rgb
    return np.flip(ds[:,:,:,1:4], 3)  # Bands 1, 2, 3, 4, 5, 7 -> rgb


def readin_batch(band1pths):
    img_lst = []
    img_names = []
    for imgpth in band1pths:
        img = read_fname(imgpth.name)
        img_lst.append(img)
        img_names.append(imgpth.name)
    return img_names, np.asarray(img_lst)


def divide_chunks(l, n): 
    # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def write_out_img(name, img_data):
    imga = tf.cast(img_data * 255, tf.uint8)
    imgencoded = tf.image.encode_png(imga)
    out_file = OUT_DIR / name
    tf.io.write_file(out_file.as_posix(), imgencoded)


def main():
    band1_paths = list(BAND_DIRS[0].glob("*.png"))
    
    model = tf.keras.models.load_model(f'{MODEL_NAME}.h5')
    
    batch_groups = list(divide_chunks(band1_paths, LOAD_SIZE))
    for i, batch in enumerate(batch_groups):
        print(f"Running inference on batch {i + 1} of {len(batch_groups)}")
        # print(f"{len(batch)}")
        names, x_pred = readin_batch(batch)
        y_pred = model.predict(x_pred)
        for name, pred in zip(names, y_pred):
            write_out_img(name, pred)


if __name__ == '__main__':
    main()
