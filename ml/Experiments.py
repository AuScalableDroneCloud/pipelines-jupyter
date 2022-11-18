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

import asdc
await asdc.connect()

import torch

torch.cuda.is_available()

torch.cuda.device_count()

torch.cuda.current_device()

torch.cuda.device(0)

torch.cuda.get_device_name(0)
