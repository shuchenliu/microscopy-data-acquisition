#!/usr/bin/env python

import os
import random
import tensorstore as ts
import zarr
from zarr.errors import ContainsArrayError

HEMIBRAIN_DIR_NAME = 'hemibrain'

def make_output_dir():
    """
    Provides the output directory based on current script location
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', '..', 'data', HEMIBRAIN_DIR_NAME)

    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_crop_start(x: int, y: int, z: int, size=1000) -> list[int]:
    """
    Saves an array of start index for each of the 3 dimensions. It guarantees there are enough elements for given size starting from the index
    """
    starts = []

    for n in [x, y, z]:
        assert n >= size
        start = random.randint(0, n - size)
        starts.append(start)


    return starts





def save_hemibrain_data(use_random=False) -> bool:
    """
    Saves a 1000x1000x1000 region from the raw data to .zarr format.

    Uses tensorstore because of https://dvid.io/blog/release-v1.2/
    "To parse the data, use one of the software libraries below or you'll have to write software to parse data using the format specification linked above."

    """

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


    # if we purely relies on random, we might end up with a very sparse array
    if use_random:
        x_start, y_start, z_start = generate_crop_start(x, y, z)
    else:
        # a decent sample block
        x_start, y_start, z_start = 5191, 18266, 18352

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
        return True
    except ContainsArrayError:
        print("File already exists, skipping saving")
        return False


if __name__ == "__main__":
    save_hemibrain_data()