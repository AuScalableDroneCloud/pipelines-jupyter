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

import argparse
from process_imagery import process_existing, process_from_start
from calculate_canopy_height import get_canopy_height
from cover_and_cv import calculate_cover_and_cv
from predictor import predict
import time
import os
import Metashape
import sys


def main():
    if args.existing:
        process_existing(
            args.input,
            args.output,
            multispec=args.multispec,
            downscale=args.downscale,
            keypoints=args.keypoints,
            tiepoints=args.tiepoints,
            gcps=args.gcps,
            crs=args.crs
        )
    elif args.process:
        process_from_start(
            args.input,
            args.output,
            multispec=args.multispec,
            downscale=args.downscale,
            keypoints=args.keypoints,
            tiepoints=args.tiepoints,
            gcps=args.gcps,
            crs=args.crs
        )
    # Path flow if no Metashape processing is to be done
    if not (args.existing or args.process):
        if not args.input.endswith('.tif'):
            raise ValueError('Wrong input format, file must be .tif')
        else:
            if args.canopy_height and (args.dtm is None or args.dem is None or args.plot_file is None):
                am_parser.error('canopy height requires --dtm and --plot_file arguments')

            if args.canopy_height and (args.dtm is not None and args.plot_file is not None):
                csv_outpath, extension = os.path.splitext(args.input)
                csv_outpath = csv_outpath + "_canopy_height.csv"
                get_canopy_height(args.plot_file, args.dem, args.dtm, csv_outpath)
            # else:
            # raise ValueError('DTM file or plot file is invalid or does not exist')
            if args.canopy_cover and args.plot_file is not None:
                csv_outpath, extension = os.path.splitext(args.input)
                csv_outpath = csv_outpath + "_canopy_cover.csv"
                predict(input_tiff=args.input,
                        tile_height=args.tile_height,
                        tile_width=args.tile_width,
                        stride_height=args.stride_height,
                        stride_width=args.stride_width,
                        batch_size=args.batch_size
                        )
                predictions_tif = args.input + "-predictions.tif"
                calculate_cover_and_cv(predictions_tif, args.plot_file, csv_outpath)

    # gets here

    if args.process or args.existing:
        print('got here')
        # removed check for DTM. Process will generate one.
        if args.canopy_height and args.plot_file is not None:
            name, extension = os.path.splitext(args.output)
            dem = name + "_DEM.tif"
            if args.dtm:
                dtm = args.dtm
            else:
                dtm = name + "_DTM.tif"
            ch_csv_filename = name + "_Canopy_Height.csv"
            get_canopy_height(args.plot_file, dem, dtm, ch_csv_filename)

        if args.canopy_cover:
            ortho_path, extension = os.path.splitext(args.output)
            ortho_name = ortho_path + "_orthomosaic.tif"
            predict(input_tiff=ortho_name,
                    tile_height=args.tile_height,
                    tile_width=args.tile_width,
                    stride_height=args.stride_height,
                    stride_width=args.stride_width,
                    batch_size=args.batch_size
                    )
            predictions_name = ortho_name + "-predictions.tif"
            predictions_csv = ortho_path + "_canopy_cover.csv"
            calculate_cover_and_cv(predictions_name, args.plot_file, predictions_csv)

    print('processing completed')


if __name__ == "__main__":
    am_parser = argparse.ArgumentParser()

    am_parser.add_argument(
        '--process', action='store_true', help='input path to location of images OR path to existing project',
    )

    am_parser.add_argument(
        '--align_only', action='store_true', help='align only for manual input of GCPs'
    )

    am_parser.add_argument(
        '--input', type=str, help='input path to location of images OR path to existing project'
    )

    am_parser.add_argument(
        '--output', type=str, help='output path to .psx file', default=None
    )

    am_parser.add_argument(
        '--gcps', type=str, nargs='?', help='path to gcp file'
    )

    am_parser.add_argument(
        '--crs', type=str, choices=['wgs', 'gda'], nargs='?', help='gcs to use: either wgs or gda'
    )

    am_parser.add_argument(
        '--existing', action='store_true', help='Use if the input location is a psx file for existing project'
    )

    am_parser.add_argument(
        '--multispec', type=bool, help='Set to true for multispec', default=False
    )

    am_parser.add_argument(
        '--canopy_height', action='store_true', help='activate this flag to get canopy height after processing',
    )

    am_parser.add_argument(
        '--dem', type=str, help='dem for canopy height calc.', default=None
    )

    am_parser.add_argument(
        '--dtm', type=str, help='dtm for use in canopy height calc.', default=None
    )

    am_parser.add_argument(
        '--plot_file', type=str, help='shapefile for plot statistics', default=None
    )

    am_parser.add_argument(
        '--downscale', type=int, help='Downscale factor', default=4
    )

    am_parser.add_argument(
        '--keypoints', type=int, help='Max no. of keypoints per img.', default=40000
    )

    am_parser.add_argument(
        '--tiepoints', type=int, help='Max no. of tiepoints per img.', default=4000
    )

    am_parser.add_argument(
        '--canopy_cover', action='store_true', help='flag to process canopy_cover stats'
    )

    am_parser.add_argument(
        '--probability', type=float, help='Probability between 0 and 1 for canopy detection tolerance', default=0.96
    )

    am_parser.add_argument(
        "--tile_width", type=int, help="prediction width.", default=512,
    )
    am_parser.add_argument(
        "--tile_height", type=int, help="prediction height.", default=512,
    )
    am_parser.add_argument(
        "--stride_width", type=int, help="prediction stride width.", default=128,
    )
    am_parser.add_argument(
        "--stride_height", type=int, help="prediction stride height.", default=128,
    )
    am_parser.add_argument(
        "--batch_size", type=int, help="prediction batch sizes.", default=8,
    )
    """
    am_parse.add_argument(
        '--filtering', type=MetashapeObject, help='Filtering mode to use'
    )
    """

    args = am_parser.parse_args()
    main()
