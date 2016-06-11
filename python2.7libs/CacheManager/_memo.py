


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

        if role == QtCore.Qt.DisplayRole:
            for item in self.items:
            return self._items[index.row()][index.column()]

        else:
            return None


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
            self.hideColumn()

    # def flags(self, index):
    #     return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    # def getHeaderTitleByKey(arg):
    #     for i in



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
