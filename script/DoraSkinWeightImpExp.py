# ——*—— coding: utf-8 _*_
import pymel.core as pm
import shutil
import os
import os.path

pm.melGlobals.initVar('string', 'gDoraSkinWeight_ver')
pm.melGlobals['gDoraSkinWeight_ver'] = "3.8.1"


def _vtx2uv(vtx):
    workString = pm.polyListComponentConversion(vtx, tuv=1, fv=1)
    ret = workString[0].replace(".map", ".uv")
    return (ret)


def _checkOverlapsList(list):
    shorteList = []
    overlapsList = []
    overlapsList2 = []
    overlapsListN = 0
    i = 0
    j = 0
    k = 0
    retString = ""
    overlapsCount = 0
    shorteList = pm.mel.stringArrayRemoveDuplicates(list)
    if len(list) == len(shorteList):
        return ("")


    else:
        overlapsListN = 0
        for i in range(0, (len(list) - 1)):
            for j in range(i + 1, len(list)):
                if list[i] == list[j]:
                    overlapsList[overlapsListN] = list[i]
                    overlapsListN += 1

        overlapsList2 = pm.mel.stringArrayRemoveDuplicates(overlapsList)
        retString = ""
        for i in range(0, len(overlapsList2)):
            overlapsCount = list.count(overlapsList2[i])
            retString += (overlapsList2[i] + " (" + str(overlapsCount) + ") ")
            if i < len(overlapsList2) - 1:
                retString += ", "

        return (retString)


def _extCheck(name, ext):
    ret = ""
    ret = name
    if len(name) <= len(ext):
        ret = name + ext


    elif ret[-(len(ext) - 1):].lower() != ext:
        ret = name + ext

    return ret


def _shapeName(obj):
    shape = []
    shape = pm.listHistory(obj)
    shape = pm.ls(shape, type='shape')
    if len(shape) == 0:
        return ("")


    else:
        return (shape[0])


def _searchSC(meshShape):
    cList = []
    cList = pm.listHistory(meshShape)
    cList = pm.ls(cList, type='skinCluster')
    if len(cList) == 0:
        return ("")


    else:
        return (cList[0])


def _simpleObjName(name):
    ret = ""
    ret = name.replace(".*|", "")
    return (ret)


def DoraSkinWeightExport(dsw_name):
    startTime = float(pm.timerX())
    mode = 0
    slList = pm.filterExpand(sm=12)
    if len(slList) == 0:
        slList = pm.filterExpand(sm=31)
        slList = pm.ls(slList, fl=1)
        if len(slList) == 0:
            pm.pm.mel.error("No objects SmoothSkinMesh selected (1)")
            return (0)


        else:
            mode = 2



    else:
        mode = 1

    shape = str(_shapeName(slList[0]))
    sc = str(_searchSC(shape))
    if sc == "":
        pm.pm.mel.error("No objects SmoothSkinMesh selected (2)")
        return (0)

    jointList = pm.listConnections((sc + ".matrix"),
                                   type="joint")
    for i in range(0, len(jointList)):
        jointList[i] = str(_simpleObjName(jointList[i]))

    overlapsJoint = str(_checkOverlapsList(jointList))
    if overlapsJoint != "":
        pm.pm.mel.error("JointName Overlaps [ " + overlapsJoint + "]")
        return (0)

    wp = []
    if mode == 1:
        wp = pm.polyEvaluate(shape, v=1)

    if mode == 2:
        wp[0] = len(slList)

    expString = []
    expString[0] = "DoraYuki Skin Weight Format 3.00"
    expLine = ",".join(jointList)
    expString[1] = (expLine)
    pm.melGlobals.initVar('string', 'gMainProgressBar')
    pm.progressBar(pm.melGlobals['gMainProgressBar'],
                   edit=1,
                   status=("Export " + str(pm.mel.basenameEx(dsw_name))),
                   maxValue=wp[0],
                   beginProgress=1)
    noneUVCount = 0
    for i in range(0, wp[0]):
        pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, step=1)
        workVtx = ""
        if mode == 1:
            workVtx = (shape + ".vtx[" + str(i) + "]")

        if mode == 2:
            workVtx = slList[i]

        weightList = pm.skinPercent(sc, workVtx, q=1, v=1)
        expLine = (str(pm.mel.floatArrayToString(weightList, ",")) + "|")
        wpos = pm.pointPosition(workVtx, w=1)
        expLine += (str(wpos[0]) + "," + str(wpos[1]) + "," + str(wpos[2]) + "|")
        workUV = str(_vtx2uv(workVtx))
        uv = [0.0] * (2)
        if workUV != "":
            uv = pm.getAttr(workUV)


        else:
            noneUVCount += 1
            uv[0] = 0.0
            uv[1] = 0.0

        expLine += (str(uv[0]) + "," + str(uv[1]))
        expString.append((expLine))

    spName = []
    spName = dsw_name.split(" ")
    exportName = ""
    if spName[0] == "[File]":
        exportName = str(
            pm.mel.toNativePath(str(pm.workspace(q=1, fn=1)) + "/" + "dsw/" + str(_extCheck(spName[1], ".dsw"))))
        os.mkdir(pm.mel.dirname(exportName))
        wResult = int(pm.mel.fwriteAllLines(exportName, expString))
        if wResult != 0:
            pm.pm.mel.error("Can not write DSW file")

    if spName[0] == "[Object]":
        exportName = ("dsw|" + str(pm.mel.basenameEx(spName[1])))
        if pm.objExists("dsw") == 0:
            pm.group(em=1, n="dsw")

        if pm.objExists(exportName):
            pm.delete(exportName)

        pm.group(em=1, p="dsw", n=pm.mel.basenameEx(spName[1]))
        for i in range(0, len(expString)):
            pm.addAttr(exportName, ln=("dsw_" + str(i)), dt="string")
            pm.setAttr((exportName + ".dsw_" + str(i)), (expString[i]),
                       type="string")

        pm.select(slList, r=1)

    expString = []
    pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, endProgress=1)
    time = float((pm.timerX() - startTime))
    wp2 = pm.polyEvaluate(shape, v=1)
    result = "=== DSW Exported ===  "
    result += ("Object:[ " + shape + " ]  ")
    result += ("Vertex:[ " + str(wp[0]) + " / " + str(wp2[0]) + " ]  ")
    result += ("NoneUV:[ " + str(noneUVCount) + " ]  ")
    result += ("Time:[ " + str(time) + " ]  ")
    result += ("DSW:[ " + spName[0] + exportName + " ]")
    print(result + "\n")
    return (1)


def _weightCopy(an, bn, sc, shape):
    workString = ""
    jointList = []
    weightList = []
    weight = 0.0
    i = 0
    jointList = pm.listConnections((sc + ".matrix"),
                                   type="joint")
    for i in range(0, len(jointList)):
        jointList[i] = str(_simpleObjName(jointList[i]))

    workString = (shape + ".vtx[" + str(an) + "]")
    weightList = pm.skinPercent(sc, workString, q=1, v=1)
    workString = ""
    for i in range(0, len(jointList)):
        weight = float(float(weightList[i]))
        workString += ("-tv " + jointList[i] + " " + str(weight) + " ")

    if workString != "":
        vtxName = (shape + ".vtx[" + str(bn) + "]")
        workString = ("skinPercent " + workString + sc + " " + vtxName)
        pm.mel.eval(workString)


