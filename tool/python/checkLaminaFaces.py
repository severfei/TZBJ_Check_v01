# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
from tool import datetimeinfo

logDate = datetimeinfo.dateTimeInfo()

# 检查是否含有lamina面
def checkLaminaFaces(*args):
    try:
        allMesh = cmds.ls(type='mesh', noIntermediate=True, long=True)
        allTransform = list(set(cmds.listRelatives(allMesh, p=True,f=True, type='transform')))
        laminaFaces = []
        for i in allTransform:
            cmds.polyMergeVertex(i, d=0, alwaysMergeTwoVertices=0, texture=1, cch=0,ws=True)
            getLamina = cmds.polyInfo(i, laminaFaces=True)
            getLaminaFlat = cmds.ls(getLamina, flatten=True)
            cmds.undo()
            if getLamina != None:
                laminaFaces.extend(getLaminaFlat)
        else:
            if len(laminaFaces) != 0:
                def laminaset(*args):
                    cmds.select(set(laminaFaces),ne=True)
                # ui edit info-------------------------------------------------------------
                wrongPrint = '\n'.join(laminaFaces)
                fieldText = logDate + u'******* Error *******\n【模型包含错误面，重叠面，请修复】\n' + wrongPrint
                cmds.button('laminaFacesCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                cmds.button('laminaFacessetbtn',e=True,en=True,c=laminaset)
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
            else:
                # ui edit info-------------------------------------------------------------
                fieldText = logDate + u'【模型错误面重叠面】check OK!\n'
                cmds.button('laminaFacesCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
                cmds.button('laminaFacessetbtn', e=True, en=False)
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    except:
        fieldText = logDate + u'当前大纲含有未清理的多余Transform节点，未能成功检查重叠模型！n请整理大纲或者跳过检查当前项！\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)




