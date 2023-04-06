# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
from tool import datetimeinfo
logDate = datetimeinfo.dateTimeInfo()

def checkMeshHistory(*args):

    all_meshes = cmds.ls(type='mesh')
    meshes_with_history = []
    for mesh in all_meshes:
        if "Orig" in mesh:
            continue
        history = cmds.listHistory(mesh)
        # 排除一些不属于历史信息的属性
        history = [node for node in history if
                   cmds.nodeType(node) not in ['groupId', 'transform', 'shadingEngine', 'mesh']]
        if len(history) > 0:
            meshes_with_history.append(mesh)
    errormesh = []
    if meshes_with_history:
        for mesh in meshes_with_history:
            errormesh.append(mesh)
        print("以下模型含有历史信息：",errormesh)

        def errorMeshselect(*args):
            errormeshTransforms = []
            for mesh in errormesh:
                errormeshTransforms.append(cmds.listRelatives(mesh, parent=True, fullPath=True)[0])
            cmds.select(set(errormeshTransforms), ne=True)

        def errorMeshsClear(*args):
            clear_mesh_history()
            cmds.select(cl=1)
            cmds.button('historysetbtn', e=True, en=False)
            cmds.button('historyClearbtn', e=True, en=False)
            checkMeshHistory()
        # ui edit info-------------------------------------------------------------
        wrongPrint = '\n'.join(errormesh)
        fieldText = logDate + u'******* Error *******\n【下列模型含有历史信息】\n' + wrongPrint + u'\n请删除掉这些模型的历史信息\n如果含有绑定信息请删除非变形历史\n'
        cmds.button('meshHistoryCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('historysetbtn', e=True, en=True, c=errorMeshselect)
        cmds.button('historyClearbtn', e=True, en=True, c=errorMeshsClear)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        print("场景中的所有模型均不含有历史信息")
        fieldText = logDate + u'【模型历史信息】Check OK！\n'
        cmds.button('meshHistoryCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('historysetbtn', e=True, en=False)
        cmds.button('historyClearbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)


def clear_mesh_history(*args):
    all_mesh = cmds.ls(type='mesh')
    all_transform = list(set(cmds.listRelatives(all_mesh, p=True, f=True, type='transform')))
    for i in all_transform:
        if "Orig" in i:
            continue
        # 删除历史信息
        cmds.delete(i, constructionHistory=True)


