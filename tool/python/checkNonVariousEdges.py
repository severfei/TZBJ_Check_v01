# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# Non-various edge check  检查是否有非多样性线
def checkNonVariousEdges(*args):
    logDate = datetimeinfo.dateTimeInfo()
    allMesh = cmds.ls(type='mesh')
    allTransform = list(set(cmds.listRelatives(allMesh, p=True,f=True, type='transform')))
    variousEdg = []
    for i in allTransform:
        getVarious = cmds.polyInfo(i, nonManifoldVertices=True)
        # print getLamina
        if getVarious != None and len(getVarious) != 0:
            variousEdg.extend(getVarious)

    if len(variousEdg) != 0:
        def nonVariousEdgesset(*args):
            cmds.select(set(variousEdg), ne=True)

        # ui edit info-------------------------------------------------------------
        wrongPrint = '\n'.join(variousEdg)
        fieldText = logDate + u'******* Error *******\n【模型存在非多样性线】，请修复！\n'
        cmds.button('nonVariousEdgesCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('nonVariousEdgessetbtn', e=True, en=True, c=nonVariousEdgesset)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        print()
        'non-various edges ok\n'
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'【非多样性线】Check OK！\n'
        cmds.button('nonVariousEdgesCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