def _distanceMin(xyz, indexList, setF, range, mode):
    pm.melGlobals.initVar('vector[]', 'gDoraSkinWeightImpExp_Vtx')
    pm.melGlobals.initVar('vector[]', 'gDoraSkinWeightImpExp_UV')
    minIndex = -1
    for i in range(0, len(indexList)):
        index = indexList[i]
        if setF[index]:
            continue

        xyzB = Vector([0, 0, 0])
        if mode == "Vtx":
            xyzB = pm.melGlobals['gDoraSkinWeightImpExp_Vtx'][index]

        if mode == "UV":
            xyzB = pm.melGlobals['gDoraSkinWeightImpExp_UV'][index]

        dis = float(abs(pm.mel.mag(xyz - xyzB)))
        if dis <= range:
            minIndex = index
            return (minIndex)

    return (-1)


def _getBlock(pos, mode):
    if mode == "Vtx":
        return (Vector([pm.mel.floor(pos.x * 0.2), pm.mel.floor(pos.y * 0.2), pm.mel.floor(pos.z * 0.2)]))

    if mode == "UV":
        return (Vector([pm.mel.floor(pos.x * 20), pm.mel.floor(pos.y * 20), 0.0]))

    return (Vector([0, 0, 0]))


def _getIndexBlock(pos, mode):
    pm.melGlobals.initVar('vector[]', 'gDoraSkinWeightImpExp_BlockVtx')
    pm.melGlobals.initVar('string[]', 'gDoraSkinWeightImpExp_BlockVtxIndex')
    pm.melGlobals.initVar('vector[]', 'gDoraSkinWeightImpExp_BlockUV')
    pm.melGlobals.initVar('string[]', 'gDoraSkinWeightImpExp_BlockUVIndex')
    index = []
    posBlock = Vector()
    block = []
    blockIndex = []
    if mode == "Vtx":
        posBlock = Vector(_getBlock(pos, "Vtx"))
        block = pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx']
        blockIndex = pm.melGlobals['gDoraSkinWeightImpExp_BlockVtxIndex']

    if mode == "UV":
        posBlock = Vector(_getBlock(pos, "UV"))
        block = pm.melGlobals['gDoraSkinWeightImpExp_BlockUV']
        blockIndex = pm.melGlobals['gDoraSkinWeightImpExp_BlockUVIndex']

    r = 1
    for i in range(0, len(block)):
        blockV = block[i]
        if (posBlock.x - r) <= blockV.x and blockV.x <= (posBlock.x + r) and (
                posBlock.y - r) <= blockV.y and blockV.y <= (posBlock.y + r) and (
                posBlock.z - r) <= blockV.z and blockV.z <= (posBlock.z + r):
            indexSp = []
            indexSp = blockIndex[i].split(",")
            for j in range(0, len(indexSp)):
                index.append(int(int(indexSp[j])))

    return (index)


def _clearVtxUV():
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_Vtx'")
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx'")
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockVtxIndex'")
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_UV'")
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockUV'")
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockUVIndex'")
    pm.melGlobals['gDoraSkinWeightImpExp_Vtx'] = []
    pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx'] = []
    pm.melGlobals['gDoraSkinWeightImpExp_BlockVtxIndex'] = []
    pm.melGlobals['gDoraSkinWeightImpExp_UV'] = []
    pm.melGlobals['gDoraSkinWeightImpExp_BlockUV'] = []
    pm.melGlobals['gDoraSkinWeightImpExp_BlockUVIndex'] = []


