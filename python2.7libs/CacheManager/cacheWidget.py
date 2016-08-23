# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Construct Cache Table widget with PySide.GtGui.
"""
#-------------------------------------------------------------------------------

import sys
sys.dont_write_bytecode = True

import os
import re
import platform
from functools import partial

from PySide import QtCore, QtGui

import hou

import core
reload(core)
import define as Define
reload(Define)


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


#-------------------------------------------------------------------------------
# QTreeWidget for displaying Cache List
#-------------------------------------------------------------------------------
class cacheTreeWidget(QtGui.QTreeWidget):
    """docstring for cacheTableView"""

    mouseReleased = QtCore.Signal(QtCore.QPoint)
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)



    HEADER_SETTING = [
        { "key": "node",           "display": "Node",           "width": 200,  "visible": True},
        { "key": "cache_path",     "display": "Cache Path",     "width": 450,  "visible": True},
        { "key": "env",            "display": "Env",            "width": 50,   "visible": True},
        { "key": "srcStatus",      "display": "Status",         "width": 50,   "visible": True},
        { "key": "expanded_path",  "display": "Expanded path",  "width": 200,  "visible": False},
        { "key": "color",          "display": "Color",          "width": None, "visible": False}
    ]


    def __init__(self, parent=None):
        super(cacheTreeWidget, self).__init__(parent)
        self.tree_items = {}
        self._cache_nodes = core.houManager.getCacheList()
        self._initUI()
        delegate = StatusDelegate(self)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def _initUI(self):

        self.setColumnCount(len(self.HEADER_SETTING))
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        headerLabels = self.makeListByDictKey("display", self.HEADER_SETTING, "")
        self.setHeaderLabels(headerLabels)
        self.setSortingEnabled(True)
        self._setHeaderWidth()
        self._setHeaderVisible()
        self.setData()
        # self.itemChanged.connect(self.checkItemEvent)
        self.customContextMenuRequested.connect(self.showCellMenu)


    def _setHeaderWidth(self):

        for i, setting in enumerate(self.HEADER_SETTING):
            width = setting.get("width")

            if width is not None:
                self.setColumnWidth(i, width)


    def _setHeaderVisible(self):

        for i, setting in enumerate(self.HEADER_SETTING):
            visible = setting.get("visible")

            if visible is False:
                self.hideColumn(i)


    def _makeHeaderLabels(self):
        header_list = []
        for item in self.HEADER_ITEMS:
            if item:
                header_list.append(item)
        return header_list


    def section(self, key):
        for i, setting in enumerate(self.HEADER_SETTING):

            if setting.get("key") == key:
                return i

        raise RuntimeError("No %s key found in table setting." % key)

    def showCellMenu(self, pos):
        """Create menu for right click on the tree widget and show.

        :param pos: <QtCore.QPoint> mouse click position.
        """

        cellMenu = QtGui.QMenu(self)
        currentItem = self.itemAt(pos.x(), pos.y())

        if currentItem is None:
            return

        ## Replace Cache File
        actionReplaceCacheFile = QtGui.QAction("Replace Cache File", self)
        actionReplaceCacheFile.triggered.connect(partial(self._replaceCacheFile, currentItem))

        actionReplaceCacheFile.setEnabled(False)
        if self._hasCacheImport(currentItem):
            actionReplaceCacheFile.setEnabled(True)

        cellMenu.addAction(actionReplaceCacheFile)

        cellMenu.addSeparator() ##----------------------------------------------

        ## Forcus selected item
        actionFocusThisNode = QtGui.QAction("Focus this node", self)
        actionFocusThisNode.triggered.connect(partial(self.focusThisNode, currentItem))

        # actionFocusThisNode.setEnabled(False)
        # if self._hasCacheImport(currentItem):
        #     actionFocusThisNode.setEnabled(True)

        cellMenu.addAction(actionFocusThisNode)


        cellMenu.addSeparator() ##----------------------------------------------

        actionExpandAll = QtGui.QAction("Expand all", self)
        actionExpandAll.triggered.connect(self.expandAll)
        cellMenu.addAction(actionExpandAll)

        actionCollapseAll = QtGui.QAction("Collapse all", self)
        actionCollapseAll.triggered.connect(self.collapseAll)
        cellMenu.addAction(actionCollapseAll)

        cellMenu.addSeparator() ##----------------------------------------------

        # Debug
        if Define.DEBUG_MODE:
            debug = QtGui.QAction("Debug", self)
            debug.triggered.connect(partial(self.getNodePath, currentItem))

            cellMenu.addAction(debug)


        cellMenu.exec_(self.mapToGlobal(QtCore.QPoint(pos.x(), pos.y() + self.header().height())))


    def setData(self):

        self.blockSignals(True)
        self.clear()
        self._nodeIDs = []

        #-----------------------------------------------------------------------
        # make tree from path
        #-----------------------------------------------------------------------
        for node in self._cache_nodes:
            path       = node.get("node_path")
            cache_path = node.get("cache_path")
            editable   = node.get("editable")
            error      = node.get("error")

            pathTokens = path.split("/")
            pathTokens.pop(0)

            if len(pathTokens)==0:
        		continue

            topToken = pathTokens.pop(0)
            rootItem = self.invisibleRootItem()
            topItem = self._findChild(rootItem, topToken)

            if topItem is None:
                topItem = QtGui.QTreeWidgetItem(rootItem, [topToken])

            if len(pathTokens) > 0:
                self._setChildItem(topItem, pathTokens, path, cache_path, editable, error)

        self.sortItems(self.section("node"), QtCore.Qt.AscendingOrder)
        self.expandAll()
        self.blockSignals(False)
        self._setHeaderWidth()


    def _findChild(self, item, nodeName):

        for idx in range(item.childCount()):
            childItem = item.child(idx)
            if nodeName == childItem.text(0):
                return childItem

        return None


    def _setChildItem(self, parentItem, restTokens, nodePathItem, cachePathItem, editable, error):

        try:
            nextToken = restTokens.pop(0)

        except IndexError:
            return childItem

        childItem = self._findChild(parentItem, nextToken)

        if childItem is None:
            childItem = QtGui.QTreeWidgetItem(parentItem, [nextToken])
            if not editable:
                childItem.setHidden(True)

        if len(restTokens) > 0:
            self._setChildItem(childItem, restTokens, nodePathItem, cachePathItem, editable, error)

        else:
            endItem = childItem
            endItem.setText(self.section("cache_path"), cachePathItem)
            endItem.setToolTip(self.section("cache_path"), cachePathItem)
            endItem.setText(self.section("srcStatus"), error)

            ## Make paire endItem with node path
            each = {}
            each["nodePath"] = nodePathItem
            each["endItem"]  = endItem
            self._nodeIDs.append(each)


    def _dirButtonClicked(self, treeItem):
        currentDir = treeItem.text(self.section("cache_path"))
        while currentDir and not os.path.exists(currentDir):
            currentDir = os.path.dirname(currentDir)

        if os.path.exists(currentDir):
            os.chdir(currentDir)

        dir = QtGui.QFileDialog.getExistingDirectory(self, caption='Set Dir', dir=currentDir)

        if dir:
            treeItem.setText(dir)


    def _replaceCacheFile(self, treeItem):
        currentPath = treeItem.text(self.section("cache_path"))
        currentDir = os.path.dirname(currentPath)
        if os.path.exists(currentDir):
            file = hou.ui.selectFile(
                    start_directory = currentDir,
                    title           = "Replace Cache File",
                    default_value   = os.path.basename(currentPath)
                )

            if not file == "":
                treeItem.setText(self.section("cache_path"),file)
                self.setParm(treeItem, file)

        else:
            file = hou.ui.selectFile(
                    title = "Replace Cache File"
                )

            if not file == "":
                treeItem.setText(self.section("cache_path"),file)
                self.setParm(treeItem, file)


    def focusThisNode(self, treeItem):
        node_path = self.getNodePath(treeItem)

        if node_path:
            hou.node(node_path).setCurrent(on=True, clear_all_selected=True)
        else:
            return False


    def _hasCacheImport(self, treeItem):
        seled_node_path = self.getNodePath(treeItem)

        for node in self._cache_nodes:
            node_path = node.get('node_path')

            if seled_node_path == node_path:
                return True


    def getNodePath(self, treeItem):
        pathTokens = []
        childPath  = treeItem.text(self.section("node"))
        parentItem = treeItem.parent()

        if parentItem:
            self._setPath(pathTokens, treeItem)

        if pathTokens:
            node_path = '/' + '/'.join(pathTokens)
            return node_path


    def _setPath(self, pathTokens, childItem):
        path = childItem.text(self.section("node"))
        pathTokens.insert(0, path)

        try:
            parentItem = childItem.parent()
        except:
            parentItem = None

        if parentItem:
            self._setPath(pathTokens, parentItem)


    def setParm(self, treeItem, cache_path):
        node_path = self.getNodePath(treeItem)
        node_type = hou.node(node_path).type().name().lower()

        for defNode in Define.CACHE_NODES:
            defNode_type = defNode.get("name")
            if node_type == defNode_type:
                parmName = defNode.get("parmName")

                hou.node(node_path).setParms({parmName:cache_path})


    def makeListByDictKey(self, key, listOfDict, default = None):

        res = []
        for d in listOfDict:
            if d.has_key(key):
                res.append(d[key])
            else:
                res.append(default)
        return res


class StatusDelegate(QtGui.QStyledItemDelegate):
    """docstring for StatusDelegate"""
    def __init__(self, parent):
        super(StatusDelegate, self).__init__(parent)
        self._parent = parent


#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
