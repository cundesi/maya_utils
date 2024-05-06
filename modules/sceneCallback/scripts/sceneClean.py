#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import os
import shutil
import maya.cmds as cmds
import maya.mel as mm


JOB_INDEX_REGEX = re.compile(r'^(\d+):')

BAD_JOD_SCRIPTS = ['leukocyte.antivirus()']

AFTER_OPEN_CALLBACK_ID = None
BEFORE_SAVE_CALLBACK_ID = None
AFTER_REFERENCE_CALLBACK_ID = None
BEFORE_REMOVE_REFERENCE_CALLBACK_ID = None
AFTER_IMPORT_REFERENCE_CALLBACK_ID = None
BEFORE_EXPORT_REFERENCE_CALLBACK_ID = None
BEFORE_UNLOAD_REFERENCE_CALLBACK_ID = None
AFTER_IMPORT_CALLBACK_ID = None
BEFORE_EXPORT_CALLBACK_ID = None


def find_bad_scripts():
    bad_script_nodes = []
    script_nodes = cmds.ls(type='script')
    for script_node in script_nodes:
        script_before_string = cmds.getAttr('{}.before'.format(script_node))
        script_after_string = cmds.getAttr('{}.after'.format(script_node))
        for script_string in [script_before_string, script_after_string]:
            if not script_string:
                continue
            if 'internalVar' in script_string or 'userSetup' in script_string or 'fuckVirus' in script_string\
                or 'python("import base64; _pycode = base64.urlsafe_b64decode' in script_string:
                bad_script_nodes.append(script_node)
    return bad_script_nodes


def del_bad_scripts(bad_script_nodes):
    for bad_script_node in bad_script_nodes:
        if cmds.referenceQuery(bad_script_node, isNodeReferenced=True):
            try:
                cmds.setAttr(bad_script_node + ".before", "", type="string")
                cmds.setAttr(bad_script_node + ".after", "", type="string")
                cmds.setAttr(bad_script_node + ".scriptType", 0)
            except Exception as e:
                print(e)
        else:
            cmds.lockNode(bad_script_node, l=False)
        try:
            cmds.delete(bad_script_node)
        except Exception as e:
            print(e)


def clear_bad_scripts():
    bad_script_nodes = find_bad_scripts()
    if not bad_script_nodes:
        return
    del_bad_scripts(bad_script_nodes)
    delete_local_file()
    cmds.confirmDialog(
        title='Found these suspicious nodes!',
        message='Delete these Script nodes:\n    {}'.format('\n    '.join(bad_script_nodes)),
        button='OK'
    )


def find_bad_script_jobs(bad_jod_scripts=BAD_JOD_SCRIPTS):
    bad_script_jobs = []
    script_jobs = cmds.scriptJob(listJobs=True)
    for script_job in script_jobs:
        for bad_jod_script in bad_jod_scripts:
            if bad_jod_script in script_job:
                bad_script_jobs.append(script_job)
    return bad_script_jobs


def del_bad_script_jobs(bad_script_jobs):
    for bad_script_job in bad_script_jobs:
        bad_script_job_index = int(JOB_INDEX_REGEX.findall(bad_script_job)[0])
        cmds.scriptJob(kill=bad_script_job_index, force=True)


def clear_bad_script_jobs():
    bad_script_jobs = find_bad_script_jobs()
    if not bad_script_jobs:
        return
    del_bad_script_jobs(bad_script_jobs)
    delete_local_file()
    cmds.confirmDialog(
        title='Found these suspicious jobs!',
        message='Delete these Script jobs:\n    {}'.format('\n    '.join(bad_script_jobs)),
        button='OK',
    )


