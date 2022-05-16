"""This module handles functions from the Metashape API"""

import os
import Metashape
from exifgeotags import get_longitude
from pathlib import Path


class MetaProcess:

    # option to use default parameters instead of kwargs
    # e.g. crs = None in function parameter
    # will use default parameters if class instantiated without params.
    def __init__(self, img_input, output_psx, gcps=None, crs='wgs'):

        self.img_input = img_input
        self.output_psx = output_psx
        self.doc = Metashape.Document()
        self.chunk = self.doc.chunk
        self.crs = crs
        self.gcp_file = gcps
        # self.params = kwargs.get('params', None)
        self.root_dir = Path(self.img_input).parent

    def get_output_name(self):
        return self.output_psx

    def new_chunk(self):
        # remove existing chunk
        self.doc.save(self.output_psx)
        self.chunk = self.doc.chunk
        # checking for existing chunks.
        # When creating a metashape document using Metashape.Document() it should default to having zero chunks.
        # If using GUI it defaults to initiating a chunk upon launching Metashape.
        if len(self.doc.chunks) > 0:
            self.doc.remove(self.chunk)
        # creating new chunk
        self.doc.addChunk()
        # using [-1] as it will always get the newest chunk incase the previous failed to delete.
        self.chunk = self.doc.chunks[-1]
        self.chunk.label = os.path.basename(self.output_psx)[:-4]  # check this

    def get_existing_chunk(self):
        self.doc.open(self.output_psx)
        self.chunk = self.doc.chunks[-1]
        # replace chunk label with shortened version of output path
        self.chunk.label = os.path.basename(self.output_psx)[:-4]
        self.doc.save()

        return self.chunk

    def add_images(self):
        path_photos = self.img_input
        photo_list = list()
        for r, d, f in os.walk(path_photos):
            for photo in f:
                    if ("jpg" or "jpeg" or "JPG" or "JPEG") in photo.lower():
                    photo_list.append(os.path.join(path_photos, r, photo))
        # print(photo_list)
        self.chunk.addPhotos(photo_list)
        self.doc.save()

        # Update crs will update the coordinate reference system for each image
        # out_crs predefined in pre-definition block before calling function
        # May have to add marker reference transform

    def update_crs(self, crs):
        for camera in self.chunk.cameras:
            if camera.reference.location:
                camera.reference.location = Metashape.CoordinateSystem.transform(camera.reference.location,
                                                                                 self.chunk.crs, self.crs)
        self.chunk.crs = self.crs
        self.chunk.updateTransform()

        # detect_markers() runs detect markers on current chunk
        # load reference will set the coordinates for each marker
        # only if the name of the markers in Metashape and the csv are the same.

    def detect_markers(self):
        self.chunk.detectMarkers(type=Metashape.CircularTarget12bit)
        # get gcp_file from argument
        if self.gcp_file is None:
            # this works if GCP file sits one directory outside of img directory
            try:
                self.chunk.importReference(os.path.join(self.root_dir, 'markers.csv'), delimiter=',', columns="nxyz")
            except FileNotFoundError:
                print('Could not automatically find gcp file.')
        else:
            try:
                self.chunk.importReference(self.gcp_file, delimiter=',', columns='nxyz')
            except FileNotFoundError:
                print('Could not find specified gcp file')

    def align_images(self, progress, downscale=4, keypoints=40000, tiepoints=4000):
        self.chunk.matchPhotos(downscale=downscale,
                               generic_preselection=True,
                               reference_preselection=True,
                               filter_mask=False,
                               keypoint_limit=keypoints,
                               tiepoint_limit=tiepoints,
                               progress=progress,
                               )

        self.chunk.alignCameras(adaptive_fitting=True)
        self.doc.save()

    # build_cloud() using GPU for processing depth maps
    def build_cloud(self, progress, downscale=4, filter_mode=Metashape.FilterMode.MildFiltering):
        Metashape.app.gpu_mask = 1  # GPU devices binary mask
        Metashape.app.cpu_enable = False
        self.chunk.buildDepthMaps(progress=progress, downscale=downscale, filter_mode=filter_mode)
        self.chunk.buildDenseCloud(progress=progress, point_colors=True)
        self.doc.save()

    def build_dem(self, source_data=Metashape.DataSource.DenseCloudData,
                  interpolation=Metashape.Interpolation.EnabledInterpolation):
        self.chunk.buildDem(source_data=source_data, interpolation=interpolation)  # region = extent removed
        self.doc.save()

    def build_orthomosaic(self, surface=Metashape.DataSource.ElevationData,
                          blending=Metashape.BlendingMode.MosaicBlending):
        self.chunk.buildOrthomosaic(surface_data=surface,
                                    blending_mode=blending,
                                    fill_holes=True)  # region = extent removed
        self.doc.save()

    def export_dtm(self, projection, max_angle=10, max_distance=0.02, cell_size=5, source=Metashape.PointClass.Created,
                   rasterformat=Metashape.RasterFormat.RasterFormatTiles):
        chunk_copy = self.chunk.copy()
        chunk_copy.dense_cloud.classifyGroundPoints(max_angle=max_angle,
                                                    max_distance=max_distance,
                                                    cell_size=cell_size,
                                                    source=source
                                                    )
        chunk_copy.buildDem(source_data=Metashape.DataSource.DenseCloudData, classes=[Metashape.PointClass.Ground])
        chunk_copy.exportRaster(self.output_psx[:-4] + "_DTM.tif",
                                format=rasterformat,
                                source_data=Metashape.DataSource.ElevationData,
                                projection=projection
                                )

    def export_all(self, projection, rasterformat=Metashape.RasterFormat.RasterFormatTiles):
        self.doc.save()
        self.chunk.exportRaster(self.output_psx[:-4] + "_DEM.tif",
                                format=rasterformat,
                                source_data=Metashape.DataSource.ElevationData,
                                projection=projection,
                                # write_world=True
                                )

        self.chunk.exportRaster(self.output_psx[:-4] + "_Orthomosaic.tif",
                                format=rasterformat,
                                # tiff_compression=compression,
                                projection=projection,
                                source_data=Metashape.DataSource.OrthomosaicData,
                                # write_world=True
                                )

        self.chunk.exportReport(self.output_psx[:-4] + "_report.pdf",
                                title=os.path.basename(self.output_psx)[:-4])
      def optimise_cameras(self):
        count = 0
        for camera in self.chunk.cameras:
            camera.reference.enabled = False
        for marker in self.chunk.markers:
            count += 1
            if marker.reference.location:
                marker.reference.enabled = True

        if count < 5:
            print('Less than 5 markers detected.')

        self.chunk.optimizeCameras(adaptive_fitting=True)

    def get_epsg(self):
        # Grabs EPSG based on longitude of geographic coordinates in EXIF
        # Australian zones

        if self.crs == 'wgs':
            epsg_dict = {
                "zone_49": 32749,
                "zone_50": 32750,
                "zone_51": 32751,
                "zone_52": 32752,
                "zone_53": 32753,
                "zone_54": 32754,
                "zone_55": 32755,
                "zone_56": 32756
            }

        # default to gda94 GCS
        if self.crs == 'gda' or self.crs is None:
            epsg_dict = {
                "zone_49": 28349,
                "zone_50": 28350,
                "zone_51": 28351,
                "zone_52": 28352,
                "zone_53": 28353,
                "zone_54": 28354,
                "zone_55": 28355,
                "zone_56": 28356
            }

        path_photos = self.img_input
        photo_list = list()
        for r, d, f in os.walk(path_photos):
            for photo in f:
                if ("jpg" or "jpeg" or "JPG" or "JPEG") in photo.lower():
                    photo_list.append(os.path.join(path_photos, r, photo))

        img_exif_to_sample = photo_list[int(len(photo_list) / 2)]

        img_long = get_longitude(img_exif_to_sample)


        if img_long < 114.0:
            epsg = epsg_dict["zone_49"]
        elif 114.0 <= img_long < 120.0:
            epsg = epsg_dict["zone_50"]
        elif 120.0 <= img_long < 126.0:
            epsg = epsg_dict["zone_51"]
        elif 126.0 <= img_long < 132.0:
            epsg = epsg_dict["zone_52"]
        elif 132.0 <= img_long < 138.0:
            epsg = epsg_dict["zone_53"]
        elif 138.0 <= img_long < 144.0:
            epsg = epsg_dict["zone_54"]
        elif 144.0 <= img_long < 150.0:
            epsg = epsg_dict["zone_55"]
        elif 150.0 <= img_long < 156.0:
            epsg = epsg_dict["zone_56"]
        else:
            raise ValueError('Invalid image geotags.')

        return epsg

    def progress_printer(self, p):
        print('Current task progress: {:.2f}%'.format(p))


