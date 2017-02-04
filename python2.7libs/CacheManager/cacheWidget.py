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

import imp
try:
    imp.find_module('PySide2')
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *

import hou

import core
reload(core)
import define as Define
reload(Define)


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


#-------------------------------------------------------------------------------
# QTreeWidget for displaying Cache List
#-------------------------------------------------------------------------------
class cacheTreeWidget(QTreeWidget):
    """docstring for cacheTableView"""

    mouseReleased = QtCore.Signal(QtCore.QPoint)
    keyPressed = QtCore.Signal(QKeyEvent)

    HEADER_SETTING = Define.HEADER_SETTING

    def __init__(self, parent=None):
        super(cacheTreeWidget, self).__init__(parent)
        self.initSettings()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def initSettings(self):
        self._cache_nodes = core.houManager.getCacheList()
        self._initUI()

    def _initUI(self):

        self.setColumnCount(len(self.HEADER_SETTING))
        headerLabels = self.makeListByDictKey("display", self.HEADER_SETTING, "")
        self.setHeaderLabels(headerLabels)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
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

        cellMenu = QMenu(self)
        currentItem = self.itemAt(pos.x(), pos.y())

        if currentItem is None:
            return

        ## Replace Cache File
        actionReplaceCacheFile = QAction("Replace Cache File", self)
        actionReplaceCacheFile.triggered.connect(partial(self._replaceCacheFile, currentItem))

        actionReplaceCacheFile.setEnabled(False)
        if self._hasCacheImport(currentItem):
            actionReplaceCacheFile.setEnabled(True)

        cellMenu.addAction(actionReplaceCacheFile)

        cellMenu.addSeparator() ##----------------------------------------------

        ## Forcus selected item
        actionFocusThisNode = QAction("Focus this node", self)
        actionFocusThisNode.triggered.connect(partial(self.focusThisNode, currentItem))

        actionFocusThisNode.setEnabled(False)
        if self.isTopItem(currentItem):
            actionFocusThisNode.setEnabled(True)

        cellMenu.addAction(actionFocusThisNode)


        cellMenu.addSeparator() ##----------------------------------------------

        actionExpandAll = QAction("Expand all", self)
        actionExpandAll.triggered.connect(self.expandAll)
        cellMenu.addAction(actionExpandAll)

        actionCollapseAll = QAction("Collapse all", self)
        actionCollapseAll.triggered.connect(self.collapseAll)
        cellMenu.addAction(actionCollapseAll)

        cellMenu.addSeparator() ##----------------------------------------------

        # Debug
        if Define.DEBUG_MODE:
            debug = QAction("Debug", self)
            debug.triggered.connect(self.debugfunc)

            cellMenu.addAction(debug)


        cellMenu.exec_(self.mapToGlobal(QtCore.QPoint(pos.x(), pos.y() + self.header().height())))


    def setData(self):

        self.blockSignals(True)
        self.clear()

        #-----------------------------------------------------------------------
        # make tree from path
        #-----------------------------------------------------------------------
        for node in self._cache_nodes:
            path       = node.get("node_path")
            cache_path = node.get("cache_path")
            rwtype     = node.get("rwtype")
            editable   = node.get("editable")
            status     = node.get("status")

            pathTokens = path.split("/")
            pathTokens.pop(0)

            if len(pathTokens)==0:
        		continue

            topToken = pathTokens.pop(0)
            rootItem = self.invisibleRootItem()
            topItem = self.findChild(rootItem, topToken)

            if topItem is None:
                topItem = QTreeWidgetItem(rootItem, [topToken])

            if len(pathTokens) > 0:
                self._setChildItem(topItem, pathTokens, path, cache_path, rwtype, editable, status)

        self.sortItems(self.section("node"), QtCore.Qt.AscendingOrder)
        self.expandAll()
        self.blockSignals(False)
        self._setHeaderWidth()


    def findChild(self, item, nodeName):

        for idx in range(item.childCount()):
            childItem = item.child(idx)
            if nodeName == childItem.text(0):
                return childItem

        return None


    def _setChildItem(self, parentItem, restTokens, nodePathItem, cachePathItem, rwtype, editable, status):

        try:
            nextToken = restTokens.pop(0)

        except IndexError:
            return childItem

        childItem = self.findChild(parentItem, nextToken)

        if childItem is None:
            childItem = QTreeWidgetItem(parentItem, [nextToken])
            self.setStatus(childItem, cachePathItem, editable, status)

        if len(restTokens) > 0:
            self._setChildItem(childItem, restTokens, nodePathItem, cachePathItem, rwtype, editable, status)

        else:
            childItem.setText(self.section("cache_path"), cachePathItem)
            childItem.setToolTip(self.section("cache_path"), cachePathItem)
            childItem.setText(self.section("rwtype"), rwtype)
            childItem.setText(self.section("status"), status)
            childItem.setText(self.section("editable"), str(editable))


    def setStatus(self, treeItem, cachePathItem, editable, status):
        if not editable:
            treeItem.setHidden(True)
        if status == "bypassed":
            # treeItem.setForeground(self.section("node"),
            #                         QBrush(QColor(Define.BYPASSED_COLOR)))
            treeItem.setForeground(self.section("cache_path"),
                                    QBrush(QColor(Define.BYPASSED_COLOR)))
            treeItem.setForeground(self.section("rwtype"),
                                    QBrush(QColor(Define.BYPASSED_COLOR)))
            treeItem.setForeground(self.section("status"),
                                    QBrush(QColor(Define.BYPASSED_COLOR)))

        if status == "error":
            # treeItem.setForeground(self.section("node"),
            #                         QBrush(QColor(Define.ERRORS_COLOR)))
            treeItem.setForeground(self.section("cache_path"),
                                    QBrush(QColor(Define.ERRORS_COLOR)))
            treeItem.setForeground(self.section("rwtype"),
                                    QBrush(QColor(Define.ERRORS_COLOR)))
            treeItem.setForeground(self.section("status"),
                                    QBrush(QColor(Define.ERRORS_COLOR)))


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
                treeItem.setText(self.section("cache_path"), file)
                treeItem.setToolTip(self.section("cache_path"), file)
                self.setParm(treeItem, file)

        else:
            file = hou.ui.selectFile(
                    title = "Replace Cache File"
                )

            if not file == "":
                treeItem.setText(self.section("cache_path"),file)
                self.setParm(treeItem, file)
                treeItem.setToolTip(self.section("cache_path"), file)


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


    def isTopItem(self, treeItem):
        parent = treeItem.parent()
        if not parent:
            return False
        else:
            return True


    def switchHeaderVisible(self, idx):

        visible = self.isColumnHidden(idx)

        if visible:
            self.showColumn(idx)

        else:
            self.hideColumn(idx)


    def switchRwVisible(self):
        self.switchHeaderVisible(self.section("rwtype"))


    def showNodesToggle(self, rwtype):
        ritems = self.findItems("read", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, self.section("rwtype"))
        witems = self.findItems("write", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, self.section("rwtype"))

        for ritem in ritems:

            if ritem.text(self.section("editable")) == "False":
                continue

            if rwtype == "read":
                ritem.setHidden(False)
            elif rwtype == "write":
                ritem.setHidden(True)
            elif rwtype == "both":
                ritem.setHidden(False)

        for witem in witems:

            if witem.text(self.section("editable")) == "False":
                continue

            if rwtype == "read":
                    witem.setHidden(True)
            elif rwtype == "write":
                    witem.setHidden(False)
            elif rwtype == "both":
                    witem.setHidden(False)

        self.showNodesStatus = rwtype


    def reload(self):
        self.clear()
        self._cache_nodes = core.houManager.getCacheList()
        self.setData()


    def debugfunc(self):
        print "test"


    def makeListByDictKey(self, key, listOfDict, default = None):

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
