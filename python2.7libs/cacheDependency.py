#-------------------------------------------------------------------------------
## Description
"""
This tool creates FileCache Nodes and ROP dependencies.
"""
#-------------------------------------------------------------------------------

__version__ = "1.0.0"

def main():
    seled_node_list = []
    seled_node_list = hou.selectedNodes()
    if len(seled_node_list) != 0:
        createCacheDependency()


def createCacheDependency():

    count = 0
    created_geo_node_list = []
    node_position = hou.Vector2(0, 0)

    for seled_node in seled_node_list:

        if seled_node.type().name() != "filecache":
            ### Create File Cache SOP Operation ###
            filecache_node = seled_node.createOutputNode("filecache")
            filecache_node.setName("cache_" + seled_node.name(),
                unique_name=True)
            filecache_node.setColor(hou.Color((1, 0.8, 0)))
            input_name = '`opinputpath("%s", 0)`' %filecache_node.path()
        else:
            filecache_node = seled_node
            input_name = '`opinputpath("%s", 0)`' %seled_node.path()

        ### Create Geometry ROP Operation ###
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

        ### Conncet nodes ###
        if count != 0:
            input_node = created_geo_node_list[count-1]
            geo_node.setFirstInput(input_node)

        ### Move created node to organise ###
        geo_node.setPosition(node_position)

        ### Update init value ###
        count += 1
        created_geo_node_list.append(geo_node)
        node_position[1] += -1
