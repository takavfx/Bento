#-------------------------------------------------------------------------------
## Description
"""
Create Cache Dependency by just cliking.
"""
#-------------------------------------------------------------------------------

__version__ = '2.0.0'

#-------------------------------------------------------------------------------

import hou

HOUDINI_MAJOR_VERSION = hou.applicationVersion()[0]


def main():
    sel_nodes = hou.selectedNodes()
    if len(sel_nodes) > 1:
        hou.ui.setStatusMessage("Single node slection is only available.",
                            severity=hou.severityType.Error)
        return

    elif sel_nodes[0].type().name() != 'geo':
        hou.ui.setStatusMessage("Geometry Network node is only available.",
        severity=hou.severityType.Error)
        return

    sel_cache = hou.ui.selectFile(title='Select BGEO cache')
    if len(sel_cache) == 0:
        hou.ui.setStatusMessage("Any cache file is not selected.",
                            severity=hou.severityType.Error)
        return


    if len(sel_nodes) == 1 and sel_nodes[0].type().name() == 'geo':
        print 'test'
        for node in sel_nodes:
            dlp = createFileLoader(sel_cache)
            node.setParms({'shop_geometrypath': dlp.path()})

    else:
        dlp = createFileLoader(sel_cache)
        crGeo = hou.node('/obj').createNode('geo', node_name='geo_dlp1', run_init_scripts=True)
        crGeo.setParms({'shop_geometrypath': dlp.path()})
        children = crGeo.children()
        for c in children:
            c.destroy()



def createFileLoader(sel_cache):
    if HOUDINI_MAJOR_VERSION <= 15:
        dlp = hou.node('/shop').createNode('vm_geo_file')
    else:
        dlp = hou.node('/mat').createNode('file')
    dlp.setParms({'file': sel_cache})

    return dlp
