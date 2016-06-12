# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Construct Cache Table with PySide.GtGui.
"""
#-------------------------------------------------------------------------------

import sys, os

from PySide import QtCore, QtGui

from . import define as Define

sys.dont_write_bytecode = True

CURRENT_PATH = os.path.driname(__file__)

class cacheTableView(QtGui.QTreeView):
    """docstring for cacheTableView"""

    mouseReleased = QtCore.Signal(QtCore.QPoint)
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    def __init__(self, parent):
        super(cacheTableView, self).__init__(parent)
        self._parent = parent
        self.cache_nodes = self.getCacheList()
        self.initSettings()

    def initSettings(self):
        # self.verticalHeader().setVisible(False)
        # self.verticalHeader().setMovable(True)
        # self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
        # self.setSortingEnabled(True)
        # self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        # self.setAlternatingRowColors(True)
        self.model = CacheTableModel()
        self.setModel(self.model)


    def unexpStrPath(self, path):
        cachePath = path + "/file"
        unExpPath = hou.parm(cachePath).unexpandedString()
        return unExpPath

    def env_Analysis(self, path):
        pathParts = path[0].split('/')
        if pathParts[0] == None:
            return "-"
        else:
            return pathParts[0]

class CacheTableModel(QtCore.QAbstractTableModel):
    """docstring for CacheTableModel"""

    CACHE_PATH =  QtCore.Qt.UserRole

    def __init__(self, parent = None, data = []):
        super(CacheTableModel, self).__init__(parent)

        self.__items = data

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.__items)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.__items[0]) -1

    def data(self, index, role = QtCore.Qt.DisplayRole):

        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.__items):
            return None

        if role == QtCore.Qt.DisplayRole:
            return self.__items[index.row()].get("title")

        else:
            return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.__items[col].get("title")


    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable


    def setHeaderSetting(self):

        for i, colInfo in enumerate(Define._HEADER_ITEMS):
            self.setColumnVisibe(i, colInfo.get("visible"))
            if colInfo.get("width") is not None:
                self.setColumnWidth(i, colInfo.get("width"))


    def getHeaderSectionByKey(self):
