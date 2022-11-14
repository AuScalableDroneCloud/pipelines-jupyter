ODMax
=====

[![PyPI](https://badge.fury.io/py/odmax.svg)](https://pypi.org/project/odmax/)
[![docs_latest](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://odmax.readthedocs.io/en/latest)
[![License](https://img.shields.io/github/license/localdevices/odmax?style=flat)](https://github.com/localdevices/odmax/blob/main/LICENSE)

**ODMax** is a utility to extract still frames from 360-degree video platforms such as GoPro or Insta. **ODMax** preserves the geoghraphical information
in videos and adds the geolocation to stills so that they can be used for geospatial applications such as geospatial photogrammetry with OpenDroneMap, or Streetview applications.

We are seeking funding for the following frequently requested functionalities:
* seamless processing via command-line to WebODM instances
* seamless processing to streetview products
* filtering options such as cloud masking, vegetation segmentation or other features
* variable frame interval detection, based on feature changes (currently a fixed frame interval must be set) 

If you wish to fund this or other work on features, please contact us at info@rainbowsensing.com.

> **_note:_**  For instructions how to get Anaconda (with lots of pre-installed libraries) or Miniconda (light weight) installed, please go to https://docs.conda.io/projects/conda/en/latest/

> **_manual:_** A full manual with examples can be found on https://odmax.readthedocs.io/

> **_compatibility:_** At this moment **ODMax** works with GoPro videos. It may or may not work with other 360 degree camera brands and models but this has not been tested.

Installation
------------

To get started with **ODMax**, we recommend to setup a python virtual environment. 
We recommend using a Miniconda or Anaconda environment as this will ease installation, and will allow you to use all
functionalities without any trouble. Especially geographical plotting with `cartopy` can be difficult to get installed. 
With a `conda` environment this is solved. We have also conveniently packaged all dependencies for you. 
In the subsections below, you can find specific instructions. 

### Installation for direct use

If you simply want to add **ODMax** to an existing python installation or virtual environment, then follow these 
instructions.

First activate the environment you want **ODMax** to be installed in (if you don't care about virtual environments, then 
simply skip this step)

Then install **ODMax** as follows:
```
pip install odmax
```
That's it! You are good to go!

### Installation from code base

To install **ODMax** from scratch in a new virtual environment from the code base, go through these steps. Logical cases
when you wish to install from the code base are:
* You wish to have the very latest non-released version
* You wish to develop on the code
* You want to use our pre-packaged conda environment with all dependencies to setup a good virtual environment

First, clone the code with `git` and move into the cloned folder.

```
git clone https://github.com/localdevices/ODMax.git
cd ODMax
```

If you want, setup a virtual environment as follows:
```
conda env create -f environment.yml
```

Now install the **ODMax** package. If you want to develop **ODMax** please type
```
pip install -e .
```
If you just want to use the lates **ODMax** code base (without the option to develop on the code) type:
```
pip install .
```
That's it, you are good to go.

### Installation of exiftool for metadata extraction

Especially for photogrammetry or 360 streetview applications, it is essential to have time stamps and geographical
coordinates embedded in the extracted stills. ODMax automatically extracts such information from 360-video files if
these are recorded by the device used. In order to do this, ODMax requires ``exiftool`` to be installed and available on
the path. To install ``exiftool`` in Windows, please follow the download and installation instructions for Windows on
https://exiftool.org/install.html. For Linux, you can also follow the download and installation instructions, or simply
acquire a stable version from the package manager of your installed distribution. 

Using ODMax
-----------
To use **ODMax**, go to a command line and type 
```
odmax --help
```
This will provide an overview of the most up-to-date command line options.
Alternatively, use our jupyter notebook examples to see common use cases on command-line as
well as directly in the API.

Acknowledgement
---------------
The development of ODMax has been supported by the Australian National University - Research School of Biology through 
funding provided by the National Collaborative Research Infrastructure Strategy (NCRIS), Australian Plant Phenomics 
Facility (APPF), and the Australian Scalabel Drone Cloud (ASDC). 

License
-------
**ODMax** is licensed under AGPL Version 3 (see [LICENSE](./LICENSE) file).

**ODMax** uses the following libraries and software with said licenses.
py360convert is not being maintained actively, therefore the py360convert code has been integrated into the **ODMax**
code base.

| Package                | Version      | License                                            |
|------------------------|--------------|----------------------------------------------------|
| numpy                  | 1.21.4       | BSD License                                        |
| opencv-python-headless | 4.5.4.60     | MIT License                                        |                                                                                      
| gpxpy                  | 1.5.0        | Apache License, Version 2.0                        |                                                                      
| tqdm                   | 4.62.3       | MIT License; Mozilla Public License 2.0 (MPL 2.0)  |                                                
| piexif                 | 1.1.3        | MIT License                                        |                                                                                      
| matplotlib             | 3.5.1        | Python Software Foundation License                 |                                                               
| geopandas              | 0.10.2       | BSD License                                        |                                                                                              
 | pandas                 | 1.3.5        | BSD License                                        |                                                                                      
 | Pillow                 | 8.4.0        | Historical Permission Notice and Disclaimer (HPND) |                                               
 | py360convert           | 0.1.0        | MIT License                                        |      

Project organisation
--------------------

    .
    ├── README.md
    ├── LICENSE
    ├── setup.py            <- setup script compatible with pip
    ├── environment.yml     <- YML-file for setting up a conda environment with dependencies
    ├── docs                <- Sphinx documentation source code
        ├── ...             <- Sphinx source code files
    ├── examples            <- Small example files used in notebooks
        ├── ...             <- individual .jpg and .mp4 files
    ├── notebooks           <- Jupyter notebooks with examples how to use the API
        ├── ...             <- individual Jupyter notebooks
    ├── odmax               <- odmax library and CLI
        ├── ...             <- odmax functions and CLI main function .py files

