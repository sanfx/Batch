if __name__ == "__main__":
   import sys, os
   args = sys.argv

   writeNode=args[1]
   nukeScript=args[2]
   startFrame=args[3]
   endFrame=args[4]
   incr= args[5]
   import nuke
   nuke.scriptOpen(nukeScript)

   nuke.execute(writeNode,int(startFrame),int(endFrame),int(incr))