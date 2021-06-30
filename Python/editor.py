import sys
import os
from pathlib import Path
from threading import Thread
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout, QGroupBox, QTableWidget, QHBoxLayout, QVBoxLayout,
                            QPushButton, QToolTip, QMessageBox, QLabel, QStyleFactory, QDialog, QSizePolicy, QAbstractScrollArea, 
                            QHeaderView)
import time


class ImageWidget(QWidget):
    def __init__(self, srcImage, parent=None):
        super(ImageWidget, self).__init__(parent)

        self.tileId = srcImage[0]
        self.imagePath = srcImage[1]

        self.picture = QPixmap(self.imagePath)
        rect = QRect(srcImage[2], srcImage[3], srcImage[4], srcImage[5])
        self.picture = self.picture.copy(rect)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect(0, 0, 64, 64)
        painter.drawPixmap(rect, self.picture)

class TableWidget(QTableWidget):
    def __init__(self, row, col, parent=None):
        super(TableWidget, self).__init__(row, col, parent)

        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)

        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) 
        self.verticalHeader().setDefaultSectionSize(70)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed) 
        self.horizontalHeader().setDefaultSectionSize(70)

        self.cellClicked.connect(self.handleCellClicked)
        # self.adjustSize()
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()  
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.setRowHeight(0, 64)

    def handleCellClicked(self, row, column):
        if self.cellWidget(row, column) is not None:
            tileEditor.tileId = self.cellWidget(row, column).tileId
        else:
            tileEditor.tileId = 'empty'

