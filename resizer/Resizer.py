# # Image resizing pipeline
#
# - Takes a project & task
# - Loads each input image in the task
# - Resizes the image to the specified size
# - Uploads the resized images to a new task

# ### Authenticate and get parameters

from ipywidgets import widgets
resize_to = widgets.IntText(value=2048, description='Resize to:')
resize_to

import asdc
await asdc.connect(mode='iframe')
asdc.task_select()


# ### Get selections

print(asdc.selected)
project_id = asdc.selected['project']
task_id = asdc.selected['task']
task_name = asdc.task_dict[task_id]['name']

# ### Create destination task for resized images

new_task_id = asdc.new_task(f"{task_name} - Resized {resize_to.value}")


# ### Get selected task image list

# +
img_list = asdc.call_api(f"/projects/{project_id}/tasks/{task_id}/images").json()

#Get the image list from mounted dir instead
#import os
#arr = os.listdir(f"/mnt/project/{project_id}/task/{asdc.selected['task']}")
#print(arr)
# -

print(img_list[0: min(20, len(img_list))])

# ### Iterate through the image list
# - Download
# - Resize
# - Upload

from tqdm.notebook import tqdm
import os
work = tqdm(img_list, leave=True)
for i in work:
    work.set_description(f"Downloading...")
    filename = asdc.download(f"/projects/{project_id}/tasks/{task_id}/images/download/{i}", progress=False)
    asdc.utils.resize_image(filename, resize_to.value)
    work.set_description(f"Uploading {filename}")
    asdc.upload(f"/projects/{project_id}/tasks/{new_task_id}/upload/", filename, progress=False)
    os.remove(filename) #Delete the file


# ### Commit
# We can now commit the task so that it'll process and run

#res = odm_requests.post_commit(url, token, project_id, task_id).json()
#print(res)
#url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/commit/"
res = asdc.call_api(f"/projects/{project_id}/tasks/{new_task_id}/commit/", data={"Test" : True}) #"test":True}) #TODO: allow POST without data provided
print(res)


