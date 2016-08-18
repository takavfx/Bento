# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Construct Cache Table widget with PySide.GtGui.
"""
#-------------------------------------------------------------------------------

import os, sys
sys.dont_write_bytecode = True

import os
import platform
from functools import partial
from PySide import QtCore, QtGui

import hou

import core
reload(core)
import define as Define
reload(Define)


# CURRENT_PATH = os.path.driname(__file__)


#-------------------------------------------------------------------------------
# QTreeWidget for displaying Cache List
#-------------------------------------------------------------------------------
class cacheTreeWidget(QtGui.QTreeWidget):
    """docstring for cacheTableView"""

    mouseReleased = QtCore.Signal(QtCore.QPoint)
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    HEADER_SETTING = [
        { "key": "node",           "display": "Node",           "width": 200,  "visible": True},
        { "key": "cache_path",     "display": "Cache Path",     "width": 500,  "visible": True},
        { "key": "srcStatus",      "display": "Status",         "width": 50,  "visible": False},
        { "key": "env",            "display": "Env",            "width": 50,   "visible": False},
        { "key": "expanded_path",  "display": "Expanded path",  "width": 200,  "visible": False},
        { "key": "color",          "display": "Color",          "width": None, "visible": False}
    ]


    def __init__(self, parent=None):
        super(cacheTreeWidget, self).__init__()
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
        actionOpenSrcFolder = QtGui.QAction("Replace Cache File", self)
        actionOpenSrcFolder.triggered.connect(partial(self.replaceCacheFile, currentItem))

        actionOpenSrcFolder.setEnabled(False)
        if currentItem.childCount() == 0:
            actionOpenSrcFolder.setEnabled(True)

        cellMenu.addAction(actionOpenSrcFolder)

        cellMenu.addSeparator()

        actionExpandAll = QtGui.QAction("Expand all", self)
        actionExpandAll.triggered.connect(self.expandAll)
        cellMenu.addAction(actionExpandAll)

        actionCollapseAll = QtGui.QAction("Collapse all", self)
        actionCollapseAll.triggered.connect(self.collapseAll)
        cellMenu.addAction(actionCollapseAll)

        cellMenu.exec_(self.mapToGlobal(QtCore.QPoint(pos.x(), pos.y() + self.header().height())))


    def setData(self):

        self.blockSignals(True)
        self.clear()
        self._cacheIDs = []

        #-----------------------------------------------------------------------
        # make tree from path
        #-----------------------------------------------------------------------
        for node in self._cache_nodes:
            path = node.get("node_path")
            cache_path = node.get("cache_path")
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
                self._setChildItem(topItem, pathTokens, path, cache_path)


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


    def _setChildItem(self, parentItem, restTokens, nodePathItem, cachePathItem):
        try:
            nextToken = restTokens.pop(0)

        except IndexError:
            return childItem

        childItem = self._findChild(parentItem, nextToken)

        if childItem is None:
            childItem = QtGui.QTreeWidgetItem(parentItem, [nextToken])

        if len(restTokens) > 0:
            self._setChildItem(childItem, restTokens, nodePathItem, cachePathItem)
        else:
            endItem = childItem
            endItem.setText(self.section("cache_path"), cachePathItem)

            ## Make pare endItem with node path
            each = {}
            each["nodePath"] = nodePathItem
            each["endItem"]  = endItem
            self._cacheIDs.append(each)


    def dirButtonClicked(self, treeItem):
        currentDir = treeItem.text(self.section("cache_path"))
        while currentDir and not os.path.exists(currentDir):
            currentDir = os.path.dirname(currentDir)

        if os.path.exists(currentDir):
            os.chdir(currentDir)

        dir = QtGui.QFileDialog.getExistingDirectory(self, caption='Set Dir', dir=currentDir)

        if dir:
            treeItem.setText(dir)


    def replaceCacheFile(self, treeItem):
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

        else:
            file = hou.ui.selectFile(
                    title = "Replace Cache File"
                )

            if not file == "":
                treeItem.setText(self.section("cache_path"),file)


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
