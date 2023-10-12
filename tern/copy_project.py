# # ADSC - TERN Coesra Interactions
#
# This notebook copies data from WebODM to TERN - CoESRA.
#
# ### Setup
#
# To connect to CoESRA remotely, one needs to create a User account in CoESRA (https://coesra.tern.org.au).
# Please make sure that your account has been provisined and is active before continuing.
#
# The second thing required is an api key for TERN Apis. An api key can be generated (https://account.tern.org.au).
#

# requires paramiko 
# !pip install paramiko

# import required libraries
import asdc
import ipywidgets
import tern


# Enter API Key
password = ipywidgets.Password(description="TERN ApiKey:")
display(password)

# setup TERN API with api key
api = tern.TERNApi(password.value)

# select ASDC / WebODM project and tasks
asdc.task_select()

# extract some info from selected project
project_id = asdc.selected['project']
task_id = asdc.selected['task']
task_name = asdc.task_dict[task_id]['name']

# set CoESRA destination folder.
# The image files and assets will be copied to the respective folders. Any folders that don't exist will be created.
# set CoESRA destination folder
imgs_dest = f"~/ASDC/{project_id}/tasks/{task_id}"
assets_dest = f"~/ASDC/{project_id}/tasks/{task_id}/assets"

# get list of images from WebODM project
img_list = asdc.call_api(f"/projects/{project_id}/tasks/{task_id}/images").json()

# upload all images from WebODM project to CoESRA
from tqdm.notebook import tqdm
import os
work = tqdm(img_list, leave=False,disable=False,dynamic_ncols=False)
for i in work:
    work.set_description(f"Downloading {i}")
    filename = asdc.download(f"/projects/{project_id}/tasks/{task_id}/images/download/{i}", progress=False)
    work.set_description(f"Uploading {i}")
    api.sftp(filename, imgs_dest, leave=False)
    os.remove(filename) #Delete the file
    work.refresh()
work.close()

# get list of assets for selected WebODM Project.
# `all.zip` is excluded, as it includes all other assets anyway
assets_list = [
    asset for asset in asdc.call_api(f"/projects/{project_id}/tasks/{task_id}").json()["available_assets"]
    if asset != "all.zip"
]

# Upload all assets from WebODM project to CoESRA
from tqdm.notebook import tqdm
import os
work = tqdm(assets_list, leave=False, disable=False, dynamic_ncols=False)
for i in work:
    work.set_description(f"Downloading {i}")
    filename = asdc.download(f"/projects/{project_id}/tasks/{task_id}/download/{i}", progress=False)
    work.set_description(f"Uploading {i}")
    api.sftp(i, assets_dest, leave=False)
    os.remove(i) #Delete the file
    work.refresh()
work.close()


