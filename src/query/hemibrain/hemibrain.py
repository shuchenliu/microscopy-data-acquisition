import os
import random
from typing import Tuple

import tensorstore as ts
import zarr
from zarr.errors import ContainsArrayError

HEMIBRAIN_DIR_NAME = ''

def make_output_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'data', HEMIBRAIN_DIR_NAME)

    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_crop_start(x: int, y: int, z: int, size=1000) -> list[int]:
    ranges = []

    for n in [x, y, z]:
        assert n >= size
        start = random.randint(0, n - size)
        ranges.append(start)


    return ranges





def save_hemibrain_data():

    # define tensorstore future
    dataset = ts.open({
        'driver':
           'neuroglancer_precomputed',
        'kvstore': 'gs://neuroglancer-janelia-flyem-hemibrain/emdata/raw/jpeg/',
        'context': {
            'cache_pool': {
                'total_bytes_limit': 100_000_000
           }
       },

     }, read=True, dimension_units=["8 nm", "8 nm", "8 nm", None]).result()

    x, y, z, _ = dataset.shape

    x_start, y_start, z_start = generate_crop_start(x, y, z)


    # there's only one channel so we leave that out
    image_stack = dataset[ts.d['channel'][0]]

    # cropping image
    crop = image_stack[x_start: x_start + 1000, y_start: y_start + 1000, z_start: z_start + 1000]
    array = crop.read().result()

    assert array.shape == (1000, 1000, 1000),  "Crop must be 1000 x 1000 x 1000"

    output_dir = make_output_dir()


    # save to zarr file
    try:
        zarr.save(f'{output_dir}/hemibrain-crop.zarr', array)
    except ContainsArrayError:
        print("File already exists, skipping saving")
        pass
