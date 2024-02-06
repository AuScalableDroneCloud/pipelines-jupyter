# # Importing task files from ODM into Jupyter then back to ODM in a new Task
# - This notebook demonstrates how to download all the images from an existing Task (including a task that was started and failed)
# - Images are download to a local folder named "TEMP-_your-task-name_"
# - Once download the images can be processed however you choose (insert your code as needed)
# - Processed images are then uploaded to a new taskon ODM and this task is started

import os
import asdc

# ### Authenticate and get Task selection

from ipywidgets import widgets

asdc.task_select()


print(asdc.selected)
project_id = asdc.selected['project']
task_id = asdc.selected['task']
task_name = asdc.task_dict[task_id]['name']
project_name = asdc.project_dict[str(project_id)]['name']  #NOTE: Project_ID is returned as a string in the project_dict

# ### Get image list from selected task 

# +
#Get the image list from mounted dir instead
#import os
#arr = os.listdir(f"/mnt/project/{project_id}/task/{asdc.selected['task']}")
#print(arr)

# +
img_list = asdc.call_api(f"/projects/{project_id}/tasks/{task_id}/images").json()

#TEMP: shorten img_list to make the code run faster
img_list = img_list[:10]


print("Total images:", len(img_list), "\n")
# Create download folder
base_name_for_outputs =  task_name.split(" |")[0]
temp_folder_name = "TEMP-" + base_name_for_outputs
task_data_folder_path = os.path.join(".", temp_folder_name)  # The '.' represents the current directory
print("Temporary files will be stored in the folder: \n\t" + task_data_folder_path)
print("\nNew files with have the base file name: \n\t" + base_name_for_outputs + "\n-----------------------------")
if not os.path.exists(task_data_folder_path):
    os.makedirs(task_data_folder_path)
# -

print("First 20 filenames: \n", img_list[0: min(20, len(img_list))])

# ### Download images to the new local TEMP folder:

# - Download

# +
import time
start_time = time.time()  # Start timing

from tqdm.notebook import tqdm
import os
print("Now downloading", len(img_list), "images to:", f"{task_data_folder_path}\n")

work = tqdm(img_list, leave=True)
for i in work:
    filename = asdc.download(f"/projects/{project_id}/tasks/{task_id}/images/download/{i}",  f"{task_data_folder_path}/{i}", progress=False)
    work.set_description(f"Downloading image: {i}")
    work.update(1)
    
elapsed_time = time.time() - start_time  # Calculate the elapsed time
print(f"Total download time = {elapsed_time:.0f} seconds.")
# -

# ### Insert your code here to modify the images:
# * In this example we resize the images

print("Input the Width you want to resize images to. Aspect ratio will be retained.\n")
resize_to = widgets.IntText(value=2048, description='Resize to:')
resize_to


# +
from tqdm.notebook import tqdm
import asdc

import os
updated_img_list = [os.path.join(task_data_folder_path, filename) for filename in img_list]

work = tqdm(updated_img_list, leave=True)
for filename in work:
    asdc.utils.resize_image(filename, 1080)
# -

# ***

# ### Now we Upload the modified images to a new task
# - Change the _"new_task_name"_ text to whatever you want to name the new task  
#
# - _**Important: this will fail if you only have read-only access to the task**_

new_task_name = (f"{task_name}| test-reupload-speed-2")
new_task_id = asdc.new_task(new_task_name)
print(new_task_id)


# +
start_time = time.time()  # Start timing
from tqdm import tqdm
updated_img_list = [os.path.join(task_data_folder_path, filename) for filename in img_list]

work = tqdm(updated_img_list, desc="Uploading images", leave=True)
for filename in work:
    asdc.upload(f"/projects/{project_id}/tasks/{new_task_id}/upload/", filename, progress=False)

    #asdc.upload_image(filename, {project_id}, {new_task_id}, progress=True)  # NOTE: you have to use the asdc.upload_image for the images to upload quickly
    ## UNCOMMENT TO DELETE IMAGES AFTER UPLOAD
    ## os.remove(filename)  # Delete the file after uploading
    work.set_description(f"Uploading {filename}")
    work.update(1)

elapsed_time = time.time() - start_time  # Calculate the elapsed time
print(f"Total upload time = {elapsed_time:.0f} seconds.")
# -

# ### Commit
# We can now commit the task so that it'll process and run - this might take a sec so sit tight!
#

# +
res = asdc.call_api(f"/projects/{project_id}/tasks/{new_task_id}/commit/", data={"Test" : True}) #"test":True}) #TODO: allow POST without data provided
print(res)

if res.status_code == 200:
    print("Success! Task has been started. You can now switch to asdc and refresh the page to see the new task")
else:
    print("Commit failed with error code:", res)

# +
#convert project name to url friendly name for search string:

from urllib.parse import quote
url_project_name = quote(project_name)

print(f"https://asdc.cloud.edu.au/dashboard/?search={url_project_name}&project_task_open={project_id}&project_task_expanded={new_task_id}")

#test-project-1&project_task_open=847&project_task_expanded=2435a3ac-70ed-4e39-8114-31552b058d3a
#https://asdc.cloud.edu.au/dashboard/?page=1&ordering=-created_at&search=test-project-1&project_task_open=847&project_task_expanded=2435a3ac-70ed-4e39-8114-31552b058d3a

# -


