# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
This file is not for releasing, just for testing.
"""
#-------------------------------------------------------------------------------

import hou

from PySide import QtCore
from PySide import QtGui

# from . import hqt
from . import define as Define
# from . import core

# reload(hqt)
reload(Define)
# reload(core)


class CacheManager(QtGui.QWidget):
    """docstring for CacheManager"""

    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Initialise the list of Current Cache Nodes in each HIP.
        self.current_cache_nodes = []

        self.initUI()

    def initUI(self):

        ## Create MenuBar and MenuItems
        self._createMenubar()
        self._createLoadMenu()

        ## Layout: table_layout
        self._createTableView()

        table_layout = QtGui.QVBoxLayout()
        table_layout.addWidget(self.table_view)

        ## Layout: body_layout (Main)
        body_layout = QtGui.QVBoxLayout()
        body_layout.addLayout(table_layout)
        body_layout.setSpacing(10)
        body_layout.setContentsMargins(0, 0, 5, 0)

        self.setLayout(body_layout)


    def _createMenubar(self):

        self.menuBar = QtGui.QMenuBar()
        self.menuBar.setFixedHeight(25)

        self.menuBar.cornerWidget(QtCore.Qt.TopRightCorner)


    def _createLoadMenu(self):

        file_menu = QtGui.QMenu(self)

        reload_menu = QtGui.QMenu("Reload", self)

        file_menu.addMenu(reload_menu)
        file_action = self.menuBar.addAction("File")
        file_action.setMenu(file_menu)


    def _createTableView(self):

        self.table_view = CacheTableView(self)



class CacheTableView(QtGui.QTableView):
    """docstring for CacheTableView"""
    def __init__(self, parent):
        super(CacheTableView, self).__init__(parent)
        self._parent = parent
        self.initSettings()

    def initSettings(self):
        cache_list = self.getCacheList()
        table_model = CacheTableModel(data = cache_list)
        self.setModel(table_model)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

    def setColumnWidthWithKey(self, width, **kargs):

        col = self.store().getHeaderSectionByKey(**kargs)

        if col > -1:
            self.setColumnWidth(col, width)

    def getCacheList(self):
        current_cache_nodes = []

        nodes = hou.pwd().allSubChildren()

        for node in nodes:
            if node.type().name().lower() in Define._CACHE_NODES:

                eachNode_dict = {}

                nodeName = node.name()
                nodePath = node.path()
                cachePath = self.unexpStrPath(nodePath)
                envName = self.env_Analysis(cachePath)
                cacheExpandedPath = node.evalParm("file")
                nodeTypeName = node.type().name().lower()
                nodeColor = node.color().rgb()

                eachNode_dict["Name"] = nodeName
                eachNode_dict["Node Path"] = nodePath
                eachNode_dict["Cache Path"] = cachePath
                eachNode_dict["Env"] = envName
                eachNode_dict["Expanded Path"] = cacheExpandedPath
                eachNode_dict["Colour"] = nodeColor

                current_cache_nodes.append(eachNode_dict)

        return current_cache_nodes



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


    def __init__(self, parent = None, data = []):
        super(CacheTableModel, self).__init__(parent)

        self._items = data

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._items)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self._items[0])

    def data(self, index, role = QtCore.QModelIndex()):

        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._items):
            return None

        if index.column() == len(Define._HEADER_ITEMS):
            return None

        hkey = Define._HEADER_ITEMS[index.column()]["key"]
        hType = Define._HEADER_ITEMS[index.column()]["type"]

        if role == QtCore.Qt.DisplayRole:

            if hType in ["string", "int"]:
                return sValue

            if hType ==

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):

        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:

            if section < len(Define._HEADER_ITEMS):
                return Define._HEADER_ITEMS[section]["title"]

            else:
                return None

        return None

    def setColumnVisibe(self):
        if visible:
            self.showColumn()
        else:
            self.hideColum.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    # def getHeaderTitleByKey(arg):
    #     for i in

#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
