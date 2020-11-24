import PyQt5
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QPoint, QTimer, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
import copy

# import pygame
from PyQt5.QtCore import Qt, QUrl
import sys
import numpy as np
import time
# import pyaudio
import os
import subprocess
import sys
import signal
import math
import pathlib
# print(pathlib.Path().absolute())

class Renderer(QObject):
    def __init__(self):
        super().__init__()
        self.blend = None
    renderDone = pyqtSignal()
    consoleRender = pyqtSignal(str)
    @pyqtSlot()
    def render(self):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        os.chdir(pathlib.Path().absolute())
        self.blend = subprocess.Popen("blender/blender.exe -b --python blender.py", startupinfo=si, stdout=subprocess.PIPE)
        line = self.blend.stdout.readline()
        #https://stackoverflow.com/a/803421
        while line:
            line = self.blend.stdout.readline()
            self.consoleRender.emit(line.decode("UTF-8"))

        print(self.blend.pid)
        self.renderDone.emit()
    def killRender(self):

        if self.blend != None:
            self.blend.kill()
        self.renderDone.emit()
class Timer(QObject):
    splashFin = pyqtSignal()
    loading = pyqtSignal(str)
    def __init__(self):

        super().__init__()


    @pyqtSlot()
    def splashTimer(self):
        self.Loader()

    def Loader(self):
        j = 0
        while j < 10:
            for i in range(1,4):
                time.sleep(0.2)
                self.loading.emit("Loading"+"".join(["."]*i))
                j+= 1
        self.splashFin.emit()


