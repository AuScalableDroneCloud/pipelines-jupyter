# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # 3D point clouds and meshes from 360 degree videos with ODMax
# ODMax has the capability to collect a large set of sample photos for photogrammetry. Combined with the extremely powerful OpenDroneMap software, a streamlined pipeline of 360-degree videos into photogrammetry products can be established. Luckily, the WebODM software offers a web platform to OpenDroneMap with an API that can be approached from python. To use this example, you need to have a running WebODM server (can be a local one on your current device via `docker`.
# Also you need to provide an .env file, in the notebook folder, or manually add your server details to your system environment variables. Here you can supply the server details and your login credentials. Below we will of course first check if your credentials are indeed picked up.
#
# We will use a number of `odmax` API functionalities. For explanation on the API, we refer to https://odmax.readthedocs.io/en/latest/api/index.html

# First, to ease the interaction with the WebODM API, let's install the `odk2odm` library from `localdevices`. This library offers odk and odm requests in pythonic form, so that you don't need to know anything about web requests to interact with your WebODM server. (PRE-INSTALLED ON ASDC CLOUD)

# This example is modified to use an input task containing the uploaded source video file, via the "Import" feature.
# It is assumed that this is the first custom asset file available in the selected task.

# ## Connect to ASDC WebODM

import asdc
from odk2odm import odm_requests
await asdc.connect()
token = asdc.auth.access_token
assert(token)
url = asdc.settings['api_audience'][0:-4] #Strip /api for odm_requests
print(url)
asdc.task_select()

# ### Get selections

# If everything works you should see a response like `Waiting for authorisation.... success`. If not then please go no further and investigate if you have the right server details and login. 
#
# If you have a valid token, then please continue below.

# +
#USING SELECTED PROJECT ID ABOVE
print(asdc.selected)
project_id = asdc.selected['project']
src_task_id = asdc.selected['task']

file_list = asdc.call_api(f'/projects/{project_id}/tasks/{src_task_id}/assets/files.json').json()

#Get the first custom asset
custom_assets = list(file_list["custom_assets"].keys())
if len(custom_assets) == 0:
    print("Source task should contain the source video file as a custom asset upload!")
    assert(False)

#Download the file
video_file = asdc.download_asset(custom_assets[0])
# -

# This should give you all the details of the selected project in WebODM. Within this project you can make several tasks to process, for instance for different areas, or different configurations. Each task consumes a set of photos and settings, and can then processed the provided photos into point clouds, meshes and other derivative products. Below we will make one task. In principle you can immediately add photos from disk to this task, but we will do a `partial` upload in smaller subtasks later on. Therefore we set the option `partial` to `True`.
#
# We also supply a list of options, that work well with ground-based datasets. For more information about the options available for WebODM tasks we refer to https://docs.opendronemap.org/

# +
# below we supply an extra option needed to work with spherical photos. The option with name "camera-lens" and 
# value "spherical" is essential if you use spherical imagery such as 360 degree photos. The job will fail if 
# you use a different (or default) camera-lens value.
options_list = {
    "camera-lens": "spherical",
    "dtm": True,
    "dsm": True,
    "feature-quality": "ultra",  # Set feature extraction quality. Higher quality generates better features, but requires more memory and takes longer
    "matcher-distance": 20,  # Good for street level photography. Will be changed when OpenSfM eventually is updated and has better defaults
    "matcher-neighbors": 800,  # Good Necessary for street level photography. Will be changed when OpenSfM eventually is updated and has better defaults
    "mesh-octree-depth": 14,  # Memory and CPU intensive but much nicer detail in meshes
    "mesh-size": 400000,  # Memory intensive. Could probably be turned up louder
    "min-num-features": 24000,  # One of the more important options: it improves matching significantly in complicated scenes.
    "pc-geometric": True,  # Cleans the final model a bit based on visibility tests
    "pc-quality": "ultra",  #Memory and CPU intensive but much nicer detail in point cloud
}
# convert into list with "name" / "value" dictionaries, suitable for ODM
options = [{"name": k, "value": v} for k, v in options_list.items()]