class MultispecProcess(MetaProcess):
    # child class of MetaProcess
    # does extra stuff for multispectral imagery
    def add_images(self):
        path_photos = self.img_input
        photo_list = list()
        for r, d, f in os.walk(path_photos):
            for photo in f:
                if ("tif" or "tiff" or "TIF" or "TIFF") in photo.lower():
                    photo_list.append(os.path.join(path_photos, r, photo))

        self.chunk.addPhotos(photo_list)
        # automatically calibrate reflectance after importing images
        self.chunk.locateReflectancePanels()
        self.chunk.calibrateReflectance(use_reflectance_panels=True, use_sun_sensor=True)

        # calculate NDVI
    def set_ndvi_transform(self):
        self.chunk.raster_transform.formula = [("B5" - "B3") / ("B5" + "B3")]
        self.chunk.raster_transform.enabled = True

        # export all of the bands to one orthomosaic
    def set_multiband_transform(self):
        self.chunk.raster_transform.formula = ["B1/32768.0", "B2/32768.0", "B3/32768.0", "B4/32768.0", "B5/32768.0"]




def process_from_start(
        input_path: str,
        output_psx: str,
        multispec: bool,
        downscale: int,
        keypoints: int,
        tiepoints: int,
        gcps: str,
        crs: str
):
    if multispec == True:
        run_project = MultispecProcess(input_path, output_psx, gcps=gcps, crs=crs)
    else:
        run_project = MetaProcess(input_path, output_psx, gcps=gcps, crs=crs)

    print('in default territory')
    run_project.new_chunk()
    run_project.add_images()

    run_project.align_images(
        downscale=downscale,
        keypoints=keypoints,
        tiepoints=tiepoints,
        progress=run_project.progress_printer
    )

    if gcps is not None:
        run_project.detect_markers()
        run_project.optimise_cameras()

    run_project.build_cloud(
        downscale=downscale,
        progress=run_project.progress_printer
    )
    run_project.build_dem()
    run_project.build_orthomosaic()

    if crs is not None:
        epsg_projection = Metashape.CoordinateSystem('EPSG::' + str(run_project.get_epsg()))
        projection = Metashape.OrthoProjection()
        projection.crs = epsg_projection
        run_project.export_dtm(projection=projection)
        run_project.export_all(projection=projection)
    else:
        print('input CRS is required to export rasters.')


