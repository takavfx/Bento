#-------------------------------------------------------------------------------
## Description
"""
This tool creates FileCache Nodes and ROP dependencies.
"""
#-------------------------------------------------------------------------------

__version__ = "1.0.1"

#-------------------------------------------------------------------------------

import hou

def main():
    sel_nodes = []
    sel_nodes = hou.selectedNodes()
    if len(sel_nodes) != 0:
        createCacheDependency(sel_nodes)


def createCacheDependency(sel_nodes):

    created_geo_node_list = []
    node_pos = hou.Vector2(0, 0)

    for x, node in enumerate(sel_nodes):

        if node.type().name() != "filecache":
            ## Create File Cache SOP Operation
            filecache_node = node.createOutputNode("filecache")
            filecache_node.setName("cache_" + node.name(),
                unique_name=True)
            filecache_node.setColor(hou.Color((1, 0.8, 0)))
            input_name = '`opinputpath("%s", 0)`' %filecache_node.path()
        else:
            filecache_node = node
            input_name = '`opinputpath("%s", 0)`' %node.path()

        ## Create Geometry ROP Operation
        geo_node = hou.node("/out").createNode("geometry")
        geo_node.setName(filecache_node.name())
        geo_node.setParms({
            "sopoutput": filecache_node.parm("file"),
            "trange": filecache_node.parm("trange"),
            "f1": filecache_node.parm("f1"),
            "f2": filecache_node.parm("f2"),
            "f3": filecache_node.parm("f3"),
            "soppath": input_name,
            "take": filecache_node.parm("take"),
            "xformtype": filecache_node.parm("xformtype")
            })
        geo_node.setColor(hou.Color((0, 0.267, 0)))

        ## Conncet nodes
        if x != 0:
            input_node = created_geo_node_list[x-1]
            geo_node.setFirstInput(input_node)

        ## Move created node to organise
        geo_node.setPosition(node_pos)

        ## Update init value
        created_geo_node_list.append(geo_node)
        node_pos[1] += -1
