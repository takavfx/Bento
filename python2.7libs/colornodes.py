# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
This script for color nodes shelf tool and also used in OnCreated script.
"""
#-------------------------------------------------------------------------------

import hou

manager_color = (0, 0.4, 1)
generator_color = (0.8, 0.8, 0.8)

# Common node type colors.  These colors affect these types in all contexts.
# Node names are matched identically with keys.
common_type_colors = {

    ### Gray ###
    "null": (0.36, 0.36, 0.36),
    "cam": (0.36, 0.36, 0.36),
    "merge": (0.36, 0.36, 0.36),
    "output": (0.36, 0.36, 0.36),

    ### Blue: Disk Output ###
    "df_alembic_export": (0, 0.4, 1),
    "PRT_ROPDriver": (0, 0.4, 1),
    "rop_geometry": (0, 0.4, 1),
    "rop_alembic": (0, 0.4, 1),
    "ropnet": (0, 0.4, 1),

    ### Yellow: Disk Input ###
    "file": (1, 0.8, 0),
    "filecache": (1, 0.8, 0),
    "filemerge": (1, 0.8, 0),
    "alembic": (1, 0.8, 0),
    "alembicarchive": (1, 0.8, 0),

    ### Purple Blue: Dop I/O ###
    "dopimport": (0.6, 0.6, 1),
    "dopimportfield": (0.6, 0.6, 1),
    "dopimportrecords": (0.6, 0.6, 1),
    "dopio": (0.6, 0.6, 1),

    ### Purple ###
    "dopnet": (0.4, 0, 0.6),

    ### Green: Geometry Fetch ###
    "object_merge": (0, 0.4, 0),

    ### Dark Green ###
    "geo": (0, 0.267, 0)


}

def run():
    if len(hou.selectedNodes()) is 0:
        nodes = hou.pwd().allSubChildren()
    else:
        nodes = []
        selected_nodes = hou.selectedNodes()
        for node in selected_nodes:
            children = node.allSubChildren()
            print children
            nodes.append(children)
            print nodes
            return

    for node in nodes:
        node_type = node.type()
        node_type_name = node_type.name()
        type_category_name = node_type.category().name().lower()

        node_color = None

        if node_type.isManager():
            node_color = manager_color

        elif node_type_name in common_type_colors:
            node_color = common_type_colors[node_type_name]

        if node_color is not None:
            node.setColor(hou.Color(node_color))
