Last login: Tue Mar 22 16:33:58 on ttys009
pet22a@SERPENTINE-HF portal-core-ui-app % pwd
/Users/pet22a/AuScope/portal-core-ui-app
pet22a@SERPENTINE-HF portal-core-ui-app % cd ../..
pet22a@SERPENTINE-HF ~ % ls
Applications				Downloads				Untitled.ipynb				lena
AuScope					Edge_Detection.ipynb			demo_notebooks				pipeline-fracture
Automatic-Fracture-Detection-Code	Library					eclipse-workspace			pyAFDC
Bingie_Bingie_area1			Movies					example.py				pyAFDC.ipynb
Bingie_Bingie_area1_small		Music					flask_project				pyJupyter
Bingie_Bingie_area2			Pictures				get-pip.py				python_to_c
DJI_0003A				Postman					ipython-in-depth
Desktop					Public					jnb.config
Documents				PyCoShREM				knownlayers.json
pet22a@SERPENTINE-HF ~ % cd ecl*
pet22a@SERPENTINE-HF eclipse-workspace % ls
RemoteSystemsTempFiles			auscope-portal-api copy 10FEB2022	portal-core copy 10FEB2022
auscope-portal-api			portal-core
pet22a@SERPENTINE-HF eclipse-workspace % cd portal-core
pet22a@SERPENTINE-HF portal-core % ls
COPYING				README.md			checkstyle.xml			pom.xml				target
COPYING.LESSER			azure-pipelines.yml		eclipse-format-java-modest.xml	src
pet22a@SERPENTINE-HF portal-core % git config --get remote.origin.url
https://github.com/chrisvpeters/portal-core.git
pet22a@SERPENTINE-HF portal-core % 
pet22a@SERPENTINE-HF portal-core % 
pet22a@SERPENTINE-HF portal-core % 
pet22a@SERPENTINE-HF portal-core % ls -lt ~/AuScope/portal-core-ui-app/projects/portal-core-ui/src/lib/service/wms/get-caps.service.ts
ls: /Users/pet22a/AuScope/portal-core-ui-app/projects/portal-core-ui/src/lib/service/wms/get-caps.service.ts: No such file or directory
pet22a@SERPENTINE-HF portal-core % pwd
/Users/pet22a/eclipse-workspace/portal-core
pet22a@SERPENTINE-HF portal-core % ls
COPYING				README.md			checkstyle.xml			pom.xml				target
COPYING.LESSER			azure-pipelines.yml		eclipse-format-java-modest.xml	src
pet22a@SERPENTINE-HF portal-core % ls -lt
total 216
-rw-r--r--  1 pet22a  staff  16597 18 Feb 14:36 pom.xml
-rw-r--r--  1 pet22a  staff   1113 18 Feb 14:36 azure-pipelines.yml
drwxr-xr-x  4 pet22a  staff    128  5 Oct  2021 target
-rw-r--r--  1 pet22a  staff   3891  5 Oct  2021 checkstyle.xml
-rw-r--r--  1 pet22a  staff  35147  5 Oct  2021 COPYING
-rw-r--r--  1 pet22a  staff  30991  5 Oct  2021 eclipse-format-java-modest.xml
-rw-r--r--  1 pet22a  staff   7651  5 Oct  2021 COPYING.LESSER
-rw-r--r--  1 pet22a  staff    131  5 Oct  2021 README.md
drwxr-xr-x  4 pet22a  staff    128  5 Oct  2021 src
pet22a@SERPENTINE-HF portal-core % pwd
/Users/pet22a/eclipse-workspace/portal-core
pet22a@SERPENTINE-HF portal-core % ls -lt ~/AuScope/portal-core-ui-app/projects/portal-core-ui/src/lib/service/wms/get-caps.service.ts
ls: /Users/pet22a/AuScope/portal-core-ui-app/projects/portal-core-ui/src/lib/service/wms/get-caps.service.ts: No such file or directory
pet22a@SERPENTINE-HF portal-core % 
pet22a@SERPENTINE-HF portal-core % pwd
/Users/pet22a/eclipse-workspace/portal-core
pet22a@SERPENTINE-HF portal-core % pwd
/Users/pet22a/eclipse-workspace/portal-core
pet22a@SERPENTINE-HF portal-core % cd ..
pet22a@SERPENTINE-HF eclipse-workspace % cd ..
pet22a@SERPENTINE-HF ~ % pwd
/Users/pet22a
pet22a@SERPENTINE-HF ~ % ls
Applications				Downloads				Untitled.ipynb				lena
AuScope					Edge_Detection.ipynb			demo_notebooks				pipeline-fracture
Automatic-Fracture-Detection-Code	Library					eclipse-workspace			pyAFDC
Bingie_Bingie_area1			Movies					example.py				pyAFDC.ipynb
Bingie_Bingie_area1_small		Music					flask_project				pyJupyter
Bingie_Bingie_area2			Pictures				get-pip.py				python_to_c
DJI_0003A				Postman					ipython-in-depth
Desktop					Public					jnb.config
Documents				PyCoShREM				knownlayers.json
pet22a@SERPENTINE-HF ~ % mkdir wheatHub
pet22a@SERPENTINE-HF ~ % cd w*
pet22a@SERPENTINE-HF wheatHub % pwd
/Users/pet22a/wheatHub
pet22a@SERPENTINE-HF wheatHub % cudnn
zsh: command not found: cudnn
pet22a@SERPENTINE-HF wheatHub % pwd
/Users/pet22a/wheatHub
pet22a@SERPENTINE-HF wheatHub % ls -lt
total 72
-rw-r--r--@ 1 pet22a  staff  14420 10 May 10:52 process_imagery.py
-rw-r--r--@ 1 pet22a  staff   1303 10 May 10:52 exifgeotags.py
-rw-r--r--@ 1 pet22a  staff   6810 10 May 10:51 dpp_main.py
-rw-r--r--@ 1 pet22a  staff   2138 10 May 10:51 cover_and_cv.py
-rw-r--r--@ 1 pet22a  staff   2509 10 May 10:50 calculate_canopy_height.py
pet22a@SERPENTINE-HF wheatHub % vi process_imagery.py
pet22a@SERPENTINE-HF wheatHub % vi    
pet22a@SERPENTINE-HF wheatHub % vi exifgeotags.py
pet22a@SERPENTINE-HF wheatHub % vi dpp_main.py
pet22a@SERPENTINE-HF wheatHub % vi cover_and_cv.py
pet22a@SERPENTINE-HF wheatHub % vi calculate_canopy_height.py

