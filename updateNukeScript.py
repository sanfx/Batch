if __name__ == "__main__":
   import sys, os
   args = sys.argv
   print args
   target_file = args[1]  #this would be the first argument you passed in
   selWrtNde  = args[2]  # write node name
   renDirPath = args[3]  # path you want to render to
   imgSeqfmt  = args[4]  # format of image sequence
   startFrame = float(args[5])  # start frame
   endFrame   = float(args[6])  # last frame
   selChannel = args[7]  # channels to be rendered RGBA or Z
   import nuke
   
   # Open nuke script
   nuke.scriptOpen(target_file)
   
   # update the selected write node
   wrtNode = nuke.toNode(selWrtNde)
   wrtNode['file'].setValue(renDirPath)
   wrtNode['file_type'].setValue(imgSeqfmt)
   wrtNode['last'].setValue(endFrame)
   wrtNode['first'].setValue(startFrame)
   wrtNode['channels'].setValue(selChannel) 
   
   # save the updated nuke script
   
   nuke.scriptSave(target_file)