# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# Non-various vertices check  检查是否有非多样性顶点
def checkNonVariousVertices(*args):
    logDate = datetimeinfo.dateTimeInfo()
    allMesh = cmds.ls(type='mesh')
    allTransform = list(set(cmds.listRelatives(allMesh, p=True,f=True, type='transform')))
    variousVtx = []
    for i in allTransform:
        getVarious = cmds.polyInfo(i, nonManifoldVertices=True)
        # print getLamina
        if getVarious != None and len(getVarious) != 0:
            variousVtx.extend(getVarious)

    if len(variousVtx) != 0:
        def nonVariousVerticesset(*args):
            cmds.select(set(variousVtx), ne=True)

        # ui edit info-------------------------------------------------------------
        wrongPrint = '\n'.join(variousVtx)
        fieldText = logDate + u'******* Error *******\n【模型包含非多样性顶点】，请修复！\n'
        cmds.button('nonVariousVerticesCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('nonVariousVerticessetbtn', e=True, en=True, c=nonVariousVerticesset)
        cmds.button('nonVariousVerticesClearbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        print()
        'non-various vertices ok\n'
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'【非多样性顶点】Check OK！\n'
        cmds.button('nonVariousVerticesCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('nonVariousVerticessetbtn', e=True, en=False)
        cmds.button('nonVariousVerticesClearbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
