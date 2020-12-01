# Diram Tabaa
# Andrew ID: dtabaa
# TP3 Date: 12/1/2020
# main.py


import PyQt5
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QPoint, \
    QTimer, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
import copy
import ffmpeg
from PyQt5.QtCore import Qt, QUrl
import sys
import time
import os
import subprocess
import signal
import math
import pathlib


class Encoder(QObject):
    def __init__(self):
        super().__init__()
        self.cancelled = False
        self.process = None

    encodingDone = pyqtSignal()
    encodingCancelled = pyqtSignal()
    consoleEncoder = pyqtSignal(str)

    @pyqtSlot()
    def encode(self):
        if os.path.exists("signalANIMR"):
            vid = "anim.mkv"
            self.process = ffmpeg.input(vid)
            self.process = self.process.video
            self.process = ffmpeg.output(self.process, "anim.webp")
            self.process = ffmpeg.overwrite_output(self.process)
            self.process = ffmpeg.run_async(self.process, pipe_stdout=True,
                                            quiet=True)
            line = self.process.stderr.readline()
            # https://www.reddit.com/r/learnpython/comments/7maq9i/how_to_read_console_output_when_calling_ffmpeg/
            # referenced this post to know which of stdout and stderr does
            # ffmpeg use to log
            while line:
                line = self.process.stderr.readline()
                self.consoleEncoder.emit(line.decode("UTF-8"))
            if not self.cancelled:
                self.encodingDone.emit()

    def encodeCancel(self):
        self.cancelled = True
        self.encodingCancelled.emit()
        if self.process != None:
            self.process.kill()
        self.cancelled = False


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
        # https://stackoverflow.com/a/7006424
        os.chdir(pathlib.Path().absolute())
        self.blend = subprocess.Popen(
            "blender/blender.exe -b --python blender.py", startupinfo=si,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line = self.blend.stdout.readline()
        # https://stackoverflow.com/a/803421
        while line:
            line = self.blend.stdout.readline()
            self.consoleRender.emit(line.decode("UTF-8"))

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
            for i in range(1, 4):
                time.sleep(0.2)
                self.loading.emit("Loading" + "".join(["."] * i))
                j += 1
        self.splashFin.emit()


class Splash(QWidget):
    mainLoad = pyqtSignal()

    @pyqtSlot()
    def __init__(self):
        super().__init__()
        self.timer = Timer()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(640, 360, 640, 360)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.splsh = QPixmap("thb.png").scaled(self.width(), self.height())
        self.label = QLabel()
        palette = QPalette(QColor(61, 61, 61))
        self.setPalette(palette)
        self.label.setPixmap(self.splsh)
        self.label.resize(self.width(), self.height())
        self.label.setLineWidth(0)
        self.label2 = QLabel()
        self.label2.move(600, 360)

        self.grid.addWidget(self.label, 0, 0)
        self.grid.addWidget(self.label2, 1, 0)
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

    def loadText(self, loading):
        self.label2.setText(loading)

    def infoShow(self):
        self.label2.hide()
        self.show()

    def closer(self, event):
        self.close()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.splash = Splash()
        self.MainWidget = QFrame()
        self.icon = QIcon("icon2.png")
        self.firstFile = open("FILE_BLEND.data", "w")
        self.firstFile2 = open("rigid_DATA.data", "w")
        self.firstFile.close()
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
        self.gridRendering = QGridLayout()
        self.gridPhysics = QGridLayout()
        self.gridStats = QGridLayout()
        self.gridTransform = QGridLayout()
        self.gridAnimation = QGridLayout()
        self.gridRigid = QGridLayout()
        self.gridMaterial = QGridLayout()
        self.gridMaterialSet = QGridLayout()
        self.gridRoughness = QGridLayout()
        self.gridColor = QGridLayout()
        self.scaleGrid = QGridLayout()
        self.gridRndSt = QGridLayout()
        self.gridRendEng = QGridLayout()
        self.gridSamples = QGridLayout()
        self.gridRendDev = QGridLayout()
        self.gridFrame = QGridLayout()

        ##CENTRALWIDGET
        self.MainWidget.resize(self.width(), self.height())
        self.setCentralWidget(self.MainWidget)
        self.MainWidget.setLayout(self.grid)

        ##MENUBAR
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)
        self.menu.setMaximumWidth(200)

        self.fileMenu = self.menu.addMenu("File")
        self.editMenu = self.menu.addMenu("Edit")
        self.objectMenu = self.menu.addMenu("Object")
        self.aboutMenu = self.menu.addMenu("About")

        self.importFile = self.fileMenu.addAction("import .blend")
        self.saveBlendFile = self.fileMenu.addAction("Save .blend")
        self.saveAsBlendFile = self.fileMenu.addAction("Save .blend as...")
        self.SplshScrn = self.aboutMenu.addAction("Splash Screen")
        self.addObj = self.objectMenu.addAction("Add Object")
        self.deleteObj = self.objectMenu.addAction("Delete Object")

        self.addObjMenu = QMenu()
        self.addObj.setMenu(self.addObjMenu)
        self.cubeObj = self.addObjMenu.addAction("Cube")
        self.sphereObj = self.addObjMenu.addAction("Sphere")
        self.CylinderObj = self.addObjMenu.addAction("Cylinder")
        self.ConeObj = self.addObjMenu.addAction("Cone")
        self.TorusObj = self.addObjMenu.addAction("Torus")
        self.MonkeObj = self.addObjMenu.addAction("Monke")
        self.addMenus = [self.cubeObj, self.sphereObj, self.CylinderObj,
                         self.ConeObj, self.TorusObj, self.MonkeObj]
        self.objList = ["cube", "uv_sphere", "cylinder", "cone", "torus",
                        "monkey"]
        for i in range(len(self.addMenus)):
            func = lambda y, x=self.objList[i]: self.addObjFunc(y, x)
            self.addMenus[i].triggered.connect(func)

        self.deleteObj.triggered.connect(self.deleteObjFunc)
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
        self.fr1.resize(self.width() / 3, self.height() / 3)
        self.fr3.setMinimumWidth(self.width() / 4)
        self.fr3.resize(self.width() / 4, self.height() / 4)
        self.grid.addWidget(self.fr1, 1, 0)
        self.grid.addWidget(self.fr2, 1, 1)
        self.grid.addWidget(self.fr3, 1, 2)

        ##TABS
        self.tabsRight = QTabWidget()
        self.tabsLeft = QTabWidget()
        self.grid2.addWidget(self.tabsRight)
        self.grid4.addWidget(self.tabsLeft)
        self.tabsLeft.setTabPosition(QTabWidget.West)
        self.frameTabObj = QFrame()
        self.frameTabScnObj = QFrame()
        self.frameTabPhysics = QFrame()
        self.frameTabRendering = QFrame()
        self.frameTabStatistics = QFrame()
        self.frameConsole = QFrame()
        self.frameTabObj.setLayout(self.grid6)
        self.frameTabScnObj.setLayout(self.grid7)
        self.frameConsole.setLayout(self.gridConsole)
        self.frameTabPhysics.setLayout(self.gridPhysics)
        self.frameTabRendering.setLayout(self.gridRendering)
        self.frameTabStatistics.setLayout(self.gridStats)
        self.tabsRight.addTab(self.frameTabObj, "Object")
        self.tabsRight.addTab(self.frameTabPhysics, "Physics")
        self.tabsRight.addTab(self.frameTabRendering, "Animations")
        self.tabsLeft.addTab(self.frameTabScnObj, "Scene Objects")
        self.tabsLeft.addTab(self.frameTabStatistics, "Render Settings")
        self.tabsLeft.addTab(self.frameConsole, "Console")

        ##THREADS
        # inspiration from
        # https://stackoverflow.com/a/33453124

        self.renderer = Renderer()
        self.encoder = Encoder()
        self.mainThread = QThread()
        self.renderer.moveToThread(self.mainThread)
        self.mainThread.started.connect(self.startedRendering)
        self.mainThread.started.connect(self.renderer.render)
        self.vidThread = QThread()
        self.encoder.moveToThread(self.vidThread)
        self.vidThread.started.connect(self.encoder.encode)
        self.encoder.encodingCancelled.connect(self.vidThread.terminate)
        self.encoder.encodingCancelled.connect(self.cancelledVid)
        self.encoder.encodingDone.connect(self.vidThread.terminate)
        self.encoder.encodingDone.connect(self.UpdateVidFinal)

        self.renderer.renderDone.connect(self.mainThread.terminate)
        self.renderer.renderDone.connect(self.doneRendering)
        self.renderer.renderDone.connect(self.updateIm)
        self.renderer.renderDone.connect(self.UpdateVid)
        self.renderer.renderDone.connect(self.updateObj)
        self.renderer.renderDone.connect(self.keepSelected)
        self.renderer.renderDone.connect(self.titleBarStat)
        self.grid = QGridLayout()
        self.setWindowState(Qt.WindowMaximized)
        self.splash.mainLoad.connect(self.show)
        self.renderer.consoleRender.connect(self.consoleFunc)
        self.encoder.consoleEncoder.connect(self.consoleFunc)
        ##PALETTE

        self.palette = QPalette()
        self.palette3 = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(61, 61, 61))
        self.palette2 = QPalette()
        self.palette2.setColor(QPalette.Base, QColor(61, 61, 61))
        self.palette2.setColor(QPalette.Text, QColor(245, 245, 245))
        self.palette2.setColor(QPalette.Button, QColor(61, 61, 61))
        self.palette2.setColor(QPalette.ButtonText, QColor(245, 245, 245))
        self.palette2.setColor(QPalette.WindowText, QColor(245, 245, 245))
        self.palette3.setColor(QPalette.Base, QColor(230, 230, 230))
        self.palette3.setColor(QPalette.Text, QColor(40, 40, 40))
        self.palette3.setColor(QPalette.Button, QColor(230, 230, 230))
        self.palette3.setColor(QPalette.ButtonText, QColor(40, 40, 40))
        self.palette3.setColor(QPalette.WindowText, QColor(40, 40, 40))
        self.palette4 = QPalette(self.palette2)
        self.palette5 = QPalette(self.palette3)
        self.palette4.setColor(QPalette.Background, QColor(61, 61, 61, 90))
        self.palette5.setColor(QPalette.Background, QColor(245, 245, 245, 90))

        self.setPalette(self.palette)
        self.menu.setPalette(self.palette2)
        self.tabsRight.setPalette(self.palette2)
        self.tabsLeft.setPalette(self.palette2)

        ##WIDGETS

        self.pix = QPixmap("thb.png")

        self.lbl = QLabel(self.fr2)

        self.loadHolder = QFrame(self.fr2)
        self.loadHolder.setLayout(self.gridLoad)
        self.loadHolder.setMaximumSize(1280, 150)
        self.loadHolder.hide()

        self.loadBox = QFrame(self.loadHolder)
        self.loadBox.setMaximumSize(100, 100)
        self.loadBox.setMinimumSize(100, 100)
        self.loadBox.setAutoFillBackground(True)
        self.loadBox2 = QFrame(self.loadHolder)
        self.loadBox2.setMaximumSize(100, 60)
        self.loadBox2.setMinimumSize(100, 60)
        self.loadBox2.setAutoFillBackground(True)

        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setLayout(self.gridPreview)
        self.lbl.setAttribute(Qt.WA_TranslucentBackground, True)
        self.lbl.setWindowOpacity(0.2)
        self.lbl.mousePressEvent = self.firstClick
        self.lbl.mouseMoveEvent = self.dragClick
        self.lbl.mouseReleaseEvent = self.dragUpdate
        self.lbl.setCursor(QCursor(Qt.OpenHandCursor))
        self.lbl.setMaximumSize(1280, 720)
        self.lbl.setToolTip(
            "drag or scroll to change the camera's perspective")
        self.lbl.setToolTipDuration(3000)
        self.lbl.wheelEvent = self.wheelEve
        self.lbl.setPixmap(self.pix.scaled(1280, 720))
        self.lbl.hide()
        self.mov = QMovie("load3.gif")
        self.mov2 = QMovie("load4.gif")
        self.mov.setScaledSize(QSize(30, 30))

        self.l2 = QLabel(self.fr1)
        self.l3 = QLabel()
        self.l3.setAlignment(Qt.AlignCenter)
        self.l3.setMaximumSize(100, 50)
        self.l4 = QLabel()
        self.l4.setAlignment(Qt.AlignCenter)
        self.l4.setMaximumSize(100, 50)
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
        self.fill1.setMinimumHeight(int(self.height() / 3))
        self.fill2.setMinimumHeight(int(self.height() / 3))

        self.firstLoad = QLabel(self.fill1)
        self.firstLoad.setText("""3D previews appear here
import a .blend file to start""")
        self.firstLoad.setAlignment(Qt.AlignCenter)

        self.list = QListWidget(self.fr3)
        self.list.itemClicked.connect(self.itemUpdate)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setCurrentFont(QFont("Courier New"))
        self.console.ensureCursorVisible()

        self.cancelBtn = QPushButton()
        self.cancelBtn.setText("cancel Preview")
        self.cancelBtn.clicked.connect(self.cancelPreview)

        ##TABS WIDGETS

        self.transformFrame = QFrame(self.frameTabObj)
        self.trFrHg = self.frameTabObj.height() // 3
        self.trFrWd = self.frameTabObj.width()
        self.transformFrame.setMinimumHeight(self.trFrHg)
        self.transformFrame.setMaximumHeight(self.trFrHg)
        self.transformFrame.setLayout(self.gridTransform)
        self.emptyLbl = QLabel()
        self.emptyLbl.setText("       ")
        self.transformLbl = QLabel()
        self.transformLbl.setText("Transform")
        self.locationLbl = QLabel()
        self.locationLbl.setMaximumSize(60, 10)
        self.locationLbl.setText("Position")
        self.locationLbl.setAlignment(Qt.AlignCenter)
        self.rotationLbl = QLabel()
        self.rotationLbl.setMaximumSize(60, 10)
        self.rotationLbl.setText("Rotation")
        self.rotationLbl.setAlignment(Qt.AlignCenter)
        self.scaleLbl = QLabel()
        self.scaleLbl.setMaximumSize(60, 10)
        self.scaleLbl.setText("Scale")
        self.scaleLbl.setAlignment(Qt.AlignCenter)
        self.xTLbl = QLabel()
        self.xTLbl.setText("x:")
        self.xTLbl.setMaximumSize(10, 20)
        self.yTLbl = QLabel()
        self.yTLbl.setText("y:")
        self.yTLbl.setMaximumSize(10, 20)
        self.zTLbl = QLabel()
        self.zTLbl.setText("z:")
        self.zTLbl.setMaximumSize(10, 20)
        self.xTEntry = QLineEdit(self.frameTabObj)
        self.yTEntry = QLineEdit(self.frameTabObj)
        self.zTEntry = QLineEdit(self.frameTabObj)
        self.xREntry = QLineEdit(self.frameTabObj)
        self.yREntry = QLineEdit(self.frameTabObj)
        self.zREntry = QLineEdit(self.frameTabObj)
        self.xSEntry = QLineEdit(self.frameTabObj)
        self.ySEntry = QLineEdit(self.frameTabObj)
        self.zSEntry = QLineEdit(self.frameTabObj)
        self.Entries = [self.xTEntry, self.yTEntry, self.zTEntry,
                        self.xREntry, self.yREntry, self.zREntry,
                        self.xSEntry, self.ySEntry, self.zSEntry,
                        ]

        for TEntry in self.Entries:
            TEntry.setText("0")
            TEntry.setMaximumHeight(30)
            TEntry.setReadOnly(True)
            TEntry.setCursor(QCursor(Qt.SizeHorCursor))
            TEntry.setValidator(QDoubleValidator())
            TEntry.mousePressEvent = lambda ev, en=TEntry: self.onEntryClick(
                ev, en)
            TEntry.editingFinished.connect(
                lambda en=TEntry: self.onEntryReturnPressed(en))
            TEntry.textEdited.connect(
                lambda ev, wid=TEntry: self.entryChanger(ev, wid))
            TEntry.mouseMoveEvent = lambda ev, en=TEntry: self.onEntryDrag(ev,
                                                                           en)
            TEntry.mouseReleaseEvent = lambda ev, en=TEntry: self.onEntryLeave(
                ev, en)
            TEntry.mouseDoubleClickEvent = lambda ev,
                                                  en=TEntry: self.onEntryDblClick(
                ev, en)

            TEntry.setAlignment(Qt.AlignCenter)

        self.scaleFrame = QFrame(self.frameTabObj)
        self.scaleFrame.setLayout(self.scaleGrid)
        self.scaleCheck = QCheckBox(self.scaleFrame)
        self.scaleCheck.setText("scale proportionally")

        self.frMT = QFrame(self.frameTabObj)
        self.frMT.setLayout(self.gridMaterial)
        self.frMT.setMaximumHeight(470)
        self.frMTset = QFrame(self.frameTabObj)
        self.frMTset.setLayout(self.gridMaterialSet)
        self.materialLabel = QLabel(self.frMT)
        self.materialLabel.setText("Material")
        self.materialLabel.setMaximumSize(70, 70)
        self.materialList = QListWidget(self.frMT)
        self.matLst = ["diffuse", "metallic", "emission", "glossy",
                       "subsurface", "glass", "custom"]
        self.materialList.insertItems(6, self.matLst)
        for i in range(7):
            item = self.materialList.item(i)
            item.setIcon(QIcon("assets\\" + self.matLst[i] + ".png"))
        self.materialList.itemClicked.connect(self.updateGUIMat)
        self.materialList.setMaximumHeight(400)
        self.materialList.setViewMode(QListView.IconMode)
        self.materialList.setMovement(QListView.Static)
        self.materialList.setIconSize(QSize(90, 90))

        self.colorFrame = QFrame()
        self.colorFrame.setLayout(self.gridColor)
        self.colorFrame.setMinimumWidth(self.fr1.width() - 20)
        self.colorFrame.setMaximumHeight(100)
        self.colorSwatchcl = QPixmap(50, 30)
        self.colorSwatch = QLabel()
        self.colorSwatch.setMaximumSize(50, 30)
        self.colorSwatch.setPixmap(self.colorSwatchcl)
        self.colorSwatch.mousePressEvent = self.tryColor
        self.colorSwatchLabel = QLabel()
        self.colorSwatchLabel.setText("color")
        self.colorSwatchLabel.setMaximumWidth(100)

        self.IOR = QLineEdit()
        self.IOR.setAlignment(Qt.AlignCenter)
        self.IORLabel = QLabel()
        self.IORLabel.setText("IOR")
        self.IORLabel.setAlignment(Qt.AlignCenter)
        self.entrySetter(self.IOR)
        self.IORvalidate = QDoubleValidator()
        self.IORvalidate.setBottom(0)
        self.roughness = QSlider()
        self.roughness.setRange(0, 1000)
        self.roughnessValue = QLineEdit()
        self.roughnessValue.setText("0")
        self.roughnessValue.setMaximumWidth(70)
        self.roughnessValue.setAlignment(Qt.AlignCenter)
        self.roughnessValue.setReadOnly(True)
        self.roughness.sliderMoved.connect(
            lambda w=self.roughness, w2=self.roughnessValue: self.sliderMove(w,
                                                                             w2))
        self.settingsLabel = QLabel()
        self.settingsLabel.setText("Material Settings")
        self.settingsLabel.setMaximumSize(140, 30)
        self.roughnessFrame = QFrame()
        self.roughnessFrame.setLayout(self.gridRoughness)
        self.roughnessFrame.setMinimumWidth(self.fr1.width() - 20)
        self.roughnessFrame.setMaximumHeight(100)
        self.roughnessLabel = QLabel()
        self.roughnessLabel.setAlignment(Qt.AlignCenter)
        self.roughnessLabel.setText("roughness")
        self.roughnessLabel.setMaximumWidth(70)
        self.roughness.setOrientation(Qt.Horizontal)
        self.materialUpdate = QPushButton()
        self.materialUpdate.setText("update material")
        self.materialUpdate.clicked.connect(self.updateMaterial)

        self.frTR1 = QFrame(self.frameTabRendering)
        self.frTR1.setMaximumHeight(100)
        self.frTR1.setLayout(self.gridAnimation)
        self.animButton = QPushButton()
        self.animButton.setText("render animation")
        self.animButton.clicked.connect(self.rendAnimation)
        self.frameFrame = QFrame()
        self.frameFrame.setLayout(self.gridFrame)
        self.frameStart = QLineEdit()
        self.frameEnd = QLineEdit()
        self.frameStep = QLineEdit()
        self.frameStartLabel = QLabel()
        self.frameStartLabel.setText("start frame")
        self.frameEndLabel = QLabel()
        self.frameEndLabel.setText("end frame")
        self.frameStepLabel = QLabel()
        self.frameStepLabel.setText("step")
        self.entrySetter(self.frameStep)
        self.entrySetter(self.frameEnd)
        self.entrySetter(self.frameStart)
        self.frameStart.setText("0")
        self.frameEnd.setText("250")
        self.frameStep.setText("1")
        self.natValidate = QIntValidator()
        self.natValidate.setBottom(1)
        self.frameStep.setValidator(self.natValidate)
        self.intValidate = QIntValidator()
        self.intValidate.setBottom(0)
        self.frameStart.setValidator(self.intValidate)
        self.frameEnd.setValidator(self.intValidate)

        self.frRG = QFrame(self.frameTabPhysics)
        self.frRG.setMaximumHeight(200)
        self.frRG.setLayout(self.gridRigid)
        self.rigidCheck = QCheckBox(self.frRG)
        self.rigidCheck.setText("Rigid Body")
        self.rigidCheck.clicked.connect(self.rigidBody)
        self.rigidType = QComboBox(self.frRG)
        self.rigidType.insertItems(2, ["Passive", "Active"])
        self.rigidMass = QLineEdit(self.frRG)
        self.rigidMassLabel = QLabel(self.frRG)
        self.rigidTypeLabel = QLabel(self.frRG)
        self.rigidMassLabel.setText("body mass")
        self.rigidTypeLabel.setText("body type")
        self.entrySetter(self.rigidMass)
        self.minValid = QDoubleValidator()
        self.minValid.setBottom(0)
        self.rigidMass.setValidator(self.minValid)
        self.IOR.setValidator(self.minValid)
        self.rigidMass.setText("1")
        self.rigidBake = QPushButton(self.frRG)
        self.rigidBake.setText("Bake Rigid Body")
        self.rigidBake.setMaximumWidth(100)
        self.rigidBake.clicked.connect(self.rigidBakeFunc)

        self.renderSettings = QFrame(self.frameTabStatistics)
        self.renderSettings.setLayout(self.gridRndSt)
        self.rendEngine = QComboBox(self.renderSettings)
        self.rendEngine.insertItems(2, ["Cycles", "Eevee"])
        self.rendEngine.currentTextChanged.connect(self.deviceCheck)
        self.rendEngineLabel = QLabel()
        self.rendEngineLabel.setText("render engine")
        self.renderEngineFrame = QFrame(self.renderSettings)
        self.renderEngineFrame.setLayout(self.gridRendEng)
        self.renderDeviceFrame = QFrame(self.renderSettings)
        self.renderDeviceFrame.setLayout(self.gridRendDev)
        self.renderDeviceFrame.setMaximumHeight(100)
        self.renderEngineFrame.setMaximumHeight(100)
        self.rendDevice = QComboBox(self.renderSettings)
        self.rendDevice.insertItems(2, ["CPU", "GPU"])
        self.rendDeviceLabel = QLabel()
        self.rendDeviceLabel.setText("render device")
        self.samplesFrame = QFrame(self.renderSettings)
        self.samplesFrame.setLayout(self.gridSamples)
        self.samplesFrame.setMaximumHeight(100)
        self.samplesFrame.setMaximumWidth(200)
        self.samples = QLineEdit(self.samplesFrame)
        self.entrySetter(self.samples)
        self.samples.setText("32")
        self.samplesLabel = QLabel(self.samplesFrame)
        self.samplesLabel.setText("samples")
        self.infoText = QLabel(self.renderSettings)
        self.infoText.setText(
            "For realistic (but slower) results use cycles.\nFor faster previews use eevee. \nUse GPU only if your device has a dedicated GPU.\nTo have less noise in cycles, increase the samples count. \nThis makes rendering much slower so it is not advisable for animations."
        )
        self.infoText.setWordWrap(True)
        self.infoText.setMaximumWidth(200)
        self.updRendSet = QPushButton(self.renderSettings)
        self.updRendSet.setText("update Render Settings")
        self.updRendSet.clicked.connect(self.rendSettingsFunc)
        self.updRendSet.setMaximumWidth(200)

        # setting palettes for widgets

        self.l3.setPalette(self.palette2)
        self.l5.setPalette(self.palette2)
        self.l6.setPalette(self.palette2)
        self.tabsRight.setPalette(self.palette2)
        self.list.setPalette(self.palette2)
        self.l2.setPalette(self.palette2)
        self.firstLoad.setPalette(self.palette2)
        self.console.setPalette(self.palette2)
        self.loadHolder.setPalette(self.palette4)

        # adding widgets to grid

        self.gridPreview.addWidget(self.fill1, 0, 0)
        self.grid3.addWidget(self.firstLoad, 1, 0)
        self.gridPreview.addWidget(self.fill2, 3, 0)
        self.grid3.addWidget(self.loadHolder, 0, 0)
        self.gridLoad.addWidget(self.l4, 0, 0)
        self.gridLoad.addWidget(self.loadBox, 0, 0)
        self.gridLoad.addWidget(self.loadBox2, 1, 0)
        self.gridLoad.addWidget(self.l3, 1, 0)
        self.gridLoad.addWidget(self.cancelBtn, 2, 0)
        self.grid7.addWidget(self.list, 0, 0)
        self.grid3.addWidget(self.lbl, 0, 0)
        self.gridConsole.addWidget(self.console)
        self.grid6.addWidget(self.transformFrame, 0, 0)
        self.grid6.addWidget(self.scaleFrame, 1, 0)
        self.gridRendering.addWidget(self.frTR1)
        self.gridPhysics.addWidget(self.frRG)
        self.grid6.addWidget(self.frMT, 2, 0)
        self.grid6.addWidget(self.frMTset, 3, 0)
        self.gridAnimation.addWidget(self.animButton, 1, 0)
        self.gridAnimation.addWidget(self.frameFrame, 0, 0)
        self.gridFrame.addWidget(self.frameStartLabel, 0, 0)
        self.gridFrame.addWidget(self.frameStart, 0, 1)
        self.gridFrame.addWidget(self.frameEndLabel, 0, 2)
        self.gridFrame.addWidget(self.frameEnd, 0, 3)
        self.gridFrame.addWidget(self.frameStepLabel, 0, 4)
        self.gridFrame.addWidget(self.frameStep, 0, 5)
        self.gridTransform.addWidget(self.emptyLbl, 1, 0)
        self.gridTransform.addWidget(self.transformLbl, 0, 0)
        self.gridTransform.addWidget(self.locationLbl, 1, 1)
        self.gridTransform.addWidget(self.rotationLbl, 1, 2)
        self.gridTransform.addWidget(self.scaleLbl, 1, 3)
        self.gridTransform.addWidget(self.xTLbl, 2, 0)
        self.gridTransform.addWidget(self.xTEntry, 2, 1)
        self.gridTransform.addWidget(self.xREntry, 2, 2)
        self.gridTransform.addWidget(self.xSEntry, 2, 3)
        self.gridTransform.addWidget(self.yTLbl, 3, 0)
        self.gridTransform.addWidget(self.yTEntry, 3, 1)
        self.gridTransform.addWidget(self.yREntry, 3, 2)
        self.gridTransform.addWidget(self.ySEntry, 3, 3)
        self.gridTransform.addWidget(self.zTLbl, 4, 0)
        self.gridTransform.addWidget(self.zTEntry, 4, 1)
        self.gridTransform.addWidget(self.zREntry, 4, 2)
        self.gridTransform.addWidget(self.zSEntry, 4, 3)
        self.gridRigid.addWidget(self.rigidCheck, 0, 0)
        self.gridRigid.addWidget(self.rigidMass, 1, 1)
        self.gridRigid.addWidget(self.rigidMassLabel, 1, 0)
        self.gridRigid.addWidget(self.rigidType, 1, 3)
        self.gridRigid.addWidget(self.rigidTypeLabel, 1, 2)
        self.gridRigid.addWidget(self.rigidBake, 2, 3)
        self.gridMaterial.addWidget(self.materialList, 1, 0)
        self.gridMaterial.addWidget(self.materialLabel, 0, 0)
        self.gridMaterialSet.addWidget(self.colorFrame, 1, 0)
        self.gridMaterialSet.addWidget(self.settingsLabel, 0, 0)
        self.gridColor.addWidget(self.colorSwatchLabel, 0, 0)
        self.gridColor.addWidget(self.colorSwatch, 0, 1)
        self.gridColor.addWidget(self.IORLabel, 0, 2)
        self.gridColor.addWidget(self.IOR, 0, 3)
        self.gridMaterialSet.addWidget(self.roughnessFrame, 2, 0)
        self.gridRoughness.addWidget(self.roughnessLabel, 0, 0)
        self.gridRoughness.addWidget(self.roughness, 0, 1)
        self.gridRoughness.addWidget(self.roughnessValue, 0, 2)
        self.gridMaterialSet.addWidget(self.materialUpdate, 3, 0)
        self.scaleGrid.addWidget(self.scaleCheck)
        self.gridStats.addWidget(self.renderSettings)
        self.gridRendEng.addWidget(self.rendEngine, 0, 1)
        self.gridRndSt.addWidget(self.renderDeviceFrame, 1, 0)
        self.gridRndSt.addWidget(self.renderEngineFrame, 0, 0)
        self.gridRendEng.addWidget(self.rendEngineLabel, 0, 0)
        self.gridRndSt.addWidget(self.updRendSet, 3, 0)
        self.gridRndSt.addWidget(self.infoText, 4, 0)
        self.gridRendDev.addWidget(self.rendDevice, 0, 1)
        self.gridRendDev.addWidget(self.rendDeviceLabel, 0, 0)
        self.gridRndSt.addWidget(self.samplesFrame, 2, 0)
        self.gridSamples.addWidget(self.samples, 0, 1)
        self.gridSamples.addWidget(self.samplesLabel, 0, 0)

        # graphics
        self.graphic1 = QGraphicsOpacityEffect()
        self.graphic1.setOpacity(0.5)
        self.lbl.setGraphicsEffect(self.graphic1)
        self.painter = QPainter(self.colorSwatch.pixmap())
        brush = QBrush(Qt.gray, Qt.SolidPattern)
        self.painter.setBrush(brush)
        self.painter.drawRect(0, 0, 50, 30)
        self.painter.end()

        self.desktop = QDesktopWidget()
        self.desktop.screenCountChanged.connect(self.resizeEvent)
        self.heightInit = self.desktop.screenGeometry().height()
        self.setMinimumHeight(2 * self.heightInit // 3)

        # onRun functions
        self.rigidBody()

        ##VARIABLES
        self.dict = {"pic": QPixmap("thb.png")}
        self.dragged = False
        self.isVideoCancelled = False
        self.timelst = []
        self.scrollLst = []
        self.currentTheme = "Dark"
        self.path = pathlib.Path().absolute()
        self.entryClicked = {self.xTEntry: False,
                             self.yTEntry: False,
                             self.zTEntry: False,
                             self.xREntry: False,
                             self.yREntry: False,
                             self.zREntry: False,
                             self.xSEntry: False,
                             self.ySEntry: False,
                             self.zSEntry: False,
                             self.rigidMass: False,
                             self.IOR: False,
                             self.samples: False,
                             self.frameEnd: False,
                             self.frameStart: False,
                             self.frameStep: False
                             }
        self.entryDragged = copy.copy(self.entryClicked)
        self.entryChanged = copy.copy(self.entryClicked)
        self.itemUpdating = False
        self.selObj = None
        self.entryXpos = {}
        self.entryVal = {}
        self.selInd = -1
        self.title = self.windowTitle()
        self.isLoaded = False
        self.defaultAnim = [1, 125, 4]
        self.isAnimation = False
        self.isRendering = False
        self.mainVid = None
        self.isMovie = False
        self.isCancelled = False
        self.isUpdated = False
        self.currentColor = QColor(255, 255, 255)
        self.currentMaterial = None
        self.materialDict = {
            "diffuse": {"color": QColor(255, 255, 255),
                        "IOR": 1.45,
                        "roughness": 0.5
                        },
            "metallic": {"color": QColor(255, 255, 255),
                         "IOR": 1.45,
                         "roughness": 0.14
                         },
            "subsurface": {"color": QColor(212, 164, 169),
                           "IOR": 1.45,
                           "roughness": 0.5
                           },
            "glossy": {"color": QColor(255, 0, 0),
                       "IOR": 1.45,
                       "roughness": 0
                       },
            "glass": {"color": QColor(255, 255, 255),
                      "IOR": 1.45,
                      "roughness": 0
                      },
            "emission": {"color": QColor(255, 255, 255),
                         "IOR": 1.45,
                         "roughness": 0.5
                         }

        }

    def deviceCheck(self):
        rendEng = self.rendEngine.currentText()
        if rendEng == "Cycles":
            self.rendDevice.setVisible(True)
            self.rendDeviceLabel.setVisible(True)
        else:
            self.rendDevice.setVisible(False)
            self.rendDeviceLabel.setVisible(False)

    def rendSettingsFunc(self):
        if self.isLoaded:
            self.loaderImage()
            rendEng = self.rendEngine.currentText()
            rendDvc = self.rendDevice.currentText()
            samples = self.samples.text()
            lst = [rendEng, rendDvc, samples]
            dataIn = open("DT_PIPIN.data", "w")
            dataIn.write("|rendSettings#" + "#".join(lst) + "#")
            self.mainThread.start()

    def rigidBakeFunc(self):
        if self.isLoaded:
            self.loaderImage()
            if self.list.selectedItems() != []:
                self.selObj = self.list.selectedItems()[0]
                objName = self.selObj.text()
                objName = objName[:len(objName) - 1]
                dataIn = open("DT_PIPIN.data", "w")
                lst = [objName]
                lst.append(self.rigidMass.text())
                lst.append(self.rigidType.currentText())
                dataIn.write("|rigidBake#" + "#".join(lst) + "#")
                self.mainThread.start()

    def deleteObjFunc(self, event):
        if self.isLoaded:
            self.itemCurrent()
            self.loaderImage()
            if self.list.selectedItems() != []:
                self.selObj = self.list.selectedItems()[0]
                objName = self.selObj.text()
                objName = objName[:len(objName) - 1]

                dataIn = open("DT_PIPIN.data", "w")
                dataIn.write("|delObj#" + objName + "#")
                self.mainThread.start()

    def addObjFunc(self, event, objType):
        if self.isLoaded:
            self.loaderImage()
            dataIn = open("DT_PIPIN.data", "w")
            dataIn.write("|addObj#" + objType + "#")
            self.mainThread.start()

    def updateGUIMat(self):
        material = self.materialList.currentItem().text()
        if material != "custom":
            self.currentMaterial = material
            materialDct = self.materialDict[material]
            self.roughness.setValue(materialDct["roughness"] * 1000)
            self.roughnessValue.setText(str(materialDct["roughness"]))
            self.IOR.setText(str(materialDct["IOR"]))
            self.colorSwatchcl.fill(materialDct["color"])
            self.colorSwatch.setPixmap(self.colorSwatchcl)
            self.currentColor = materialDct["color"]

    def updateMaterial(self):
        if self.isLoaded:
            self.itemCurrent()
            self.loaderImage()
            self.selObj = self.list.selectedItems()[0]
            objName = self.selObj.text()
            objName = objName[:len(objName) - 1]
            dataIn = open("DT_PIPIN.data", "w")

            lst = [self.currentMaterial, self.roughness.value()]
            lst = lst + [self.IOR.text(), self.currentColor.getRgb()]
            lst = list(map(lambda x: str(x), lst))
            dataIn.write("|UpdMat#" + objName + "#" + "#".join(lst) + "#")
            self.itemUpdating = True
            self.mainThread.start()

    def sliderMove(self, widget, widget2):
        val = widget
        widget2.setText(str(round(val / 1000, 4)))
        self.materialList.setCurrentRow(6)

    def tryColor(self, event):
        color = QColorDialog.getColor(self.currentColor)

        if color.isValid():
            self.currentColor = color

            self.painter = QPainter(self.colorSwatch.pixmap())
            brush = QBrush(color, Qt.SolidPattern)
            self.painter.setBrush(brush)
            self.painter.drawRect(0, 0, 50, 30)
            self.painter.end()
            self.materialList.setCurrentRow(6)

    def rigidBody(self):
        if self.rigidCheck.checkState() == 0:
            self.rigidBake.setVisible(False)
            self.rigidMass.setVisible(False)
            self.rigidType.setVisible(False)
            self.rigidMassLabel.setVisible(False)
            self.rigidTypeLabel.setVisible(False)
        if self.rigidCheck.checkState() == 2:
            self.rigidBake.setVisible(True)
            self.rigidMass.setVisible(True)
            self.rigidType.setVisible(True)
            self.rigidMassLabel.setVisible(True)
            self.rigidTypeLabel.setVisible(True)

    def doneRendering(self):
        self.isRendering = False

    def startedRendering(self):
        self.isRendering = True
        self.isUpdated = False

    def SaveDiag(self):
        if self.isLoaded:
            dict = open("DT_PIPIN.data", "w")
            dict.write("|Save#Null")
            self.mainThread.start()
        else:
            QMessageBox.warning(self, "Error",
                                "there are no loaded .blend files to save")

    def titleBarStat(self):
        status = open("BLEND_SAVE.data", "r")
        statDat = status.read()
        self.setWindowTitle(self.title + " " + statDat)

    def entryChanger(self, ev, wid):
        self.entryChanged[wid] = True

    def keepSelected(self):
        self.list.setCurrentRow(self.selInd)

    def itemCurrent(self):
        self.selObj = self.list.selectedItems()[0]
        self.selInd = self.list.currentRow()

    def updateObj(self):
        if self.itemUpdating:
            readData = open("ob_TRANS.data", "r")
            transData = readData.read().split("#")
            rigidData = open("rigid_DATA.data", "r")
            rigidInfo = rigidData.read().split("#")
            if rigidInfo[0] != "None":
                self.rigidCheck.setChecked(True)
                self.rigidMass.setText(rigidInfo[2])
                if rigidInfo[1] == "PASSIVE":
                    self.rigidType.setCurrentIndex(0)
                else:
                    self.rigidType.setCurrentIndex(1)
            else:
                self.rigidCheck.setChecked(False)
            self.rigidBody()
            for i in range(len(self.Entries)):
                self.Entries[i].setText(transData[i])
                self.itemUpdating = False

    def itemUpdate(self):
        self.itemCurrent()
        self.selObj = self.list.selectedItems()[0]
        objName = self.selObj.text()
        objName = objName[:len(objName) - 1]
        dataIn = open("DT_PIPIN.data", "w")
        dataIn.write("|ObjData#" + objName + "#")
        dataIn.write("|RigidData#" + objName + "#")
        dataIn.close()
        self.itemUpdating = True
        self.mainThread.start()

    def onEntryClick(self, event, widget):
        self.entryClicked[widget] = True
        lst3 = [self.samples, self.frameStart, self.frameEnd, self.frameStep]
        if widget not in lst3:
            self.entryXpos[widget] = round(
                event.x() / 10 - float(widget.text()), 4)
        else:
            self.entryXpos[widget] = round(event.x() - float(widget.text()))
        self.entryVal[widget] = float(widget.text())

        if self.scaleCheck.checkState() == Qt.Checked:
            for i in range(len(self.Entries)):
                if i // 3 == 2:
                    wid = self.Entries[i]
                    self.entryVal[wid] = float(wid.text())

    def onEntryDrag(self, event, widget):
        lst = [self.rigidMass, self.IOR, self.samples]
        lst = lst + [self.frameStart, self.frameEnd, self.frameStep]
        lst2 = [self.samples, self.frameStep]
        lst3 = [self.samples, self.frameStart, self.frameEnd, self.frameStep]
        if self.entryClicked[widget]:
            if widget not in lst3:
                value = round(event.x() / 10 - self.entryXpos[widget], 4)
            else:
                value = round(event.x() - self.entryXpos[widget])
            if not (widget in lst and value <= 0):
                if not (widget in lst2 and value < 1):
                    c1 = self.scaleCheck.checkState() == Qt.Checked
                    c2 = widget in self.Entries

                    if c2 and self.Entries.index(widget) // 3 == 2 and c1:
                        for i in range(len(self.Entries)):
                            if i // 3 == 2:

                                wid = self.Entries[i]
                                valO = self.entryVal[widget]
                                if valO == 0:
                                    valO += 0.1
                                val1 = self.entryVal[wid]
                                wid.setText(
                                    str(round(val1 * (value / valO), 4)))
                    else:
                        widget.setText(str(value))
                    if widget == self.IOR:
                        self.materialList.setCurrentRow(6)
            self.entryDragged[widget] = True

    def onEntryLeave(self, event, widget):
        if self.entryDragged[widget] and widget in self.Entries:
            val = widget.text()
            i = self.Entries.index(widget)
            if self.list.selectedItems() != []:
                self.ObjTransform(i, val)
        self.entryClicked[widget] = False
        self.entryDragged[widget] = False

    def onEntryDblClick(self, event, widget):
        widget.setReadOnly(False)

    def onEntryReturnPressed(self, widget):

        widget.setReadOnly(True)
        widget.setCursor(QCursor(Qt.SizeHorCursor))
        if widget in self.Entries:
            i = self.Entries.index(widget)
            val = widget.text()
            if self.list.selectedItems() != [] and self.entryChanged[widget]:
                self.ObjTransform(i, val)

        if widget == self.rigidMass:
            if widget.text() == "0":
                widget.setText("0.001")
        self.entryChanged[widget] = False

    def ObjTransform(self, i, val):
        ObjCor = ["xT", "yT", "zT", "xR", "yR", "zR", "xS", "yS", "zS"]
        self.loaderImage()
        self.selObj = self.list.selectedItems()[0]
        objName = self.selObj.text()
        objName = objName[:len(objName) - 1]
        dataIn = open("DT_PIPIN.data", "w")
        c = self.scaleCheck.checkState() == Qt.Checked
        dataIn.write(
            "|ObjTrans#" + objName + "#" + ObjCor[i] + "#" + val + "#" + str(
                c) + "#")
        self.mainThread.start()

    def consoleFunc(self, text):

        self.console.insertPlainText(text)
        self.console.moveCursor(QTextCursor.End)
        scrollBar = self.console.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())

    def changeTheme(self):

        if self.currentTheme == "Dark":
            frame = self.mov.currentFrameNumber()
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
            self.currentTheme = "Light"
        else:
            frame = self.mov2.currentFrameNumber()

            self.list.setPalette(self.palette2)
            self.tabsRight.setPalette(self.palette2)
            self.tabsLeft.setPalette(self.palette2)
            self.l2.setPalette(self.palette2)
            self.setPalette(self.palette)
            self.menu.setPalette(self.palette2)
            self.l3.setPalette(self.palette2)
            self.firstLoad.setPalette(self.palette4)
            self.loadHolder.setPalette(self.palette4)
            self.console.setPalette(self.palette2)

            self.currentTheme = "Dark"

    def entrySetter(self, TEntry):
        TEntry.setText("0")
        TEntry.setMaximumHeight(30)
        TEntry.setMaximumWidth(70)
        TEntry.setReadOnly(True)
        TEntry.setCursor(QCursor(Qt.SizeHorCursor))
        TEntry.setValidator(QDoubleValidator())
        TEntry.mousePressEvent = lambda ev, en=TEntry: self.onEntryClick(ev,
                                                                         en)
        TEntry.editingFinished.connect(
            lambda en=TEntry: self.onEntryReturnPressed(en))
        TEntry.textEdited.connect(
            lambda ev, wid=TEntry: self.entryChanger(ev, wid))
        TEntry.mouseMoveEvent = lambda ev, en=TEntry: self.onEntryDrag(ev, en)
        TEntry.mouseReleaseEvent = lambda ev, en=TEntry: self.onEntryLeave(ev,
                                                                           en)
        TEntry.mouseDoubleClickEvent = lambda ev,
                                              en=TEntry: self.onEntryDblClick(
            ev, en)

    def OpenFileDiag(self):
        QFileDialog.getOpenFileName(self, "Open Rendorium Project", "C:/",
                                    "Rendorium  Files (*.drm)")

    def ImportFileDiag(self):
        importer = QFileDialog.getOpenFileName(self, "Import Blender Project",
                                               "C:/",
                                               "Blender Project (*.blend)")
        if importer[0]:
            self.Importer(importer[0])

    def SaveAsDiag(self):
        if self.isLoaded:
            saveAs = QFileDialog.getSaveFileName(self, "Save Blender Project",
                                                 "C:/",
                                                 "Blender Project (*.blend)")
            if saveAs[0]:
                self.SaverAs(saveAs[0])
        else:

            QMessageBox.warning(self, "Error",
                                "there are no loaded .blend files to save")

    def SaverAs(self, filePath):
        dict = open("DT_PIPIN.data", "w")
        dict.write("|SaveAs#" + filePath)
        self.mainThread.start()

    def wheelEve(self, mouseEvent):
        self.scrolling = True
        QTimer.singleShot(500, self.funScroll)
        point = mouseEvent.angleDelta()
        self.scrollLst.append(point.y())
        self.timelst.append(time.time())
        self.scrolling = False

    def funScroll(self):
        b = time.time()
        if b - self.timelst[-1] >= 0.5:
            distance = sum(self.scrollLst)
            self.cameraPan(dz=str(distance))
            self.scrollLst = []

    def firstClick(self, mouseEvent):
        self.lbl.setCursor(QCursor(Qt.ClosedHandCursor))
        self.x1 = mouseEvent.globalX()
        self.y1 = mouseEvent.globalY()
        self.dragged = False
        self.x2 = 0
        self.y2 = 0

    def dragClick(self, mouseEvent):
        self.x2 = mouseEvent.globalX()
        self.y2 = mouseEvent.globalY()
        self.dragged = True

    def dragUpdate(self, mouseEvent):
        self.lbl.setCursor(QCursor(Qt.OpenHandCursor))
        if self.dragged:
            ddx = str(self.x2 - self.x1)
            dy = str(self.y2 - self.y1)

            self.cameraPan(ddx=ddx, dy=dy)

    def itemListUpdate(self):
        items = open("ob_DATA.data", "r")
        self.list.clear()
        a = items.readlines()
        self.list.insertItems(len(a), a)

    def UpdateVidFinal(self):
        if not self.isVideoCancelled:
            self.mainVid = QMovie("anim.webp")
            aspect = (self.width() // 2) / 1920
            height2 = 1080 * aspect
            self.movSize = QSize(self.width() // 2, height2)
            self.mainVid.setScaledSize(self.movSize)
            self.mainVid.setSpeed(self.defaultAnim[2] * 100)
            self.lbl.clear()
            self.lbl.setMovie(self.mainVid)
            self.mainVid.start()
            self.loadHolder.hide()
            self.l3.hide()
            self.l4.hide()
            self.graphic1.setOpacity(1)
            self.lbl.show()
            items = open("ob_DATA.data", "r")
            self.list.clear()
            a = items.readlines()
            self.list.insertItems(len(a), a)
            self.isAnimation = False
            self.isMovie = True
            self.isVideoCancelled = False

    def cancelledVid(self):

        self.isVideoCancelled = True
        if not self.isMovie:
            self.updateIm()

    def UpdateVid(self):
        if self.isAnimation and os.path.exists("signalANIMR"):
            self.vidThread.start()
        else:
            self.isAnimation = False
            self.updateIm()

        if os.path.exists("signalANIMR"):
            os.system("del signalANIMR")

    def rendSettingsGet(self):
        file1 = open("rend_DATA.data", "r")
        rendLst = file1.read()
        rendLst = rendLst.split("#")
        if rendLst[0] == "CYCLES":
            self.rendEngine.setCurrentIndex(0)
            self.rendDevice.setCurrentIndex(["CPU", "GPU"].index(rendLst[1]))
            self.samples.setText(rendLst[2])
        else:
            self.rendEngine.setCurrentIndex(1)
            self.samples.setText(rendLst[2])

    def updateIm(self):
        if (not self.isLoaded) and self.isCancelled:
            self.loadHolder.hide()
            self.l3.hide()
            self.l4.hide()
            self.firstLoad.show()
            self.isCancelled = False
            self.isVideoCancelled = False
            self.isUpdated = True

        if not self.isAnimation and not self.isUpdated:

            self.pix = QPixmap("render.png")
            self.dict["pic"] = QPixmap("render.png")
            self.var = 'QPixmap("render.png")'
            self.pix = self.pix.scaled(self.picSize[0], self.picSize[1],
                                       Qt.KeepAspectRatio)
            self.lbl.setPixmap(self.pix)
            self.loadHolder.hide()
            self.l3.hide()
            self.l4.hide()
            self.graphic1.setOpacity(1)
            self.lbl.show()
            items = open("ob_DATA.data", "r")
            self.list.clear()
            a = items.readlines()
            self.list.insertItems(len(a), a)
            self.rendSettingsGet()
            self.isLoaded = True
            self.isMovie = False
            self.isCancelled = False
            self.isVideoCancelled = False
            if os.path.exists("signalANIMR"):
                os.system("del signalANIMR")

    def changeLabel(self):
        a = self.angle.value()
        b = self.angle2.value()
        c = self.angle3.value()
        self.l2.setText(str(a))
        self.l5.setText(str(b))
        self.l6.setText(str(c))
        self.released = True

    def Importer(self, fileName):
        self.loaderImage()
        dict = open("DT_PIPIN.data", "w")
        lst = ["|import", fileName]
        combined = "#".join(lst)
        dict.write(combined)
        self.mainThread.start()

    def renderR(self, n=False, ddx="0", dy="0", dz="0"):
        self.loaderImage()
        str1 = self.comb.currentText()
        str2 = self.comb2.currentText()
        str3 = self.comb3.currentText()
        dict = open("DT_PIPIN.data", "w")
        lst = ["|test", str1, str2, str3, str(self.angle.value()),
               str(self.angle2.value()), str(self.angle3.value()), ddx, dy, dz]
        combined = "#".join(lst)
        dict.write(combined)
        self.mainThread.start()

    def rendAnimation(self):
        if self.isLoaded:
            self.loaderImage()
            self.isVideoCancelled = False
            dict = open("DT_PIPIN.data", "w")
            f1 = int(self.frameStart.text())
            f2 = int(self.frameEnd.text())
            f3 = int(self.frameStep.text())
            self.defaultAnim = [f1, f2, f3]
            lst = ["|Anim"] + self.defaultAnim
            combined = "#".join(map(lambda x: str(x), lst))
            dict.write(combined)
            self.isAnimation = True
            if os.path.exists("anim.mkv"):
                os.system("del anim.mkv")
            if os.path.exists("signalANIMR"):
                os.system("del signalANIMR")
            self.mainThread.start()

    def cameraPan(self, n=False, ddx="0", dy="0", dz="0"):
        self.loaderImage()
        dict = open("DT_PIPIN.data", "w")
        lst = ["|cameraPan", ddx, dy, dz]
        combined = "#".join(lst)
        dict.write(combined)
        self.mainThread.start()

    def loaderImage(self):
        imgpath = open("IMG_PATH.data", "w")
        imgpath.write(str(pathlib.Path().absolute()))
        width = self.fr2.width()
        self.fr2.setMinimumWidth(width)
        self.lbl.clear()
        self.lbl.setPixmap(self.pix)
        if self.mainVid != None:
            self.mainVid.stop()
        self.firstLoad.hide()
        self.loadHolder.show()
        self.l3.show()
        self.l4.show()
        self.fill1.show()
        self.fill2.show()
        self.graphic1.setOpacity(0.5)

    def onRun(self):
        self.splash.onBoot()

    def cancelPreview(self, event):
        self.isCancelled = True
        self.renderer.killRender()
        self.encoder.encodeCancel()
        self.console.insertPlainText("\nPreview Cancelled\n")

    def closeEvent(self, event):
        self.mainThread.terminate()
        self.vidThread.terminate()
        self.renderer.killRender()

    def resizeEvent(self, event):

        self.fill1.setMinimumHeight(int(self.height() / 3))
        self.fill2.setMinimumHeight(int(self.height() / 3))
        self.fr3.setMinimumWidth(self.width() // 4)
        self.picSize = (int(self.width() / 2), int(self.height() / 2))
        if not self.isMovie:
            self.pixa = self.dict["pic"]
            self.pixa = self.pixa.scaled(self.picSize[0], self.picSize[1],
                                         Qt.KeepAspectRatio)
            self.fr2.setMinimumWidth(int(self.width() / 2))
            self.lbl.setPixmap(self.pixa)
        else:
            self.mainVid.stop()
            width = self.mainVid.scaledSize().width()
            aspect = (self.width() // 2) / width
            height = self.mainVid.scaledSize().height()
            height = height * aspect
            self.fr2.setMinimumWidth(int(self.width() / 2))
            self.movSize = QSize((self.width() // 2), height)
            self.mainVid.setScaledSize(self.movSize)
            self.mainVid.start()


App = QApplication(sys.argv)
App.setStyle('Fusion')

w = Main()
w.onRun()
App.exec_()
