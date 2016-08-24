# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Core program to exchange datas.
"""
#-------------------------------------------------------------------------------

import sys
sys.dont_write_bytecode = True

import os
import re

import hou

from . import define as Define
reload(Define)

#-------------------------------------------------------------------------------
# Core API to access to Houdini Datas
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

            for item in Define.CACHE_NODES:

                node_type = item.get("name")
                iotype    = item.get("iotype")

                if node.type().name().lower() == node_type:

                    eachNode_dict     = {}
                    node_path         = node.path()
                    node_type         = node.type().name().lower()
                    cache_path        = self.unexpStrPath(node_path, node_type)
                    node_cat          = node.type().category().name()
                    evalCachePath     = self.evalStrPath(node_path, node_type)

                    eachNode_dict["name"]           = node.name()
                    eachNode_dict["node_path"]      = node_path
                    eachNode_dict["cache_path"]     = cache_path
                    eachNode_dict["env"]            = self.analizeEnv(cache_path)
                    eachNode_dict["expanded_path"]  = evalCachePath
                    eachNode_dict["color"]          = node.color().rgb()
                    eachNode_dict["iotype"]         = self.setIoType(node_path, iotype, node_cat)
                    eachNode_dict["editable"]       = self.isEditable(node_path)
                    eachNode_dict["status"]         = self.setStatus(node, node_cat)

                    current_cache_nodes.append(eachNode_dict)

        # print current_cache_nodes

        return current_cache_nodes

    @classmethod
    def unexpStrPath(self, path, opType):
        try:
            for item in Define.CACHE_NODES:
                if item.get("name") == opType:
                    parmName = item.get("parmName")

            parmPath = path + '/' + parmName
            unExpPath = hou.parm(parmPath).unexpandedString()

            return unExpPath
        except:
            return None

    @classmethod
    def evalStrPath(self, path, opType):
        try:
            for item in Define.CACHE_NODES:
                if item.get("name") == opType:
                    parmName = item.get("parmName")

            parmPath = path + '/' + parmName
            evalPath = hou.evalParm(parmPath)

            return evalPath
        except:
            return None

    @classmethod
    def analizeEnv(self, path):
        try:
            obj = re.search("$", path)

            if obj:
                pathTokens = path.split('/')
                return "-"
            else:
                return pathTokens[0]
        except:
            return None

    @classmethod
    def isEditable(self, path):
        pathTokens = path.split("/")

        while range(len(pathTokens)):
            pathTokens.pop(-1)
            node_path = '/'.join(pathTokens)

            if pathTokens >= 2:
                try:
                    node_type = hou.node(node_path).type().name().lower()
                except:
                    return True

                for defNodes in Define.NODES_EXCEPTION:
                    if node_type == defNodes:
                        return False

                for defNodes in Define.CHILDNODES_EXCEPTION:
                    if node_type == defNodes:
                        return False

            else:
                return True
                break


    @classmethod
    def setStatus(self, node, node_cat):

        error  = node.errors()

        if node_cat == "Sop":
            if node.isBypassed():
                return "bypassed"

            if not error == "":
                return "error"


    @classmethod
    def setIoType(self, path, iotype, node_cat):

        if node_cat == "Driver":
            return "write"

        if iotype[0] == "read":
            return iotype[0]

        elif iotype[0] == "write":
            return iotype[0]

        elif iotype[0] == "both":

            parm = path + '/' + iotype[1]
            switch = hou.evalParm(parm)

            if switch in iotype[2]:
                return "read"

            elif switch in iotype[3]:
                return "write"

            else:
                return "both"



#-------------------------------------------------------------------------------
# OS file management class
#-------------------------------------------------------------------------------
class fileManager(object):
    """OS file management class
    """
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



#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
