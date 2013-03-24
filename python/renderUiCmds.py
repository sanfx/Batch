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

def savNkScript(self):
	"""Saves updated Nuke script to disk"""
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

class Priority(QtGui.QtMainWindow):

	def __init__(self,direction):
		self.__direction = direction
		crntRow = newrow = self.listWidget.currentRow()
		total   = self.listWidget.count()

	def getPriorty(self):
		
		pass

	def setPriority(self):

		pass