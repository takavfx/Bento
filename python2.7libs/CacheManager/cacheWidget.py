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

    HEADER_SETTING = Define.CACHE_ITEMS

    def __init__(self, parent=None):
        super(cacheTreeWidget, self).__init__()
        self.cache_nodes = core.houManager().getCacheList()
        self._initSettings()
        self.childItems = []

        # self._makeLevelList()


    def _initSettings(self):

        self.setColumnCount(len(self.HEADER_SETTING))
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        headerLabels = core.makeListByDictKey("display", self.HEADER_SETTING, "")
        self.setHeaderLabels(headerLabels)
        self.setSortingEnabled(True)
        self._setHeaderWidth()
        self._setHeaderVisible()
        # self.itemChanged.connect(self.checkItemEvent)
        # self.customContextMenuRequested.connect(self.showCellMenu)


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


    # def showCellMenu(self, pos):
    #
    #     cellMenu = QtGui.QMenu(self)
    #     currentItem = self.itemAt(pos.x(), pos.y())



    def setData(self, shotData, category = None, uncheckAll = False):

        for node in self.cache_nodes:
            path = node.get("node_path")

            for n, level in path:
                self.childItem(level)



    def _make_level(self, widget):

        for cache_node in self.cache_nodes:
            node_paths = cache_node.get("node_path")

            for path in node_paths:
                level = root.appendChild(path)


    def _makeLevelTreeStructure(lst):

        items = []
        while len(lst):
            (k,v,n) = lst.pop(0)
            item = QTreeWidgetItem(QStringList(QString(str(k))))
            item.setData(0,Qt.UserRole,v)
            items.append(item)
            if n is not None:
                items[-1].addChildren( make_tree(n) )

        return items



    lst = [("0",0,None),
           ("1",1,
            [
                ("1-0",10,None),
                ("1-1",11,None),
                ("1-2",12,
                 [
                        ("1-2-0",120,None),
                        ("1-2-1",121,None)
                        ]
                 ),
                ("1-3",13,None)
                ]
            ),
           ["2",2,None]]



#-------------------------------------------------------------------------------
# QTreeWidget for displaying Cache List
#-------------------------------------------------------------------------------
class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class CacheItemModel(QtCore.QAbstractItemModel):
    """docstring for CacheItemModel"""
    def __init__(self, node_path, parent=None):
        super(CacheItemModel, self).__init__()
        self.arg = arg


#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