def _setVtxUV(shape):
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_Vtx'")
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx'")
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockVtxIndex'")
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_UV'")
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockUV'")
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_BlockUVIndex'")
    _clearVtxUV()
    wp = []
    wp = pm.polyEvaluate(shape, v=1)
    for i in range(0, wp[0]):
        vtx = (shape + ".vtx[" + str(i) + "]")
        pos_f = pm.pointPosition(vtx, w=1)
        pos_v = Vector([pos_f[0], pos_f[1], pos_f[2]])
        pm.melGlobals['gDoraSkinWeightImpExp_Vtx'][i] = pos_v
        hit = 0
        block = Vector(_getBlock(pos_v, "Vtx"))
        for j in range(0, len(pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx'])):
            if pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx'][j] == block:
                workString = pm.melGlobals['gDoraSkinWeightImpExp_BlockVtxIndex'][j]
                pm.melGlobals['gDoraSkinWeightImpExp_BlockVtxIndex'][j] = (workString + "," + str(str(i)))
                hit = 1
                break

        if hit == 0:
            index = len(pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx'])
            pm.melGlobals['gDoraSkinWeightImpExp_BlockVtx'][index] = block
            pm.melGlobals['gDoraSkinWeightImpExp_BlockVtxIndex'][index] = str(str(i))

        uv = str(_vtx2uv(vtx))
        if uv != "":
            pos_f = pm.getAttr(uv)


        else:
            pos_f[0] = 0.0
            pos_f[1] = 0.0

        pos_v = Vector([pos_f[0], pos_f[1], 0.0])
        pm.melGlobals['gDoraSkinWeightImpExp_UV'][i] = pos_v
        hit = 0
        block = Vector(_getBlock(pos_v, "UV"))
        for j in range(0, len(pm.melGlobals['gDoraSkinWeightImpExp_BlockUV'])):
            if pm.melGlobals['gDoraSkinWeightImpExp_BlockUV'][j] == block:
                workString = pm.melGlobals['gDoraSkinWeightImpExp_BlockUVIndex'][j]
                pm.melGlobals['gDoraSkinWeightImpExp_BlockUVIndex'][j] = (workString + "," + str(str(i)))
                hit = 1
                break

        if hit == 0:
            index = len(pm.melGlobals['gDoraSkinWeightImpExp_BlockUV'])
            pm.melGlobals['gDoraSkinWeightImpExp_BlockUV'][index] = block
            pm.melGlobals['gDoraSkinWeightImpExp_BlockUVIndex'][index] = str(str(i))


def _getParam_weightSet(selectJoint, exist, unknown, joint, weightAll):
    param = ""
    weight = []
    weight = weightAll.split(",")
    for i in range(0, len(exist)):
        jName = selectJoint[exist[i]]
        for j in range(0, len(joint)):
            if jName == joint[j]:
                param += ("-tv " + jName + " " + weight[j] + " ")
                break

    for i in range(0, len(unknown)):
        param += ("-tv " + selectJoint[unknown[i]] + " 0 ")

    return (param)


def _addParam_sameWeight(dsw_line, weight, weightSetF, shape):
    param = ""
    for i in range(2, len(dsw_line)):
        if weightSetF[i - 2]:
            continue

        lineSp = []
        lineSp = dsw_line[i].split("|")
        if lineSp[0] == weight:
            param += (" " + shape + ".vtx[" + str((i - 2)) + "]")
            weightSetF[i - 2] = 1

    return (param)


def _addParam_sameWeightVtx(dsw_line, weight, weightSetF, shape, range, mode):
    param = ""
    for i in range(2, len(dsw_line)):
        lineSp = []
        lineSp = dsw_line[i].split("|")
        if lineSp[0] == weight:
            posSp = []
            pos = Vector([0, 0, 0])
            indexList = []
            if mode == "Vtx":
                posSp = lineSp[1].split(",")
                pos = Vector([float(posSp[0]), float(posSp[1]), float(posSp[2])])
                indexList = _getIndexBlock(pos, "Vtx")

            if mode == "UV":
                posSp = lineSp[2].split(",")
                pos = Vector([float(posSp[0]), float(posSp[1]), 0])
                indexList = _getIndexBlock(pos, "UV")

            minIndex = int(_distanceMin(pos, indexList, weightSetF, range, mode))
            if minIndex == -1:
                continue

            if weightSetF[minIndex]:
                continue

            param += (" " + shape + ".vtx[" + str(minIndex) + "]")
            weightSetF[minIndex] = 1

    return (param)


def _readDSW(dsw_name):
    spName = []
    spName = dsw_name.split(" ")
    dsw_text = ""
    dsw_line = []
    ImportName = ""
    if spName[0] == "[File]":
        ImportName = (str(pm.workspace(q=1, fn=1)) + "/dsw/" + spName[1])
        if os.access(ImportName, os.R_OK) == 0:
            pm.pm.mel.error("Read DSW File Error")
            return ([])

        dsw_text = str(pm.mel.freadAllText(ImportName))
        dsw_line = dsw_text.split("\r\n")
        dsw_text = ""

    if spName[0] == "[Object]":
        ImportName = "dsw|" + spName[1]
        if pm.objExists(ImportName + ".dsw_0"):
            i = 0
            while 1:
                if not (pm.objExists(ImportName + ".dsw_" + str(i))):
                    break

                dsw_line[i] = str(pm.getAttr(ImportName + ".dsw_" + str(i)))

                i += 1



        else:
            ImportName += ".notes"
            if pm.objExists(ImportName) == 0:
                pm.pm.mel.error("Read DSW Object Error")
                return ([])

            dsw_text = str(pm.getAttr(ImportName))
            dsw_line = dsw_text.split("\r\n")
            dsw_text = ""

    if len(dsw_line) < 3:
        pm.pm.mel.error("No DSW Data")
        return ([])

    if dsw_line[0] != "DoraYuki Skin Weight Format 3.00":
        pm.pm.mel.error("Not DSW Format 3.00")
        return ([])

    if dsw_line[1] == "":
        pm.pm.mel.error("No DSW JointData")
        return ([])

    return (dsw_line)


def _bindSkinDSW(obj, dsw):
    shape = str(_shapeName(obj))
    sc = str(_searchSC(shape))
    if sc != "":
        pm.skinCluster(shape, e=1, ub=1)

    dsw_line = _readDSW(dsw)
    jointList = []
    jointList = dsw_line[1].split(",")
    for j in range(0, len(jointList)):
        jointList[j] = str(_simpleObjName(jointList[j]))

    pm.melGlobals.initVar('string[]', 'gDoraSkinWeightImpExp_jointNameNew')
    if pm.window('DoraSkinWeightImpExpJointNameEditWindow', ex=1) == True:
        for i in range(0, len(jointList)):
            jointList[i] = pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][i]

    pm.mel.eval("select -r " + " ".join(jointList) + " " + obj)
    pm.skinCluster(toSelectedBones=1, n=("skinCluster_" + obj))
    return (1)


def DoraSkinWeightImport(dsw_name, importMode, interpolationWeight, interpolationMode, para, bindSkin):
    startTime = float(pm.timerX())
    if dsw_name == "":
        return (0)

    slList = pm.filterExpand(sm=12)
    if len(slList) == 0:
        pm.pm.mel.error("No objects SmoothSkinMesh selected (1)")
        return (0)

    shape = str(_shapeName(slList[0]))
    if bindSkin:
        if _bindSkinDSW(slList[0], dsw_name) == 0:
            return (0)

    sc = str(_searchSC(shape))
    if sc == "":
        pm.pm.mel.error("No objects SmoothSkinMesh selected (2)")
        return (0)

    targetJointList = pm.listConnections((sc + ".matrix"),
                                         type="joint")
    for i in range(0, len(targetJointList)):
        targetJointList[i] = str(_simpleObjName(targetJointList[i]))

    overlapsJoint = str(_checkOverlapsList(targetJointList))
    if overlapsJoint != "":
        pm.pm.mel.error("JointName Overlaps [ " + overlapsJoint + "]")
        return (0)

    dsw_line = _readDSW(dsw_name)
    wp = pm.polyEvaluate(shape, v=1)
    jointList = []
    jointList = dsw_line[1].split(",")
    for j in range(0, len(jointList)):
        jointList[j] = str(_simpleObjName(jointList[j]))

    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'")
    if pm.window('DoraSkinWeightImpExpJointNameEditWindow', ex=1) == True:
        for i in range(0, len(jointList)):
            jointList[i] = pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][i]

    existJointN = []
    unknownJointN = []
    for s in range(0, len(targetJointList)):
        check = 0
        for d in range(0, len(jointList)):
            if targetJointList[s] == jointList[d]:
                existJointN.append(int(s))
                check = 1
                break

        if check == 0:
            unknownJointN.append(int(s))

    weightSetF = []
    for i in range(0, wp[0]):
        weightSetF[i] = 0

    pm.melGlobals.initVar('string', 'gMainProgressBar')
    pm.progressBar(pm.melGlobals['gMainProgressBar'],
                   edit=1,
                   status=("Import " + str(pm.mel.basenameEx(dsw_name))),
                   maxValue=wp[0],
                   beginProgress=1)
    pm.setAttr((sc + ".normalizeWeights"),
               0)
    pm.setAttr((sc + ".envelope"),
               0)
    _setVtxUV(shape)
    r = 2
    if importMode == 0:
        for i in range(0, wp[0]):
            pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, step=1)
            if len(dsw_line) <= r:
                break

            if dsw_line[r] == "":
                break

            lineSp = []
            lineSp = dsw_line[r].split("|")
            r += 1
            if weightSetF[i]:
                continue

            weightSetParam = str(_getParam_weightSet(targetJointList, existJointN, unknownJointN, jointList, lineSp[0]))
            if weightSetParam == "":
                continue

            addVtxParam = str(_addParam_sameWeight(dsw_line, lineSp[0], weightSetF, shape))
            weightSetParam = ("skinPercent -r false " + weightSetParam + sc + addVtxParam)
            pm.mel.eval(weightSetParam)

    if importMode == 1 or importMode == 2:
        while len(dsw_line) > r:
            pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, step=1)
            if dsw_line[r] == "":
                break

            lineSp = []
            lineSp = dsw_line[r].split("|")
            r += 1
            mode = ""
            workXYZs = []
            dswPos = Vector()
            if importMode == 1:
                mode = "Vtx"
                workXYZs = lineSp[1].split(",")
                dswPos = Vector([float(workXYZs[0]), float(workXYZs[1]), float(workXYZs[2])])

            if importMode == 2:
                mode = "UV"
                workXYZs = lineSp[2].split(",")
                dswPos = Vector([float(workXYZs[0]), float(workXYZs[1]), 0])

            indexList = _getIndexBlock(dswPos, mode)
            minIndex = int(_distanceMin(dswPos, indexList, weightSetF, para, mode))
            if minIndex == -1:
                continue

            weightSetParam = str(_getParam_weightSet(targetJointList, existJointN, unknownJointN, jointList, lineSp[0]))
            if weightSetParam == "":
                continue

            addVtxParam = str(_addParam_sameWeightVtx(dsw_line, lineSp[0], weightSetF, shape, para, mode))
            weightSetParam = ("skinPercent -r false " + weightSetParam + sc + addVtxParam)
            pm.mel.eval(weightSetParam)

    if interpolationWeight == 1:
        pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1,
                       status=("Interpolate " + str(pm.mel.basenameEx(dsw_name))))
        for i in range(0, len(weightSetF)):
            if weightSetF[i]:
                continue

            pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, step=1)
            pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_Vtx'")
            pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_UV'")
            minIndex = -1
            dis = float(12345678)
            fs = 0
            for j in range(0, wp[0]):
                if i == j or weightSetF[j] != 1:
                    continue

                if fs == 0:
                    minIndex = j
                    fs = 1
                    continue

                dis2 = float(0)
                if interpolationMode == 1:
                    dis2 = float(abs(pm.mel.mag(
                        pm.melGlobals['gDoraSkinWeightImpExp_Vtx'][i] - pm.melGlobals['gDoraSkinWeightImpExp_Vtx'][j])))

                if interpolationMode == 2:
                    dis2 = float(abs(pm.mel.mag(
                        pm.melGlobals['gDoraSkinWeightImpExp_UV'][i] - pm.melGlobals['gDoraSkinWeightImpExp_UV'][j])))

                if dis > dis2:
                    dis = dis2
                    minIndex = j

            if minIndex == -1:
                break

            _weightCopy(minIndex, i, sc, shape)
            weightSetF[i] = 2

    _clearVtxUV()
    pm.setAttr((sc + ".envelope"),
               1)
    pm.skinPercent(sc, shape, normalize=True)
    pm.setAttr((sc + ".normalizeWeights"),
               1)
    pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, endProgress=1)
    selectParam = ""
    for i in range(0, wp[0]):
        if weightSetF[i] == 1:
            selectParam += (shape + ".vtx[" + str(i) + "] ")

        if weightSetF[i] == 2:
            uvName = str(_vtx2uv(shape + ".vtx[" + str(i) + "] "))
            uvName = uvName.replace(".uv", ".map")
            selectParam += (uvName + " ")

    if selectParam != "":
        pm.mel.eval("select " + selectParam)

    time = float((pm.timerX() - startTime))
    setCount = int(pm.mel.intArrayCount(1, weightSetF))
    setCount2 = int(pm.mel.intArrayCount(2, weightSetF))
    result = "=== DSW Imported ===  "
    result += ("Object:[ " + shape + " ]  ")
    result += ("Vertex:[ " + str((setCount + setCount2)) + " ( " + str(setCount2) + " ) / " + str(wp[0]) + " ]  ")
    result += ("Time:[ " + str(time) + " ]  ")
    print(result + "\n")
    return (1)


