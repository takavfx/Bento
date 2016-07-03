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
    # "alembic",
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
    { "key": "name", "title": "Name", "width": 100, "visible": True },
    { "key": "node_path", "title": "Node Path", "width": 200, "visible": True},
    { "key": "cache_path", "title": "Cache Path", "width": 200, "visible": True },
    { "key": "env", "title": "Env", "width": 50, "visible": True},
    { "key": "expanded_path", "title":"Expanded path", "width": 200, "visible": False},
    { "key": "color", "title": "Color", "width": None, "visible": False}
]

# Menu Items
MENU_HELP = "Help"
MENU_RELOAD = "Reload"

#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
