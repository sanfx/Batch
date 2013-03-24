import os

def settingFile():
    userDir = os.path.expanduser('~')
    winSvn= os.path.join(userDir,"Documents")
    if os.path.isdir(winSvn):
        snoBallSetting=os.path.join(winSvn,"Snowball","setting")
        if not os.path.isdir(snoBallSetting):
            os.makedirs(snoBallSetting)
        settingFile = os.path.join(snoBallSetting,"setting.txt")
        return settingFile
    else:
        winxp=os.path.join(userDir,"My Documents")
        snoBallSetting=os.path.join(winxp,"Snowball","setting")
        if os.path.isdir(snoBallSetting):
            os.makedirs(snoBallSetting)
        settingFile = os.path.join(snoBallSetting,"setting.txt")
        return settingFile