# ASDC API templates
# Working wrappers for adding to your library or Jupyter Notebook 

import requests
import json
from getpass import getpass

### Setup your ASDC user access
# 1. go to https://dev2pi.sswp.cosinecrm.com.au
# 2. log in to your SSWP account 
# 3. go to SSWP Apps > Manage account
# 4. Set an App password using the Update Password interface in the middle of the screen

### Obtain a token for API access
# 1. go to https://dev2pi.sswp.cosinecrm.com.au/sswpapps-api/auth
# 2. log in with your ASDC user name and password
# 3. Copy out the token, and paste it into the following cell as a string

class ASDC_API_wrappers:
    base_url = "https://dev2pi.sswp.cosinecrm.com.au/sswpapps-api/"

    header = ""

    def __init__(self, token):
       self.header = {'Authorization': 'Bearer ' + token.strip(), 'Content-Type': 'application/json'}
        #print(self.header)

### Calling:	
# Make calls to https://dev2pi.sswp.cosinecrm.com.au/sswpapps-api/
# use a BEARER type authorisation header containing your token
# and any JSON options as data in the BODY
# API url term:	/sswpapps-api/

    # Basic endpoints:
    
    ####
    # Test connection:
    ####

    # "info":	"Data:{"json":false} Service details, json:false displays HTML-ishly"
    def info_request(self):
        request_url = self.base_url + "info"
        return requests.post(request_url, headers=self.header)

    # "test":	"Test GET endpoint"
    def test_request(self):
        request_url = self.base_url + "test"
        return requests.post(request_url, headers=self.header)

    # "loopback":	"Data:{"__AnyThingForLoopback__":"__SomeDataToConfirm__"} Test POST endpoint"
    def test_loopback(self, payload={'param A': 'shouldReturnThis', 'param B': 'andAlsoThis'}):
        request_url = self.base_url + "loopback"
        return requests.post(request_url, headers=self.header, json=payload)

    # ASDC endpoints:
    
    ####
    # Explore storage:
    ####

    # "uploads":	"Data:{"get":true} List all owned files or by uploads/#id"
    def asdc_uploads(self,  select_no="", get_data=False):
        request_url = self.base_url + "uploads/" + str(select_no)
        return requests.post(request_url, headers=self.header, json={'get': get_data})

    # "uploads/list":	"Data:{"get":true} List all owned files or by uploads/list/#id",
    def asdc_upload_list(self,  select_no="", get_data=False):
        request_url = self.base_url + "uploads/list/" + str(select_no)
        return requests.post(request_url, headers=self.header, json={'get': get_data})

    # "uploads/runs":	"Data:{"get":true} List all owned results from ColourPicker processing, or by runs/#id"
    def asdc_runs(self, select_no="", get_data=False):
        request_url = self.base_url + "uploads/runs/" + str(select_no)
        return requests.post(request_url, headers=self.header, json={'get': get_data})

    # "uploads/swatches":	"Data:{"get":true} List all owned results from ColourRange processing, or by swatches/#id"
    def asdc_swatches(self, select_no="", get_data=False):
        request_url = self.base_url + "uploads/swatches/" + str(select_no)
        return requests.post(request_url, headers=self.header, json={'get': get_data})

    # "uploads/sources":	"Data:{"get":true} List all owned FileUploads processed, or by sources/#id"
    def asdc_sources(self, select_no="", get_data=False):
        request_url = self.base_url + "uploads/sources/" + str(select_no)
        return requests.post(request_url, headers=self.header, json={'get': get_data})

    ####
    # Manage processing:
    ####

    # "processes/source":	"Data:{"put":{"title":"__UniqueProcessName__","list":["myURI","myURI","myURI"]}}"
    # "Start FileUpload process on given list of public facing URI's"
    def asdc_processes_source(self, title, uri_list = []):
        request_url = self.base_url + "processes/source"
        process_data = {'title': title, 'list': uri_list}
        payload = {'put': process_data}
        return requests.post(request_url, headers=self.header, json=payload)

    # "processes/chain":	"Data:{"run":{"title":"__UniqueProcessName__","source":"#id","upload":"#id","space":"__BGR_or_HSV__","bands":"n","spread":"nn"}}"
    # "Chain ColourRange process on file=SOURCE from UPLOAD, through ColourPicker process, per input data, default is 2-bands 98%-spread BGR"
    def asdc_processes_chain(self, title, source_id, upload_id, colorspace="BGR", bands=2, spread=98):
        request_url = self.base_url + "processes/chain"
        process_data = {'title': title, 'source': source_id, "upload": upload_id,
                        'space': colorspace, 'bands': bands, 'spread': spread}
        payload = {'run': process_data}
        return requests.post(request_url, headers=self.header, json=payload)

    # "processes/range":	"Data:{"run":{"title":"__UniqueProcessName__","source":"#id","upload":"#id","space":"__BGR_or_HSV__","bands":"n","spread":"nn"}}"
    # "Start ColourRange process on file=SOURCE from UPLOAD, per input data, default is 2-bands 98%-spread BGR"
    def asdc_processes_range(self, title, source_id, upload_id, colorspace="BGR", bands=2, spread=98):
        request_url = self.base_url + "processes/range"
        process_data = {'title': title, 'source': source_id, "upload": upload_id,
                        'space': colorspace, 'bands': bands, 'spread': spread}
        payload = {'run': process_data}
        return requests.post(request_url, headers=self.header, json=payload)

    # "processes/picker":	"Data:{"run":{"title":"__UniqueProcessName__","swatch":"#id","upload":"#id"}}"
    # "Start ColourPicker process per input data"
    def asdc_processes_picker(self, title, swatch_id, upload_id):
        request_url = self.base_url + "processes/picker"
        process_data = {'title': title, 'swatch': swatch_id, "upload": upload_id}
        payload = {'run': process_data}
        return requests.post(request_url, headers=self.header, json=payload)

    # "processes/refresh":	"Refresh queue status of all processing or by refresh/#id/__range_or_picker_or_source__"
    def asdc_process_refresh(self, select_no=""):
        request_url = self.base_url + "processes/refresh/" + str(select_no)
        return requests.post(request_url, headers=self.header)

    ####
    # Download stored files:
    ####

    # "downloads/#idOfUpload/#idOfFile":	"Data:{"get":true} {"json":true} Return file download as plaintext link, json link, or forcibly GET BLOB"
    def asdc_download(self, upload_id, file_id):
        request_url = self.base_url + "downloads/" + str(upload_id) + "/" + str(file_id)
        return requests.post(request_url, headers=self.header, json={'get': True, 'json': True})

    def asdc_download_by_link(self, request_url):
        return requests.post(request_url, headers=self.header, json={'json': False})

    ####
    # I/O helpers:
    ####
    
    # Creates a human readable response format. 
    def format_human_readable(self, resp):
        print(resp)
        try:
            # print("Raw response: " + str(resp.json()))
            if resp.ok:
                payload = json.dumps(resp.json()['response']['payload'],
                                     indent=4, separators=(',', ':\t'))
                payload = payload.replace('\\"', '"')
                print("Payload: \n" + payload)
            else:
                print(resp.reason + ': ' + resp.json()['response']['message'])
        except json.decoder.JSONDecodeError:
            print(resp.content)


if __name__ == '__main__':
    main = ASDC_API_wrappers()
    main.format_human_readable(main.test_request())
    main.format_human_readable(main.test_loopback())
    main.format_human_readable(main.test_loopback({'MainSentTest':"TestSample"}))
