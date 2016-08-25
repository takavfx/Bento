# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Define file for Cache Manager Tool.
"""
#-------------------------------------------------------------------------------

## Define Cache Nodes to deal with this script.
CACHE_NODES = [
    {"name":"file",             "parmName":"file",            "iotype":["both", "filemode", [1], [2]]},
    {"name":"filecache",        "parmName":"file",            "iotype":["both", "loadfromdisk", [True], [False]]},
    {"name":"alembic",          "parmName":"fileName",        "iotype":["read"]},
    {"name":"alembicarchive",   "parmName":"fileName",        "iotype":["read"]},
    {"name":"dopio",            "parmName":"file",            "iotype":["both", "loadfromdisk", [True], [False]]},
    {"name":"geometry",         "parmName":"sopoutput",       "iotype":["write"]},
    {"name":"rop_geometry",     "parmName":"sopoutput",       "iotype":["write"]},
    {"name":"alembic",          "parmName":"filename",        "iotype":["write"]},
    {"name":"rop_alembic",      "parmName":"filename",        "iotype":["write"]},
    {"name":"dopnet",           "parmName":"playfilesname",   "iotype":["both", "isplayer", [None], [None]]},
    {"name":"vm_geo_file",      "parmName":"file",            "iotype":["read"]},
]

CHILDNODES_EXCEPTION = [
    "filecache",
    "dopio",
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
    "cam",
    "testgeometry_pighead",
    "testgeometry_rubbertoy",
    "testgeometry_squab",
    "testgeometry_ragdoll",
]



#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
