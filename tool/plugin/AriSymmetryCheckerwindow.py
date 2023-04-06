# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# 启动模型对称检查插件
def AriSymmetryCheckerwindow(*args):
    # mel_script = os.path.join(os.path.dirname('__file__'), 'AriSymmetryChecker.mel')
    mel_script = os.path.join('D:/TZBJ_Check_v01/script/AriSymmetryChecker.mel')
    # print (mel_script)
    pm.mel.eval("source \"{}\";".format(mel_script))
    pm.mel.eval('AriSymmetryChecker')
    logDate = datetimeinfo.dateTimeInfo()
    fieldText = logDate + u'已打开AriSymmetryChecker对称检查插件！！\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)