class Splash(QWidget):
    mainLoad = pyqtSignal()
    @pyqtSlot()
    def __init__(self):
        super().__init__()
        self.timer = Timer()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(640,360,640,360)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.splsh = QPixmap("thb.png").scaled(self.width(),self.height())
        self.label = QLabel()
        palette = QPalette(QColor(61,61,61))
        self.setPalette(palette)
        self.label.setPixmap(self.splsh)
        self.label.resize(self.width(),self.height())
        self.label.setLineWidth(0)
        self.label2 = QLabel()
        self.label2.move(600,360)

        self.grid.addWidget(self.label,0,0)
        self.grid.addWidget(self.label2,1,0)
        self.thread = QThread()
        self.timer.moveToThread(self.thread)
        self.timer.splashFin.connect(self.close)
        self.timer.loading.connect(self.loadText)
        self.timer.splashFin.connect(self.thread.terminate)
        self.thread.started.connect(self.timer.Loader)
        self.timer.splashFin.connect(self.mainLoad.emit)
    def onBoot(self):
        self.thread.start()
        self.show()
    def loadText(self,loading):

        self.label2.setText(loading)
    def infoShow(self):

        self.label2.hide()
        self.show()
    def closer(self,event):
        self.close()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.splash = Splash()
        self.MainWidget = QFrame()
        self.icon = QIcon("icon2.png")
        self.firstFile = open("FILE_BLEND.data","w")
        self.firstFile.close()
        # self.grid.addWidget(self.fr1,0,0)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Rendorium alpha 0.11 (open-source)")


        ##LAYOUTS
        self.grid = QGridLayout()
        self.grid2 = QGridLayout()
        self.grid3 = QGridLayout()
        self.grid4 = QGridLayout()
        self.grid6 = QGridLayout()
        self.grid7 = QGridLayout()
        self.grid5 = QVBoxLayout()
        self.gridPreview = QGridLayout()
        self.gridLoad = QGridLayout()
        self.gridConsole = QGridLayout()
        self.gridCamera = QGridLayout()
        self.gridLights = QGridLayout()
        self.gridRendering = QGridLayout()
        self.gridScene = QGridLayout()
        self.gridPhysics = QGridLayout()
        self.gridStats = QGridLayout()
        self.gridTransform = QGridLayout()
        ##CENTRALWIDGET
        self.MainWidget.resize(self.width(),self.height())
        self.setCentralWidget(self.MainWidget)
        self.MainWidget.setLayout(self.grid)


        ##MENUBAR
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)
        self.menu.setMaximumWidth(200)

        # self.grid.addWidget(self.menu,0,0)
        self.fileMenu = self.menu.addMenu("File")
        self.editMenu = self.menu.addMenu("Edit")
        self.aboutMenu = self.menu.addMenu("About")


        # below are menu items not yet implemented, just uncomment those
        # lines for preview purposes

        # self.newFile = self.fileMenu.addAction("New...")
        # self.openFile = self.fileMenu.addAction("Open file")
        # self.saveFile = self.fileMenu.addAction("Save")
        # self.saveAsFile = self.fileMenu.addAction("Save as...")
        # self.openFile.triggered.connect(self.OpenFileDiag)

        self.importFile = self.fileMenu.addAction("import .blend")
        self.saveBlendFile = self.fileMenu.addAction("Save .blend")
        self.saveAsBlendFile = self.fileMenu.addAction("Save .blend as...")
        self.SplshScrn = self.aboutMenu.addAction("Splash Screen")

        self.SplshScrn.triggered.connect(self.splash.infoShow)
        self.mousePressEvent = self.splash.closer
        self.importFile.triggered.connect(self.ImportFileDiag)
        self.saveAsBlendFile.triggered.connect(self.SaveAsDiag)
        self.saveBlendFile.triggered.connect(self.SaveDiag)
        self.theme = self.editMenu.addAction("Change Theme")
        self.theme.triggered.connect(self.changeTheme)



        ##FRAMES
        self.fr1 = QFrame()
        self.fr2 = QFrame()
        self.fr3 = QFrame()
        self.fr1.setLineWidth(0)
        self.fr2.setLineWidth(0)
        self.fr3.setLineWidth(0)
        self.fr1.setFrameShape(QFrame.NoFrame)
        self.fr2.setFrameShape(QFrame.NoFrame)
        self.fr3.setFrameShape(QFrame.NoFrame)
        self.fr1.setLayout(self.grid2)
        self.fr2.setLayout(self.grid3)
        self.fr3.setLayout(self.grid4)
        self.fr1.resize(self.width()/3,self.height()/3)
        # self.fr2.resize(self.width()/3,self.height()/3)
        # self.fr3.setMaximumWidth(self.width()/4)
        self.fr3.resize(self.width()/4,self.height()/4)
        self.grid.addWidget(self.fr1,1,0)
        self.grid.addWidget(self.fr2,1,1)
        self.grid.addWidget(self.fr3,1,2)




        ##TABS
        self.tabsRight = QTabWidget()
        self.tabsLeft = QTabWidget()
        self.grid2.addWidget(self.tabsRight)
        self.grid4.addWidget(self.tabsLeft)
        self.tabsLeft.setTabPosition(QTabWidget.West)
        self.frameTabObj = QFrame()
        self.frameTabScnObj = QFrame()
        self.frameTabLight = QFrame()
        self.frameTabCamera = QFrame()
        self.frameTabScene = QFrame()
        self.frameTabPhysics = QFrame()
        self.frameTabRendering = QFrame()
        self.frameTabStatistics = QFrame()
        self.frameConsole = QFrame()
        self.frameTabObj.setLayout(self.grid6)
        self.frameTabScnObj.setLayout(self.grid7)
        self.frameConsole.setLayout(self.gridConsole)
        self.frameTabLight.setLayout(self.gridLights)
        self.frameTabCamera.setLayout(self.gridCamera)
        self.frameTabScene.setLayout(self.gridScene)
        self.frameTabPhysics.setLayout(self.gridPhysics)
        self.frameTabRendering.setLayout(self.gridRendering)
        self.frameTabStatistics.setLayout(self.gridStats)
        self.tabsRight.addTab(self.frameTabObj,"Object")
        self.tabsRight.addTab(self.frameTabLight,"Lights")
        self.tabsRight.addTab(self.frameTabCamera,"Cameras")
        self.tabsRight.addTab(self.frameTabScene,"Scene")
        self.tabsRight.addTab(self.frameTabPhysics,"Physics")
        self.tabsRight.addTab(self.frameTabRendering,"Rendering")
        self.tabsLeft.addTab(self.frameTabScnObj,"Scene Objects")
        self.tabsLeft.addTab(self.frameTabStatistics,"Statistics")
        self.tabsLeft.addTab(self.frameConsole,"Console")



        ##THREADS
        self.renderer = Renderer()
        self.mainThread = QThread()
        self.renderer.moveToThread(self.mainThread)
        self.mainThread.started.connect(self.renderer.render)
        self.renderer.renderDone.connect(self.mainThread.terminate)
        self.renderer.renderDone.connect(self.updateIm)
        self.renderer.renderDone.connect(self.updateObj)
        self.renderer.renderDone.connect(self.keepSelected)
        self.renderer.renderDone.connect(self.titleBarStat)
        self.grid = QGridLayout()
        # self.setLayout(self.grid)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowMaximized)
        self.splash.mainLoad.connect(self.show)
        self.renderer.consoleRender.connect(self.consoleFunc)

        ##PALETTE

        self.palette = QPalette()
        self.palette3 = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(61,61,61))
        self.palette2 = QPalette()
        self.palette2.setColor(QPalette.Base,QColor(61,61,61))
        self.palette2.setColor(QPalette.Text,QColor(245,245,245))
        self.palette2.setColor(QPalette.Button,QColor(61,61,61))
        self.palette2.setColor(QPalette.ButtonText,QColor(245,245,245))
        self.palette2.setColor(QPalette.WindowText,QColor(245,245,245))
        self.palette3.setColor(QPalette.Base,QColor(230,230,230))
        self.palette3.setColor(QPalette.Text,QColor(40,40,40))
        self.palette3.setColor(QPalette.Button,QColor(230,230,230))
        self.palette3.setColor(QPalette.ButtonText,QColor(40,40,40))
        self.palette3.setColor(QPalette.WindowText,QColor(40,40,40))
        self.palette4 = QPalette(self.palette2)
        self.palette5 = QPalette(self.palette3)

        self.palette4.setColor(QPalette.Background,QColor(61,61,61,90))
        self.palette5.setColor(QPalette.Background,QColor(245,245,245,90))
        self.setPalette(self.palette)
        self.menu.setPalette(self.palette2)
        self.tabsRight.setPalette(self.palette2)
        self.tabsLeft.setPalette(self.palette2)

        ##WIDGETS

        self.pix = QPixmap("thb.png")

        self.lbl = QLabel(self.fr2)

        self.loadHolder = QFrame(self.fr2)
        self.loadHolder.setLayout(self.gridLoad)
        self.loadHolder.setMaximumSize(1280,150)
        self.loadHolder.hide()

        self.loadBox = QFrame(self.loadHolder)
        self.loadBox.setMaximumSize(100,100)
        self.loadBox.setMinimumSize(100,100)
        self.loadBox.setAutoFillBackground(True)
        self.loadBox2 = QFrame(self.loadHolder)
        self.loadBox2.setMaximumSize(100,60)
        self.loadBox2.setMinimumSize(100,60)
        self.loadBox2.setAutoFillBackground(True)

        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setLayout(self.gridPreview)
        self.lbl.setAttribute(Qt.WA_TranslucentBackground,True)
        self.lbl.setWindowOpacity(0.2)
        self.lbl.mousePressEvent = self.firstClick
        self.lbl.mouseMoveEvent = self.dragClick
        self.lbl.mouseReleaseEvent = self.dragUpdate
        self.lbl.setCursor(QCursor(Qt.OpenHandCursor))
        self.lbl.setMaximumSize(1280,720)
        self.lbl.setToolTip("drag or scroll to change the camera's perspective")
        self.lbl.setToolTipDuration(3000)
        self.lbl.wheelEvent = self.wheelEve
        self.lbl.setPixmap(self.pix.scaled(1280,720))
        self.lbl.hide()
        # self.lbl.show()




        # self.angle.valueChanged.connect(self.changeLabel)
        # self.angle.sliderReleased.connect(self.renderR)
        # self.angle.setPalette(self.palette2)
        # self.angle.setWrapping(True)
        # self.angle.setMaximum(360)
        # self.angle.setNotchesVisible(True)
        # self.angle2.setNotchesVisible(True)
        # self.angle2.valueChanged.connect(self.changeLabel)
        # self.angle2.sliderReleased.connect(self.renderR)
        # self.angle2.setPalette(self.palette2)
        # self.angle2.setWrapping(True)
        # self.angle2.setMaximum(360)
        # self.angle2.setNotchesVisible(True)
        # self.angle3.valueChanged.connect(self.changeLabel)
        # self.angle3.sliderReleased.connect(self.renderR)
        # self.angle3.setPalette(self.palette2)
        # self.angle3.setWrapping(True)
        # self.angle3.setMaximum(360)
        # self.angle3.setNotchesVisible(True)

        self.mov = QMovie("load3.gif")
        self.mov2 = QMovie("load4.gif")
        self.mov.setScaledSize(QSize(30,30))


        self.l2 = QLabel(self.fr1)


        self.l3 = QLabel()
        self.l3.setAlignment(Qt.AlignCenter)

        self.l3.setMaximumSize(100,50)
        self.l4 = QLabel()
        self.l4.setAlignment(Qt.AlignCenter)
        self.l4.setMaximumSize(100,50)
        self.l4.setMovie(self.mov)

        self.l3.hide()
        self.l4.hide()

        self.l3.setText("Loading Preview")

        self.l5 = QLabel(self.fr1)
        self.l6 = QLabel(self.fr1)


        self.mov.start()
        self.mov2.start()

        self.fill1 = QFrame(self.lbl)
        self.fill2 = QFrame(self.lbl)

        self.fill1.show()
        self.fill2.show()

        self.fill1.setMinimumHeight(int(self.height()/3))
        self.fill2.setMinimumHeight(int(self.height()/3))

        self.firstLoad = QLabel(self.fill1)
        self.firstLoad.setText("""3D previews appear here
import a .blend file or load a save to start""")
        self.firstLoad.setAlignment(Qt.AlignCenter)

        #
        # self.comb.insertItems(5,["sphere","cube","cylinder"])
        # self.comb.setMaximumWidth(100)
        #
        # self.comb2.insertItems(5,["sphere","cube","cylinder"])
        # self.comb2.setMaximumWidth(100)
        #
        # self.comb3.insertItems(5,["sphere","cube","cylinder"])
        # self.comb3.setMaximumWidth(100)

        self.list = QListWidget(self.fr3)

        self.list.itemClicked.connect(self.itemUpdate)

        # self.btn = QPushButton()
        # self.btn.setText("RENDER!!!!!")
        # self.btn.clicked.connect(self.renderR)
        # self.btn.setMaximumWidth(100)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setCurrentFont(QFont("Courier New"))
        self.console.ensureCursorVisible()

        self.cancelBtn = QPushButton()
        self.cancelBtn.setText("cancel Preview")
        self.cancelBtn.clicked.connect(self.cancelPreview)
        # self.btn.setMaximumWidth(100)

        ##tab objects
        self.transformFrame = QFrame(self.frameTabObj)
        self.trFrHg = self.frameTabObj.height()//3
        self.trFrWd = self.frameTabObj.width()
        self.transformFrame.setMinimumHeight(self.trFrHg)
        self.transformFrame.setMaximumHeight(self.trFrHg)
        self.transformFrame.setLayout(self.gridTransform)
        self.emptyLbl = QLabel()
        self.emptyLbl.setText("       ")
        self.transformLbl = QLabel()
        self.transformLbl.setText("Transform")
        self.locationLbl = QLabel()
        self.locationLbl.setMaximumSize(60,10)
        self.locationLbl.setText("Position")
        self.locationLbl.setAlignment(Qt.AlignCenter)
        self.rotationLbl = QLabel()
        self.rotationLbl.setMaximumSize(60,10)
        self.rotationLbl.setText("Rotation")
        self.rotationLbl.setAlignment(Qt.AlignCenter)
        self.scaleLbl = QLabel()
        self.scaleLbl.setMaximumSize(60,10)
        self.scaleLbl.setText("Scale")
        self.scaleLbl.setAlignment(Qt.AlignCenter)
        self.xTLbl = QLabel()
        self.xTLbl.setText("x:")
        self.xTLbl.setMaximumSize(10,20)
        self.yTLbl = QLabel()
        self.yTLbl.setText("y:")
        self.yTLbl.setMaximumSize(10,20)
        self.zTLbl = QLabel()
        self.zTLbl.setText("z:")
        self.zTLbl.setMaximumSize(10,20)
        self.xTEntry = QLineEdit(self.frameTabObj)
        self.yTEntry = QLineEdit(self.frameTabObj)
        self.zTEntry = QLineEdit(self.frameTabObj)
        self.xREntry = QLineEdit(self.frameTabObj)
        self.yREntry = QLineEdit(self.frameTabObj)
        self.zREntry = QLineEdit(self.frameTabObj)
        self.xSEntry = QLineEdit(self.frameTabObj)
        self.ySEntry = QLineEdit(self.frameTabObj)
        self.zSEntry = QLineEdit(self.frameTabObj)
        self.Entries = [self.xTEntry,self.yTEntry,self.zTEntry,
                        self.xREntry,self.yREntry,self.zREntry,
                        self.xSEntry,self.ySEntry,self.zSEntry,
        ]

        for TEntry in self.Entries:
            TEntry.setText("0")
            TEntry.setMaximumHeight(30)
            TEntry.setReadOnly(True)
            TEntry.setCursor(QCursor(Qt.SizeHorCursor))
            TEntry.setValidator(QDoubleValidator())
            TEntry.mousePressEvent = lambda ev,en = TEntry: self.onEntryClick(ev,en)
            TEntry.editingFinished.connect(lambda en = TEntry :self.onEntryReturnPressed(en))
            TEntry.textEdited.connect(lambda ev,wid = TEntry: self.entryChanger(ev,wid))
            TEntry.mouseMoveEvent = lambda ev,en = TEntry: self.onEntryDrag(ev,en)
            TEntry.mouseReleaseEvent = lambda ev,en = TEntry: self.onEntryLeave(ev,en)
            TEntry.mouseDoubleClickEvent = lambda ev,en = TEntry: self.onEntryDblClick(ev,en)

            TEntry.setAlignment(Qt.AlignCenter)




        #setting palettes for widgets
        self.l3.setPalette(self.palette2)
        self.l5.setPalette(self.palette2)
        self.l6.setPalette(self.palette2)
        self.tabsRight.setPalette(self.palette2)
        # self.btn.setPalette(self.palette2)
        self.list.setPalette(self.palette2)
        self.l2.setPalette(self.palette2)
        self.firstLoad.setPalette(self.palette2)
        self.console.setPalette(self.palette2)
        # self.lbl.setPalette(self.palette4)
        self.loadHolder.setPalette(self.palette4)
       #adding widgets to grid

        self.gridPreview.addWidget(self.fill1,0,0)
        self.grid3.addWidget(self.firstLoad,1,0)
        self.gridPreview.addWidget(self.fill2,3,0)
        self.grid3.addWidget(self.loadHolder,0,0)
        self.gridLoad.addWidget(self.l4,0,0)
        self.gridLoad.addWidget(self.loadBox,0,0)
        self.gridLoad.addWidget(self.loadBox2,1,0)
        self.gridLoad.addWidget(self.l3,1,0)
        self.gridLoad.addWidget(self.cancelBtn,2,0)
        # self.grid6.addWidget(self.angle,2,0)
        # self.grid6.addWidget(self.l2,2,1)
        # self.grid6.addWidget(self.angle2,3,0)
        # self.grid6.addWidget(self.l5,3,1)
        # self.grid6.addWidget(self.angle3,4,0)
        # self.grid6.addWidget(self.l6,4,1)
        self.grid7.addWidget(self.list,0,0)
        self.grid3.addWidget(self.lbl,0,0)
        # self.grid6.addWidget(self.comb,0,0)
        # self.grid6.addWidget(self.comb2,0,1)
        # self.grid6.addWidget(self.comb3,0,2)
        # self.grid6.addWidget(self.btn,1,1)
        self.gridConsole.addWidget(self.console)
        self.grid6.addWidget(self.transformFrame,0,0)
        self.gridTransform.addWidget(self.emptyLbl,1,0)
        self.gridTransform.addWidget(self.transformLbl,0,0)
        self.gridTransform.addWidget(self.locationLbl,1,1)
        self.gridTransform.addWidget(self.rotationLbl,1,2)
        self.gridTransform.addWidget(self.scaleLbl,1,3)
        self.gridTransform.addWidget(self.xTLbl,2,0)
        self.gridTransform.addWidget(self.xTEntry,2,1)
        self.gridTransform.addWidget(self.xREntry,2,2)
        self.gridTransform.addWidget(self.xSEntry,2,3)
        self.gridTransform.addWidget(self.yTLbl,3,0)
        self.gridTransform.addWidget(self.yTEntry,3,1)
        self.gridTransform.addWidget(self.yREntry,3,2)
        self.gridTransform.addWidget(self.ySEntry,3,3)
        self.gridTransform.addWidget(self.zTLbl,4,0)
        self.gridTransform.addWidget(self.zTEntry,4,1)
        self.gridTransform.addWidget(self.zREntry,4,2)
        self.gridTransform.addWidget(self.zSEntry,4,3)



        # QApplication.restoreOverrideCursor()

        #graphics
        self.graphic1 = QGraphicsOpacityEffect()
        self.graphic1.setOpacity(0.5)
        self.lbl.setGraphicsEffect(self.graphic1)






        ##VARIABLES
        self.dict = {"pic":QPixmap("thb.png")}
        self.dragged = False
        self.timelst =[]
        self.scrollLst = []
        self.currentTheme = "Dark"
        self.path = pathlib.Path().absolute()
        self.entryClicked = {self.xTEntry: False,
                             self.yTEntry:False,
                             self.zTEntry:False,
                             self.xREntry:False,
                             self.yREntry:False,
                             self.zREntry:False,
                             self.xSEntry:False,
                             self.ySEntry:False,
                             self.zSEntry:False,
        }
        self.entryDragged = copy.copy(self.entryClicked)
        self.entryChanged = copy.copy(self.entryClicked)
        self.itemUpdating = False
        self.selObj = None
        self.entryXpos = {}
        self.selInd = -1
        self.title = self.windowTitle()
        self.isLoaded = False


    def SaveDiag(self):
        if self.isLoaded:
            dict = open("DT_PIPIN.data","w")
            dict.write("|Save#Null")
            self.mainThread.start()
        else:
            QMessageBox.warning(self, "Error","there are no loaded .blend files to save")


    def titleBarStat(self):
        status = open("BLEND_SAVE.data","r")
        statDat = status.read()
        # statDat = statDat[:len(statDat)-1]
        self.setWindowTitle(self.title + " " + statDat)


    def entryChanger(self,ev,wid):
        self.entryChanged[wid] = True

    def keepSelected(self):
        self.list.setCurrentRow(self.selInd)

    def itemCurrent(self):
        self.selObj = self.list.selectedItems()[0]
        self.selInd = self.list.currentRow()


    def updateObj(self):
        if self.itemUpdating:
            readData = open("ob_TRANS.data","r")
            transData = readData.read().split("#")
            for i in range(len(self.Entries)):
                self.Entries[i].setText(transData[i])
                self.itemUpdating = False


    def itemUpdate(self):
        self.itemCurrent()
        self.selObj = self.list.selectedItems()[0]
        objName = self.selObj.text()
        objName = objName[:len(objName)-1]
        dataIn = open("DT_PIPIN.data","w")
        dataIn.write("|ObjData#"+objName+"#")
        self.itemUpdating = True
        self.mainThread.start()




    def onEntryClick(self,event,widget):
        self.entryClicked[widget] = True
        self.entryXpos[widget] = event.x() - float(widget.text())
        print(self.entryXpos)


    def onEntryDrag(self,event,widget):
        if self.entryClicked[widget]:
            value = event.x() - self.entryXpos[widget]
            widget.setText(str(value))
            self.entryDragged[widget] = True


    def onEntryLeave(self,event,widget):
        if self.entryDragged[widget]:
            val = widget.text()
            i = self.Entries.index(widget)
            if self.list.selectedItems() != []:
                self.ObjTransform(i,val)
        self.entryClicked[widget] = False
        self.entryDragged[widget] = False


    def onEntryDblClick(self,event,widget):
        widget.setReadOnly(False)


    def onEntryReturnPressed(self,widget):
        print("itsa me")

        widget.setReadOnly(True)
        widget.setCursor(QCursor(Qt.SizeHorCursor))
        i = self.Entries.index(widget)
        val = widget.text()
        if self.list.selectedItems() != [] and  self.entryChanged[widget]:
            self.ObjTransform(i,val)
        print(self.entryChanged[widget])
        self.entryChanged[widget] = False


    def ObjTransform(self,i,val):
        ObjCor = ["xT","yT","zT","xR","yR","zR","xS","yS","zS"]
        self.loaderImage()
        self.selObj = self.list.selectedItems()[0]
        objName = self.selObj.text()
        objName = objName[:len(objName)-1]
        dataIn = open("DT_PIPIN.data","w")
        dataIn.write("|ObjTrans#"+objName+"#"+ObjCor[i]+"#"+val)
        self.mainThread.start()




    def consoleFunc(self,text):

        self.console.insertPlainText(text)
        self.console.moveCursor(QTextCursor.End)
        scrollBar = self.console.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())

    def changeTheme(self):

        if self.currentTheme == "Dark":
            frame = self.mov.currentFrameNumber()
            # self.btn.setPalette(self.palette3)
            self.list.setPalette(self.palette3)

            self.tabsRight.setPalette(self.palette3)
            self.tabsLeft.setPalette(self.palette3)
            self.l2.setPalette(self.palette3)
            self.setPalette(self.palette3)
            self.menu.setPalette(self.palette3)
            self.l3.setPalette(self.palette3)
            self.firstLoad.setPalette(self.palette5)
            self.loadHolder.setPalette(self.palette5)
            self.console.setPalette(self.palette3)
            # self.mov2.jumpToFrame(frame)
            # self.l4.setMovie(self.mov2)
            self.currentTheme = "Light"
        else:
            frame = self.mov2.currentFrameNumber()
            # self.btn.setPalette(self.palette2)
            self.list.setPalette(self.palette2)
            # self.comb.setPalette(self.palette2)
            # self.comb2.setPalette(self.palette2)
            # self.comb3.setPalette(self.palette2)
            self.tabsRight.setPalette(self.palette2)
            self.tabsLeft.setPalette(self.palette2)
            self.l2.setPalette(self.palette2)
            self.setPalette(self.palette)
            self.menu.setPalette(self.palette2)
            self.l3.setPalette(self.palette2)
            self.firstLoad.setPalette(self.palette4)
            self.loadHolder.setPalette(self.palette4)
            self.console.setPalette(self.palette2)
            # self.l4.setMovie(self.mov)
            # self.mov.jumpToFrame(frame)

            self.currentTheme = "Dark"

    def OpenFileDiag(self):
        QFileDialog.getOpenFileName(self, "Open Rendorium Project", "C:/", "Rendorium  Files (*.drm)")


    def ImportFileDiag(self):
        importer = QFileDialog.getOpenFileName(self, "Import Blender Project", "C:/", "Blender Project (*.blend)")
        if importer[0]:
            self.Importer(importer[0])

    def SaveAsDiag(self):
        if self.isLoaded:
            saveAs = QFileDialog.getSaveFileName(self, "Save Blender Project", "C:/", "Blender Project (*.blend)")
            if saveAs[0]:
                self.SaverAs(saveAs[0])
        else:

            QMessageBox.warning(self, "Error","there are no loaded .blend files to save")
    def SaverAs(self,filePath):
        dict = open("DT_PIPIN.data","w")
        dict.write("|SaveAs#"+filePath)
        self.mainThread.start()

    def wheelEve(self, mouseEvent):
        self.scrolling = True
        print(self.scrollLst)
        QTimer.singleShot(500, self.funScroll)
        point = mouseEvent.angleDelta()
        self.scrollLst.append(point.y())
        self.timelst.append(time.time())
        self.scrolling = False


    def funScroll(self):
        b = time.time()
        if b - self.timelst[-1] >= 0.5:
            distance = sum(self.scrollLst)
            print(distance)
            self.cameraPan(dz = str(distance))
            self.scrollLst = []


    def firstClick(self,mouseEvent):
        self.lbl.setCursor(QCursor(Qt.ClosedHandCursor))
        self.x1 = mouseEvent.globalX()
        self.y1 = mouseEvent.globalY()
        self.dragged = False
        self.x2 = 0
        self.y2 = 0


    def dragClick(self,mouseEvent):
        self.x2 = mouseEvent.globalX()
        self.y2 = mouseEvent.globalY()
        self.dragged = True


    def dragUpdate(self,mouseEvent):
        self.lbl.setCursor(QCursor(Qt.OpenHandCursor))
        if self.dragged:
            ddx = str(self.x2 - self.x1)
            dy = str(self.y2 - self.y1)
            print(dy,ddx)
            self.cameraPan(ddx = ddx,dy = dy)


    def updateIm(self):
        self.pix = QPixmap("render.png")
        self.dict = {"pic":QPixmap("render.png")}
        self.var = 'QPixmap("render.png")'
        self.pix = self.pix.scaled(self.picSize[0],self.picSize[1],Qt.KeepAspectRatio)

        self.lbl.setPixmap(self.pix)
        self.loadHolder.hide()
        self.l3.hide()
        self.l4.hide()
        self.graphic1.setOpacity(1)
        # self.fill1.hide()
        # self.fill2.hide()
        self.lbl.show()
        items = open("ob_DATA.data","r")
        self.list.clear()
        a = items.readlines()
        self.list.insertItems(len(a),a)
        self.isLoaded = True
        # items.close()


    def changeLabel(self):
        a = self.angle.value()
        b = self.angle2.value()
        c = self.angle3.value()
        self.l2.setText(str(a))
        self.l5.setText(str(b))
        self.l6.setText(str(c))
        self.released = True


    def Importer(self,fileName):
        self.loaderImage()
        dict = open("DT_PIPIN.data","w")
        lst = ["|import",fileName]
        combined = "#".join(lst)
        dict.write(combined)
        self.mainThread.start()


    def renderR(self,n = False,ddx="0",dy="0",dz ="0"):
        self.loaderImage()
        str1 = self.comb.currentText()
        str2 = self.comb2.currentText()
        str3 = self.comb3.currentText()
        dict = open("DT_PIPIN.data","w")
        lst = ["|test",str1,str2,str3,str(self.angle.value()),str(self.angle2.value()),str(self.angle3.value()),ddx,dy,dz]
        combined = "#".join(lst)
        dict.write(combined)
        # dict.close()
        self.mainThread.start()

    def cameraPan(self,n = False,ddx= "0",dy= "0",dz = "0"):
        self.loaderImage()
        dict = open("DT_PIPIN.data","w")
        lst = ["|cameraPan",ddx,dy,dz]
        combined = "#".join(lst)
        dict.write(combined)
        self.mainThread.start()


    def loaderImage(self):
        imgpath = open("IMG_PATH.data","w")
        imgpath.write(str(pathlib.Path().absolute()))
        width = self.fr2.width()
        self.fr2.setMinimumWidth(width)
        self.firstLoad.hide()
        self.loadHolder.show()
        self.l3.show()
        self.l4.show()
        self.fill1.show()
        self.fill2.show()
        self.graphic1.setOpacity(0.5)


    def onRun(self):
        self.splash.onBoot()

    def cancelPreview(self,event):
        self.renderer.killRender()

    def closeEvent(self, event):
        self.mainThread.terminate()
        self.renderer.killRender()


    def resizeEvent(self, event):
        self.fill1.setMinimumHeight(int(self.height()/3))
        self.fill2.setMinimumHeight(int(self.height()/3))
        self.fr3.setMaximumWidth(self.width()/4)
        self.pixa = self.dict["pic"]
        self.picSize = (int(self.width()/2),int(self.height()/2))
        self.pixa = self.pixa.scaled(self.picSize[0],self.picSize[1],Qt.KeepAspectRatio)
        self.fr2.setMinimumWidth(int(self.width()/2))
        self.lbl.setPixmap(self.pixa)


# w = Splash()
# w.onBoot()
App = QApplication(sys.argv)
App.setStyle('Fusion')

w = Main()
w.onRun()
App.exec_()