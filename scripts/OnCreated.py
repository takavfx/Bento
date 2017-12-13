# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
This script runs when Houdini nodes are created.
"""
#-------------------------------------------------------------------------------

from Bento import colornodes

# Node type information.
node = kwargs["node"]
node_type = node.type()
node_type_name = node_type.name()

# Start with no node color:
node_color = None

# Manager nodes (sopnet, chopnet, ropnet, etc).
if node_type.isManager():
    node_color = colornodes.manager_color

# Common node types (nulls, switches, etc) are colored the same across
# different contexts.
elif node_type_name in colornodes.common_type_colors:
    node_color = colornodes.common_type_colors[node_type_name]


# If we found a color mapping, set the color of the node.
if node_color is not None:
    node.setColor(hou.Color(node_color))
