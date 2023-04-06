# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
from tool import datetimeinfo

logDate = datetimeinfo.dateTimeInfo()

# duplicate obj check  检查模型是否有多个模型重叠
def checkDuplicateOBJ(*args):
    allMesh = cmds.ls(type='mesh', noIntermediate=True, long=True)  # 获取所有mesh节点
    allTransform = list(set(cmds.listRelatives(allMesh, p=True,f=True, type='transform')))  # 获取所有mesh节点的transform节点
    positionDict = {}  # 创建一个字典来存储所有transform节点的位置信息
    try:
        # 获取全部模型的世界坐标和缩放
        for i in allTransform:
            point = cmds.xform(i, query=True, translation=True, worldSpace=True)  # 获取transform节点的位置信息
            scale = cmds.xform(i, query=True, scale=True, relative=True)  # 获取transform节点的缩放信息
            roundPoint = [round(v, 4) for v in point]  # 四舍五入，保留小数点后4位
            roundScale = [round(v, 4) for v in scale]  # 四舍五入，保留小数点后4位
            positionDict[i] = (roundPoint, roundScale)  # 将transform节点的位置信息和缩放信息存入字典
        cmds.select(clear=True)  # 清除选择
        objs = positionDict.keys()
        objPosition = positionDict.values()
        hitList = {}  # 这是一个双面模型的字典
        for i in objs:
            for e in objs:  # 进行模型对比
                if i != e:  # 如果模型不相同，进一步比较它们的形状节点是否相同
                    forcmdsheck = cmds.shapeCompare(i, e)  # 检查两个形状节点是否相同
                    if forcmdsheck == 0:
                        if positionDict[i] == positionDict[e]:  # 检查两个transform节点的位置信息是否相同
                            other = []
                            if i not in hitList:
                                hitList[i] = []
                            else:
                                other = hitList[i]
                            other.append(e)
                            hitList[i] = other
        # 如果有重叠模型
        if len(hitList) != 0:
            duplicates = []
            for key in hitList:   # 将所有重叠模型存入列表
                duplicates.append(key)
                for value in hitList[key]:
                    duplicates.append(value)
            duplicates = list(set(duplicates))  # 将重叠模型列表去重

            def duplicateset(*args):    # 选择所有重叠模型
                cmds.select(duplicates,ne=True)

            # ui edit info-------------------------------------------------------------
            wrongPrint = '\n'.join(duplicates)
            fieldText = logDate + u'******* Error *******\n【包含重叠在一起的模型】，请修复！' + '\n' + wrongPrint
            cmds.button('DuplicateOBJCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
            cmds.button('DuplicateOBJsetbtn',e=True, en=True,c=duplicateset)
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        else:
            # ui edit info-------------------------------------------------------------
            fieldText = logDate + u'【模型重叠】Check OK！\n'
            cmds.button('DuplicateOBJCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
            cmds.button('DuplicateOBJsetbtn', e=True, en=False)
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    except:
        fieldText = logDate + u'当前大纲含有未清理的多余Transform节点，未能成功检查重叠模型！n请整理大纲或者跳过检查当前项！\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)



