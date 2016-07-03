# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Core program to exchange datas.
"""
#-------------------------------------------------------------------------------

import os, sys
sys.dont_write_bytecode = True
import hou

from . import define as Define
reload(Define)

#-------------------------------------------------------------------------------
# Houdini data management Class
#-------------------------------------------------------------------------------
class houManager(object):
    """docstring for houManager"""
    def __init__(self):
        super(houManager, self).__init__()


    def getCacheList(self, all_nodes = []):

        all_nodes = hou.pwd().allSubChildren()

        for node in all_nodes:
            if node.type().name().lower() in Define._CACHE_NODES:

                eachNode_dict = {}

                nodeName          = node.name()
                nodePath          = node.path()
                cachePath         = self.unexpStrPath(nodePath)
                envName           = self.env_Analysis(cachePath)
                cacheExpandedPath = node.evalParm("file")
                nodeTypeName      = node.type().name().lower()
                nodeColor         = node.color().rgb()

                eachNode_dict["Name"]           = nodeName
                eachNode_dict["Node Path"]      = nodePath
                eachNode_dict["Cache Path"]     = cachePath
                eachNode_dict["Env"]            = envName
                eachNode_dict["Expanded Path"]  = cacheExpandedPath
                eachNode_dict["Colour"]         = nodeColor

                current_cache_nodes.append(eachNode_dict)

        return current_cache_nodes

#-------------------------------------------------------------------------------
# OS file management class
#-------------------------------------------------------------------------------
class fileManager(object):
    """docstring for fileManager"""
    def __init__(self):
        super(fileManager, self).__init__()


    def copy(self, filepath, remove = False):
        pass


    def copyFile(self, filepath, remove = False):
        pass


    def copyDir(self, dir, remove = False):
        pass

    def fileCheck(self, filepath):
        pass


#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
