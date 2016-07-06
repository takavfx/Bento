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
# Houdini data management class
#-------------------------------------------------------------------------------
class houManager(object):

    ALL_NODES = hou.pwd().allSubChildren()

    """docstring for houManager"""
    def __init__(self):
        super(houManager, self).__init__()


    def getCacheList(self):

        current_cache_nodes = []

        for node in self.ALL_NODES:
            if node.type().name().lower() in Define.CACHE_NODES:

                eachNode_dict = {}

                nodeName          = node.name()
                nodePath          = node.path()
                cachePath         = self.unexpStrPath(nodePath)
                envName           = self.analizeEnv(cachePath)
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


    def makeListFromPath(self, path=""):
        path_hierarchy = []
        path_hierarchy = path.split("/")
        return path_hierarchy


    def unexpStrPath(self, path=""):
        cachePath = path + "/file"
        unExpPath = hou.parm(cachePath).unexpandedString()
        return unExpPath

    def analizeEnv(self, path=""):
        pathParts = path[0].split('/')
        if pathParts[0] == None:
            return "-"
        else:
            return pathParts[0]


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
# Other useful methods
#-------------------------------------------------------------------------------

def makeListByDictKey(key, listOfDict, default = None):
    res = []
    for d in listOfDict:
        if d.has_key(key):
            res.append(d[key])
        else:
            res.append(default)
    return res


#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