def DoraSkinWeightXYZCheck():
    importFileName = str(pm.mel.toNativePath(str(pm.workspace(q=1, fn=1)) + "/*.dsw"))
    importFileName = str(pm.fileDialog(dm=importFileName))
    if importFileName == "":
        return

    workString = "particle "
    textLine = pm.mel.freadAllLines(importFileName)
    if textLine[0] != "DoraYuki Skin Weight Format 3.00":
        return

    i = 0
    for i in range(2, len(textLine)):
        pointData = []
        pointData = textLine[i].split("|")
        workXYZs = []
        pm.mel.tokenizeList(pointData[1], workXYZs)
        workString = (workString + "-p " + workXYZs[0] + " " + workXYZs[1] + " " + workXYZs[2] + " ")

    workString = (workString + "-c 1 -n skinWeightPoint")
    pm.mel.eval(workString)
    pm.addAttr('skinWeightPointShape', min=1, ln="pointSize", max=60, at='long', internalSet=True, dv=8)


def DoraSkinWeightCreateSkinJointSet():
    slList = pm.filterExpand(sm=12)
    if len(slList) == 0:
        pm.pm.mel.error("No objects SmoothSkinMesh selected (1)")
        return (0)

    shape = str(_shapeName(slList[0]))
    sc = str(_searchSC(shape))
    if sc == "":
        pm.pm.mel.error("No objects SmoothSkinMesh selected (2)")
        return (0)

    jointList = pm.listConnections((sc + ".matrix"),
                                   type="joint")
    pm.mel.eval("sets -name \"SkinJointSet_" + slList[0] + "\" " + " ".join(jointList))
    return (1)


def DoraSkinWeightCheckDigit(digit):
    if digit <= 0:
        pm.pm.mel.error("Input one or more digits")
        return (0)

    slList = pm.filterExpand(sm=12)
    if len(slList) == 0:
        pm.pm.mel.error("No objects SmoothSkinMesh selected (1)")
        return (0)

    shape = str(_shapeName(slList[0]))
    sc = str(_searchSC(shape))
    if sc == "":
        pm.pm.mel.error("No objects SmoothSkinMesh selected (2)")
        return (0)

    wp = []
    wp = pm.polyEvaluate(shape, v=1)
    pm.melGlobals.initVar('string', 'gMainProgressBar')
    pm.progressBar(pm.melGlobals['gMainProgressBar'],
                   edit=1,
                   status=("Check " + str(pm.mel.basenameEx(slList[0]))),
                   maxValue=wp[0],
                   beginProgress=1)
    selVtx = ""
    for i in range(0, wp[0]):
        pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, step=1)
        vtx = (shape + ".vtx[" + str(i) + "]")
        weightList = pm.skinPercent(sc, vtx, q=1, v=1)
        for w in range(0, len(weightList)):
            weightS = str(weightList[w])
            weightSp = []
            weightSp = weightS.split(".")
            if len(weightSp[- 1]) > digit:
                print("Check : [ " + weightS + " ] " + vtx + "\n")
                selVtx += (vtx + " ")
                break

    pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, endProgress=1)
    if selVtx != "":
        pm.mel.eval("select " + selVtx)


    else:
        print("Check Pass ( " + str(digit) + " Digit )\n")

    return (1)


