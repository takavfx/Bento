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
    { "name":"alembic",         "cat":"Driver",   "parmName":"filename",        "rwtype":["write"]},
    { "name":"alembic",         "cat":"Sop",      "parmName":"fileName",        "rwtype":["read"]},
    { "name":"alembicarchive",  "cat":"Object",   "parmName":"fileName",        "rwtype":["read"]},
    { "name":"dopio",           "cat":"Sop",      "parmName":"file",            "rwtype":["both", "loadfromdisk", [True], [False]]},
    { "name":"dopnet",          "cat":"Object",   "parmName":"playfilesname",   "rwtype":["both", "isplayer", [None], [None]]},
    { "name":"dopnet",          "cat":"Sop",      "parmName":"playfilesname",   "rwtype":["both", "isplayer", [None], [None]]},
    { "name":"file",            "cat":"Sop",      "parmName":"file",            "rwtype":["both", "filemode", [1], [2]]},
    { "name":"filecache",       "cat":"Sop",      "parmName":"file",            "rwtype":["both", "loadfromdisk", [True], [False]]},
    { "name":"gasupres::2.0",   "cat":"Dop",      "parmName":"lowresfile",      "rwtype":["read"]},
    { "name":"geometry",        "cat":"Driver",   "parmName":"sopoutput",       "rwtype":["write"]},
    { "name":"mdd",             "cat":"Sop",      "parmName":"file",            "rwtype":["read"]},
    { "name":"rop_geometry",    "cat":"Sop",      "parmName":"sopoutput",       "rwtype":["write"]},
    { "name":"rop_alembic",     "cat":"Sop",      "parmName":"filename",        "rwtype":["write"]},
    { "name":"tableimport",     "cat":"Sop",      "parmName":"file",            "rwtype":["read"]},
    { "name":"vm_geo_file",     "cat":"Shop",     "parmName":"file",            "rwtype":["read"]},
]

CHILDNODES_EXCEPTION = [
    "dopio",
    "filecache",
    "gasupres::2.0",
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
    "cam",
    "light",
    "hlight",
    "ambient",
    "indirectlight",
    "arnold_light",
    "popobject",
    "shopnet",
    "solver",
    "testgeometry_pighead",
    "testgeometry_rubbertoy",
    "testgeometry_squab",
    "testgeometry_ragdoll",
]
