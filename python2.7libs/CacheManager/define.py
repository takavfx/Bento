# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Define file for Cache Manager Tool.
"""
#-------------------------------------------------------------------------------

BYPASSED_COLOR = "#ecdd16"

## Define Cache Nodes to deal with this script.
CACHE_NODES = [
    {"name":"file",             "parmName":"file",            "rwtype":["both", "filemode", [1], [2]]},
    {"name":"filecache",        "parmName":"file",            "rwtype":["both", "loadfromdisk", [True], [False]]},
    {"name":"alembic",          "parmName":"fileName",        "rwtype":["read"]},
    {"name":"alembicarchive",   "parmName":"fileName",        "rwtype":["read"]},
    {"name":"dopio",            "parmName":"file",            "rwtype":["both", "loadfromdisk", [True], [False]]},
    {"name":"geometry",         "parmName":"sopoutput",       "rwtype":["write"]},
    {"name":"rop_geometry",     "parmName":"sopoutput",       "rwtype":["write"]},
    {"name":"alembic",          "parmName":"filename",        "rwtype":["write"]},
    {"name":"rop_alembic",      "parmName":"filename",        "rwtype":["write"]},
    {"name":"dopnet",           "parmName":"playfilesname",   "rwtype":["both", "isplayer", [None], [None]]},
    {"name":"vm_geo_file",      "parmName":"file",            "rwtype":["read"]},
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

ERRORS_COLOR = "#ec1616"

HEADER_SETTING = [
    { "key": "node",           "display": "Node",           "width": 200,  "visible": True},
    { "key": "cache_path",     "display": "Cache Path",     "width": 400,  "visible": True},
    { "key": "env",            "display": "Env",            "width": 50,   "visible": False},
    { "key": "rwtype",         "display": "R/W",            "width": 70,   "visible": False},
    { "key": "status",         "display": "Status",         "width": 50,   "visible": True},
    { "key": "expanded_path",  "display": "Expanded path",  "width": 200,  "visible": False},
    { "key": "editable",       "display": "Editable",       "width": None, "visible": False},
    { "key": "color",          "display": "Color",          "width": None, "visible": False},
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