def DoraSkinWeightCheckSamePos():
    slList = pm.filterExpand(sm=12)
    if len(slList) == 0:
        pm.pm.mel.error("No objects SmoothSkinMesh selected (1)")
        return (0)

    shape = str(_shapeName(slList[0]))
    sc = str(_searchSC(shape))
    if sc == "":
        pm.pm.mel.error("No objects SmoothSkinMesh selected (2)")
        return (0)

    pm.select(cl=1)
    wp = []
    wp = pm.polyEvaluate(shape, v=1)
    checkF = []
    for i in range(0, wp[0]):
        checkF[i] = 0

    _setVtxUV(shape)
    pm.melGlobals.initVar('vector[]', "pm.melGlobals['gDoraSkinWeightImpExp_Vtx'")
    vtx = pm.melGlobals['gDoraSkinWeightImpExp_Vtx']
    pm.melGlobals.initVar('string', 'gMainProgressBar')
    pm.progressBar(pm.melGlobals['gMainProgressBar'],
                   edit=1,
                   status=("Check " + str(pm.mel.basenameEx(slList[0]))),
                   maxValue=wp[0],
                   beginProgress=1)
    pass_ = 1
    for i in range(0, wp[0]):
        pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, step=1)
        if checkF[i]:
            continue

        checkF[i] = 1
        indexList = _getIndexBlock(vtx[i], "Vtx")
        vtxS = []
        vtxS[0] = (shape + ".vtx[" + str(i) + "]")
        vtxL = vtxS[0]
        weight = str(pm.mel.floatArrayToString(pm.skinPercent(sc, vtxS[0], q=1, v=1), ","))
        hit = str(0)
        for j in range(0, len(indexList)):
            ci = indexList[j]
            if checkF[ci]:
                continue

            if abs(pm.mel.mag(vtx[i] - vtx[ci])) < 0.001:
                checkF[ci] = 1
                vtxS.append((shape + ".vtx[" + str(ci) + "]"))
                vtxL += (" vtx[" + str(ci) + "]")
                weight2 = str(pm.mel.floatArrayToString(pm.skinPercent(sc, vtxS[- 1], q=1, v=1), ","))
                if weight != weight2:
                    hit = str(1)
                    pass_ = 0

        if hit:
            print("Check : " + vtxL + "\n")
            pm.mel.eval("select -tgl " + " ".join(vtxS))

    pm.progressBar(pm.melGlobals['gMainProgressBar'], edit=1, endProgress=1)
    _clearVtxUV()
    if pass_:
        print("Check Pass\n")

    return (1)


def _dswAppendListGet():
    ret = ""
    list = []
    dswDir = ""
    i = 0
    ret = ""
    dswDir = (str(pm.workspace(q=1, fn=1)) + "/dsw/")
    list = pm.getFileList(folder=dswDir, filespec="*.dsw")
    for i in range(0, len(list)):
        ret = (ret + "-a \"[File] " + list[i] + "\" ")

    list = pm.ls("dsw|*")
    for i in range(0, len(list)):
        ret = (ret + "-a \"[Object] " + list[i] + "\" ")

    return ret


def DoraSkinWeightFileListUpdate():
    dswAppendList = ""
    work = ""
    pm.textScrollList('DSW_TXTSL_ExpList', e=1, ra=1)
    pm.textScrollList('DSW_TXTSL_ImpList', e=1, ra=1)
    dswAppendList = str(_dswAppendListGet())
    if len(dswAppendList) != 0:
        work = ("textScrollList -e " + dswAppendList + " DSW_TXTSL_ExpList")
        pm.mel.eval(work)
        work = ("textScrollList -e " + dswAppendList + " DSW_TXTSL_ImpList")
        pm.mel.eval(work)


def DoraSkinWeightTSL2BaseName(tsl):
    spName = []
    spName = tsl[0].split(" ")
    if len(spName) >= 2:
        return (spName[1])


    else:
        return (spName[0])


def _JointNameEdit_SetgJointName():
    pm.melGlobals.initVar('string[]', 'gDoraSkinWeightImpExp_jointName')
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'")
    pm.melGlobals['gDoraSkinWeightImpExp_jointName'] = []
    pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'] = []
    impList = []
    impList = pm.textScrollList('DSW_TXTSL_ImpList', q=1, si=1)
    if impList[0] == "":
        return (0)

    spName = []
    spName = impList[0].split(" ")
    dsw_text = ""
    dsw_line = []
    ImportName = ""
    if spName[0] == "[File]":
        ImportName = (str(pm.workspace(q=1, fn=1)) + "/dsw/" + spName[1])
        if os.access(ImportName, os.R_OK) == 0:
            return (0)

        dsw_text = str(pm.mel.freadAllText(ImportName))

    if spName[0] == "[Object]":
        ImportName = "dsw|" + spName[1] + ".notes"
        if pm.objExists(ImportName) == 0:
            return (0)

        dsw_text = str(pm.getAttr(ImportName))

    dsw_line = dsw_text.split("\r\n")
    if dsw_line[0] != "DoraYuki Skin Weight Format 3.00":
        return (0)

    pm.mel.tokenizeList(dsw_line[1], pm.melGlobals['gDoraSkinWeightImpExp_jointName'])
    pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'] = pm.melGlobals['gDoraSkinWeightImpExp_jointName']
    return (1)


def _JointNameEdit_jointEditListString():
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointName'")
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'")
    ret = ""
    ret = ""
    for i in range(0, len(pm.melGlobals['gDoraSkinWeightImpExp_jointName'])):
        ret += ("-a \"[ " + pm.melGlobals['gDoraSkinWeightImpExp_jointName'][i] + " ] ---> [ " +
                pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][i] + " ]\" ")

    return (ret)


def JointNameEdit_listAllSelect():
    i = 0
    n = 0
    n = int(pm.textScrollList('DSW_TXTSL_jne_JointList', q=1, ni=1))
    for i in range(0, n):
        pm.textScrollList('DSW_TXTSL_jne_JointList', sii=(i + 1), e=1)


def _JointNameEdit_listUpdate():
    if pm.window('DoraSkinWeightImpExpJointNameEditWindow', ex=1) == False:
        return (0)

    workString = str(_JointNameEdit_jointEditListString())
    pm.textScrollList('DSW_TXTSL_jne_JointList', e=1, ra=1)
    pm.mel.eval("textScrollList -e -showIndexedItem 1 " + workString + " DSW_TXTSL_jne_JointList")
    return (1)


