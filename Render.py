from PyQt4 import QtCore,QtGui
from darkOrange import DarkOrange
from images import resource_ui
from functools import partial
import sys,os,subprocess
import pickle,json
import ast,datetime
import settingFilePath


class Window(DarkOrange):

    renderer={
        'Mental Ray':'mr',
        'Maya Software':'sw',
        'Maya Vecter':'vr',
        'Maya Hardware 2.0':'mayaHardware2',
        'Maya Hardware':'mayaHardware',
        'Maxwell':'maxwell'
    }
    absPath = os.path.abspath(__file__)

    def __init__(self,*args,**kwargs):
        super(Window,self).__init__(*args,**kwargs)
        self.setWindowTitle("Snowball Batch Renderer")

        self.resize(700,400)
        self.setMinimumSize(400,300)
        self.setMaximumSize(700,400)
        self.setWindowIcon(QtGui.QIcon(':images/Snowball-icon.png'))
        self.defaultBatDir=""
        self.mayaPrjPath=""
        self.nukePrjPath=""
        self.nukeAppl=""
        # variable initialiezed to handle data to passed over to update nuke script
        self.updSf = ""      # isSettingChanged()
        self.updEf = ""      # updateNukeScript()
        self.updFmt = ""
        self.updChnl = ""
        
        self.css=("""
                    QPushButton {
                                font-size: 12px;
                                color: #272B39;
                                font-family: Segoe UI,MS Sans Serif;
                                border: 1px solid #000;
                                border-radius: 1px;
                                padding: 0px;
                                min-width: 20px;
                                background: qradialgradient(cx: 0.3, cy: -0.4,
                                fx: 0.3, fy: -0.4,
                                radius: 1.00, stop: 0 #888, stop: 1 #888);
                                }
                """)
        self.userDir = os.path.expanduser('~')
        self.settingFile = settingFilePath.settingFile()

        # set the default file filter
        #self.openfileFilters="All Image Formats(*.jpg *.png *.tiff *.gif *.tga *.cgi *.dpx);;"  
        self.openfileFilters="All Supported(*.ma *.mb *.nk);; Maya Ascii(*.ma);; Maya Binary( *.mb );; Nuke Script( *.nk ) ;; All Image Formats( *.jpg *.png *.tiff *.gif *.tga *.cgi *.dpx)"   

        self.items = self.readSettingFile()[1]

        self.createUI()

        self.setting=self.readSettingFile()
        
        self.nukePathApp = self.setting[5]
        self.batsDir=os.path.expanduser('~')
        self.getSelectedRendertype()


    def readSettingFile(self):
        """ Read the setting file that contains the Maya Application paths"""
        try:
            read=open(self.settingFile,"r")
            data = pickle.load(read)
            return data
        except Exception as error:
            QtGui.QMessageBox.warning(self, "Error",error)

    def getSelectedRendertype(self):
        if self.mayachkBox.checkState() == QtCore.Qt.Checked:
         
            self.directory=self.readSettingFile()[3]
            self.label.setText("Maya Scene File")
            self.rndCB.setEnabled(True)
            self.camCB.setEnabled(True)
            self.camlbl.setText("Camera to Render")
            self.savNkScrptAction.setEnabled(False)
        elif self.nukechkBox.checkState() == QtCore.Qt.Checked:
        
            self.directory=str(self.setting[4])
            self.label.setText("Nuke Script File")
            self.rndCB.setEnabled(False)
            self.camCB.setEnabled(True)
            self.camlbl.setText("Write node")
            self.savNkScrptAction.setEnabled(True)
        elif self.convtChkbox.checkState() == QtCore.Qt.Checked:
            self.directory = self.readSettingFile()[3]
            self.openfileFilters="All Image Formats(*.jpg *.png *.tiff *.gif *.tga *.cgi *.dpx);;"   
            self.label.setText("Image Sequence")
            self.rndCB.setEnabled(False)
            self.camCB.setEnabled(False)
    
    def convtImgSeq(self):
        if os.path.splitext(fileToOpen)[-1] in [".jpg", ".gif",".png"]:
            print "Image Selected"   
            
            #imgcvt -n 1 50 1 shot@@.jpg shot.@@@@.jpg            
        #print 
        pass
    
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
        ntitleBar=QtGui.QHBoxLayout()
        ntitleIcon=QtGui.QPixmap(":images/Snowball-icon.png")
        lbl = QtGui.QLabel(self)
        lbl.setPixmap(ntitleIcon)

        miniBtn=QtGui.QPushButton("-")
        miniBtn.setStyleSheet(self.css)
        closeBtn=QtGui.QPushButton("x")
        closeBtn.setStyleSheet(self.css)

        quitAction=QtGui.QAction('&Exit',self)
        quitAction.triggered.connect(self.close)
        newAction = QtGui.QAction('&New',self)
        newAction.triggered.connect(self.newReset)
        self.savNkScrptAction = QtGui.QAction('Save &Nuke Script',self)
        self.savNkScrptAction.triggered.connect(self.savNkScript)
        self.alwaysOnTopAction = QtGui.QAction('Always on &Top',self)
        self.alwaysOnTopAction.setCheckable(True)
        self.alwaysOnTopAction.setChecked(True)
        self.alwaysOnTopAction.triggered.connect(self.alwaysOnTop)
        settingAction=QtGui.QAction('Settings',self)
        settingAction.triggered.connect(self.settingWindow)
        fileMenu=QtGui.QMenuBar()
        miniBtn.clicked.connect(self.showMinimized)
        closeBtn.clicked.connect(self.close)
        phile=fileMenu.addMenu('&File')
        tools = fileMenu.addMenu('&Tools')
        help=fileMenu.addMenu('&Help')
        phile.addAction(newAction)
        phile.addAction(self.savNkScrptAction)
        phile.addAction(self.alwaysOnTopAction)
        phile.addAction(settingAction)
        phile.addAction(quitAction)

        prevMenu = tools.addMenu('Preview')
        prevNkAction = prevMenu.addAction('Using &Nuke')
        prevNkAction.triggered.connect(self.prevInNuke)
        prevFchk = prevMenu.addAction('Using &Fcheck')
        prevFchk.triggered.connect(self.prevInFcheck)


        ntitleBar.addWidget(lbl)
        ntitleBar.addWidget(fileMenu)
        ntitleBar.addStretch(1)
        ntitleBar.addWidget(miniBtn)
        ntitleBar.addWidget(closeBtn)
        
       
        #add my checkboxes to select render type task
        self.mayachkBox = QtGui.QCheckBox()
        #self.mayachkBox.setCheckState(QtCore.Qt.Checked)
        self.mayachkBox.stateChanged.connect(self.getSelectedRendertype)
        mayaIcon = QtGui.QPixmap(":images/maya_icon.jpg")
        self.mayachkBox.setIcon(QtGui.QIcon(mayaIcon))
        self.mayachkBox.setIconSize(QtCore.QSize(25,25))
        ### Nuke render selection
        self.nukechkBox = QtGui.QCheckBox()
        nukeIcon = QtGui.QPixmap(":images/nuke_icon.png")
        self.nukechkBox.setIcon(QtGui.QIcon(nukeIcon))
        self.nukechkBox.stateChanged.connect(self.getSelectedRendertype)
        self.nukechkBox.setIconSize(QtCore.QSize(25,25))
        chkboxLayout = QtGui.QHBoxLayout()
        # Image format converter 
        fmtconvtIcon = QtGui.QPixmap(":images/convert.png")
        self.convtChkbox = QtGui.QCheckBox()
        self.convtChkbox.setIcon(QtGui.QIcon(fmtconvtIcon))
        self.convtChkbox.setIconSize(QtCore.QSize(28,28))
        self.convtChkbox.setCheckState(QtCore.Qt.Checked)
        

        chkboxLayout.addStretch(1)
        chkboxLayout.addWidget(self.convtChkbox)
        chkboxLayout.addWidget(self.mayachkBox)
        chkboxLayout.addWidget(self.nukechkBox)  
        chkboxLayout.addStretch(1)
        # make button exclusive
        self.chkBoxGrp = QtGui.QButtonGroup()
        self.chkBoxGrp.setExclusive(True)
        # add checkBoxes to exclusive groups
        self.chkBoxGrp.addButton(self.convtChkbox)
        self.chkBoxGrp.addButton(self.mayachkBox)
        self.chkBoxGrp.addButton(self.nukechkBox)
        

        # initialize tab widget
        tab_widget = QtGui.QTabWidget()
        # Everything will go inside the QWidgets below
        tab1 = QtGui.QWidget()
        tab2 = QtGui.QWidget()

        p1_vertical      = QtGui.QVBoxLayout(tab1)
        self.p2_vertical = QtGui.QVBoxLayout(tab2)

        tab_widget.addTab(tab1, "Render Setup")
        tab_widget.addTab(tab2, "Task Queue")

        gridLayout  = QtGui.QGridLayout()
        self.label = QtGui.QLabel("Maya Scene File")
        gridLayout.addWidget(self.label,0,0)
        self.scnFilePath = QtGui.QLineEdit()
        self.scnFilePath.setToolTip("Enter scene file name")
        gridLayout.addWidget(self.scnFilePath,0,1)
        self.browseBtn = QtGui.QPushButton("Browse")
        self.browseBtn.setObjectName('browsbtn')
        gridLayout.addWidget(self.browseBtn,0,2)
        dirlabel = QtGui.QLabel("Render Directory")
        gridLayout.addWidget(dirlabel,1,0)
        self.renDir = QtGui.QLineEdit()
        self.renDir.setToolTip("Specify the directory you want render to go")
        gridLayout.addWidget(self.renDir,1,1)
        self.rdBtn = QtGui.QPushButton("Browse")
        gridLayout.addWidget(self.rdBtn,1,2)
        gHBox=QtGui.QHBoxLayout()

        gridLayout2=QtGui.QGridLayout()

        sfLbl=QtGui.QLabel("Start Frame")
        sfLbl.setAlignment(QtCore.Qt.AlignCenter)
        sfLbl.setFixedWidth(80)
        gridLayout2.addWidget(sfLbl,0,0)
        self.sfEdt = QtGui.QLineEdit()
        self.sfEdt.setFixedWidth(50)
        gridLayout2.addWidget(self.sfEdt,0,1)
        eflbl=QtGui.QLabel("End Frame")
        eflbl.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout2.addWidget(eflbl,1,0)
        self.efEdt = QtGui.QLineEdit()
        self.efEdt.setFixedWidth(50)
        gridLayout2.addWidget(self.efEdt,1,1)
        byfrlbl = QtGui.QLabel("By Frame")
        byfrlbl.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout2.addWidget(byfrlbl,2,0)
        self.byfrEdt = QtGui.QLineEdit()
        self.byfrEdt.setFixedWidth(50)
        gridLayout2.addWidget(self.byfrEdt,2,1)

        rgtsideVBox = QtGui.QVBoxLayout()
        addCmdlbl = QtGui.QLabel("Additional Commands(Optional)")
        addCmdlbl.setFixedWidth(160)
        self.addCmdEdt = QtGui.QLineEdit()
        self.addCmdEdt.setFixedWidth(180)

        newHbox = QtGui.QHBoxLayout()
        newHbox.addStretch(1)
        newHbox.addWidget(addCmdlbl)

        newHBox2 = QtGui.QHBoxLayout()
        newHBox2.addStretch(1)
        newHBox2.addWidget(self.addCmdEdt)
        gridLayout2.addLayout(newHbox,0,2)
        gridLayout2.addLayout(newHBox2,1,2)

        hbox=QtGui.QHBoxLayout()
        self.rgbchkBox = QtGui.QCheckBox("RGB")
        self.rgbchkBox.setCheckState(QtCore.Qt.Checked)
        self.alpchkBox = QtGui.QCheckBox("Alpha")
        self.depchkBox = QtGui.QCheckBox("Z-Depth")
        hbox.addStretch(1)
        hbox.addWidget(self.rgbchkBox)
        hbox.addWidget(self.alpchkBox)
        hbox.addWidget(self.depchkBox)

        gridLayout2.addLayout(hbox,2,2)

        gHBox.addLayout(gridLayout2)
        gHBox.addLayout(rgtsideVBox)
        HBox = QtGui.QHBoxLayout()

        gridLayout3 = QtGui.QGridLayout()
        rndlbl = QtGui.QLabel("Renderer")
        HBox.addWidget(rndlbl)

        self.rndCB=QtGui.QComboBox()
        self.rndCB.addItems(self.renderer.keys())
        self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Software'))
        HBox.addWidget(self.rndCB)
        HBox.addStretch(1)
        self.camlbl = QtGui.QLabel("Camera to Render")
        HBox.addWidget(self.camlbl)

        self.camCB = QtGui.QComboBox()
        self.camlbl.setFixedWidth(90)
        HBox.addWidget(self.camCB)
        HBox.addStretch(1)

        fmtlbl = QtGui.QLabel("Format")
        HBox.addWidget(fmtlbl)

        self.fmtCB = QtGui.QComboBox()
        self.fmtCB.addItems(self.readImageFormats().values())
        HBox.addWidget(self.fmtCB)

        #Create a validator for each frame number text box
        self.sfEdt.setValidator(QtGui.QIntValidator())
        self.efEdt.setValidator(QtGui.QIntValidator())
        self.byfrEdt.setValidator(QtGui.QIntValidator())

        hLine = QtGui.QFrame(self)
        hLine.setFrameShape(QtGui.QFrame.HLine)
        hLine.setFrameShadow(QtGui.QFrame.Raised)
        nxtbtnbox = QtGui.QHBoxLayout()
        ## Render Buttons
        self.bgnBatRndBtn = QtGui.QPushButton("Render Current")
        self.addTaskBtn   = QtGui.QPushButton("Add to Render Queue")
        #self.connect(self.addTaskBtn,QtCore.SIGNAL("clicked()"),self.accessAction.makebatFileTasks)
        self.addTaskBtn.clicked.connect(self.addToRenderQueue)
        nxtbtnbox.addWidget(self.bgnBatRndBtn)
        nxtbtnbox.addWidget(self.addTaskBtn)

        #add status bar
        self.statusbar = QtGui.QStatusBar()
        self.statusbar.showMessage("Ready")

        # assign signals to slots
        scnFile = partial(self.showFileDialog,self.browseBtn,self.openfileFilters)
        self.browseBtn.clicked.connect(scnFile)
        rndPath = partial(self.showFileDialog,self.rdBtn)
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
       
        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(0)
        vbox.addLayout(ntitleBar)

        vbox.addLayout(chkboxLayout)
        vbox.addWidget(tab_widget)
        vbox.addWidget(self.statusbar)
        self.setLayout(vbox)
        
   
    def savNkScript(self):
        if str(self.scnFilePath.text()).endswith(".nk"):
            if self.isSettingChanged():
                self.updSavNukeScrpt()
            else: self.statusbar.showMessage("Nothing to save.",2000)
   
    def changePriority(self,direction):
        """ Reorder the items in the listWidget """
        crntRow = newrow = self.listWidget.currentRow()
        total   = self.listWidget.count()
        self.statusbar.showMessage("Total no. of items %s, and selected item number is %s"%(total,crntRow),2500)
        if direction == 'up':
            if crntRow > 0 : newrow -= 1
            else: self.statusbar.showMessage("This is the first item cannot move up further.",1500)
        elif direction == 'down':
            if crntRow + 1  < total: newrow += 1
            else: self.statusbar.showMessage("This is the last item cannot move down further.",1500)
        if crntRow != newrow:
            crntItem=self.listWidget.takeItem(crntRow)
            self.listWidget.insertItem(newrow,crntItem)
            self.listWidget.setCurrentItem(crntItem)
            
    def prevInNuke(self):
        os.chdir(os.path.split(self.nukePathApp)[0])# takes away dependency of having nuke full licence
        nukeApp = os.path.split(self.nukePathApp)[-1]        
        if self.renDir.text():
            stFrm = str(self.sfEdt.text())
            enFrm = str(self.efEdt.text())
            fileName = str(self.renDir.text()) +" " +stFrm +" " +enFrm
            launch  = nukeApp + " -v " +fileName
            self.execProces(launch)
        
    def prevInFcheck(self):
        os.chdir(os.path.split(self.items['imgcvt'])[0])
        if self.renDir.text():
            stFrm = str(self.sfEdt.text())
            enFrm = str(self.efEdt.text())        
            fileName = "fcheck -n "+ stFrm + " " + enFrm + " " + str(self.byfrEdt.text()) + " " + str(self.renDir.text())
            fileName = str(fileName).replace("#","@").replace("\'",os.path.sep)
            self.execProces(fileName)
                  
    def execProces(self,launch):
        return subprocess.Popen(launch,shell=True,stdout=subprocess.PIPE)  
    
    def makeBatFile(self):
        text=""
        for each in xrange(self.listWidget.count()):
            text += "echo [Task Id:%s]\n" % each
            text += self.listWidget.item(each).text() +"\n"
        self.writeBatFile("batch",text)

    def removeItem(self):
        """ Delete item from listWidget """
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None

    def addToRenderQueue(self):
        if str(self.renDir.text()):
            ext=os.path.splitext(str(self.scnFilePath.text()))[-1]
            if self.mayachkBox.isChecked() and (ext=='.ma'):
                img_mIcon = QtGui.QPixmap(":images/icon_maya-small.png")
                ntask = self.makeBatTask()
                self.itemTask = QtGui.QListWidgetItem(ntask)
                self.itemTask.setIcon(QtGui.QIcon(img_mIcon))
                self.listWidget.insertItem(0,self.itemTask)
            elif self.nukechkBox.isChecked() and (ext == '.nk'):
                img_nIcon = QtGui.QPixmap(":images/nuke.png")
                ntask = self.makeBatTask()
                self.itemTask = QtGui.QListWidgetItem(ntask)
                self.itemTask.setIcon(QtGui.QIcon(img_nIcon))
                self.listWidget.insertItem(0,self.itemTask)
        else: self.statusbar.showMessage("Please enter some directory you want to render to.",1500)

                # print "Please select the Nuke Script, currenly selected\
    #file is: %s"% os.path.split(str(self.scnFilePath.text()))[-1]
    
    def isSettingChanged(self):
        lst = self.nukeData[str(self.selectedItem)]
        ext = os.path.splitext(str(self.scnFilePath.text()))[-1]
        if self.nukechkBox.isChecked() and (ext == '.nk'):
            updSf = int(self.sfEdt.text())
            if updSf != int(lst[0]):
                self.updSf = updSf
            else: self.updSf = int(lst[0])
                
            updEf = int(self.efEdt.text())
            if updEf != int(lst[1]):
                self.updEf = updEf
            else: self.updEf = int(lst[1])
            updBf = int(self.byfrEdt.text())
    
            #if updBf != int(lst[2]):
                #self.updBf = updBf
            updRnDir = str(self.renDir.text())
            if  updRnDir != str(lst[2]):
                self.updRnDir = updRnDir
            else: self.updRnDir = lst[2]
                #print "Render Direcotory is %s" % updRnDir
            updFmt = str(self.fmtCB.currentText()).lower()
            if updFmt != str(lst[3]):
                self.updFmt =updFmt
            else: self.updFmt = lst[3]
            
                #print "Format changed to %s." %self.updFmt
            #updChnl = str(lst[4])
            if self.rgbchkBox.checkState() == QtCore.Qt.Checked:
                self.updChnl = "rgb"
            elif self.alpchkBox.checkState() == QtCore.Qt.Checked:
                self.updChnl = "a"
            elif (self.rgbchkBox.checkState() == QtCore.Qt.Checked) and (self.alpchkBox.checkState() == QtCore.Qt.Checked):
                self.updChnl = "rgba"
            else: self.updChnl = "rgba"
            return [self.updSf,self.updEf,self.updFmt]
          
    def writeBatFile(self,do = "single",task = None):
        if str(self.scnFilePath.text()).endswith(".nk"):
            os.chdir(os.path.split(self.nukePathApp)[0])# takes away dependency of having nuke full licence
        self.task=task
        now = datetime.datetime.now()
        ext = os.path.splitext(str(self.scnFilePath.text()))[-1]
        #print "Anything updated: ",any(self.isSettingChanged())
        if self.nukechkBox.isChecked() and (ext == '.nk'):
            self.isSettingChanged()
            self.updSavNukeScrpt()## save the Nuke script with new values
        if self.convtChkbox.isChecked() and (ext in [".jpg", ".gif",".png"]):
            print "Beginning Image Sequence Conversion."
            imgcvt = self.readSettingFile()[1]['imgcvt']
            
            os.chdir(os.path.split(imgcvt)[0])
        buildCrntTime = str(now.hour) +"_" + str(now.minute)
        selected   = str(self.scnFilePath.text())
        quikBatNam = os.path.basename(selected).split(".")[0]+"_"+buildCrntTime+".bat"
        if do != "batch":
            self.batfiletoSave = os.path.join(os.path.split(selected)[0],quikBatNam)
            self.task = str(self.makeBatTask())
        else: self.batfiletoSave = os.path.join(self.batsDir,buildCrntTime+".bat")
        if self.task != None:
            try:
                writeBat=open(self.batfiletoSave,'w')
                writeBat.write(self.task)
                self.execRender()
            except Exception as er: print er
            finally: writeBat.close()

        #self.statusbar.showMessage("preparing to render with modified settings.",3000)
    
    def updSavNukeScrpt(self):
        filetoUpdate = str(self.scnFilePath.text())
        updateNukeScript = os.path.join(os.path.split(self.absPath)[0],"updateNukeScript.py")
        fileName = updateNukeScript+ " " + filetoUpdate 
        if filetoUpdate:
            os.chdir(os.path.split(self.nukePathApp)[0])# takes away dependency of having nuke full licence
            nukeApp = os.path.split(self.nukePathApp)[-1]
            launch  = nukeApp + " -t " + fileName + " " + self.selectedItem + " "  + self.updRnDir + " " + self.updFmt + " " + str(self.updSf) + " " + str(self.updEf) + " " + self.updChnl
            process=subprocess.Popen(launch,shell=True,stdout=subprocess.PIPE)
            if process.returncode == 0:
                self.statusbar.showMessage("Success updating : %s" % os.path.basename(filetoUpdate),2000)            

    def execApp(self):
        ## call to readMayaFile.py using mayapy.exe interpreter
        fileToOpen = str(self.scnFilePath.text())
        readFile = os.path.join(os.path.split(self.absPath)[0],"readFile.py")
        fileName = readFile+" " + fileToOpen
        if fileToOpen:
            if os.path.splitext(fileToOpen)[-1] in ['.ma','.mb']:
                if os.getcwd() != os.path.split(self.absPath)[0]:# run mayapy from specified location
                    os.chdir(os.path.split(self.absPath)[0]) # takes away dependency of setting environment variables
                mayapy  = os.path.split(self.readSettingFile()[1]['Mayapy Interpreter'])[-1]
                launch  = mayapy+" "+ fileName
                process = subprocess.Popen(launch, shell=True, stdout=subprocess.PIPE)
                process.wait()
                if process.returncode == 0: # 0 = success, optional check
                    self.statusbar.showMessage("Success Reading: %s" % os.path.basename(fileToOpen),1600)
                    # read the result to a string
                    pipeData = json.loads(process.stdout.read())
                    self.objRead = pipeData
                    self.fillInputs()
                else: self.statusbar.showMessage("Unable to read maya scene file: %s" % os.path.basename(fileToOpen),1600)
            elif os.path.splitext(fileToOpen)[-1] == ".nk":               
                os.chdir(os.path.split(self.nukePathApp)[0])# takes away dependency of having nuke full licence
                nukeApp = os.path.split(self.nukePathApp)[-1]
                launch  = nukeApp + " -t " +fileName
                process=subprocess.Popen(launch,shell=True,stdout=subprocess.PIPE)
                process.wait()
                if process.returncode == 0:
                    self.statusbar.showMessage("Success Reading : %s" % os.path.basename(fileToOpen),1600)
                    #Read the result to a string
                    #nukeDataRead=(process.stdout.read()).split(".nk")[-1]
                    nukeData = ast.literal_eval(process.stdout.read().split("\n")[-1])
                    if not nukeData:
                        self.statusbar.showMessage("No write node found in %s"\
                                                   % os.path.basename(str(self.scnFilePath.text())),2500)
                    else:
                        self.nukeData = nukeData
                        self.fillNukeData()
            
            self.bgnBatRndBtn.setFocus(True)

    def fillNukeData(self):
        self.camCB.clear()
        self.camCB.addItems(self.nukeData.keys())

    def selWriteNode(self):
        if self.nukechkBox.isChecked():
            self.selectedItem=self.nukeData.keys()[self.camCB.currentIndex()]
            self.nukeSet()

    def nukeSet(self):
        self.sfEdt.setText(str(int(self.nukeData[str(self.selectedItem)][0])))
        self.efEdt.setText(str(int(self.nukeData[str(self.selectedItem)][1])))
        self.byfrEdt.setText("1")
        # select renderer in case of maya
        # set what to render rgb only or with alpha
        if self.nukeData[str(self.selectedItem)][4]   =='rgb':
            self.rgbchkBox.setCheckState(QtCore.Qt.Checked)
            self.alpchkBox.setCheckState(QtCore.Qt.Unchecked)
        elif self.nukeData[str(self.selectedItem)][4] =='rgba':
            self.rgbchkBox.setCheckState(QtCore.Qt.Checked)
            self.alpchkBox.setCheckState(QtCore.Qt.Checked)
        selImgForm=str(self.nukeData[str(self.selectedItem)][3])
        if selImgForm == "jpeg":
            selImgForm = "jpg"
        if selImgForm.upper() in self.readImageFormats().values():
            self.fmtCB.setItemText(0,selImgForm.upper())
        self.renDir.setText(self.pathStrCheck(str(self.nukeData[str(self.selectedItem)][2])))

    def pathStrCheck(self,pathString):
        """Check is path string contains padding"""
        if os.path.split(pathString)[-1].count("#") > 1:
            return pathString
        else:
            ext = os.path.splitext(pathString)[-1]
            locString = os.path.split(pathString)[0]
            return  os.path.join(locString,os.path.split(pathString)[-1].split(".")[0]+self.createPadding(str(self.sfEdt.text()),str(self.efEdt.text()))+ext)

    def createPadding(self, a, b):
        """returns frame padding based on highest number"""
        #endString = 
        #print (" A is %s and B is %s") %(len(str(a)) ,len(str(b)))
        if a > b:
            return  "_"+"#"*len(str(a)) #+ "."+self.nukeData[str(self.selectedItem)][3]
        else:
            return  "_" + "#"*len(str(b)) #+ "."+self.nukeData[str(self.selectedItem)][3]

    def execRender(self):
        rend= self.batfiletoSave
        process = subprocess.Popen(rend, shell=True)

    def fillInputs(self):
        self.camCB.clear()
        self.camCB.addItems(self.objRead['camsLst'])
        self.sfEdt.setText(str(self.objRead['startFrame']))
        self.efEdt.setText(str(self.objRead['endFrame']))
        self.byfrEdt.setText(str(self.objRead['stepByFrame']))
        ## Select the default renderer
        if str(self.objRead['defaultRenderer']) == 'mayaSoftware':
            self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Software'))

        elif str(self.objRead['defaultRenderer']) == 'mayaHardware':
            self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Hardware'))

        elif str(self.objRead['defaultRenderer']) == 'mentalRay':
            self.rndCB.setCurrentIndex(self.renderer.keys().index('Mental Ray'))

        elif str(self.objRead['defaultRenderer']) == 'mayaVector':
            self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Vecter'))

        elif str(self.objRead['defaultRenderer']) == 'mayaHardware2':
            self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Hardware 2.0'))

        else: self.rndCB.setCurrentIndex(self.renderer.keys().index(str(self.objRead['defaultRenderer'])))
        ## select image format set in render globals
        if str(self.objRead['imageFormat']) in self.readImageFormats().keys():
            self.fmtCB.setCurrentIndex(self.readImageFormats().values().index(self.readImageFormats()[self.objRead['imageFormat']]))

    def makeBatTask(self):
        selRend = self.renderer[str(self.rndCB.currentText())]
        rendDir = str(self.renDir.text())
        startFrame = self.sfEdt.text()
        endFrame=self.efEdt.text()
        byFrame  = self.byfrEdt.text()
        selCam   = self.camCB.currentText()
        addiFlag = self.addCmdEdt.text()
        scnFile=self.scnFilePath.text()
        if str(scnFile).endswith(".ma"):
            if str(self.fmtCB.currentText()).lower()in ["maya iff",'maya16 iff','tif16']:
                imgFormat= 'iff'
            elif str(self.fmtCB.currentText()).lower() == 'sgi16':
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
        elif str(self.scnFilePath.text()).endswith(".nk"):
            nukeRenderScript=os.path.join(os.path.split(self.absPath)[0],"nukeRender.py")
            return os.path.split(self.nukePathApp)[-1] + " -t "+nukeRenderScript+" "+selCam+" "+str(self.scnFilePath.text()) +" "+startFrame+" "+ endFrame+" "+ byFrame +" test"

    def showFileDialog(self,btnPressed,fileFilters=""):
        self._fileFilters=fileFilters
        self.btnPressed=btnPressed
            # this block is for file mode
        if self.btnPressed != self.rdBtn:

            fname=str(QtGui.QFileDialog.getOpenFileName(self,'Open File',self.directory,self.tr(self._fileFilters)))

            if self.btnPressed == self.browseBtn: self.scnFilePath.setText(fname)

        else: # this block is for directory mode
            if self.nukechkBox.isChecked() and (self.btnPressed==self.rdBtn):
                setfile=QtGui.QFileDialog(self)
                setfile.setFileMode(QtGui.QFileDialog.AnyFile)
                setfile.setNameFilter('Image Format selected (*.*)')
                if not setfile.exec_():
                    # exit if cancel
                    return
                self.renDir.setText(self.pathStrCheck(str(setfile.selectedFiles().takeFirst())))
            else:
                selectedDir=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Render Directory",self.directory))
                if self.btnPressed==self.rdBtn:
                    self.renDir.setText(os.path.normpath(selectedDir))
                if not selectedDir:
                    self.statusbar.showMessage("No directory selected",2500)
                    return # exit if cancel

    def newReset(self):
        """ Reset to setup for new scene file batch render."""
        self.scnFilePath.setText("")
        self.renDir.setText("")
        self.sfEdt.setText("")
        self.efEdt.setText("")
        self.byfrEdt.setText("")
        self.camCB.clear()
        self.rndCB.setCurrentIndex(self.renderer.keys().index('Maya Software'))
        self.addCmdEdt.setText("")
        self.browseBtn.setFocus(True)

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

    def secondTabContent(self):
        vBox=QtGui.QVBoxLayout()

        prihbox=QtGui.QHBoxLayout()
        prihbox.addStretch(1)
        # create priority buttons
        movUpBtn=QtGui.QPushButton()
        delBtn=QtGui.QPushButton()
        movDnBtn=QtGui.QPushButton()
        # set icons for buttoons
        upIcon=QtGui.QPixmap(":images\icon_moveup.gif")
        downIcon=QtGui.QPixmap(":images\icon_movedown.gif")
        delIcon=QtGui.QPixmap(":images\delete-icon-large.gif")
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
        
    def locateMelFile(self):
        """Locate the createImageFormat.mel file"""
        return QtGui.QFileDialog.getOpenFileName(self,'Open File',self.userDir,self.tr("Mel Script( *.mel )"))#,self.directory,self.tr("Mel Script( *.mel )"))
        
    def settingWindow(self):
        from settingWinUI import SettingWindow
        dialog = SettingWindow()
        dialog.exec_()
    
    def readImageFormats(self):
        melFile="scripts/others/createImageFormats.mel"
        phile = os.path.join(os.path.split(os.path.split(self.readSettingFile()[1]['Maya Executable'])[0])[0],melFile)
        
        if not os.path.isfile(phile):
            phile = self.locateMelFile()
        
        imageFormatIndex={}
        try:
            read_phile=open(phile,"r")
            text =str(read_phile.read())
        except Exception as e: print e
        finally: read_phile.close()

        lst = text.split("$i =")
        for each in lst:
            if each.split()[0].split(";")[0].isdigit() :
                if (each.split()[-1].split(";")[0].replace('"',"")).isalnum():
                    imageFormatIndex[each.split()[0].split(";")[0]] = each.split()[-1].split(";")[0].replace('"',"").upper()

        imageFormatIndex.update({'12':'YUV'})
        imageFormatIndex.update({'13':'SGI16'})
        imageFormatIndex.update({'4':'TIF16'})
        imageFormatIndex.update({'10':'MAYA16IFF'})
        imageFormatIndex.update({'7':'MAYAIFF'})
        return imageFormatIndex

def run():
    """Run the Snowball Batch Renderer"""    
    win = Window()
    win.show()
    win.raise_()
    sys.exit(app.exec_()) 
    
if __name__ =='__main__':    
    app = QtGui.QApplication(sys.argv)
    settingFile = settingFilePath.settingFile()
    if not os.path.isfile(settingFile):
        from settingWinUI import SettingWindow
        dialog = SettingWindow()
        if dialog.exec_() == dialog.Accepted: run()            
    else: run()