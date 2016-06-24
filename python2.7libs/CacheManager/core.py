# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Core program to exchange datas.
"""
#-------------------------------------------------------------------------------

import os, sys
import hou

def getCacheList(all_nodes = []):
    current_cache_nodes = []

    # all_nodes = hou.pwd().allSubChildren()

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

def copy(dirMan, remove = False):
    """Copy main method. Can be run from threading or command process.

    :param dirMan: <DirectoryMan> should holds copy information.

    :param remove: <bool> True if remove source path files after copy process.

    :return: <bool> True if successed.
    """

    if os.path.isdir(dirMan.srcPath):
        return copyDir(dirMan, remove)

    elif os.path.isfile(dirMan.srcPath):
        return copyFile(dirMan, remove)

    else:
        return False


def copyFile(dirMan, remove = False):

    if not os.path.exists(os.path.dirname(dirMan.dstPath)):
        os.makedirs(os.path.dirname(dirMan.dstPath))

    actionLabel = "Copy"
    action = shutil.copy

    if remove:
        actionLabel = "Move"
        action = shutil.move

    logger.info("%s from %s to %s" % (actionLabel, dirMan.srcPath, dirMan.dstPath))
    action(dirMan.srcPath, dirMan.dstPath)
    return True


def copyDir(dirMan, remove = False):

    if os.path.exists(dirMan.dstPath):
        shutil.rmtree(dirMan.dstPath)

    if not os.path.exists(os.path.dirname(dirMan.dstPath)):
        os.makedirs(os.path.dirname(dirMan.dstPath))

    actionLabel = "Copy"
    action = shutil.copytree

    if remove:
        actionLabel = "Move"
        action = shutil.move

    logger.info("%s from %s to %s" % (actionLabel, dirMan.srcPath, dirMan.dstPath))
    action(dirMan.srcPath, dirMan.dstPath)
