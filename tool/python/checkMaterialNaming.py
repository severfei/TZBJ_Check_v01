# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import pymel.core as pm
from tool import datetimeinfo
logDate = datetimeinfo.dateTimeInfo()

# 检查材质球命名
def checkMaterialNaming(*args):
    # 获取场景中所有的材质球节点
    allMaterials = cmds.ls(mat=True)

    # 默认材质球名称
    defaultMaterials = ['lambert1', 'particleCloud1', 'shaderGlow1', 'standardSurface1']

    # 找到非默认材质球并检查命名
    errorMaterials = []
    for material in allMaterials:
        if material not in defaultMaterials:
            # 判断材质球名称是否以'_mat'结尾
            if not material.endswith('_mat'):
                errorMaterials.append(material)

    # 输出检查结果
    if not errorMaterials:
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'【材质球命名】 check OK！\n'
        cmds.button('materialCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        # cmds.confirmDialog(title=u'材质球命名检查结果', message=u'所有材质球命名正确', button=[u'确定'])

    else:
        # 构造错误信息
        # ui edit info-------------------------------------------------------------
        for material in errorMaterials:
            errormatname = material
            fieldText = logDate + u'******* Error *******\n【以下材质球命名错误】：%s\n请重命名为 -> [ _mat ] 结尾，具体要求根据项目需求调整！\n'%(errormatname)
        cmds.button('materialCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        cmds.select(errorMaterials)


