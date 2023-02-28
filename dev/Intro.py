# # ASDC Pipelines
#
# Development documentation and examples
#

# ### Authenticate and get selected project / task data

import asdc
asdc.task_select()


# ### Get selections

print(asdc.selected)
project_id = asdc.selected['project']
task_id = asdc.selected['task']
task_name = asdc.task_dict[task_id]['name']

