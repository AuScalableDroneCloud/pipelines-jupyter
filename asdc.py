"""
# ASDC API v0.1

## Australian Scalable Drone Cloud data access API module

### Initial goals:

- Get tokens to access the WebODM API at https://asdc.cloud.edu.au/api
- Provide convenience functions for calling above API
- Functions for moving drone data to and from cloud storage services, S3, CloudStor etc

### Requirements:
jupyterhub_oauth2 (git url: )


"""

import jupyter_oauth2_api as auth

#Settings should be provided in env variables
# JUPYTERHUB_URL
# JUPYTER_OAUTH2_API_AUDIENCE
# JUPYTER_OAUTH2_CLIENT_ID
# JUPYTER_OAUTH2_SCOPE
# JUPYTER_OAUTH2_AUTH_PROVIDER_URL

import os
# load .env if vars not already in env
if not "JUPYTER_OAUTH2_CLIENT_ID" in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

auth.setup()

