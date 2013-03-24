from PyQt4 import QtGui,QtCore
import sys,os,pickle
from functools import partial
from darkOrange import DarkOrange
import settingFilePath

class SettingWindow(QtGui.QDialog):
    items={
        'Maya Executable':'',
        'Render':'',
        'Mayapy Interpreter':'',
        'imgcvt':'',
        'IMConvert':''
    }

    def __init__(self,*args,**kwargs):
        super(SettingWindow,self).__init__(*args,**kwargs)
        self.setAutoFillBackground(True)
        self.resize(700,400)
        self.setWindowFlags( QtCore.Qt.WindowStaysOnTopHint);
        styleFile=os.path.join(os.path.split(__file__)[0],"darkorange.stylesheet")
        with open(styleFile,"r") as fh:
            self.setStyleSheet(fh.read())      
        self.setWindowIcon(QtGui.QIcon(':images/Snowball-icon.png'))
        self.setWindowTitle('Settings of Snowball Batch Renderer required to Initialize')
        self.setMinimumSize(400,200)
        self.setMaximumSize(700,200)

        self.settingFile   = settingFilePath.settingFile()
              
        self.defaultBatDir = ""
        self.mayaPrjPath   = ""
        self.nukePrjPath   = ""
        self.nukeAppl      = ""
        
        self.setFileDS={1:self.items,2:self.defaultBatDir,3:self.mayaPrjPath,4:self.nukePrjPath,5:self.nukeAppl}

        self.userDir = os.path.expanduser('~')
        winSvn= os.path.join(self.userDir,"Documents")
        if os.path.isdir(winSvn):
            snoBallSetting=os.path.join(winSvn,"Snowball","setting")
            if not os.path.isdir(snoBallSetting):
                os.makedirs(snoBallSetting)
            self.settingFile = os.path.join(snoBallSetting,"setting.txt")
        #####Create the UI#
        self.createUI()
        self.showReadSetting()
        self.connectSignals()


    def prepSetFile(self):
        """This method updates data structure for saving"""
        
        self.defaultBatDir = str(self.batDirEdt.text())
        self.mayaPrjPath   = str(self.prjDirEdt.text())
        self.nukePrjPath   = str(self.nkprjEdt.text())
        self.nukeAppl      = str(self.nkEdt.text())
        
        self.setFileDS[1]  = self.updateAppPaths()
        self.setFileDS[2]  = self.defaultBatDir
        self.setFileDS[3]  = self.mayaPrjPath
        self.setFileDS[4]  = self.nukePrjPath
        self.setFileDS[5]  = self.nukeAppl
        return self.setFileDS

    def savSettingFile(self):
        
        """Saves application paths and default folder paths to setting file on disk"""
        
        dataTodump=self.prepSetFile()
        if all(dataTodump.values()):
            try:
                #settingFile=os.path.join(self.settingsDir,"setting.txt")
                #print "saved setting file to %s " % self.settingFile
                pickle.dump(dataTodump,open(self.settingFile, 'wb'), 0)
                return True
            except Exception as er:
                print er
                return False
        else: QtGui.QMessageBox.warning(self, "Please fill all the columns","It looks like you are missing something.")

    def readSettingFile(self):
        
        """ Read the setting file that contains the Maya Application paths"""
        
        try:
            read=open(self.settingFile,"r")
            data = pickle.load(read)
            return data
        except Exception as error:
            QtGui.QMessageBox.warning(self, "Error",error)
            
    def showReadSetting(self):
        if os.path.isfile(self.settingFile):
            self.items = self.readSettingFile()[1]
            setting=self.readSettingFile()
            self.nkEdt.setText(setting[5])
            self.batDirEdt.setText(setting[2])
            self.prjDirEdt.setText(setting[3])
            self.nkprjEdt.setText(setting[4])
            self.batsDir=setting[2]
            self.nukeApp=str(self.nkEdt.text())# path of Nuke to run in commandline
            self.appExeCB.setCurrentIndex(self.items.keys().index('Maya Executable'))
            if str(self.appExeCB.currentText())=='Maya Executable':
                self.appExeEdt.setText(self.items['Maya Executable'])
    
    def appExeCBSelChange(self):
        """Sets the path of selected items to self.appExeEdt(QLineEdit)"""
        self.appExeEdt.setText(self.items[str(self.appExeCB.currentText())])

    def createUI(self):
        """Content of the settings window"""
        p3_HBox=QtGui.QHBoxLayout()
        self.appExeCB  = QtGui.QComboBox()
        self.appExeCB.addItems(self.items.keys())

        self.appExeEdt = QtGui.QLineEdit()
        
        self.brwBtn=QtGui.QPushButton("Browse")
        [p3_HBox.addWidget(each) for each in [self.appExeCB,self.appExeEdt,self.brwBtn]]

        p3_HBox2=QtGui.QHBoxLayout()
        self.nklbl   = QtGui.QLabel("Nuke Application")
        self.nkEdt   = QtGui.QLineEdit()
        self.nkbrwBtn= QtGui.QPushButton("Browse")

        p3_HBox4 = QtGui.QHBoxLayout()

        batDirlbl= QtGui.QLabel("Batch Files")
        self.batDirEdt = QtGui.QLineEdit()
        batDirlbl.setFixedWidth(100)
        batDirlbl.setAlignment(QtCore.Qt.AlignCenter)
        self.batbrwsBtn=QtGui.QPushButton("Browse")

        [p3_HBox4.addWidget(each) for each in [batDirlbl,self.batDirEdt,self.batbrwsBtn]]

        p3_HBox5        = QtGui.QHBoxLayout()
        self.mprjDirlbl = QtGui.QLabel("Maya Projects")
        self.prjDirEdt  = QtGui.QLineEdit()
        self.prjDirBtn  = QtGui.QPushButton("Browse")

        [p3_HBox5.addWidget(each) for each in [self.mprjDirlbl,self.prjDirEdt,self.prjDirBtn]]

        p3_HBox6      = QtGui.QHBoxLayout()
        nkprjlbl      = QtGui.QLabel("Nuke Projects")
        self.nkprjEdt = QtGui.QLineEdit()
        self.nkprjBtn = QtGui.QPushButton("Browse")

        [p3_HBox6.addWidget(each) for each in [nkprjlbl,self.nkprjEdt,self.nkprjBtn]]

        p3_HBox3 = QtGui.QHBoxLayout()
        self.savSetBtn = QtGui.QPushButton("Save Settings")
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        p3_HBox3.addStretch(1)
        p3_HBox3.addWidget(self.buttonBox)

        [p3_HBox2.addWidget(each) for each in [self.nklbl,self.nkEdt,self.nkbrwBtn]]

        self.appExeCB.setFixedWidth(100)
        self.nklbl.setFixedWidth(100)
        self.nklbl.setAlignment(QtCore.Qt.AlignCenter)
        self.p3_vertical = QtGui.QVBoxLayout()

        [self.p3_vertical.addLayout(each) for each in [p3_HBox,p3_HBox2,p3_HBox4,p3_HBox5,p3_HBox6]]

        self.p3_vertical.addStretch(1)
        self.p3_vertical.addLayout(p3_HBox3)
        self.setLayout(self.p3_vertical)

    def connectSignals(self):
        self.appExeEdt.textChanged.connect(self.updateAppPaths)
        self.appExeCB.currentIndexChanged.connect(self.appExeCBSelChange)
        self.appFiles = partial(self.showFileDialog,self.brwBtn,"Maya Executable( *.exe )")
        self.brwBtn.clicked.connect(self.appFiles)
        self.setNukeApp = (partial(self.showFileDialog,self.nkbrwBtn,"Nuke Application( *.exe )"))
        self.nkbrwBtn.clicked.connect(self.setNukeApp)
        batBtnConnect = partial(self.showFileDialog,self.batbrwsBtn)
        self.batbrwsBtn.clicked.connect(batBtnConnect)
        prjBtnConnect = partial(self.showFileDialog,self.prjDirBtn)
        self.prjDirBtn.clicked.connect(prjBtnConnect)
        nkprjBtnConnect = partial(self.showFileDialog,self.nkprjBtn)
        self.nkprjBtn.clicked.connect(nkprjBtnConnect)
        #Save maya application paths (self.items) to a file on disk and exit.     
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

    def accept(self):
        if self.savSettingFile():
            super(SettingWindow,self).accept()


    def showFileDialog(self,btnPressed,fileFilters=""):
        self._fileFilters=fileFilters
        self.directory = os.path.join(os.path.splitdrive(self.userDir)[0],os.path.sep,"Program Files")
        self.btnPressed=btnPressed
            # this block is for file mode
        if self.btnPressed in [self.brwBtn,self.nkbrwBtn]:
            fname=str(QtGui.QFileDialog.getOpenFileName(self,'Open File',self.directory,self.tr(self._fileFilters)))

            if self.btnPressed == self.nkbrwBtn: self.nkEdt.setText(fname)
            elif self.btnPressed == self.brwBtn: self.appExeEdt.setText(fname)


        else: # this block is for directory mode
            self.directory = self.userDir
            selectedDir=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Directory",self.directory))
            if self.btnPressed   == self.batbrwsBtn:
                self.batDirEdt.setText(os.path.normpath(selectedDir))
            elif self.btnPressed == self.prjDirBtn:
                self.prjDirEdt.setText(os.path.normpath(selectedDir))
            elif self.btnPressed == self.nkprjBtn:
                self.nkprjEdt.setText(os.path.normpath(selectedDir))
            else: pass

            if not selectedDir:
                self.statusbar.showMessage("No directory selected",2500)
                return # exit if cancel

    def updateAppPaths(self):
        appSel = str(self.appExeEdt.text())
        if os.path.isfile(appSel):
            if os.path.split(appSel)[-1] == "maya.exe":
                self.items['Maya Executable']=appSel
            else:
                appSel=os.path.join(os.path.split(appSel)[0],"maya.exe")
                if os.path.isfile(appSel):
                    self.items['Maya Executable'] = appSel
            mayapy=os.path.join(os.path.split(appSel)[0],"mayapy.exe")
            if os.path.isfile(mayapy):
                self.items['Mayapy Interpreter'] = mayapy
            imgcvt=os.path.join(os.path.split(appSel)[0],"imgcvt.exe")
            if os.path.isfile(imgcvt):
                self.items['imgcvt']=imgcvt
            IMConvert=os.path.join(os.path.split(appSel)[0],"imconvert.exe")
            if os.path.isfile(IMConvert):
                self.items['IMConvert'] = IMConvert
            Render=os.path.join(os.path.split(appSel)[0],"render.exe")
            if os.path.isfile(Render):
                self.items['Render'] = Render
            return self.items


if __name__ =='__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    win = SettingWindow()
    win.show()
    sys.exit(app.exec_())