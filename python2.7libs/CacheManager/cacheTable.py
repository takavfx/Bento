
import hou
import sys, os

from PySide import QtCore, QtGui

from . import hqt
from . import utils as Utils
from . import define as Define

sys.dont_write_bytecode = True

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