def JointNameEdit_reload():
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'")
    workStringA = []
    if pm.window('DoraSkinWeightImpExpJointNameEditWindow', ex=1) == False or pm.window('DoraSkinWeightImpExpWindow',
                                                                                        ex=1) == False:
        return (0)

    if _JointNameEdit_SetgJointName() == 0:
        return (0)

    workStringA = pm.textScrollList('DSW_TXTSL_ImpList', q=1, si=1)
    workStringA[0] = (workStringA[0] + " - " + str(len(pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'])) + " joint")
    pm.text('DSW_TXT_jne_dswName', e=1, label=workStringA[0])
    _JointNameEdit_listUpdate()
    return (1)


def JointNameEdit_jointNameUpdate():
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'")
    selectItem = []
    selectItem = pm.textScrollList('DSW_TXTSL_jne_JointList', q=1, sii=1)
    if len(selectItem) <= 0:
        return (0)

    selectItem[0] = selectItem[0] - 1
    pm.textField('DSW_TXTF_jne_JointName', text=(pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[0]]),
                 e=1)
    return (1)


def JointNameEdit_changeJointName(mode, selectMin):
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'")
    selectItem = []
    i = 0
    search = ""
    replace = ""
    workString = ""
    loop = 0
    slList = []
    selectItem = pm.textScrollList('DSW_TXTSL_jne_JointList', q=1, sii=1)
    if len(selectItem) < selectMin:
        return (0)

    for i in range(0, len(selectItem)):
        selectItem[i] = selectItem[i] - 1

    slList = pm.ls(sl=1)
    slList = pm.ls(slList, fl=1)
    for i in range(0, len(selectItem) and loop == 1):
        if mode == 1:
            pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[i]] = str(
                pm.textField('DSW_TXTF_jne_JointName', q=1, text=1))


        elif mode == 2:
            workString = pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[0]]

            pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[0]] = \
            pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[1]]

            pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[1]] = workString

            loop = 0


        elif mode == 3:
            if i < len(slList):
                pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[i]] = slList[i]


            else:
                loop = 0





        elif mode == 4:
            search = str(pm.textField('DSW_TXTF_jne_search', q=1, text=1))

            replace = str(pm.textField('DSW_TXTF_jne_replace', q=1, text=1))

            pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[i]] = \
            pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[i]].replace(search, replace)


        elif mode == 5:
            pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[i]] = (
                        str(pm.textField('DSW_TXTF_jne_prefix', q=1, text=1)) +
                        pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'][selectItem[i]] + str(
                    pm.textField('DSW_TXTF_jne_suffix', q=1, text=1)))

    _JointNameEdit_listUpdate()
    for i in range(0, len(selectItem)):
        pm.textScrollList('DSW_TXTSL_jne_JointList', sii=(selectItem[i] + 1), e=1)

    return (1)


def DoraSkinWeightJointNameEdit():
    pm.melGlobals.initVar('string[]', "pm.melGlobals['gDoraSkinWeightImpExp_jointNameNew'")
    i = 0
    workString = ""
    if pm.window('DoraSkinWeightImpExpWindow', ex=1) == False:
        return (0)

    if _JointNameEdit_SetgJointName() == 0:
        return (0)

    workString = str(_JointNameEdit_jointEditListString())
    if pm.window('DoraSkinWeightImpExpJointNameEditWindow', ex=1):
        return (0)

    pm.window('DoraSkinWeightImpExpJointNameEditWindow', s=1, mnb=1, mxb=1, t="Edit JointMap", wh=(400, 480))
    pm.formLayout('DSW_JointFL')
    pm.text('DSW_TXT_jne_dswName', label="")
    pm.textScrollList('DSW_TXTSL_jne_JointList', showIndexedItem=1, h=180, ams=True)
    pm.columnLayout('DSW_CL_jne_set')
    pm.text(label="JointName")
    pm.textField('DSW_TXTF_jne_JointName', h=20, w=160)
    pm.button('DSW_BTN_jne_set', h=20, w=160, label="Set JointName")
    pm.setParent('..')
    pm.columnLayout('DSW_CL_jne_substitution')
    pm.text(h=20, label="Search")
    pm.textField('DSW_TXTF_jne_search', h=20, w=160)
    pm.text(h=20, label="Replace")
    pm.textField('DSW_TXTF_jne_replace', h=20, w=160)
    pm.button('DSW_BTN_jne_substitution', h=20, w=160, label="Substitution")
    pm.setParent('..')
    pm.columnLayout('DSW_CL_jne_add')
    pm.text(h=20, label="Prefix")
    pm.textField('DSW_TXTF_jne_prefix', h=20, w=160)
    pm.text(h=20, label="Suffix")
    pm.textField('DSW_TXTF_jne_suffix', h=20, w=160)
    pm.button('DSW_BTN_jne_add', h=20, w=160, label="Add Prefix/Suffix")
    pm.setParent('..')
    pm.button('DSW_BTN_jne_swap', h=20, w=160, label="Swap JointName")
    pm.button('DSW_BTN_jne_selectName', h=20, w=160, label="Set SelectObjectName")
    pm.button('DSW_BTN_jne_reset', h=20, w=160, label="Reset")
    pm.setParent('..')
    pm.formLayout('DSW_JointFL', edit=1,
                  ac=[('DSW_TXTSL_jne_JointList', "top", 0, 'DSW_TXT_jne_dswName'),
                      ('DSW_TXTSL_jne_JointList', "right", 0, 'DSW_CL_jne_set'),
                      ('DSW_CL_jne_set', "top", 0, 'DSW_TXT_jne_dswName'),
                      ('DSW_CL_jne_substitution', "top", 8, 'DSW_CL_jne_set'),
                      ('DSW_CL_jne_add', "top", 8, 'DSW_CL_jne_substitution'),
                      ('DSW_BTN_jne_swap', "top", 16, 'DSW_CL_jne_add'),
                      ('DSW_BTN_jne_selectName', "top", 4, 'DSW_BTN_jne_swap'),
                      ('DSW_BTN_jne_reset', "top", 16, 'DSW_BTN_jne_selectName')],
                  af=[('DSW_TXT_jne_dswName', "top", 8), ('DSW_TXT_jne_dswName', "left", 0),
                      ('DSW_TXTSL_jne_JointList', "bottom", 0), ('DSW_TXTSL_jne_JointList', "left", 0),
                      ('DSW_CL_jne_set', "right", 0), ('DSW_CL_jne_substitution', "right", 0),
                      ('DSW_CL_jne_add', "right", 0), ('DSW_BTN_jne_swap', "right", 0),
                      ('DSW_BTN_jne_selectName', "right", 0), ('DSW_BTN_jne_reset', "right", 0)])
    pm.textScrollList('DSW_TXTSL_jne_JointList', sc=lambda *args: pm.mel.JointNameEdit_jointNameUpdate(), e=1)
    pm.textScrollList('DSW_TXTSL_jne_JointList', e=1, dcc=lambda *args: pm.mel.JointNameEdit_listAllSelect())
    pm.button('DSW_BTN_jne_set', c=lambda *args: pm.mel.JointNameEdit_changeJointName(1, 1), e=1)
    pm.textField('DSW_TXTF_jne_JointName', e=1, ec=lambda *args: pm.mel.JointNameEdit_changeJointName(1, 1))
    pm.button('DSW_BTN_jne_swap', c=lambda *args: pm.mel.JointNameEdit_changeJointName(2, 2), e=1)
    pm.button('DSW_BTN_jne_reset', c=lambda *args: pm.mel.JointNameEdit_reload(), e=1)
    pm.button('DSW_BTN_jne_substitution', c=lambda *args: pm.mel.JointNameEdit_changeJointName(4, 1), e=1)
    pm.button('DSW_BTN_jne_add', c=lambda *args: pm.mel.JointNameEdit_changeJointName(5, 1), e=1)
    pm.button('DSW_BTN_jne_selectName', c=lambda *args: pm.mel.JointNameEdit_changeJointName(3, 1), e=1)
    JointNameEdit_reload()
    pm.showWindow('DoraSkinWeightImpExpJointNameEditWindow')
    return (1)


