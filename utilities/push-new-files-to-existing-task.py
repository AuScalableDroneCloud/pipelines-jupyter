# # Push a new file to an existing ASDC Task
# - This notebook demonstrates how to upload a file to an existing ASDC Task
# - This is handy since ODM doesn't support adding additiona files once a Task has been run (or failed to run), so if you are testing something like a GCP file, this code will let you upload additional files and then re-run the task
# - To get started, upload the file you want to push to an ODM task into the same directory as this notebook.
# - Enter the filename in the 4th step below

import os
import asdc

# ### Authenticate and get Task selection

from ipywidgets import widgets

asdc.task_select()


project_id = asdc.selected['project']
task_id = asdc.selected['task']
task_name = asdc.task_dict[task_id]['name']
project_name = asdc.project_dict[str(project_id)]['name']  #NOTE: Project_ID is returned as a string in the project_dict
print("Project Name:", project_name)
print("Project ID:", project_id)
print("Task Name:", task_name)
print("Task ID:", task_id)

# ### Upload the new file
# 1. Make sure the file has been uploaded to the same directory as this notebook
# 2. Update the "filename" variable below to the correct file name
# 3. Note that this has only been tested with JPG, TIF and TXT files. If you are uploading a file that is not an image or txt (ie gcp or geo file) then you will need to adjust the upload path in ways that aren't clearly document yet. See [the Fracture Detectiuo pipeline use case](https://github.com/AuScalableDroneCloud/pipeline-fracture/blob/main/Jupyter/ASDC_CoSheRem_notebook.py) for an example of uploading other file types

# +
filename = "geo.txt"
filename = "DJI_0011.TIF"
## Uncomment this to upload files to a new task rather than the one selected above:
#   new_task_id = asdc.import_task(f"{task_name}-testing")
#   asdc.upload(f"/projects/{project_id}/tasks/{new_task_id}/upload/", filename, progress=True)

asdc.upload(f"/projects/{project_id}/tasks/{task_id}/upload/", filename, progress=True)
# -

# ***
# #### Code below here not integrated yet
# ### Commit
# We can now commit the task so that it'll process and run

res = asdc.call_api(f"/projects/{project_id}/tasks/{new_task_id}/commit/", data={"Test" : True}) #"test":True}) #TODO: allow POST without data provided
if res == 200:
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


