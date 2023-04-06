# ——*—— coding: utf-8 _*_

import maya.OpenMaya as om
import maya.cmds as cmds
from tool import datetimeinfo

def checkUVOut(*args):
    logDate = datetimeinfo.dateTimeInfo()
    dagIterator = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
    out_uv_models = {}
    try:
        while not dagIterator.isDone():
            mObject = dagIterator.currentItem()
            fnMesh = om.MFnMesh(mObject)
            # 检查是否存在多组UV
            if fnMesh.numUVSets() > 1:
                for uvSet in range(1, fnMesh.numUVSets()):
                    uvSetNames = om.MStringArray()
                    fnMesh.getUVSetNames(uvSetNames)
                    fnMesh.setCurrentUVSetName(uvSetNames[uvSet])
                    uArray, vArray = om.MFloatArray(), om.MFloatArray()
                    fnMesh.getUVs(uArray, vArray, uvSetNames[uvSet])
                    for i, (u, v) in enumerate(zip(uArray, vArray)):
                        if u > 1.0 or u < 0.0 or v > 1.0 or v < 0.0:
                            if fnMesh.fullPathName() not in out_uv_models:
                                out_uv_models[fnMesh.fullPathName()] = []
                            out_uv_models[fnMesh.fullPathName()].append(i)
            else:
                uArray, vArray = om.MFloatArray(), om.MFloatArray()
                fnMesh.getUVs(uArray, vArray)
                for i, (u, v) in enumerate(zip(uArray, vArray)):
                    if u > 1.0 or u < 0.0 or v > 1.0 or v < 0.0:
                        if fnMesh.fullPathName() not in out_uv_models:
                            out_uv_models[fnMesh.fullPathName()] = []
                        out_uv_models[fnMesh.fullPathName()].append(i)
            dagIterator.next()

        if out_uv_models:
            def UVOutselect(*args):
                models_to_select = []
                uvs_to_select = []
                for model, indices in out_uv_models.items():
                    print(model, indices)
                    models_to_select.append(model)
                    for index in indices:
                        uvs_to_select.append('%s.map[%d]' % (model, index))
                cmds.select(models_to_select)
                cmds.select(uvs_to_select, add=True)

            error_models = [model for model in out_uv_models.keys()]
            error_count = len(error_models)
            error_model_text = '\n'.join(['- ' + model for model in error_models])
            fieldText = logDate + u'******* Error *******\n【%s个模型有UV超出第一象限】：\n%s\n请检查模型问题！\n'% (
            error_count, error_model_text)
            cmds.button('UVCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
            cmds.button('UVsetbtn', e=True, en=True,c=UVOutselect)
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        else:
            fieldText = logDate + u'【无UV超出第一象限的模型】Check OK！\n'
            cmds.button('UVCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
            cmds.button('UVsetbtn', e=True, en=False)
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    except:
        fieldText = u'部分模型UV有错误，跳过检查！\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)