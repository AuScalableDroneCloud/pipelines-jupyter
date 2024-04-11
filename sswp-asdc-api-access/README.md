# Use case helpers and notes for SSWP/ASDC application API

This repository contains:
 - API documentation
```
sswp-asdc-api-access\SSWP _ ASDC application API services.pdf
```

 - Simple wrappers/stubs for managing tokens and data when calling the API from Python
```
sswp-asdc-api-access\jupyter\ASDC_API_support.py
```

 - A Jupyter notebook demonstrating API functions through a practical workflow approach to the ColourPicker
```
sswp-asdc-api-access\jupyter\ASDC_API_ColourPicker_Workflow.ipynb
```

 - Sample images for expermimental ColourPicker runs against a swatch collaged from Orange Hawkweed pixel clippings
 ```
 sswp-asdc-api-access\images
 ```

---------------------------------------------------------

## SSWP / ASDC application API services
```

Calling : Make calls to https://abcqrsxyz/sswpapps-api/ with a BEARER type authorisation header containing your token and any JSON options as data in the BODY

API url term : /sswpapps-api/

info : Data:{"json":false} Service details, json:false displays HTML-ishly
test : Test GET endpoint
loopback : Data:{"__AnyThingForLoopback__":"__SomeDataToConfirm__"} Test POST endpoint


```


```
***
"uploads" calls return summaries of objects with upload relations
Use Data:{"get":true} to inspect the object's referenced contents (eg:files links)
***

uploads : Data:{"get":true} List all owned files or by uploads/#id
uploads/list : Data:{"get":true} List all owned files or by uploads/list/#id
uploads/swatches : Data:{"get":true} List all owned results from ColourRange processing, or by swatches/#id
uploads/runs : Data:{"get":true} List all owned results from ColourPicker processing, or by runs/#id
uploads/sources : Data:{"get":true} List all owned FileUploads processed, or by sources/#id


```


```
***
"processes" calls trigger cloud activities, uploading sources and for ColourPicking steps
***

processes/range : Data:{"run":{"title":"__UniqueProcessName__","source":"#id","upload":"#id","space":"__BGR_or_HSV__","bands":"n","spread":"nn"}} 
Start ColourRange process on file=SOURCE from UPLOAD, per input data, default is 2-bands 98%-spread BGR

processes/picker : Data:{"run":{"title":"__UniqueProcessName__","swatch":"#id","upload":"#id"}} 
Start ColourPicker process per input data

processes/chain : Data:{"run":{"title":"__UniqueProcessName__","source":"#id","upload":"#id","space":"__BGR_or_HSV__","bands":"n","spread":"nn"}} 
Chain ColourRange process on file=SOURCE from UPLOAD, through ColourPicker process, per input data, default is 2-bands 98%-spread BGR

processes/source : Data:{"put":{"title":"__UniqueProcessName__","list":["myURI","myURI","myURI"]}} 
Start FileUpload process on given list of public facing URI's


```


```
***
"processes" calls require periodic refresh to inspect progress and flush cloud signalling
Process id's may be non-unique, specify the process type if using refresh to indicate status by single id
***

processes/refresh : Refresh queue status of all processing or by refresh/#id/__range_or_picker_or_source__


```


```
***
"downloads" are accomplished by polling the API, yielding presigned s3 access
***

downloads/#idOfUpload/#idOfFile : Data:{"get":true} {"json":true} Return file download as plaintext link, json link, or GET as BLOB

```

