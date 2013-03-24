from PyQt4 import QtCore,QtGui
from functools import partial
import sys,os,subprocess
import Render
import pickle,json
import ast,datetime

class Window(QtGui.QWidget):

    renderer={
            'Mental Ray':'mr',
            'Maya Software':'sw',
            'Maya Vecter':'vr',
            'Maya Hardware 2.0':'mayaHardware2',
            'Maya Hardware':'mayaHardware',
            'Maxwell':'maxwell'
                }
    absPath = os.path.abspath(__file__)

    browsBtnSig=QtCore.pyqtSignal(int)

    def __init__(self,*args,**kwargs):
          super(Window,self).__init__(*args,**kwargs)

          self.setWindowTitle("Snowball Batch Renderer")
          self.resize(700,400)
          self.setMinimumSize(400,300)
          self.setMaximumSize(700,400)
          self.setWindowIcon(QtGui.QIcon('images/Snowball-icon.png'))
          self.defaultBatDir=""
          self.mayaPrjPath=""
          self.nukePrjPath=""
          self.nukeAppl=""
          self.userDir = os.path.expanduser('~')
          windows7= os.path.join(self.userDir,"Documents")
          if os.path.isdir(windows7):
             snoBallSetting=os.path.join(windows7,"Snowball","setting")
             if not os.path.isdir(snoBallSetting):
                os.makedirs(snoBallSetting)
             self.settingFile = os.path.join(snoBallSetting,"setting.txt")
          else:
               winxp=os.path.join(userDir,"My Documents")
               snoBallSetting=os.path.join(winxp,"Snowball","setting")
               if os.path.isdir(snoBallSetting):
                  os.makedirs(snoBallSetting)
               self.settingFile = os.path.join(snoBallSetting,"setting.txt")

          # set the default file filter
          self.openfileFilters="All Supported(*.ma *.mb *.nk );; Maya Ascii(*.ma);; Maya Binary( *.mb );; Nuke Script( *.nk )"



          self.createUI()

          if os.path.isfile(self.settingFile):
             setting=self.readSettingFile()
             self.nkEdt.setText(setting[5])
             self.batDirEdt.setText(setting[2])
             self.prjDirEdt.setText(setting[3])
             self.nkprjEdt.setText(setting[4])
             self.batsDir=setting[2]
             self.nukeApp=str(self.nkEdt.text())# path of Nuke to run in commandline
          else:
            if os.path.isfile(self.settingFile):
                self.items = self.readSettingFile()[1]
            else:
               self.items={
                'Maya Executable':'',
                'Render':'',
                'Mayapy Interpreter':'',
                'imgcvt':'',
                'IMConvert':''}
               try:
                    self.setFileDS={1:self.items,2:self.defaultBatDir,3:self.mayaPrjPath,4:self.nukePrjPath,5:self.nukeApp}
                    self.batsDir=os.path.expanduser('~')
               except Exception as error:
                print error



    def readSettingFile(self):
        """ Read the setting file that contains the Maya Application paths"""
        try:
            read=open(self.settingFile,"r")
            data = pickle.load(read)
            return data
        except Exception as error:
            return {1:{'Maya Executable':''}}


    def initializeSetting(self):

        self.getSelectedRendertype()

        if os.path.isfile(self.settingFile):
           if str(self.appExeCB.currentText())=='Maya Executable':
              self.appExeEdt.setText(self.items['Maya Executable'])

    def appExeCBSelChange(self):
        """
        Sets the path of selected items to self.appExeEdt(QLineEdit)
        """
        self.appExeEdt.setText(self.items[str(self.appExeCB.currentText())])

    def getSelectedRendertype(self):
        if self.mayachkBox.checkState() == QtCore.Qt.Checked:
           self.directory=str(self.prjDirEdt.text())
           self.label.setText("Maya Scene File")
           self.rndCB.setEnabled(True)
           self.camlbl.setText("Camera to Render")
        elif self.nukechkBox.checkState() == QtCore.Qt.Checked:
             self.directory=str(self.nkprjEdt.text())
             self.label.setText("Nuke Script File")
             self.rndCB.setEnabled(False)
             self.camlbl.setText("Write node")

    def prepSetFile(self):
        """This method updates data structure for saving"""
        self.defaultBatDir=str(self.batDirEdt.text())
        self.mayaPrjPath=str(self.prjDirEdt.text())
        self.nukePrjPath=str(self.nkprjEdt.text())
        self.nukeAppl=str(self.nkEdt.text())

        self.setFileDS[2]=self.defaultBatDir
        self.setFileDS[3]=self.mayaPrjPath
        self.setFileDS[4]=self.nukePrjPath
        self.setFileDS[5]=self.nukeAppl
        return self.setFileDS

    def createUI(self):
          quitAction=QtGui.QAction('&Exit',self)
          quitAction.triggered.connect(self.close)
          newAction = QtGui.QAction('&New',self)
          newAction.triggered.connect(self.newReset)
          fileMenu=QtGui.QMenuBar()

          phile=fileMenu.addMenu('&File')
          help=fileMenu.addMenu('&Help')
          phile.addAction(newAction)
          phile.addAction(quitAction)

          #add my checkboxes to select render type task
          self.mayachkBox=QtGui.QCheckBox()
          self.mayachkBox.setCheckState(QtCore.Qt.Checked)
          self.mayachkBox.stateChanged.connect(self.getSelectedRendertype)
          mayaIcon=QtGui.QPixmap("images/Maya_Icon.png")
          self.mayachkBox.setIcon(QtGui.QIcon(mayaIcon))
          self.mayachkBox.setIconSize(QtCore.QSize(25,25))
          self.nukechkBox=QtGui.QCheckBox()
          nukeIcon= QtGui.QPixmap("images/nuke_icon.png")
          self.nukechkBox.setIcon(QtGui.QIcon(nukeIcon))
          self.nukechkBox.stateChanged.connect(self.getSelectedRendertype)
          self.nukechkBox.setIconSize(QtCore.QSize(25,25))
          chkboxLayout=QtGui.QHBoxLayout()
          chkboxLayout.addStretch(1)
          chkboxLayout.addWidget(self.mayachkBox)
          chkboxLayout.addWidget(self.nukechkBox)
          chkboxLayout.addStretch(1)
          #make button exclusive
          self.chkBoxGrp=QtGui.QButtonGroup()
          self.chkBoxGrp.setExclusive(True)
          # add checkBoxes to exclusive groups
          self.chkBoxGrp.addButton(self.mayachkBox)
          self.chkBoxGrp.addButton(self.nukechkBox)

          # initialize tab widget
          tab_widget = QtGui.QTabWidget()
          # Everything will go inside the QWidgets below
          tab1 = QtGui.QWidget()
          tab2 = QtGui.QWidget()
          tab3 = QtGui.QWidget()

          p1_vertical = QtGui.QVBoxLayout(tab1)
          self.p2_vertical = QtGui.QVBoxLayout(tab2)
          self.p3_vertical = QtGui.QVBoxLayout(tab3)

          tab_widget.addTab(tab1, "Render Setup")
          tab_widget.addTab(tab2, "Task Queue")
          tab_widget.addTab(tab3, "Settings")

          gridLayout  = QtGui.QGridLayout()
          self.label=QtGui.QLabel("Maya Scene File")
          gridLayout.addWidget(self.label,0,0)
          self.scnFilePath=QtGui.QLineEdit()
          self.scnFilePath.setToolTip("Enter scene file name")
          gridLayout.addWidget(self.scnFilePath,0,1)
          self.browseBtn=QtGui.QPushButton("Browse")
          self.browseBtn.setObjectName('browsbtn')
          gridLayout.addWidget(self.browseBtn,0,2)
          dirlabel=QtGui.QLabel("Render Directory")
          gridLayout.addWidget(dirlabel,1,0)
          self.renDir=QtGui.QLineEdit()
          self.renDir.setToolTip("Specify the directory you want render to go")
          gridLayout.addWidget(self.renDir,1,1)
          self.rdBtn=QtGui.QPushButton("Browse")
          gridLayout.addWidget(self.rdBtn,1,2)
          gHBox=QtGui.QHBoxLayout()

          gridLayout2=QtGui.QGridLayout()

          sfLbl=QtGui.QLabel("Start Frame")
          sfLbl.setAlignment(QtCore.Qt.AlignCenter)
          sfLbl.setFixedWidth(80)
          gridLayout2.addWidget(sfLbl,0,0)
          self.sfEdt=QtGui.QLineEdit()
          self.sfEdt.setFixedWidth(50)
          gridLayout2.addWidget(self.sfEdt,0,1)
          eflbl=QtGui.QLabel("End Frame")
          eflbl.setAlignment(QtCore.Qt.AlignCenter)
          gridLayout2.addWidget(eflbl,1,0)
          self.efEdt=QtGui.QLineEdit()
          self.efEdt.setFixedWidth(50)
          gridLayout2.addWidget(self.efEdt,1,1)
          byfrlbl=QtGui.QLabel("By Frame")
          byfrlbl.setAlignment(QtCore.Qt.AlignCenter)
          gridLayout2.addWidget(byfrlbl,2,0)
          self.byfrEdt=QtGui.QLineEdit()
          self.byfrEdt.setFixedWidth(50)
          gridLayout2.addWidget(self.byfrEdt,2,1)

          rgtsideVBox = QtGui.QVBoxLayout()
          addCmdlbl=QtGui.QLabel("Additional Commands(Optional)")
          addCmdlbl.setFixedWidth(160)
          self.addCmdEdt=QtGui.QLineEdit()
          self.addCmdEdt.setFixedWidth(180)

          newHbox=QtGui.QHBoxLayout()
          newHbox.addStretch(1)
          newHbox.addWidget(addCmdlbl)

          newHBox2=QtGui.QHBoxLayout()
          newHBox2.addStretch(1)
          newHBox2.addWidget(self.addCmdEdt)
          gridLayout2.addLayout(newHbox,0,2)
          gridLayout2.addLayout(newHBox2,1,2)

          hbox=QtGui.QHBoxLayout()
          self.rgbchkBox=QtGui.QCheckBox("RGB")
          self.rgbchkBox.setCheckState(QtCore.Qt.Checked)
          self.alpchkBox=QtGui.QCheckBox("Alpha")
          self.depchkBox=QtGui.QCheckBox("Z-Depth")
          hbox.addStretch(1)
          hbox.addWidget(self.rgbchkBox)
          hbox.addWidget(self.alpchkBox)
          hbox.addWidget(self.depchkBox)

          gridLayout2.addLayout(hbox,2,2)

          gHBox.addLayout(gridLayout2)
          gHBox.addLayout(rgtsideVBox)
          HBox=QtGui.QHBoxLayout()

          gridLayout3=QtGui.QGridLayout()
          rndlbl=QtGui.QLabel("Renderer")
          HBox.addWidget(rndlbl)

          self.rndCB=QtGui.QComboBox()
          self.rndCB.addItems(self.renderer.keys())
          self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Software'))
          HBox.addWidget(self.rndCB)
          HBox.addStretch(1)
          self.camlbl=QtGui.QLabel("Camera to Render")
          HBox.addWidget(self.camlbl)

          self.camCB=QtGui.QComboBox()
          HBox.addWidget(self.camCB)
          HBox.addStretch(1)

          fmtlbl=QtGui.QLabel("Format")
          HBox.addWidget(fmtlbl)

          self.fmtCB=QtGui.QComboBox()
          self.fmtCB.addItems(self.readImageFormats().values())
          HBox.addWidget(self.fmtCB)


          #Create a validator for each frame number text box
          self.sfEdt.setValidator(QtGui.QIntValidator())
          self.efEdt.setValidator(QtGui.QIntValidator())
          self.byfrEdt.setValidator(QtGui.QIntValidator())


          hLine=QtGui.QFrame(self)
          hLine.setFrameShape(QtGui.QFrame.HLine)
          hLine.setFrameShadow(QtGui.QFrame.Raised)
          nxtbtnbox=QtGui.QHBoxLayout()
          ## Render Buttons
          self.bgnBatRndBtn=QtGui.QPushButton("Render Current")
          self.addTaskBtn=QtGui.QPushButton("Add to Render Queue")
          #self.connect(self.addTaskBtn,QtCore.SIGNAL("clicked()"),self.accessAction.makebatFileTasks)
          self.addTaskBtn.clicked.connect(self.addToRenderQueue)
          nxtbtnbox.addWidget(self.bgnBatRndBtn)
          nxtbtnbox.addWidget(self.addTaskBtn)

          #add status bar
          self.statusbar=QtGui.QStatusBar()
          self.statusbar.showMessage("Ready")

          # assign signals to slots
          scnFile=partial(self.showFileDialog,self.browseBtn,self.openfileFilters)
          self.browseBtn.clicked.connect(scnFile)
          rndPath=partial(self.showFileDialog,self.rdBtn)
          self.rdBtn.clicked.connect(rndPath)
          self.scnFilePath.textChanged.connect(self.execApp)
          self.camCB.currentIndexChanged.connect(self.selWriteNode)
          #self.camCB.activated.connect(self.setSelWriteNode)
          self.bgnBatRndBtn.clicked.connect(self.writeBatFile)

          # add layouts that contain inside of tab1 widgets
          p1_vertical.addLayout(gridLayout)
          p1_vertical.addLayout(gHBox)
          p1_vertical.addLayout(HBox)

          p1_vertical.addWidget(hLine)
          p1_vertical.addLayout(nxtbtnbox)
          self.secondTabContent()
          self.settingTabContent()
          vbox = QtGui.QVBoxLayout()
          vbox.setMargin(0)
          vbox.addWidget(fileMenu)

          vbox.addLayout(chkboxLayout)
          vbox.addWidget(tab_widget)
          vbox.addWidget(self.statusbar)
          self.setLayout(vbox)

    def changePriority(self,direction):
        """ Reorder the items in the listWidget """
        crntRow = newrow = self.listWidget.currentRow()
        total=self.listWidget.count()
        self.statusbar.setMessage("Total no. of items %s, and selected item number is %s"%(total,crntRow),2500)
        if direction =='up':
           if crntRow > 0 : newrow -=1
           else: print "This is the first item cannot move up further."
        elif direction=='down':
           if crntRow + 1  < total: newrow +=1
           else:  print "This is the last item cannot move down further."
        if crntRow != newrow:
           crntItem=self.listWidget.takeItem(crntRow)
           self.listWidget.insertItem(newrow,crntItem)
           self.listWidget.setCurrentItem(crntItem)


    def makeBatFile(self):
        text=""
        for each in xrange(self.listWidget.count()):
            text += "echo [Task Id:%s]\n" % each
            text += self.listWidget.item(each).text() +"\n"
            print text
        self.writeBatFile("batch",text)

    def removeItem(self):
        """ Delete item from listWidget """
        item=self.listWidget.takeItem(self.listWidget.currentRow())
        item = None

    def addToRenderQueue(self):
        ext=os.path.splitext(str(self.scnFilePath.text()))[-1]
        if self.mayachkBox.isChecked() and (ext=='.ma'):
           img_mIcon=QtGui.QPixmap("images\icon_maya-small.png")
           ntask=self.makeBatTask()
           self.itemTask=QtGui.QListWidgetItem(ntask)
           self.itemTask.setIcon(QtGui.QIcon(img_mIcon))
           self.listWidget.insertItem(0,self.itemTask)
        else: print "Please select the Nuke Script, currenly selected\
 file is: %s"% os.path.split(str(self.scnFilePath.text()))[-1]

    def writeBatFile(self,do="single",task=None):
        self.task=task
        now = datetime.datetime.now()

        buildCrntTime=str(now.hour) +"_" + str(now.minute)
        selected=str(self.scnFilePath.text())
        quikBatNam=os.path.basename(selected).split(".")[0]+"_"+buildCrntTime+".bat"
        if do !="batch":
            self.batfiletoSave=os.path.join(os.path.split(selected)[0],quikBatNam)
            self.task = str(self.makeBatTask())
        else:
            self.batfiletoSave=os.path.join(self.batsDir,buildCrntTime+".bat")
        try:
            writeBat=open(self.batfiletoSave,'w')
            writeBat.write(self.task)
            self.execRender()
        except Exception as er: print er
        finally: writeBat.close()

    def execApp(self):
        ## call to readMayaFile.py using mayapy.exe interpreter
        fileToOpen=str(self.scnFilePath.text())
        readFile = os.path.join(os.path.split(self.absPath)[0],"readFile.py")
        fileName=readFile+" "+fileToOpen
        if fileToOpen:
           if os.path.splitext(fileToOpen)[-1] in ['.ma','.mb']:
              if os.getcwd() != os.path.split(self.absPath)[0]:# run mayapy from specified location
                 os.chdir(os.path.split(self.absPath)[0]) # takes away dependency of setting environment variables
              mayapy=os.path.split(self.readSettingFile()[1]['Mayapy Interpreter'])[-1]
              launch=mayapy+" "+ fileName
              process = subprocess.Popen(launch, shell=True, stdout=subprocess.PIPE)
              process.wait()
              if process.returncode==0: # 0 = success, optional check
                 print "Success Reading: %s" % os.path.basename(fileToOpen)
                 # read the result to a string
                 pipeData= json.loads(process.stdout.read())
                 self.objRead = pipeData
                 self.fillInputs()
              else: print "Unable to read maya scene file: %s" % os.path.basename(fileToOpen)
           elif os.path.splitext(fileToOpen)[-1] == ".nk":
                #print fileName,"Nuke Path",(os.path.split(self.nukeApp)[0])
                os.chdir(os.path.split(self.nukeApp)[0])# takes away dependency of having nuke full licence
                nukeApp = os.path.split(self.nukeApp)[-1]
                launch = nukeApp + " -t " +fileName
                process=subprocess.Popen(launch,shell=True,stdout=subprocess.PIPE)
                process.wait()
                if process.returncode == 0:
                   print "Success Reading : %s" % os.path.basename(fileToOpen)
                   #Read the result to a string
                   #nukeDataRead=(process.stdout.read()).split(".nk")[-1]
                   nukeData = ast.literal_eval(process.stdout.read().split("\n")[-1])
                   print nukeData
                   if not nukeData:
                      self.statusbar.showMessage("No write node found in %s"\
                       % os.path.basename(str(self.scnFilePath.text())),2500)
                   else:
                        self.nukeData = nukeData
                        self.fillNukeData()

    def fillNukeData(self):
        self.camCB.clear()
        self.camCB.addItems(self.nukeData.keys())

    def selWriteNode(self):
        if self.nukechkBox.isChecked():
           self.selectedItem=self.nukeData.keys()[self.camCB.currentIndex()]
           self.nukeSet()

    def nukeSet(self):
        self.sfEdt.setText(str(self.nukeData[str(self.selectedItem)][0]))
        self.efEdt.setText(str(self.nukeData[str(self.selectedItem)][1]))
        self.byfrEdt.setText("1")
        # select renderer in case of maya
        # set what to render rgb only or with alpha
        if self.nukeData[str(self.selectedItem)][4]=='rgb':
           self.rgbchkBox.setCheckState(QtCore.Qt.Checked)
           self.alpchkBox.setCheckState(QtCore.Qt.Unchecked)
        elif self.nukeData[str(self.selectedItem)][4]=='rgba':
             self.rgbchkBox.setCheckState(QtCore.Qt.Checked)
             self.alpchkBox.setCheckState(QtCore.Qt.Checked)
        selImgForm=str(self.nukeData[str(self.selectedItem)][3])
        if selImgForm =="jpeg":
           selImgForm="jpg"
        if selImgForm.upper() in self.readImageFormats().values():
           self.fmtCB.setItemText(0,selImgForm.upper())
        self.renDir.setText(str(os.path.normpath(self.nukeData[str(self.selectedItem)][2])))


    def execRender(self):

        rend= self.batfiletoSave
        process = subprocess.Popen(rend, shell=True)
        #stdout,stderr = process.communicate()
        #print process.returncode

    def fillInputs(self):

        self.camCB.clear()
        self.camCB.addItems(self.objRead['camsLst'])
        self.sfEdt.setText(str(self.objRead['startFrame']))
        self.efEdt.setText(str(self.objRead['endFrame']))
        self.byfrEdt.setText(str(self.objRead['stepByFrame']))
        ## Select the default renderer
        if str(self.objRead['defaultRenderer'])=='mayaSoftware':
           self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Software'))

        elif str(self.objRead['defaultRenderer'])=='mayaHardware':
             self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Hardware'))

        elif str(self.objRead['defaultRenderer'])=='mentalRay':
             self.rndCB.setCurrentIndex(self.renderer.keys().index('Mental Ray'))

        elif str(self.objRead['defaultRenderer'])=='mayaVector':
             self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Vecter'))

        elif str(self.objRead['defaultRenderer'])=='mayaHardware2':
             self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Hardware 2.0'))

        else: self.rndCB.setCurrentIndex(self.renderer.keys().index(str(self.objRead['defaultRenderer'])))
        ## select image format set in render globals
        if str(self.objRead['imageFormat']) in self.readImageFormats().keys():
           self.fmtCB.setCurrentIndex(self.readImageFormats().values().index(self.readImageFormats()[self.objRead['imageFormat']]))

    def makeBatTask(self):
        selRend = self.renderer[str(self.rndCB.currentText())]
        rendDir = str(self.renDir.text())
        startFrame=self.sfEdt.text()
        endFrame=self.efEdt.text()
        byFrame=self.byfrEdt.text()
        selCam = self.camCB.currentText()
        addiFlag= self.addCmdEdt.text()
        scnFile=self.scnFilePath.text()
        if str(scnFile).endswith(".ma"):
           if str(self.fmtCB.currentText()).lower()in ["maya iff",'maya16 iff','tif16']:
              imgFormat= 'iff'
           elif str(self.fmtCB.currentText()).lower()=='sgi16':
                 imgFormat = 'sgi'
           else: imgFormat = str(self.fmtCB.currentText()).lower()

           if self.rgbchkBox.checkState() == QtCore.Qt.Checked:
               rgb= " -rgb True "
           else: rgb =" -rgb False "
           if self.alpchkBox.checkState() == QtCore.Qt.Checked:
               alpha =" -alpha True "
           else: alpha = " -alpha False "
           if self.depchkBox.checkState() == QtCore.Qt.Checked:
               depth = " -depth True "
           else: depth = " -depth False "
           ## building the render string for bat file
           return "render -r " + selRend +" -rd " + rendDir +" -s " + startFrame + " -e " +endFrame +"\
 -b "+ byFrame +" -cam " + selCam +" "+ addiFlag + " -of " +imgFormat + rgb + alpha + depth +"\
 "+scnFile
        elif str(self.scnFilePath.text()).endswith("nk"):
             return os.path.split(self.nukeApp)[-1] + " -x '"+str(self.scnFilePath.text()) +"' " +startFrame +" "+ endFrame


    def showFileDialog(self,btnPressed,fileFilters=""):


        self._fileFilters=fileFilters
        self.btnPressed=btnPressed

         # this block is for file mode
        if self.btnPressed not in  [self.rdBtn,self.prjDirBtn,self.batbrwsBtn,self.nkprjBtn]:
           fname=str(QtGui.QFileDialog.getOpenFileName(self,'Open File',self.directory,self.tr(self._fileFilters)))

           if self.btnPressed == self.nkbrwBtn: self.nkEdt.setText(fname)
           elif self.btnPressed == self.brwBtn: self.appExeEdt.setText(fname)
           elif self.btnPressed == self.browseBtn: self.scnFilePath.setText(fname)

        else: # this block is for directory mode
             if self.nukechkBox.isChecked() and (self.btnPressed==self.rdBtn):
                setfile=QtGui.QFileDialog(self)
                setfile.setFileMode(QtGui.QFileDialog.AnyFile)
                setfile.setNameFilter('Image Format selected (*.*)')
                if not setfile.exec_():
                   # exit if cancel
                   return
                self.renDir.setText(str(setfile.selectedFiles().takeFirst()))
             else:
                  selectedDir=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Render Directory",directory))
                  if self.btnPressed==self.batbrwsBtn:
                     self.batDirEdt.setText(os.path.normpath(selectedDir))
                  elif self.btnPressed == self.prjDirBtn:
                       self.prjDirEdt.setText(os.path.normpath(selectedDir))
                  elif self.btnPressed == self.nkprjBtn:
                       self.nkprjEdt.setText(os.path.normpath(selectedDir))
                  else: self.renDir.setText(os.path.normpath(selectedDir))
                  if not selectedDir:
                     self.statusbar.showMessage("No directory selected",2500)
                     return # exit if cancel

    def newReset(self):
        """
        Reset to setup for new scene file batch render.
        """
        self.scnFilePath.setText("")
        self.renDir.setText("")
        self.sfEdt.setText("")
        self.efEdt.setText("")
        self.byfrEdt.setText("")
        self.camCB.clear()
        self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Software'))
        self.addCmdEdt.setText("")


    def updateAppPaths(self):
        appSel = str(self.appExeEdt.text())
        if os.path.isfile(appSel):
           if os.path.split(appSel)[-1]=="maya.exe":
              self.items['Maya Executable']=appSel
           else:
                appSel=os.path.join(os.path.split(appSel)[0],"maya.exe")
                if os.path.isfile(appSel):
                   self.items['Maya Executable']=appSel
           mayapy=os.path.join(os.path.split(appSel)[0],"mayapy.exe")
           if os.path.isfile(mayapy):
             self.items['Mayapy Interpreter']=mayapy
           imgcvt=os.path.join(os.path.split(appSel)[0],"imgcvt.exe")
           if os.path.isfile(imgcvt):
             self.items['imgcvt']=imgcvt
           IMConvert=os.path.join(os.path.split(appSel)[0],"imconvert.exe")
           if os.path.isfile(IMConvert):
             self.items['IMConvert']=IMConvert
           Render=os.path.join(os.path.split(appSel)[0],"render.exe")
           if os.path.isfile(Render):
             self.items['Render']=Render

    def savSettingFile(self):
        """Saves Maya Application paths to setting file on disk"""
        dataTodump=self.prepSetFile()
        try:
            settingFile=os.path.join(self.settingsDir,"setting.txt")
            pickle.dump(dataTodump,open(settingFile, 'wb'), 0)
        except Exception as er: print er
        #finally: output_phil.close()

    def secondTabContent(self):
        vBox=QtGui.QVBoxLayout()

        prihbox=QtGui.QHBoxLayout()
        prihbox.addStretch(1)
        # create priority buttons
        movUpBtn=QtGui.QPushButton()
        delBtn=QtGui.QPushButton()
        movDnBtn=QtGui.QPushButton()
        # set icons for buttoons
        upIcon=QtGui.QPixmap("images\icon_moveup.gif")
        downIcon=QtGui.QPixmap("images\icon_movedown.gif")
        delIcon=QtGui.QPixmap("images\delete-icon-large.gif")
        movUpBtn.setIcon(QtGui.QIcon(upIcon))
        delBtn.setIcon(QtGui.QIcon(delIcon))
        movDnBtn.setIcon(QtGui.QIcon(downIcon))
        # add priority buttons
        prihbox.addWidget(movUpBtn)
        prihbox.addWidget(delBtn)
        prihbox.addWidget(movDnBtn)

        self.listWidget=QtGui.QListWidget()
        self.batRndBtn=QtGui.QPushButton("Begin Render")
        HBox=QtGui.QHBoxLayout()
        HBox.addStretch(0)
        HBox.addWidget(self.batRndBtn)
        vBox.addLayout(prihbox)
        vBox.addWidget(self.listWidget)
        vBox.addLayout(HBox)
        self.p2_vertical.addLayout(vBox)

        #assign slots
        upSlot=partial(self.changePriority,"up")
        movUpBtn.clicked.connect(upSlot)
        downSlot=partial(self.changePriority,"down")
        movDnBtn.clicked.connect(downSlot)
        delBtn.clicked.connect(self.removeItem)
        self.batRndBtn.clicked.connect(self.makeBatFile)

    def readImageFormats(self):
        melFile="scripts/others/createImageFormats.mel"
        phile = os.path.join(os.path.split(os.path.split(self.readSettingFile()[1]['Maya Executable'])[0])[0],melFile)
        imageFormatIndex={}
        try:
              read_phile=open(phile,"r")
              text =str(read_phile.read())
              lst = text.split("$i =")
              for each in lst:
                if each.split()[0].split(";")[0].isdigit() :
                 if (each.split()[-1].split(";")[0].replace('"',"")).isalnum():
                    imageFormatIndex[each.split()[0].split(";")[0]]=each.split()[-1].split(";")[0].replace('"',"").upper()

                    imageFormatIndex.update({'12':'YUV'})
                    imageFormatIndex.update({'13':'SGI16'})
                    imageFormatIndex.update({'4':'TIF16'})
                    imageFormatIndex.update({'10':'MAYA16 IFF'})
                    imageFormatIndex.update({'7':'MAYA IFF'})
                    return imageFormatIndex
        except Exception as e:
            return {'1':'Not Found'}
        #finally: read_phile.close()

    def settingTabContent(self):
        """
        Content of the settings tab and signal to slot conntections
        """

        p3_HBox=QtGui.QHBoxLayout()
        self.appExeCB=QtGui.QComboBox()
        try:
            self.appExeCB.addItems(self.items.keys())

            self.appExeCB.setCurrentIndex(self.items.keys().index('Maya Executable'))
        except: pass
        self.appExeEdt=QtGui.QLineEdit()
        self.brwBtn=QtGui.QPushButton("Browse")
        [p3_HBox.addWidget(each) for each in [self.appExeCB,self.appExeEdt,self.brwBtn]]

        p3_HBox2=QtGui.QHBoxLayout()
        self.nklbl=QtGui.QLabel("Nuke Application")
        self.nkEdt=QtGui.QLineEdit()
        self.nkbrwBtn=QtGui.QPushButton("Browse")

        p3_HBox4=QtGui.QHBoxLayout()
        #p3_HBox4.addStretch(0)
        batDirlbl=QtGui.QLabel("Batch Files")
        self.batDirEdt=QtGui.QLineEdit()
        batDirlbl.setFixedWidth(100)
        batDirlbl.setAlignment(QtCore.Qt.AlignCenter)
        self.batbrwsBtn=QtGui.QPushButton("Browse")

        [p3_HBox4.addWidget(each) for each in [batDirlbl,self.batDirEdt,self.batbrwsBtn]]

        p3_HBox5      =QtGui.QHBoxLayout()
        self.mprjDirlbl =QtGui.QLabel("Maya Projects")
        self.prjDirEdt=QtGui.QLineEdit()
        self.prjDirBtn=QtGui.QPushButton("Browse")

        [p3_HBox5.addWidget(each) for each in [self.mprjDirlbl,self.prjDirEdt,self.prjDirBtn]]
        p3_HBox6 = QtGui.QHBoxLayout()
        nkprjlbl=QtGui.QLabel("Nuke Projects")
        self.nkprjEdt=QtGui.QLineEdit()
        self.nkprjBtn=QtGui.QPushButton("Browse")

        [p3_HBox6.addWidget(each) for each in [nkprjlbl,self.nkprjEdt,self.nkprjBtn]]

        p3_HBox3=QtGui.QHBoxLayout()
        self.savSetBtn=QtGui.QPushButton("Save Settings")

        p3_HBox3.addStretch(1)
        p3_HBox3.addWidget(self.savSetBtn)

        #Connect buttons to slots
        self.appFiles=partial(self.showFileDialog,self.brwBtn,"Maya Executable( *.exe )")
        self.brwBtn.clicked.connect(self.appFiles)
        self.appExeEdt.textChanged.connect(self.updateAppPaths)
        self.appExeCB.currentIndexChanged.connect(self.appExeCBSelChange)
        self.setNukeApp=(partial(self.showFileDialog,self.nkbrwBtn,"Nuke Application( *.exe )"))
        self.nkbrwBtn.clicked.connect(self.setNukeApp)
        batBtnConnect=partial(self.showFileDialog,self.batbrwsBtn)
        self.batbrwsBtn.clicked.connect(batBtnConnect)
        prjBtnConnect=partial(self.showFileDialog,self.prjDirBtn)
        self.prjDirBtn.clicked.connect(prjBtnConnect)
        nkprjBtnConnect=partial(self.showFileDialog,self.nkprjBtn)
        self.nkprjBtn.clicked.connect(nkprjBtnConnect)
        #Save maya application paths (self.items) to a file on disk
        self.savSetBtn.clicked.connect(self.savSettingFile)

        [p3_HBox2.addWidget(each) for each in [self.nklbl,self.nkEdt,self.nkbrwBtn]]
        self.appExeCB.setFixedWidth(100)
        self.nklbl.setFixedWidth(100)
        self.nklbl.setAlignment(QtCore.Qt.AlignCenter)

        [self.p3_vertical.addLayout(each) for each in [p3_HBox,p3_HBox2,p3_HBox4,p3_HBox5,p3_HBox6]]

        self.p3_vertical.addStretch(1)
        self.p3_vertical.addLayout(p3_HBox3)
        self.initializeSetting()


if __name__ =='__main__':
   app = QtGui.QApplication(sys.argv)
   app.setStyle("cleanlooks")
   win = Window()
   win.show()
   sys.exit(app.exec_())