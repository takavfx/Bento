#-------------------------------------------------------------------------------
## Description
"""
Create Cache Dependency by just cliking.
"""
#-------------------------------------------------------------------------------

__version__ = "1.0.0"

import hou

def main():
    sel_cache = hou.ui.selectFile(title="Select BGEO cache")

    if len(sel_cache) >= 1:
        crDlp = hou.node("/shop").createNode("vm_geo_file")
        crDlp.setParms({"file": sel_cache})
        dlp_path = crDlp.path()

        crGeo = hou.node("/obj").createNode("geo", node_name="geo_dlp1")
        crGeo.setParms({"shop_geometrypath": dlp_path})
        fileobj = crGeo.node("file1")
        fileobj.destroy()
