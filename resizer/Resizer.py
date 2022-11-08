# # Image resizing pipeline
#
# - Takes a project & task
# - Loads each input image in the task
# - Resizes the image to the specified size
# - Uploads the resized images to a new task

import asdc
await asdc.connect()
asdc.task_select()
from ipywidgets import widgets
resize_to = widgets.IntText(value=2048, description='Resize to:')
resize_to


#Get selections
print(asdc.selected)
project_id = asdc.selected['project']
task_id = asdc.selected['task']
task_name = asdc.task_dict[task_id]['name']

# +
#Create a new task, "partial" enabled to allow later upload of images
#https://github.com/localdevices/odk2odm/blob/main/odk2odm/odm_requests.py
import json
options_list = {
    "auto-boundary": True,
    "dsm": True
}
# convert into list with "name" / "value" dictionaries, suitable for ODM
options = [{"name": k, "value": v} for k, v in options_list.items()]
#print("OPTIONS",options)
data = {
    "partial": True,
    "name": f"{task_name} - Resized {resize_to.value}",
    "options": options
}
#def post_task(base_url, token, project_id, data={}, files=[]):
#from odk2odm import odm_requests
#url = asdc.auth.settings["api_audience"] + f"/projects/{project_id}/tasks/"
#print(url)
#res = odm_requests.post_task(url, asdc.auth.access_token, project_id, data=data)

res = asdc.call_api(f"/projects/{project_id}/tasks/", data=data)
print(res)
task = res.json()
print(task)
new_task_id = res.json()["id"]


# +
img_list = asdc.call_api(f"/projects/{project_id}/tasks/{task_id}/images").json()
#https://dev.asdc.cloud.edu.au/api/projects/7/tasks/921edd3b-df10-4881-8175-dab92e4b5f05/images/download

#Get the image list from mounted dir instead
#import os
#arr = os.listdir(f"/mnt/project/{project_id}/task/{asdc.selected['task']}")
#print(arr)
# -

print(img_list)

#Resize function from WebODM/app/models/task,py
import logging
logger = logging.getLogger('app.logger')
import re
import os
from PIL import Image
import piexif
def resize_image(image_path, resize_to, done=None):
    """
    :param image_path: path to the image
    :param resize_to: target size to resize this image to (largest side)
    :param done: optional callback
    :return: path and resize ratio
    """
    try:
        can_resize = False

        # Check if this image can be resized
        # There's no easy way to resize multispectral 16bit images
        # (Support should be added to PIL)
        is_jpeg = re.match(r'.*\.jpe?g$', image_path, re.IGNORECASE)

        if is_jpeg:
            # We can always resize these
            can_resize = True
        else:
            try:
                bps = piexif.load(image_path)['0th'][piexif.ImageIFD.BitsPerSample]
                if isinstance(bps, int):
                    # Always resize single band images
                    can_resize = True
                elif isinstance(bps, tuple) and len(bps) > 1:
                    # Only resize multiband images if depth is 8bit
                    can_resize = bps == (8, ) * len(bps)
                else:
                    logger.warning("Cannot determine if image %s can be resized, hoping for the best!" % image_path)
                    can_resize = True
            except KeyError:
                logger.warning("Cannot find BitsPerSample tag for %s" % image_path)

        if not can_resize:
            logger.warning("Cannot resize %s" % image_path)
            return {'path': image_path, 'resize_ratio': 1}

        im = Image.open(image_path)
        path, ext = os.path.splitext(image_path)
        resized_image_path = os.path.join(path + '.resized' + ext)

        width, height = im.size
        max_side = max(width, height)
        if max_side < resize_to:
            logger.warning('You asked to make {} bigger ({} --> {}), but we are not going to do that.'.format(image_path, max_side, resize_to))
            im.close()
            return {'path': image_path, 'resize_ratio': 1}

        ratio = float(resize_to) / float(max_side)
        resized_width = int(width * ratio)
        resized_height = int(height * ratio)

        im = im.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
        params = {}
        if is_jpeg:
            params['quality'] = 100

        if 'exif' in im.info:
            exif_dict = piexif.load(im.info['exif'])
            #exif_dict['Exif'][piexif.ExifIFD.PixelXDimension] = resized_width
            #exif_dict['Exif'][piexif.ExifIFD.PixelYDimension] = resized_height
            im.save(resized_image_path, exif=piexif.dump(exif_dict), **params)
        else:
            im.save(resized_image_path, **params)

        im.close()

        # Delete original image, rename resized image to original
        os.remove(image_path)
        os.rename(resized_image_path, image_path)

        logger.info("Resized {} to {}x{}".format(image_path, resized_width, resized_height))
    except (IOError, ValueError) as e:
        logger.warning("Cannot resize {}: {}.".format(image_path, str(e)))
        if done is not None:
            done()
        return None

    retval = {'path': image_path, 'resize_ratio': ratio}

    if done is not None:
        done(retval)

    return retval



from tqdm.notebook import tqdm
work = tqdm(len(img_list), leave=True)
for i in img_list:
    filename = asdc.download(f"/projects/{project_id}/tasks/{task_id}/images/download/{i}")
    #print(dl)
    resize_image(filename, resize_to.value)
    
    #res = odm_requests.get_thumbnail(url, token, project_id, task_id, filename=filename)
    #if res.status_code == 200:
    #    work.set_description(f"File {filename} already exists on ODM task, skipping...")
    #else:
    #work.set_description(f"Uploading {filename}")
    # add field to uploads of tasks. In the post below, the actual uploading of one face of one frame is occurring
    #res = odm_requests.post_upload(url, token, project_id, task_id, fields)  
    #def upload(url, filepath, block_size=8192, throw=False, prefix=auth.settings["token_prefix"], **kwargs):
    #/projects/{project_pk}/tasks/{id}/upload/
    work.set_description(f"Uploading {filename}")
    asdc.upload(f"/projects/{project_id}/tasks/{new_task_id}/upload/", filename) #TODO: Allow disabling progress so can use single prog bar
    os.remove(filename) #Delete the file
    #break


# We can now commit the task so that it'll process and run

#res = odm_requests.post_commit(url, token, project_id, task_id).json()
#print(res)
#url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/commit/"
res = asdc.call_api(f"/projects/{project_id}/tasks/{new_task_id}/commit/", data={"Test" : True}) #"test":True}) #TODO: allow POST without data provided
print(res)


