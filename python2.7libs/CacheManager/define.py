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
    {"name":"dopio", "parmName":"file"},

]

CHILDNODES_EXCEPTION = [
    "filecache",
    "dopio",
    "df_alembic_import",
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
