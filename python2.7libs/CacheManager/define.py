# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Define file for Cache Manager Tool.
"""
#-------------------------------------------------------------------------------

## Define Cache Nodes to deal with this script.
CACHE_NODES = [
    "file",
    "filecache",
    # "alembic",
    # "alembicarchive",
]

CHILDNODES_EXCEPTION = [
    "filecache",
]

## Define Houdini Environment Varialbes. This will also be used for displaying.
ENV_TYPE = [
    '-',
    'HIP',
    'JOB',
]


## Menu Items.
MENU_HELP = "Help"
MENU_RELOAD = "Reload"

## Listed CHACHE_NODES node has children which should be got rid of as default.
PARENTNODES_EXCEPTION = [
    "hlight",
    "arnold_light",

]



#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
