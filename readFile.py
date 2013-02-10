if __name__ == "__main__":
   import sys, os
   args = sys.argv

   this_script = args[0]  #this will be the name of this file
   target_file = args[1]  #this would be the first argument you passed in

   if os.path.splitext(target_file)[-1] in ['.ma','.mb']:
      # maya party
      import json
      import maya.standalone
      maya.standalone.initialize()
      import maya.cmds as cmds

      try:
         cmds.file(target_file, open = True, force = True)
         camsLst=cmds.ls(type='camera')
         startFrame=cmds.getAttr("defaultRenderGlobals.startFrame")
         endFrame=cmds.getAttr("defaultRenderGlobals.endFrame")
         stepByFrame=cmds.getAttr("defaultRenderGlobals.byFrameStep")
         defaultRenderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")
         imageFormat = cmds.getAttr("defaultRenderGlobals.imageFormat")
         readItemsObj={'camsLst':camsLst,
                       'startFrame':startFrame,
                       'endFrame':endFrame,
                       'stepByFrame':stepByFrame,
                       'defaultRenderer':defaultRenderer,
                       'imageFormat':str(imageFormat)
                       }
         data=json.dumps(readItemsObj)
         sys.stdout.write(data)
         quit()
      except RuntimeError:
         sys.stderr.write('could not find %s\n' % target_file)
         raise
   elif os.path.splitext(target_file)[-1]=='.nk':
      try: # Nuke party
         import nuke
         # Open nuke script
         nuke.scriptOpen(target_file)
         allWriteNodes=nuke.allNodes("Write")
         writeNodes=[]
         wnodeData={}
         attributes=[]
         for index,each in enumerate(allWriteNodes):
            writeNodes.insert(index,each.name())
         for wNode in writeNodes:
            for eachAttrib in ['first','last','file','file_type','channels','use_limit']:
               wnodeData.setdefault(wNode,[]).append(nuke.toNode(wNode)[eachAttrib].value())
         sys.stdout.write(str(wnodeData))
         quit()
      except RuntimeError:
         sys.stderr.write('could not find %s\n' % target_file)
         raise