class Window(QDialog):
    def __init__(self, rows=22, cols=25, parent=None):
        super(Window, self).__init__(parent)

        opLabel = QLabel("Select a tile in editor window, then click game window to add it.\n\nClick save button to save 2D map to file.")
        font = opLabel.font()
        font.setPointSize(10)
        opLabel.setFont(font)
        opLabel.setFixedSize(430, 120)
        opLabel.setWordWrap(True)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(lambda: self.save2_file(rows, cols))  
        # saveButton.setGeometry(100, 0, 100, 30)
        # saveButton.setFixedSize(100, 30)

        topLayout = QVBoxLayout()
        topLayout.addWidget(opLabel)
        topLayout.addWidget(self.saveButton)
        # topLayout.addStretch(1)
        topLayout.setContentsMargins(5, 5, 5, 5)

        # load image resources 
        self.players = []
        self.minions = []
        self.items = []
        self.tiles = []

        resourceManager = resource_manager.ResourceManager.getInstance()
        imgManager = resourceManager.getImgManager()
        loadedTiles = imgManager.getLoadedTileInfo()
        loadedSprites = imgManager.getLoadedSpriteInfo()

        for tileId, tileType, srcFile, x, y, w, h in loadedTiles:
            if tileType == 'Tile':
                self.tiles.append((tileId, srcFile, int(x), int(y), int(w), int(h)))
            elif tileType == 'Item':
                self.items.append((tileId, srcFile, int(x), int(y), int(w), int(h)))

        for spriteId, spriteType, srcFile, x, y, w, h in loadedSprites:
            if spriteType == 'Player':
                self.players.append((spriteId, srcFile, int(x), int(y), int(w), int(h)))
            elif spriteType == 'Minion':
                self.minions.append((spriteId, srcFile, int(x), int(y), int(w), int(h)))

        # make new tileMap data structure
        oldRows, oldCols = len(tileEditor.tileMap), len(tileEditor.tileMap[0])

        for i in range(rows):
            if i >= oldRows:
                tileEditor.tileMap.append([])

        for i in range(rows):
            for j in range(cols):
                if i >= oldRows or j >= oldCols:
                    tileEditor.tileMap[i].append('empty')

        self.createPlayerGroupBox()
        self.createMinionGroupBox()
        self.createItemGroupBox()
        self.createTileGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.playerGroupBox, 1, 0)
        mainLayout.addWidget(self.minionGroupBox, 2, 0)
        mainLayout.addWidget(self.itemGroupBox, 3, 0)
        mainLayout.addWidget(self.tileGroupBox, 4, 0)
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setColumnStretch(0, 1)
        self.setLayout(mainLayout)

        self.changeStyle('windowsvista')
        self.setWindowTitle("TileMap Editor")

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()
    
    def changePalette(self):
        QApplication.setPalette(QApplication.style().standardPalette())

    def createPlayerGroupBox(self):
        self.playerGroupBox = QGroupBox("Player")
        tableWidget = TableWidget(1, 5)

        cnt = 0
        for player in self.players:
            image = ImageWidget(player, tableWidget)
            tableWidget.setCellWidget(cnt / 5, cnt % 5, image)
            cnt += 1
            
        hbox = QHBoxLayout()
        # hbox.setContentsMargins(5, 5, 5, 5)
        hbox.addWidget(tableWidget)
        self.playerGroupBox.setLayout(hbox)

    def createMinionGroupBox(self):
        self.minionGroupBox = QGroupBox("Minion")
        tableWidget = TableWidget(2, 5)

        cnt = 0
        for minion in self.minions:
            image = ImageWidget(minion, tableWidget)
            tableWidget.setCellWidget(cnt / 5, cnt % 5, image)
            cnt += 1

        hbox = QHBoxLayout()
        # hbox.setSizePolicy(QSizePolicy.Expanding,
        #         QSizePolicy.Ignored)
        # hbox.setContentsMargins(5, 5, 5, 5)
        hbox.addWidget(tableWidget)
        self.minionGroupBox.setLayout(hbox)

    def createItemGroupBox(self):
        self.itemGroupBox = QGroupBox("Item")
        tableWidget = TableWidget(2, 5)

        cnt = 0
        for item in self.items:
            image = ImageWidget(item, tableWidget)
            tableWidget.setCellWidget(cnt / 5, cnt % 5, image)
            cnt += 1

        hbox = QHBoxLayout()
        # hbox.setSizePolicy(QSizePolicy.Expanding,
        #         QSizePolicy.Ignored)
        # hbox.setContentsMargins(5, 5, 5, 5)
        hbox.addWidget(tableWidget)
        self.itemGroupBox.setLayout(hbox)

    def createTileGroupBox(self):
        self.tileGroupBox = QGroupBox("Tile")
        tableWidget = TableWidget(2, 5)

        cnt = 0
        for tile in self.tiles:
            image = ImageWidget(tile, tableWidget)
            tableWidget.setCellWidget(cnt / 5, cnt % 5, image)
            cnt += 1

        hbox = QHBoxLayout()
        # hbox.setSizePolicy(QSizePolicy.Expanding,
        #         QSizePolicy.Ignored)
        # hbox.setContentsMargins(5, 5, 5, 5)
        hbox.addWidget(tableWidget)
        self.tileGroupBox.setLayout(hbox)

        # mygameengine.foo_null("100")
        # wId = self.effectiveWinId().__int__()
        # capsule = ctypes.c_void_p(wId)
        # ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
        # handle = ctypes.pythonapi.PyCapsule_GetPointer(capsule, None)
        # win32gui.SetWindowLong(handle, win32con.GWL_WNDPROC, self.new_window_procedure)  

    def save2_file(self, rows, cols):
        with open('editor_level.txt', 'w') as filehandle:
            filehandle.write('editor_level.txt\n')
            filehandle.write(str(rows) + '\n')
            filehandle.write(str(cols) + '\n')
            for row in tileEditor.tileMap:
                for tile in row:
                    filehandle.write(tile + " ")
                filehandle.write('\n')
        print('Successfully wrote to editor_level.txt')
        print('new TileMap is', tileEditor.tileMap)

def game_thread():
    main()
    os._exit(0)

if __name__ == "__main__":
    gameRoot = str(Path(sys.argv[1]).absolute()) if len(sys.argv) > 1 else str(Path('../').absolute())
    sys.path.append(gameRoot)
    os.chdir(gameRoot)
    from main import *

    Thread(target=game_thread, args=[]).start()

    # wait until all resources of game loaded
    time.sleep(1.5)

    app = QApplication(sys.argv)
    if len(sys.argv) >= 4:
        window = Window(int(sys.argv[2]), int(sys.argv[3]))
    else:
        window = Window()
    window.show()
   
    os._exit(app.exec())