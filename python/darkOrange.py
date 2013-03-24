from PyQt4 import QtCore,QtGui
from images import styleResource
import os
class DarkOrange(QtGui.QFrame):
      def __init__(self,*args, **kwargs):
            super(DarkOrange,self).__init__(*args,**kwargs)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint |  QtCore.Qt.WindowStaysOnTopHint);
            self.setAutoFillBackground(True)            

            styleFile=os.path.join(os.path.split(__file__)[0],"darkorange.stylesheet")
            with open(styleFile,"r") as fh:
                  self.setStyleSheet(fh.read())
      def alwaysOnTop(self):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint) 
            self.show()
      def mousePressEvent(self, event):
            self.offset = event.pos()

      def mouseMoveEvent(self, event):
            try:
                  x=event.globalX()
                  y=event.globalY()
                  x_w = self.offset.x()
                  y_w = self.offset.y()
                  self.move(x-x_w, y-y_w)
            except: pass       