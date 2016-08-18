# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Construct Cache Table widget with PySide.GtGui.
"""
#-------------------------------------------------------------------------------

import os, sys
sys.dont_write_bytecode = True

from PySide import QtCore, QtGui

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

    # HEADER_SETTING = Define.CACHE_ITEMS

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
        self._cache_nodes = core.houManager().getCacheList()
        self._initUI()
        self.childItems = []


    def _initUI(self):

        self.setColumnCount(len(self.HEADER_SETTING))
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        headerLabels = core.makeListByDictKey("display", self.HEADER_SETTING, "")
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

        actionExpandAll = QtGui.QAction("Expand all", self)
        actionExpandAll.triggered.connect(self.expandAll)
        cellMenu.addAction(actionExpandAll)

        actionCollapseAll = QtGui.QAction("Collapse all", self)
        actionCollapseAll.triggered.connect(self.collapseAll)
        cellMenu.addAction(actionCollapseAll)

        cellMenu.addSeparator()

        actionOpenSrcFolder = QtGui.QAction("Open source folder in explorer", self)
        actionOpenSrcFolder.triggered.connect(partial(self.openSrcFolderEvent, currentItem))

        if currentItem.parent() is None:
            actionOpenSrcFolder.setEnabled(False)

        cellMenu.addAction(actionOpenSrcFolder)

        if self._treeType == self.ERROR_TYPE:
            actionOpenSrcFolder.setDisabled(True)

        cellMenu.addAction(actionOpenSrcFolder)

        cellMenu.exec_(self.mapToGlobal(QtCore.QPoint(pos.x(), pos.y() + self.header().height())))


    def setData(self):

        self.blockSignals(True)
        self.clear()

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
                self._addChildItem(topItem, pathTokens, cache_path)

        self.expandAll()
        self.blockSignals(False)
        self._setHeaderWidth()

    def _findChild(self, item, nodeName):

        for idx in range(item.childCount()):
            childItem = item.child(idx)
            if nodeName == childItem.text(0):
                return childItem

        return None


    def _addChildItem(self, parentItem, restTokens, cachePathItem):
        try:
            nextToken = restTokens.pop(0)

        except IndexError:
            return childItem

        childItem = self._findChild(parentItem, nextToken)

        if childItem is None:
            childItem = QtGui.QTreeWidgetItem(parentItem, [nextToken])

        if len(restTokens) > 0:
            self._addChildItem(childItem, restTokens, cachePathItem)
        else:
            endItem = childItem
            endItem.setText(self.section("cache_path"), cachePathItem)


    def openSrcFolderEvent(self, treeItem):
        """Slot called when open source folder menu was clicked.

        :param treeItem: <QtGui.QTreeWidgetItem> tree item clicked.
        """

        if not hasattr(treeItem, "itemData"):
            return

        dirMan = treeItem.itemData
        self.openExplorer(dirMan.srcPath)



class StatusDelegate(QtGui.QStyledItemDelegate):

    SELECTED_BG_COLOR = QtGui.QColor.fromRgb(120, 135, 155)
    UNSELECTED_BG_COLOR = QtGui.QColor.fromRgb(32, 31, 31)
    def __init__(self, parent):
        super(StatusDelegate, self).__init__(parent)
        self._parent = parent

#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
