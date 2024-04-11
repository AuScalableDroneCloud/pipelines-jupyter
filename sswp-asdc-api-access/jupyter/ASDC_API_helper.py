import io, math, cv2
import numpy as np
import ASDC_API_support
import PIL.Image as Image
from getpass import getpass
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, Markdown


class Helper:
    def __init__(self):
        token = getpass("Paste your ASDC API token here:")     
        self.asdc_api = ASDC_API_support.ASDC_API_wrappers(token)
        self.selection = {}
        
    
    def select_upload(self):        
        uploads = self.asdc_api.asdc_uploads()
        try:
            uploads = uploads.json()['response']['payload']['uploads']
            list_uploads = []
            for i in uploads:
                list_uploads.append(str(i.get('id')) + ": " + str(i.get('title')))
        except KeyError:
            print("No uploads.")
            return None
    
        def selecter(upload):
            self.selection['upload_title'] = selected.value
            # get the file list from the selected upload
            upload_details = self.asdc_api.asdc_uploads(selected.value, get_data=True)
            #asdc_api.format_human_readable(upload_details)
            files = upload_details.json()['response']['payload']['uploads'][0]['results']
            file_dict = {}
            for i in files:
                file_dict[str(i.get('file'))] = {
                    'filename': str(i.get('filename')),
                    'display_name': str(i.get('filename'))
                }
            self.selection['upload'] = file_dict
            self.selection['upload_id'] = files[0]['upload']

        #layout = widgets.Layout(width='auto', height='40px')
        selected = widgets.Dropdown(
            options=list_uploads, 
            value=list_uploads[0],
            description="Select an upload:",
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style={'description_width': 'initial'},
            layout={'width': 'max-content'}
        )
        i = widgets.interactive(selecter, upload=selected)
        display(i)

    
    def select_run(self):        
        runs = self.asdc_api.asdc_runs()
        try:
            runs = runs.json()['response']['payload']['runs']
            list_runs = []
            for i in runs:
                list_runs.append(str(i.get('id')) + ": " + str(i.get('title')))
        except KeyError:
            print("No runs.")
            return None
    
        def selecter(run):
            self.selection['run_title'] = selected.value
            # get the file list from the selected run
            run_details = self.asdc_api.asdc_runs(selected.value, get_data=True)
            
            files = run_details.json()['response']['payload']['runs'][0]['results']
            file_dict = {}
            for i in files:
                file_dict[str(i.get('file'))] = {
                    'filename': str(i.get('filename')),
                    'display_name': str(i.get('filename')).split('picked_')[-1],
                    'bounds': i.get('bounds')
                }
            self.selection['run'] = file_dict
            self.selection['run_id'] = run_details.json()['response']['payload']['runs'][0]['id']
            self.selection['run_root_id'] = files[0]['upload']
    
        selected = widgets.Dropdown(
            options=list_runs, 
            value=list_runs[0],
            description="Select a run:"
        )
        i = widgets.interactive(selecter, run=selected)
        display(i)

    
    def get_image_content(self, id, files):
        for image_id in files:
            image_bytes = self.asdc_api.asdc_download(id, image_id).content
            image = Image.open(io.BytesIO(image_bytes))
            files[image_id]['content'] = image


    def get_image_arrays(self, id, files):
        for image_id in files:
            image_bytes = self.asdc_api.asdc_download(id, image_id).content
            img_stream = io.BytesIO(image_bytes)
            file_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            files[image_id]['array'] = img

    def get_crops(self, id):
        try:
            files = self.selection['run']
        except KeyError as e:
            display(Markdown("No run selected. Try running `helper.select_run()` first."))
            return None
            
        for image_id in files:
            crops = []
            for str_bounds in self.selection['run'][image_id]['bounds']:
                bounds = str_bounds.split(',')
                xmin, ymin, xmax, ymax = [int(x) for x in bounds]
                crop = self.selection['run'][image_id]['array'][ymin+5:ymax-5, xmin+5:xmax-5]
                crops.append(crop)
            self.selection['run'][image_id]['crops'] = crops

    
    def plot_figures(self, figures, ncols=1, size=2):
        num_figures = len(figures)
        nrows = math.ceil(num_figures / ncols)
        
        fig, axeslist = plt.subplots(ncols=ncols, nrows=nrows)
        fig.set_size_inches(ncols*size, nrows*size, forward=True)
        for ind, image_id in enumerate(figures):
            try:
                axeslist.ravel()[ind].imshow(figures[image_id]['content'])
            except KeyError:
                axeslist.ravel()[ind].imshow(figures[image_id]['array'])
            axeslist.ravel()[ind].set_title(figures[image_id]['display_name'])
            axeslist.ravel()[ind].set_axis_off()
        
        if num_figures < nrows*ncols:
            difference = (nrows*ncols) - num_figures
            for i in range(difference):
                fig.delaxes(axeslist[nrows-1][ncols-1-i])
        plt.tight_layout() # optional