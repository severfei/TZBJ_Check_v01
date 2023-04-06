# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# Non-parallel plane check  检查非平面
def checkNonParallelPlane(*args):
    logDate = datetimeinfo.dateTimeInfo()
    nonParallel = []
    allMesh = cmds.ls(type='mesh')
    allTransform = list(set(cmds.listRelatives(allMesh, p=True,f=True, type='transform')))
    for i in allTransform:
        cmds.select(i, r=True)
        cmds.polySelectConstraint(mode=3, t=8, planarity=1, size=2, convexity=0)
        nonParallelPlane = cmds.ls(sl=True, flatten=True)
        nonParallel.extend(nonParallelPlane)
        cmds.select(clear=True)

    cmds.polySelectConstraint(mode=3, t=8, planarity=0, size=0, convexity=0)
    cmds.select(clear=True)

    if len(nonParallel) != 0:
        def nonParallelPlaneset(*args):
            cmds.select(set(nonParallel), ne=True)

        def nonParallelPlaneClear(*args):
            # cmds.polyNormalPerVertex(set(nonParallel),ufn=True)
            cmds.select(cl=1)
            cmds.button('nonParallelPlanesetbtn', e=True, en=False)
            cmds.button('nonParallelPlaneClearbtn', e=True, en=False)
            checkNonParallelPlane()
            fieldText = '已解除法线锁定'

        # ui edit info-------------------------------------------------------------
        wrongPrint = '\n'.join(nonParallel)
        fieldText = logDate + u'******* Error *******\n【模型存在非平面错误】\n'
        cmds.button('nonParallelPlaneCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('nonParallelPlanesetbtn', e=True, en=True, c=nonParallelPlaneset)
        cmds.button('nonParallelPlaneClearbtn', e=True, en=True, c=nonParallelPlaneClear)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        print()
        'parallel face ok\n'
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'【模型非平面】Check OK\n'
        cmds.button('nonParallelPlaneCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('nonParallelPlanesetbtn', e=True, en=False)
        cmds.button('nonParallelPlaneClearbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
