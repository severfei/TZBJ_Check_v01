# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
from tool import datetimeinfo
import os
logDate = datetimeinfo.dateTimeInfo()

def checkantivirus(*args):
    doc_folder = os.path.expanduser("~")
    if "Documents" in doc_folder:
        pass
    else:
        doc_folder = os.path.expanduser("~\\Documents")
    print(doc_folder)
    maya_script_path = doc_folder + "\\" + "maya\scripts\\"
    print(maya_script_path)

    ######## cleanup userSetup.Py #######
    userSetupPath = maya_script_path + "userSetup.py"

    # Check if userSetup.py exists
    if os.path.isfile(userSetupPath):
        # open File
        with open(userSetupPath, "r") as file:
            filedata = file.read()

        # replaceLine
        filedata = filedata.replace("import vaccine\r\n", "")
        filedata = filedata.replace("cmds.evalDeferred('leukocyte = vaccine.phage()')\r\n", "")
        filedata = filedata.replace("cmds.evalDeferred('leukocyte.occupation()')", "")

        # write File
        with open(userSetupPath, "w") as file:
            file.write(filedata)
    #####################################

    virus_py_dir = maya_script_path + "vaccine.py"
    virus_pyc_dir = maya_script_path + "vaccine.pyc"
    print(virus_py_dir)
    print(virus_pyc_dir)

    try:
        if not os.path.isfile(virus_py_dir):
            if not os.path.isfile(virus_pyc_dir):
                print(" Not Infected")
                fieldText = logDate + u'【未发现病毒文件】 check OK！\n'
                cmds.button('virusCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

                print("---------------------------")
                print("| cant find vaccine Files |")
                print("---------------------------")
        else:
            def clearVirus(*args):
                try:
                    if os.path.isfile(virus_py_dir):
                        print("Infected")
                        os.remove(virus_py_dir)
                        fieldText = logDate + u'已经移除 removed vaccine.py 文件！\n'
                        cmds.button('virusCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
                        cmds.button('virusClearbtn', e=True, en=False)
                        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
                        print("----------------------")
                        print("| removed vaccine.py |")
                        print("----------------------")
                except:
                    pass

                try:
                    if os.path.isfile(virus_pyc_dir):
                        print("Infected")
                        os.remove(virus_pyc_dir)
                        fieldText = logDate + u'已经移除  removed vaccine.pyc 文件！\n'
                        cmds.button('virusCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
                        cmds.button('virusClearbtn', e=True, en=False)
                        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
                        print("-----------------------")
                        print("| removed vaccine.pyc |")
                        print("-----------------------")
                except:
                    pass

                try:
                    os.mkdir(maya_script_path + "vaccine.py")
                    fieldText = logDate + u'创建 vaccine.py 文件夹，防止二次感染！\n'
                    cmds.button('virusCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
                    cmds.button('virusClearbtn', e=True, en=False)
                    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

                    print("------------------")
                    print("| make py folder |")
                    print("------------------")
                except:
                    pass
                try:
                    os.mkdir(maya_script_path + "vaccine.pyc")
                    fieldText = logDate + u'创建 vaccine.pyc 文件夹，防止二次感染！\n'
                    cmds.button('virusCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
                    cmds.button('virusClearbtn', e=True, en=False)
                    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
                    checkantivirus()
                    print("-------------------")
                    print("| make pyc folder |")
                    print("-------------------")
                except:
                    pass

            fieldText = logDate + u'******* Error *******\n【发现病毒文件】请修复！\n'
            cmds.button('virusCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
            cmds.button('virusClearbtn', e=True, en=True, c=clearVirus)


    except:
        pass
