# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
from tool import datetimeinfo

# mesh nSide face check 检查模型是否有五边面
def checkNsideFaces(*args):
    logDate = datetimeinfo.dateTimeInfo()
    nSideFace = []
    allMesh = cmds.ls(type='mesh')
    allTransform = list(set(cmds.listRelatives(allMesh, p=True,f=True, type='transform')))
    for i in allTransform:
        cmds.select(i, r=True)
        cmds.polySelectConstraint(mode=3, t=8, planarity=0, size=3, convexity=0)
        selNsides = cmds.ls(sl=True, flatten=True)
        nSideFace.extend(selNsides)
        cmds.select(clear=True)

    cmds.polySelectConstraint(mode=3, t=8, planarity=0, size=0, convexity=0)
    cmds.select(clear=True)

    if len(nSideFace) != 0:
        # 选择五边面模型
        def nSideFaceset(*args):
            cmds.select(set(nSideFace), ne=True)

        # 清理五边面模型
        def nSideFaceClear(*args):
            cmds.select(set(nSideFace), ne=True)
            pm.mel.polyCleanupArgList(4, ["0", "1", "1", "0", "1", "0", "0", "0", "0", "1e-05", "0", "1e-05", "0",
                                          "1e-05", "0", "-1", "0", "0"])
            cmds.select(cl=1)
            cmds.button('nSideFacessetbtn', e=True, en=False)
            cmds.button('nSideFacesClearbtn', e=True, en=False)
            checkNsideFaces()

        # ui edit info-------------------------------------------------------------
        wrongPrint = '\n'.join(nSideFace)
        fieldText = logDate + u'******* Error *******\n【下列模型含有多边面】\n' + wrongPrint + u'\n请清理模型！\n'
        cmds.button('nSideFacesCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('nSideFacessetbtn', e=True, en=True, c=nSideFaceset)
        cmds.button('nSideFacesClearbtn', e=True, en=True, c=nSideFaceClear)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        print()
        'nSide face ok\n'
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'【模型五边面】Check OK！\n'
        cmds.button('nSideFacesCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('nSideFacessetbtn', e=True, en=False)
        cmds.button('nSideFacesClearbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)