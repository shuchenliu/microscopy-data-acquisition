# Microscopy Data Acquisition

### What
This software downloads certain microscopy dataset from various sources including [EMPIAR](https://www.ebi.ac.uk/empiar/EMPIAR-11759/), [EPFL](https://www.epfl.ch/labs/cvlab/data/data-em/), [Janelia](https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2), [OpenMicroScopy](https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740), and [Hemibrain](https://tinyurl.com/hemibrain-ng)

### How
Prerequisites: `git` and `docker`
1. `$ git clone https://github.com/shuchenliu/microscopy-data-acquisition.git` to clone this repo
2. `$ docker-compose up --build -d` to start a docker container named `microscopy-data`
3. `$ docker exec -it microscopy-data python orchestration.py` to start the data query process. This commands will display an interface showing related information.

Datasets will be written to `./data`, as the directory is mounted to the docker container as an output volume. A meta-data table can be viewed at the './data' directory's [README](./data/README.md).

### Misc
1. The total downloading time could be over 10 minutes, depending on the geolocation and local bandwidth. For example, the direct download offered by `EPFL` originates from their server in Switzerland and thus may take the longest time. In comparison, the data syncing from Janelia, querying files hosted in AWS's `N.Virginia` zone, may take a fraction of time used while ~3 times larger in size.
2. Tools considerations:
   - `aria2`: EPFL's endpoint supports multi-part and multi-connection, which is a good use case for `aria2` instead of `curl`
   - `s5cmd` is used instead of `AWS-cli` to sync data from Janelia, since it's utilizing Golang's worker pool to read/write files, which is suitable for transferring directory storage (.zarr) files
   - while `EMPIAR` offers ftp server access similar to that of OpenMicroScopy, as well as `Aspera CLI` for data syncing, the target dataset here is only around `~1.3G`, and can be accessed as an archive directly from their `/get_zip` endpoint. Therefore, the simple `curl` is used to query the single, compressed file. 