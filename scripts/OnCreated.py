# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
This script runs when Houdini nodes are created.

This code is basaed on
"""
#-------------------------------------------------------------------------------

manager_color = (0, 0.4, 1)
generator_color = (0.8, 0.8, 0.8)

# Common node type colors.  These colors affect these types in all contexts.
# Node names are matched identically with keys.
common_type_colors = {

    ### Gray ###
    "null": (0.36, 0.36, 0.36),
    "cam": (0.36, 0.36, 0.36),
    "merge": (0.36, 0.36, 0.36),

    ### Blue: Disk Output ###
    "df_alembic_export": (0, 0.4, 1),
    "PRT_ROPDriver": (0, 0.4, 1),
    "rop_geometry": (0, 0.4, 1),
    "rop_alembic": (0, 0.4, 1),
    "ropnet": (0, 0.4, 1),
    "rf_sd_export": (0, 0.4, 1),
    "rf_particle_export": (0, 0.4, 1),
    "rf_mesh_export": (0, 0.4, 1),

    ### Blue: Composite ###
    "cop2net": (0, 0.2, 0.6),

    ### Yellow: Disk Input ###
    "file": (1, 0.8, 0),
    "filecache": (1, 0.8, 0),
    "filemerge": (1, 0.8, 0),
    "alembic": (1, 0.8, 0),
    "df_alembic_import": (1, 0.8, 0),
    "alembicarchive": (1, 0.8, 0),
    "rf_particle_display": (1, 0.8, 0),
    "rf_mesh_import": (1, 0.8, 0),

    ### Purple Blue: Dop I/O ###
    "dopimport": (0.6, 0.6, 1),
    "dopimportfield": (0.6, 0.6, 1),
    "dopimportrecords": (0.6, 0.6, 1),
    "dopio": (0.6, 0.6, 1),
    "rf_particle_export": (0.6, 0.6, 1),

    ### Purple ###
    "dopnet": (0.4, 0, 0.6),

    ### Green ###
    "object_merge": (0, 0.4, 0),

    ### Dark Green ###
    "geo": (0, 0.267, 0)


}

# Node type information.
node = kwargs["node"]
node_type = node.type()
node_type_name = node_type.name()
type_category_name = node_type.category().name().lower()


# Start with no node color:
node_color = None

# Manager nodes (sopnet, chopnet, ropnet, etc).
if node_type.isManager():
    node_color = manager_color

# Common node types (nulls, switches, etc) are colored the same across
# different contexts.
elif node_type_name in common_type_colors:
    node_color = common_type_colors[node_type_name]


# If we found a color mapping, set the color of the node.
if node_color is not None:
    node.setColor(hou.Color(node_color))
