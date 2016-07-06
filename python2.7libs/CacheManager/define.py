# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Define file for Cache Manager Tool.
"""
#-------------------------------------------------------------------------------

# Define Cache Nodes to deal with this script
CACHE_NODES = [
    "file",
    "filecache"
    "alembic",
    # "alembicarchive"
]


# Define Houdini Environment Varialbes. This will also be used for displaying.
ENV_TYPE = [
    '-',
    'HIP',
    'JOB'
]

# Define Header Items
HEADER_ITEMS = [
    { "key": "name",           "display": "Name",           "width": 100,  "visible": False},
    { "key": "node",           "display": "Node",           "width": 200,  "visible": True},
    { "key": "cache_path",     "display": "Cache Path",     "width": 500,  "visible": True},
    { "key": "srcStatus",      "display": "Status",         "width": 50,  "visible": True},
    { "key": "env",            "display": "Env",            "width": 50,   "visible": False},
    { "key": "expanded_path",  "display": "Expanded path",  "width": 200,  "visible": False},
    { "key": "color",          "display": "Color",          "width": None, "visible": False}
]

# Menu Items
MENU_HELP = "Help"
MENU_RELOAD = "Reload"

#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