data = {
    "partial": True,
    "name": "batch_1",
    "options": options
}
res = odm_requests.post_task(url, token, project_id, data=data)
task = res.json()
task_id = res.json()["id"]
print(task)
# -

# If everything went as normal, you should see information about the created task above. We create a `Video` object that we can extract frames with. Let's have a quick look at the geographical information too with the `.plot_gps` method.

# +
import odmax
#video_file = "GOPR0011_1599383304667.mp4"
Video = odmax.Video(video_file)

# Let's have a quick look at the GPS track with the beautiful plotting function for the GPS track. If you have GPS data it'll be plotted
Video.plot_gps(
    geographical=True,
    tiles="OSM",
    zoom_level=18,
    plot_kwargs={"color": "r", "marker": "x"}
)


# -

# Finally we are at the point where we can let `odmax` extract stills, reproject them, and upload them into the defined task. Let's first open a video and then define some settings we want to use. We want to extract stills from `t_start = 23` until `t_end = 76`. We choose this part because it is a part of video where some turns are taken and therefore lots of imagery is captured from different angles. With `odmax` functionalities we make a list of frames to process. 

t_start = 23
t_end = 76
# get the start and end frame
start_frame = odmax.io.get_frame_number(Video.cap, t_start)
end_frame = odmax.io.get_frame_number(Video.cap, t_end)
# make a list of frames with 5-frame intervals
frames = list(range(start_frame, end_frame, 5))
print(frames)


# Now we need to do several things in a loop. Per frame we will:
# * extract the frame using `Video.get_frame`. Let's skip reprojection for now, but you could add with `reprojection=True`, especially if you wish to mix photos from different platforms (e.g. 360-degree + drone)
# * encode the images into a ByteIO stream (we do not write any intermediate result to disk!). This stream can be    directly uploaded.
# * make a list of images with file names ready for uploading. This follows the ODM API, see https://docs.webodm.org.
# * Upload these images to the open WebODM task. 
#
# To make this easier, we make a small helper function for the encoding. We also check if there is already a thumbnail for the stills, if that is the case we don't bother re-uploading it. We use `tqdm` to track progress. 

# +
import cv2
import io
from tqdm.notebook import tqdm


work = tqdm(frames, leave=True)
for f in work:
    # read the frame
    Frame = Video.get_frame(f)
    # convert into bytestream
    bytestream = Frame.to_bytes()
    # prepare fields for upload 
    filename = "still_{:04d}.jpg".format(f)
    fields = {
        "images": (
            filename,
            bytestream,
            'images/jpg'
        )
    } 
    res = odm_requests.get_thumbnail(url, token, project_id, task_id, filename=filename)
    if res.status_code == 200:
        work.set_description(f"File {filename} already exists on ODM task, skipping...")
    else:
        work.set_description(f"Uploading {filename}")
        # add field to uploads of tasks. In the post below, the actual uploading of one face of one frame is occurring
        res = odm_requests.post_upload(url, token, project_id, task_id, fields)  

# -

# It is time to have a look at your current task within the WebODM environment. You will get the link to the appropriate task below. Click on it to display it in a separate window. You may have to login first, and then click on the link below again once logged in to get the right task. Return after inspection to do the final parts.

end_point = f"{url}/dashboard/?project_task_open={project_id}&project_task_expanded={task_id}"
print(end_point)

# We can now commit the task so that it'll process and run

res = odm_requests.post_commit(url, token, project_id, task_id).json()
print(res)

# Now we can track the progress of the task. You can do this by running the cell below and keep it running until it is done. It will take several hours to process this, you can simply leave this notebook and open your WebODM task on the WebODM dashboard to track progress and see results as well!

import time
running_progress = 0.
print("The status bar below shows how far the processing is. When this is reaching 100% go back to your ODM server and check the results. Dependent on the resources, this may take a long time. You can also still got to:")
print(end_point)
print("if you like to see the WebODM web-interface")
with tqdm(total=100) as pbar:
    while running_progress < 1.:
        res = odm_requests.get_task(url, token, project_id, task_id)
        status = res.json()
        running_progress = status["running_progress"]
        time.sleep(1)
        pbar.n = running_progress*100
        pbar.refresh()
    


