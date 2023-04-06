# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# 新建模型不显示mel
def modeldonotshow(*args):
    pm.mel.eval(
        '''select -ne :initialShadingGroup;
        lockNode -l 0 -lu 0;
        select -ne :initialParticleSE;
        lockNode -l 0 -lu 0;'''
    )
    logDate = datetimeinfo.dateTimeInfo()
    fieldText = logDate + u'新建模型不显示错误尝试修复完成！！\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)