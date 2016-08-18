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
    """Core API to access to Houdini Datas
    """
    def __init__(self):
        super(houManager, self).__init__()

    @classmethod
    def getCacheList(self):
        ## Init variable
        current_cache_nodes = []
        all_nodes = hou.pwd().allSubChildren()

        for node in all_nodes:
            if node.type().name().lower() in Define.CACHE_NODES:

                eachNode_dict     = {}
                node_path         = node.path()
                cachePath         = self.unexpStrPath(node_path)

                eachNode_dict["name"]           = node.name()
                eachNode_dict["node_path"]      = node_path
                eachNode_dict["cache_path"]     = self.unexpStrPath(node_path)
                eachNode_dict["env"]            = self.analizeEnv(cachePath)
                eachNode_dict["expanded_path"]  = node.evalParm("file")
                eachNode_dict["color"]         = node.color().rgb()

                current_cache_nodes.append(eachNode_dict)

        return current_cache_nodes


    @classmethod
    def unexpStrPath(self, path=""):
        cachePath = path + "/file"
        unExpPath = hou.parm(cachePath).unexpandedString()
        return unExpPath


    @classmethod
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