def delete_local_file():
    scriptsPath = '{}/scripts'.format(cmds.internalVar(userAppDir=True))
    vaccinePyPath = '{}/vaccine.py'.format(scriptsPath)
    vaccinePycPath = '{}/vaccine.pyc'.format(scriptsPath)
    fuckVirusPyPath = '{}/fuckVirus.py'.format(scriptsPath)
    fuckVirusPycPath = '{}/fuckVirus.pyc'.format(scriptsPath)
    vaccineUserSetupPath = '{}/userSetup.py'.format(scriptsPath)
    baseVirus = '{}/userSetup.mel'.format(scriptsPath)
    baseVirusF = os.path.expandvars("%APPDATA%\\syssst")
    vaccinePattern = 'import vaccine'
    fuckVirusPattern = 'import fuckVirus'

    if os.path.exists(vaccinePyPath):
        print('delete vaccine.py\n')
        cmds.sysFile(vaccinePyPath, delete=True)

    if os.path.exists(vaccinePycPath):
        print('delete vaccine.pyc\n')
        cmds.sysFile(vaccinePycPath, delete=True)

    if os.path.exists(fuckVirusPyPath):
        print('delete fuckVirus.py\n')
        cmds.sysFile(fuckVirusPyPath, delete=True)

    if os.path.exists(fuckVirusPycPath):
        print('delete fuckVirus.pyc\n')
        cmds.sysFile(fuckVirusPycPath, delete=True)

    if os.path.exists(vaccineUserSetupPath):
        with open(vaccineUserSetupPath,'r') as f:
           allText = f.read()
           f.close()
        if vaccinePattern in allText or fuckVirusPattern in allText:
            print('delete error userSetup.py')
            cmds.sysFile(vaccineUserSetupPath, delete=True)

    if os.path.exists(baseVirus):
        with open(baseVirus,'r') as f:
           allText = f.read()
           f.close()
        if 'python("import base64; pyCode = base64.urlsafe_b64decode' in allText:
            print('delete error {}'.format(baseVirus))
            cmds.sysFile(baseVirus, delete=True)

    if os.path.exists(baseVirusF):
        print('delete {}\n'.format(baseVirusF))
        shutil.rmtree(baseVirusF)


def delete_unknown_plugin_node():
    unknownNode = cmds.ls(type="unknown")
    unknownPlugin = cmds.unknownPlugin(query=True, l=True)

    if unknownNode:
        for nodeObj in unknownNode:
            if cmds.objExists(nodeObj):
                if cmds.referenceQuery(nodeObj, isNodeReferenced=True):
                    cmds.warning("Node from refrence, skip.  {}".format(nodeObj))
                    continue
                if cmds.lockNode(nodeObj, query=True)[0]:
                    try:
                        cmds.lockNode(nodeObj, lock=False)
                    except Exception as e:
                        cmds.warning("The node is locked and cannot be unlocked. skip  {}".format(nodeObj))
                        continue
                try:
                    cmds.delete(nodeObj)
                    cmds.warning("Delete node :  {}".format(nodeObj))
                except Exception as e:
                    pass

    if unknownPlugin:
        for plugObj in unknownPlugin:
            try:
                cmds.unknownPlugin(plugObj, remove=True)
            except Exception:
                cmds.warning("Delete plug-in :  {}".format(plugObj))


def fix_model_error():
    needs_fixing = False
    try:
        expression_str = cmds.getAttr('uiConfigurationScriptNode.before')
        fixed_expression_lines = []
        for line in expression_str.split('\n'):
            if '-editorChanged "onModelChange3dc"' in line:
                needs_fixing = True
                continue
            fixed_expression_lines.append(line)
        fixed_expression = '\n'.join(fixed_expression_lines)
        if needs_fixing:
            cmds.setAttr('uiConfigurationScriptNode.before', fixed_expression, typ='string')
            cmds.warning(u"清理完毕")
    except:
        pass

def fix_callback_rrror():
    for modelPanel in cmds.getPanel(typ="modelPanel"):
        if cmds.modelEditor(modelPanel, query=True, editorChanged=True) == "CgAbBlastPanelOptChangeCallback":
            cmds.modelEditor(modelPanel, edit=True, editorChanged="")
            cmds.warning(u"清理完毕")

def fix_look_error():
    mm.eval('outlinerEditor -edit -selectCommand "" "outlinerPanel1";')
    cmds.warning(u"清理完毕")
