# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Define file for Cache Manager Tool.
"""
#-------------------------------------------------------------------------------

## Define Cache Nodes to deal with this script.
CACHE_NODES = [
    {"name":"file", "parmName":"file"},
    {"name":"filecache", "parmName":"file"},
    {"name":"alembic", "parmName":"fileName"},
    {"name":"alembicarchive", "parmName":"fileName"},
]

CHILDNODES_EXCEPTION = [
    "filecache",
]

DEBUG_MODE = False

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
NODES_EXCEPTION = [
    "light",
    "hlight",
    "ambient",
    "indirectlight",
    "arnold_light",
]



#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