def DoraSkinWeightImpExp():
    pm.melGlobals.initVar('string', 'gDoraSkinWeight_ver')
    pm.melGlobals.initVar('int', 'gDoraSkinWeightImpExp_ImpMode')
    script = ""
    print("Dora SkinWeight Imp/Exp " + pm.melGlobals['gDoraSkinWeight_ver'] + "\n")
    if pm.window('DoraSkinWeightImpExpWindow', ex=1):
        return

    pm.window('DoraSkinWeightImpExpWindow', s=1, mnb=1, mxb=1,
              t=("Dora SkinWeight"),
              wh=(280, 480))
    pm.melGlobals['gDoraSkinWeightImpExp_ImpMode'] = 0
    pm.tabLayout('DSW_TL')
    pm.formLayout('DSW_ImpFL')
    pm.text('DSW_TXT_ImpList', h=20, align="left", label="DSW List")
    pm.textScrollList('DSW_TXTSL_ImpList', h=80, shi=1)
    pm.textField('DSW_TXTF_ImpName', vis=False)
    pm.text('DSW_TXT_ImpMode', h=20, label="Import Mode")
    pm.radioCollection()
    pm.radioButton('DSW_RDOC_ImpMode1', h=20, sl=1, label="Vertex Order")
    pm.radioButton('DSW_RDOC_ImpMode2', h=20, label="XYZ Position")
    pm.radioButton('DSW_RDOC_ImpMode3', h=20, label="UV Position")
    pm.text('DSW_TXT_Accuracy', h=20, en=False, label="Accuracy")
    pm.floatField('DSW_FFLD_Accuracy', pre=6, h=20, en=False, w=70, value=0.001)
    pm.checkBox('DSW_CKBX_Interpolation', h=20, en=True, value=False, label="Interpolate")
    pm.radioCollection('DSW_RDOC_InterpolationMode')
    pm.radioButton('DSW_RDOC_InterpolationMode1', h=20, en=False, data=1, sl=1, label="XYZ")
    pm.radioButton('DSW_RDOC_InterpolationMode2', h=20, en=False, data=2, label="UV")
    pm.checkBox('DSW_CKBX_BindSkin', h=20, en=True, value=False, label="Bind Skin")
    pm.button('DSW_BTN_jne', h=20, w=110, label="Edit JointMap")
    pm.button('DSW_BTN_imp', h=24, label="Import DSW")
    pm.setParent('..')
    pm.formLayout('DSW_ImpFL', edit=1,
                  ac=[('DSW_TXTSL_ImpList', "top", 0, 'DSW_TXT_ImpList'),
                      ('DSW_TXTSL_ImpList', "bottom", 8, 'DSW_TXT_ImpMode'),
                      ('DSW_TXT_ImpMode', "bottom", 0, 'DSW_RDOC_ImpMode1'),
                      ('DSW_RDOC_ImpMode1', "bottom", 0, 'DSW_RDOC_ImpMode2'),
                      ('DSW_RDOC_ImpMode2', "bottom", 0, 'DSW_RDOC_ImpMode3'),
                      ('DSW_RDOC_ImpMode3', "bottom", 8, 'DSW_TXT_Accuracy'),
                      ('DSW_TXT_Accuracy', "bottom", 8, 'DSW_CKBX_Interpolation'),
                      ('DSW_FFLD_Accuracy', "bottom", 8, 'DSW_CKBX_Interpolation'),
                      ('DSW_FFLD_Accuracy', "left", 8, 'DSW_TXT_Accuracy'),
                      ('DSW_CKBX_Interpolation', "bottom", 8, 'DSW_CKBX_BindSkin'),
                      ('DSW_RDOC_InterpolationMode1', "bottom", 8, 'DSW_CKBX_BindSkin'),
                      ('DSW_RDOC_InterpolationMode1', "left", 8, 'DSW_CKBX_Interpolation'),
                      ('DSW_RDOC_InterpolationMode2', "bottom", 8, 'DSW_CKBX_BindSkin'),
                      ('DSW_RDOC_InterpolationMode2', "left", 8, 'DSW_RDOC_InterpolationMode1'),
                      ('DSW_CKBX_BindSkin', "bottom", 8, 'DSW_BTN_jne'), ('DSW_BTN_jne', "bottom", 8, 'DSW_BTN_imp')],
                  af=[('DSW_TXT_ImpList', "top", 8), ('DSW_TXT_ImpList', "left", 0), ('DSW_TXT_ImpList', "right", 0),
                      ('DSW_TXTSL_ImpList', "left", 0), ('DSW_TXTSL_ImpList', "right", 0),
                      ('DSW_TXT_ImpMode', "left", 0), ('DSW_RDOC_ImpMode1', "left", 0),
                      ('DSW_RDOC_ImpMode2', "left", 0), ('DSW_RDOC_ImpMode3', "left", 0),
                      ('DSW_TXT_Accuracy', "left", 0), ('DSW_CKBX_Interpolation', "left", 0),
                      ('DSW_CKBX_BindSkin', "left", 0), ('DSW_BTN_jne', "left", 0), ('DSW_BTN_imp', "bottom", 0),
                      ('DSW_BTN_imp', "left", 0), ('DSW_BTN_imp', "right", 0)])
    pm.formLayout('DSW_ExpFL')
    pm.text('DSW_TXT_ExpList', h=20, align="left", label="DSW List")
    pm.textScrollList('DSW_TXTSL_ExpList', h=80, shi=1)
    pm.text('DSW_TXT_ExpName', h=20, align="left", label="Export DSW Name")
    pm.textField('DSW_TXTF_ExpName', h=20, w=220)
    pm.button('DSW_BTN_exp', h=24, label="Export DSW [File]")
    pm.button('DSW_BTN_expObj', h=24, label="Export DSW [Object]")
    pm.setParent('..')
    pm.formLayout('DSW_ExpFL', edit=1,
                  ac=[('DSW_TXTSL_ExpList', "top", 0, 'DSW_TXT_ExpList'),
                      ('DSW_TXTSL_ExpList', "bottom", 8, 'DSW_TXT_ExpName'),
                      ('DSW_TXT_ExpName', "bottom", 0, 'DSW_TXTF_ExpName'),
                      ('DSW_TXTF_ExpName', "bottom", 8, 'DSW_BTN_exp'), ('DSW_BTN_exp', "bottom", 4, 'DSW_BTN_expObj')],
                  af=[('DSW_TXT_ExpList', "top", 8), ('DSW_TXT_ExpList', "left", 0), ('DSW_TXT_ExpList', "right", 0),
                      ('DSW_TXTSL_ExpList', "left", 0), ('DSW_TXTSL_ExpList', "right", 0),
                      ('DSW_TXT_ExpName', "left", 0), ('DSW_TXTF_ExpName', "left", 0), ('DSW_TXTF_ExpName', "right", 0),
                      ('DSW_BTN_exp', "left", 0), ('DSW_BTN_exp', "right", 0), ('DSW_BTN_expObj', "bottom", 0),
                      ('DSW_BTN_expObj', "left", 0), ('DSW_BTN_expObj', "right", 0)])
    pm.formLayout('DSW_etcFL')
    pm.button('DSW_BTN_chkXYZ', h=20, label="Check DSW XYZ Point")
    pm.button('DSW_BTN_creSet', h=20, label="Create Set SkinJoint")
    pm.intField('DSW_IFLD_chkDig', h=20, w=32, value=2, min=1)
    pm.button('DSW_BTN_chkDig', h=20, label="Check SkinWeight Digit")
    pm.button('DSW_BTN_chkSP', h=20, label="Check SkinWeight SamePosition")
    pm.setParent('..')
    pm.formLayout('DSW_etcFL', edit=1,
                  ac=[('DSW_BTN_creSet', "top", 8, 'DSW_BTN_chkXYZ'), ('DSW_IFLD_chkDig', "top", 8, 'DSW_BTN_creSet'),
                      ('DSW_BTN_chkDig', "top", 8, 'DSW_BTN_creSet'), ('DSW_BTN_chkDig', "left", 2, 'DSW_IFLD_chkDig'),
                      ('DSW_BTN_chkSP', "top", 8, 'DSW_BTN_chkDig')],
                  af=[('DSW_BTN_chkXYZ', "top", 8), ('DSW_BTN_chkXYZ', "left", 0), ('DSW_BTN_chkXYZ', "right", 0),
                      ('DSW_BTN_creSet', "left", 0), ('DSW_BTN_creSet', "right", 0), ('DSW_IFLD_chkDig', "left", 0),
                      ('DSW_BTN_chkDig', "right", 0), ('DSW_BTN_chkSP', "left", 0), ('DSW_BTN_chkSP', "right", 0)])
    pm.tabLayout('DSW_TL', edit=1, tabLabel=[('DSW_ImpFL', "Import"), ('DSW_ExpFL', "Export"), ('DSW_etcFL', "etc")])
    pm.tabLayout('DSW_TL', cc=lambda *args: pm.mel.DoraSkinWeightFileListUpdate(), e=1,
                 dcc=lambda *args: pm.mel.DoraSkinWeightFileListUpdate())
    script = "textField -e -text `textScrollList -q -si DSW_TXTSL_ImpList` DSW_TXTF_ImpName;JointNameEdit_reload();"
    pm.textScrollList('DSW_TXTSL_ImpList', sc=lambda *args: pm.mel.script(), e=1)
    pm.radioButton('DSW_RDOC_ImpMode1', onc=lambda *args: pm.mel.eval(
        "$gDoraSkinWeightImpExp_ImpMode= 0;floatField -e -en false DSW_FFLD_Accuracy;text -e -en false DSW_TXT_Accuracy;"),
                   e=1)
    pm.radioButton('DSW_RDOC_ImpMode2', onc=lambda *args: pm.mel.eval(
        "$gDoraSkinWeightImpExp_ImpMode= 1;floatField -e -en true DSW_FFLD_Accuracy;text -e -en true DSW_TXT_Accuracy;"),
                   e=1)
    pm.radioButton('DSW_RDOC_ImpMode3', onc=lambda *args: pm.mel.eval(
        "$gDoraSkinWeightImpExp_ImpMode= 2;floatField -e -en true DSW_FFLD_Accuracy;text -e -en true DSW_TXT_Accuracy;"),
                   e=1)
    pm.checkBox('DSW_CKBX_Interpolation',
                onc=lambda *args: [pm.radioButton('DSW_RDOC_InterpolationMode1', en=True, e=1),
                                   pm.radioButton('DSW_RDOC_InterpolationMode2', en=True, e=1)], e=1)
    pm.checkBox('DSW_CKBX_Interpolation',
                ofc=lambda *args: [pm.radioButton('DSW_RDOC_InterpolationMode1', en=False, e=1),
                                   pm.radioButton('DSW_RDOC_InterpolationMode2', en=False, e=1)], e=1)
    pm.button('DSW_BTN_jne', edit=1, command=lambda *args: pm.mel.DoraSkinWeightJointNameEdit())
    pm.button('DSW_BTN_imp', edit=1,
              command=lambda *args: pm.mel.DoraSkinWeightImport(pm.textField('DSW_TXTF_ImpName', q=1, text=1),
                                                                gDoraSkinWeightImpExp_ImpMode,
                                                                pm.checkBox('DSW_CKBX_Interpolation', q=1, value=1),
                                                                pm.mel.eval("radioButton -q -da " + str(
                                                                    pm.radioCollection('DSW_RDOC_InterpolationMode',
                                                                                       q=1, sl=1))),
                                                                pm.floatField('DSW_FFLD_Accuracy', q=1, value=1),
                                                                pm.checkBox('DSW_CKBX_BindSkin', q=1, value=1)))
    script = "string $temp=DoraSkinWeightTSL2BaseName(`textScrollList -q -si DSW_TXTSL_ExpList`); textField -e -text $temp DSW_TXTF_ExpName;"
    pm.textScrollList('DSW_TXTSL_ExpList', sc=lambda *args: pm.mel.script(), e=1)
    pm.button('DSW_BTN_exp', edit=1, command=lambda *args: pm.mel.eval(
        "if(`textField -q -text DSW_TXTF_ExpName`!=\"\")DoraSkinWeightExport( \"[File] \" + `textField -q -text DSW_TXTF_ExpName` );DoraSkinWeightFileListUpdate();"))
    pm.button('DSW_BTN_expObj', edit=1, command=lambda *args: pm.mel.eval(
        "if(`textField -q -text DSW_TXTF_ExpName`!=\"\")DoraSkinWeightExport( \"[Object] \" + `textField -q -text DSW_TXTF_ExpName` );DoraSkinWeightFileListUpdate();"))
    pm.button('DSW_BTN_chkXYZ', edit=1, command=lambda *args: pm.mel.DoraSkinWeightXYZCheck())
    pm.button('DSW_BTN_creSet', edit=1, command=lambda *args: pm.mel.DoraSkinWeightCreateSkinJointSet())
    pm.button('DSW_BTN_chkDig', edit=1,
              command=lambda *args: pm.mel.DoraSkinWeightCheckDigit(pm.intField('DSW_IFLD_chkDig', q=1, v=1)))
    pm.button('DSW_BTN_chkSP', edit=1, command=lambda *args: pm.mel.DoraSkinWeightCheckSamePos())
    DoraSkinWeightFileListUpdate()
    pm.showWindow('DoraSkinWeightImpExpWindow')