def process_existing(
        input_path: str,
        output_psx: str,
        multispec: bool,
        downscale: int,
        keypoints: int,
        tiepoints: int,
        gcps: str,
        crs: str
):
    if multispec:
        run_project = MultispecProcess(input_path, output_psx, gcps=gcps)
    else:
        run_project = MetaProcess(input_path, output_psx, gcps=gcps)

    run_project = run_project.get_existing_chunk()

    if not run_project.point_cloud:
        run_project.align_images(
            downscale=downscale,
            keypoints=keypoints,
            tiepoints=tiepoints,
            progress=run_project.progress_printer
        )

        if gcps is not None:
            run_project.detect_markers()
            run_project.optimise_cameras()

    if not run_project.dense_cloud:
        run_project.build_cloud(
            downscale=downscale,
            progress=run_project.progress_printer
        )
    if not run_project.elevation:
        run_project.build_dem()
    if not run_project.orthomosaic:
        run_project.build_orthomosaic()


def process_alignment_only(
        input_path: str,
        output_psx: str,
        multispec: bool,
        downscale: int,
        keypoints: int,
        tiepoints: int,
        gcps: str,
):
    if multispec:
        run_project = MultispecProcess(input_path, output_psx, gcps=gcps)
    else:
        run_project = MetaProcess(input_path, output_psx, gcps=gcps)
    run_project.new_chunk()
    run_project.add_images()
    run_project.align_images(
        downscale=downscale,
        keypoints=keypoints,
        tiepoints=tiepoints,
        progress=run_project.progress_printer
    )

