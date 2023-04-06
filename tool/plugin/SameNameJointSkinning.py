# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import getpass
def SameNameJointWindow(*args):
    if cmds.window("FKIKmaker", exists=True):
        cmds.deleteUI("FKIKmaker")
    cmds.window("FKIKmaker", title='FKIKmaker', widthHeight=(200, 90))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="SameNameJointSkinningJoint")
    cmds.button(label='SameNameJointSkinningJoint', command=SameNameJointSkinningJoint)
    cmds.text(label="ObjectMerge")
    cmds.button(label='ObjectMerge', command=mergeRun)
    cmds.showWindow("FKIKmaker")



def SameNameJointSkinningJoint(*args):
    selectModel = cmds.ls("MDL_*", type="transform")
    allJoint = cmds.ls(type="joint")
    selectJoint = []
    for loop in allJoint:
        if "end" in loop:
            continue
        if "root" in loop:
            continue
        if "center" in loop:
            continue
        selectJoint.append(loop)

    for loopModel in selectModel:
        for loopJoint in selectJoint:
            if (loopModel.split("_", 1)[1]).rsplit("_", 2)[0] == loopJoint.rsplit("_", 1)[0]:
                print((loopModel.split("_", 1)[1]).rsplit("_", 2)[0] + "+" + loopJoint.rsplit("_", 1)[0])
                cmds.skinCluster(loopJoint, loopModel, tsb=True)


def ObjectMerge(MDLName):
    BodyMdlList = []
    VisorMdlList = []
    EmitMdlList = []
    DecalMdlList = []
    GlassMdlList = []
    MdlList = []

    selectModel = cmds.ls("MDL_*", type="transform")
    for loop in selectModel:
        history = cmds.listHistory(loop)
        for i in history:
            if cmds.objectType(i, isType='skinCluster'):
                if loop.rsplit("_", 1)[1] == "Bd":
                    print(loop + "Body")
                    BodyMdlList.append(loop)
                elif loop.rsplit("_", 1)[1] == "Vs":
                    print(loop + "Visor")
                    VisorMdlList.append(loop)
                elif loop.rsplit("_", 1)[1] == "Em":
                    print(loop + "Emit")
                    EmitMdlList.append(loop)
                elif loop.rsplit("_", 1)[1] == "Dc":
                    print(loop + "Decal")
                    DecalMdlList.append(loop)
                elif loop.rsplit("_", 1)[1] == "Gl":
                    print(loop + "Glass")
                    GlassMdlList.append(loop)
                else:
                    continue

    if MDLName == "Body":
        MdlList = BodyMdlList
    elif MDLName == "Visor":
        MdlList = VisorMdlList
    elif MDLName == "Emit":
        MdlList = EmitMdlList
    elif MDLName == "Decal":
        MdlList = DecalMdlList
    elif MDLName == "Glass":
        MdlList = GlassMdlList

    if len(MdlList) <= 1:
        cmds.rename(MdlList[0], "MDL_" + MDLName)
        return
    Object = cmds.polyUniteSkinned(MdlList, ch=True, op=True)
    cmds.select(Object)
    mel.eval('doBakeNonDefHistory( 1, {"prePost"});')
    cmds.rename(Object[0], "MDL_" + MDLName)

def mergeRun(*args):
    ObjectMerge("Body")
    ObjectMerge("Visor")
    ObjectMerge("Emit")
    ObjectMerge("Glass")
    ObjectMerge("Decal")
