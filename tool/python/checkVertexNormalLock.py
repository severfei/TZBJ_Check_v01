# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
from tool import datetimeinfo

# lock normal vertex chek 检查法线是否锁定
def checkVertexNormalLock(*args):
    logDate = datetimeinfo.dateTimeInfo()
    allMesh = cmds.ls(type='mesh')
    allTransform = list(set(cmds.listRelatives(allMesh, p=True,f=True, type='transform')))
    lockedVtx = []
    checkedTransforms = set()
    for i in allTransform:
        vtx = cmds.polyListComponentConversion(i, toVertex=True)
        itemFrat = cmds.ls(vtx, flatten=True)
        for e in itemFrat:
            vartexNormalList = cmds.polyNormalPerVertex(e, q=True, freezeNormal=True)
            if True in vartexNormalList:
                lockedVtx.append(e)
        checkedTransforms.add(i)
    if lockedVtx:
        def vertexNormalLockset(*args):
            cmds.select(lockedVtx, replace=True)
        def vertexNormalLockClear(*args):
            cmds.polyNormalPerVertex(set(lockedVtx),ufn=True)
            cmds.select(cl=1)
            cmds.button('vertexNormalLocksetbtn', e=True, en=False)
            cmds.button('vertexNormalLockClearbtn', e=True, en=False)
            checkVertexNormalLock()
        # ui edit info-------------------------------------------------------------
        wrongPrint = '\n'.join(lockedVtx)
        fieldText = logDate + u'******* Error *******\n【模型法线锁定错误】\n' + u'请解除法线锁定！\n'
        cmds.button('vertexNormalLockCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('vertexNormalLocksetbtn', e=True, en=True,c=vertexNormalLockset)
        cmds.button('vertexNormalLockClearbtn', e=True, en=True,c=vertexNormalLockClear)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'【模型法线锁定】Check OK！\n'
        cmds.button('vertexNormalLockCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('vertexNormalLocksetbtn', e=True, en=False)
        cmds.button('vertexNormalLockClearbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

# checkVertexNormalLock()