"""This module outputs a csv filled with canopy heights for each plot. It requires a plot shapefile, DSM and DTM"""

import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject
from rasterio.enums import Resampling
import numpy as np
from rasterstats import zonal_stats
import pandas as pd
import geopandas as gpd
from shapely import speedups
speedups.disable()


# calculates canopy height using the 99th percentile of CHM values
# CHM = DSM - DTM
def get_canopy_height(plots, dsm, dtm, csv_outpath, method='percentile_99'):
    with rio.open(dsm) as src:
        out_meta = src.meta.copy()
        dst_crs = src.crs
        # get the transform, width and height from the DSM
        new_transform, new_width, new_height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)

        hold_src = src.read(1)

    with rio.open(dtm) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': new_transform,
            'width': new_width,
            'height': new_height,
        })

        # set the shape of the destination numpy array
        dst_shape = (new_height, new_width)
        # initialise a numpy array of zeros with shape: dst_shape
        np_dst = np.zeros(dst_shape, np.float32)

        reproject(
            source=src.read(1),
            destination=np_dst,
            src_transform=src.transform,
            src_crs=src.crs,
            # apply transform from DSM to destination numpy array
            dst_transform=new_transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest)

        canopy_height = hold_src - np_dst

        # remove no_data from canopy_height output
        # mostly for visualisation purposes
        canopy_height[canopy_height >= 32767] = 0.0
        canopy_height[canopy_height <= -32767] = 0.0

    gdf = gpd.read_file(plots)
    gdf['canopy_height'] = pd.DataFrame(zonal_stats(
        vectors=gdf['geometry'],
        raster=canopy_height,
        affine=new_transform,
        stats=method)
    )
    gdf = gdf.set_index('Plot_ID')
    gdf = gdf[['Row', 'Range', 'canopy_height']]
    gdf.to_csv(csv_outpath)
    # if joining both tables in main script - return should be used.
    # return gdf
