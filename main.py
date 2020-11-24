from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QPoint, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
import PyQt5
# import pygame
from PyQt5.QtCore import Qt, QUrl
import sys
import numpy as np
import time
# import pyaudio
import os
import subprocess
import sys
import math
import pathlib
# print(pathlib.Path().absolute())

class Renderer(QObject):
    renderDone = pyqtSignal()
    @pyqtSlot()
    def render(self):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        path = pathlib.Path(__file__).parent.absolute()
        os.chdir(path)
        blend = subprocess.run("blender/blender.exe -b --python br4.py", startupinfo=si, capture_output=True)

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
        self.label2 = QLabel()
        self.label2.move(600,360)
        self.label2
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

        ##LAYOUTS
        self.grid = QGridLayout()
        self.grid2 = QGridLayout()
        self.grid3 = QGridLayout()
        self.grid4 = QGridLayout()
        self.grid6 = QGridLayout()
        self.grid7 = QGridLayout()
        self.grid5 = QVBoxLayout()

        ##CENTRALWIDGET
        self.MainWidget.resize(self.width(),self.height())
        self.setCentralWidget(self.MainWidget)
        self.MainWidget.setLayout(self.grid)


        ##MENUBAR
        self.menu = QMenuBar(self)
        self.fileMenu = self.menu.addMenu("File")
        self.editMenu = self.menu.addMenu("Edit")
        self.aboutMenu = self.menu.addMenu("About")
        self.newFile = self.fileMenu.addAction("New...")
        self.openFile = self.fileMenu.addAction("Open file")
        self.importFile = self.fileMenu.addAction("import .blend")
        self.saveFile = self.fileMenu.addAction("Save")
        self.saveAsFile = self.fileMenu.addAction("Save as...")
        self.saveBlendFile = self.fileMenu.addAction("Save .blend")
        self.saveAsBlendFile = self.fileMenu.addAction("Save .blend as...")
        self.SplshScrn = self.aboutMenu.addAction("Splash Screen")
        self.openFile.triggered.connect(self.OpenFileDiag)
        self.SplshScrn.triggered.connect(self.splash.infoShow)
        self.mousePressEvent = self.splash.closer
        self.importFile.triggered.connect(self.ImportFileDiag)

        self.fr1 = QFrame()
        self.frameTab1 = QFrame()
        self.frameTab2 = QFrame()
        self.fr1.resize(self.width()/3,self.height()/3)
        self.tabler = QTabWidget()
        self.grid2.addWidget(self.tabler)
        self.tabler.addTab(self.frameTab1,"Tab1")
        self.tabler.addTab(self.frameTab2,"Tab2")
        self.fr2 = QFrame()
        # self.fr2.resize(self.width()/3,self.height()/3)
        self.frameTab1.setLayout(self.grid6)
        self.frameTab2.setLayout(self.grid7)
        self.fr3 = QFrame()
        self.fr3.setMaximumWidth(self.width()/4)
        self.fr3.resize(self.width()/4,self.height()/4)
        self.fr1.setLayout(self.grid2)
        self.fr2.setLayout(self.grid3)
        self.fr3.setLayout(self.grid4)

        self.grid.addWidget(self.fr1,0,0)
        self.grid.addWidget(self.fr2,0,1)
        self.grid.addWidget(self.fr3,0,2)

        self.renderer = Renderer()
        self.mainThread = QThread()
        self.renderer.moveToThread(self.mainThread)
        self.mainThread.started.connect(self.renderer.render)
        self.renderer.renderDone.connect(self.mainThread.terminate)
        self.renderer.renderDone.connect(self.updateIm)
        self.grid = QGridLayout()
        # self.setLayout(self.grid)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowMaximized)
        palette = QPalette()
        palette.setColor(self.backgroundRole(), QColor(61,61,61))
        palette2 = QPalette()
        palette2.setColor(QPalette.Base,QColor(61,61,61))
        palette2.setColor(QPalette.Text,QColor(245,245,245))
        palette2.setColor(QPalette.Button,QColor(61,61,61))
        palette2.setColor(QPalette.ButtonText,QColor(245,245,245))
        palette2.setColor(QPalette.WindowText,QColor(245,245,245))
        self.setPalette(palette)
        self.menu.setPalette(palette2)
        self.icon = QIcon("icon2.png")
        # self.grid.addWidget(self.fr1,0,0)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Rendorium Alpha 0.1 (open-source)")
        self.comb = QComboBox(self.fr1)
        self.comb.insertItems(5,["sphere","cube","cylinder"])
        self.comb.setMaximumWidth(100)
        self.comb2 = QComboBox(self.fr1)
        self.comb2.insertItems(5,["sphere","cube","cylinder"])
        self.comb2.setMaximumWidth(100)
        self.comb3 = QComboBox(self.fr1)
        self.comb3.insertItems(5,["sphere","cube","cylinder"])
        self.comb3.setMaximumWidth(100)
        self.angle = QDial(self.fr1)
        self.angle2 = QDial(self.fr1)
        self.angle3 = QDial(self.fr1)
        self.l2 = QLabel(self.fr1)
        self.l5 = QLabel(self.fr1)
        self.l6 = QLabel(self.fr1)
        self.mov = QMovie("ld2.gif")
        self.fill1 = QFrame(self.fr2)
        self.fill2 = QFrame(self.fr2)
        self.fill1.setMinimumHeight(int(self.height()/3))
        self.fill2.setMinimumHeight(int(self.height()/3))
        self.tabler.setPalette(palette2)
        self.l3 = QLabel(self.fr2)
        self.l4 = QLabel(self.fr2)
        self.l3.setAlignment(Qt.AlignCenter)
        self.l4.setAlignment(Qt.AlignCenter)
        self.l4.resize(40,40)
        self.l4.setMovie(self.mov)
        self.mov.start()
        self.grid3.addWidget(self.fill1,0,0)
        self.grid3.addWidget(self.fill2,3,0)

        self.l3.setPalette(palette2)
        self.l5.setPalette(palette2)
        self.l6.setPalette(palette2)
        self.l3.setText("Loading Preview")

        self.grid3.addWidget(self.l4,1,0)
        self.grid3.addWidget(self.l3,2,0)

        self.l3.hide()
        self.l4.hide()
        self.fill1.show()
        self.fill2.show()
        self.angle.valueChanged.connect(self.changeLabel)
        self.angle.sliderReleased.connect(self.renderR)
        self.angle.setPalette(palette2)
        self.angle.setWrapping(True)
        self.angle.setMaximum(360)
        self.angle.setNotchesVisible(True)
        self.angle2.setNotchesVisible(True)
        self.angle2.valueChanged.connect(self.changeLabel)
        self.angle2.sliderReleased.connect(self.renderR)
        self.angle2.setPalette(palette2)
        self.angle2.setWrapping(True)
        self.angle2.setMaximum(360)
        self.angle2.setNotchesVisible(True)
        self.angle3.valueChanged.connect(self.changeLabel)
        self.angle3.sliderReleased.connect(self.renderR)
        self.angle3.setPalette(palette2)
        self.angle3.setWrapping(True)
        self.angle3.setMaximum(360)
        self.angle3.setNotchesVisible(True)

        self.grid6.addWidget(self.angle,2,0)
        self.grid6.addWidget(self.l2,2,1)
        self.grid6.addWidget(self.angle2,3,0)
        self.grid6.addWidget(self.l5,3,1)
        self.grid6.addWidget(self.angle3,4,0)
        self.grid6.addWidget(self.l6,4,1)
        # self.comb3.setStyleSheet("""color: rgb(245,245,245)
        #                         ; background-color: rgb(61,61,61)""")
        self.comb.setPalette(palette2)
        self.comb2.setPalette(palette2)
        self.comb3.setPalette(palette2)
        self.tabler.setPalette(palette2)
        self.l2.setPalette(palette2)
        self.lbl = QLabel(self.fr2)
        self.pix = QPixmap("thb.png")
        self.dict = {"pic":QPixmap("thb.png")}
        self.lbl.setPixmap(self.pix.scaled(1280,720))
        QApplication.restoreOverrideCursor()
        self.lbl.mousePressEvent = self.firstClick
        self.lbl.mouseMoveEvent = self.dragClick
        self.lbl.mouseReleaseEvent = self.dragUpdate

        self.lbl.setCursor(QCursor(Qt.OpenHandCursor))
        self.lbl.wheelEvent = self.wheelEve
        self.list = QListWidget()
        self.grid7.addWidget(self.list,0,0)
        self.grid3.addWidget(self.lbl,0,0)
        self.grid6.addWidget(self.comb,0,0)
        self.grid6.addWidget(self.comb2,0,1)
        self.grid6.addWidget(self.comb3,0,2)
        self.splash.mainLoad.connect(self.show)
        self.btn = QPushButton()
        self.btn.setPalette(palette2)
        self.list.setPalette(palette2)
        self.btn.setText("RENDER!!!!!")
        self.btn.clicked.connect(self.renderR)
        self.grid6.addWidget(self.btn,1,1)
        self.btn.setMaximumWidth(100)
        self.dragged = False
        self.lbl.hide()
        self.lbl.show()
        self.timelst =[]
        self.scrollLst = []

    def OpenFileDiag(self):
        QFileDialog.getOpenFileName(self, "Open Rendorium Project", "C:/", "Rendorium  Files (*.drm)")
    def ImportFileDiag(self):
        importer = QFileDialog.getOpenFileName(self, "Import Blender Project", "C:/", "Blender Project (*.blend)")
        self.Importer(importer[0])
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
            self.renderR(dz = str(distance))
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
            self.renderR(ddx = ddx,dy = dy)

    def updateIm(self):
        self.pix = QPixmap("render.png")
        self.dict = {"pic":QPixmap("render.png")}
        self.var = 'QPixmap("render.png")'
        self.pix = self.pix.scaled(self.picSize[0],self.picSize[1],Qt.KeepAspectRatio)
        self.lbl.setPixmap(self.pix)
        self.l3.hide()
        self.l4.hide()
        self.fill1.hide()
        self.fill2.hide()

        self.lbl.show()
        items = open("ob_DATA.data","r")
        self.list.clear()
        a = items.readlines()
        self.list.insertItems(len(a),a)
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
        a = self.fr2.width()
        print(a,self.lbl.width())
        self.fr2.setMinimumWidth(a)
        self.lbl.hide()
        self.l3.show()
        self.l4.show()
        self.fill1.show()
        self.fill2.show()
        self.l3.resize(a,self.height())
        self.fr2.resize(a,self.height())
        dict = open("something.drm","w")
        lst = ["|import",fileName]
        combined = "#".join(lst)
        dict.write(combined)
        self.mainThread.start()
    def renderR(self,n = False,ddx="0",dy="0",dz ="0"):
        print(ddx,dy)
        a = self.fr2.width()
        print(a,self.lbl.width())
        self.fr2.setMinimumWidth(a)
        self.lbl.hide()
        self.l3.show()
        self.l4.show()
        self.fill1.show()
        self.fill2.show()

        self.l3.resize(a,self.height())
        self.fr2.resize(a,self.height())

        str1 = self.comb.currentText()
        str2 = self.comb2.currentText()
        str3 = self.comb3.currentText()
        dict = open("something.drm","w")
        lst = ["|test",str1,str2,str3,str(self.angle.value()),str(self.angle2.value()),str(self.angle3.value()),ddx,dy,dz]
        combined = "#".join(lst)
        dict.write(combined)
        # dict.close()
        self.mainThread.start()
    def onRun(self):
        self.splash.onBoot()
    def closeEvent(self, event):
        self.mainThread.terminate()
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
path = pathlib.Path(__file__).parent.absolute()
os.chdir(path)
App = QApplication(sys.argv)
# App.exec()
w = Main()

App.setStyle('Fusion')
w.onRun()
