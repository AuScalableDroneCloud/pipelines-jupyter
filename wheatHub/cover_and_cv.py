"""This module calculates the canopy cover and covariance and stores outputs in a csv"""
"""It requires a predictions tiff - the output from the predictor.py module AND a plot shapefile"""

import rasterio
import cv2
import numpy as np
from rasterstats import zonal_stats
import pandas as pd
import geopandas as gpd
from shapely import speedups
speedups.disable()


def calculate_cover_and_cv(predictions, plot_shp, csv_outpath, probability=0.98, window_size=21):
    # open raster and set nodata value to -9999
    with rasterio.open(predictions, 'r+') as src:
        array = src.read(1)
        affine = src.transform
        src.nodata = 0

    # set threshold and mask out cells with values below probability value
    # cells with a 'probability of below the set probability (default=0.98), will be filtered out and not included in canopy cover calc
    array_masked = np.ma.masked_less(array, probability)
    array_masked = np.ma.filled(array_masked, fill_value=0)
    array_rounded = np.rint(array_masked)
    kernel = np.ones((window_size, window_size))
    filtered = cv2.filter2D(array_rounded, -1, kernel)

    # read in plots to perform zonal stats with
    gdf = gpd.read_file(plot_shp)

    gdf[['mean', 'std']] = pd.DataFrame(zonal_stats(
        vectors=gdf['geometry'],
        raster=filtered,
        affine=affine,
        stats=['mean', 'std'],
        nodata=0
    )
    )[['mean', 'std']]

    gdf['canopy_count'] = pd.DataFrame(zonal_stats(
        vectors=gdf['geometry'],
        raster=array_masked,
        affine=affine,
        stats=['count'],
        nodata=0
    )
    )['count']

    gdf['total_count'] = pd.DataFrame(zonal_stats(
        vectors=gdf['geometry'],
        raster=array,
        affine=affine,
        stats=['count'],
        nodata=0
    )
    )['count']

    gdf = gdf.set_index('Plot_ID')
    gdf['canopy_cover'] = gdf['canopy_count'] / gdf['total_count']
    gdf['cv'] = gdf['std'] / gdf['mean']
    # gdf = gdf[['Row', 'Range', 'canopy_cover', 'cv']]
    gdf = gdf[['canopy_cover', 'cv']]
    gdf.to_csv(csv_outpath)
