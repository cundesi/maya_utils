#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import maya.cmds as cmds
import maya.mel as mm

# Regular expressions and bad script patterns
JOB_INDEX_REGEX = re.compile(r'^(\d+):')
BAD_SCRIPT_PATTERNS = [
    'internalVar', 'userSetup', 'fuckVirus', 
    'python("import base64; _pycode = base64.urlsafe_b64decode'
]
BAD_JOB_SCRIPTS = ['leukocyte.antivirus()']

# Cleanup configuration
SCRIPTS_PATH = os.path.join(cmds.internalVar(userAppDir=True), 'scripts')
BAD_FILE_PATHS = [
    'vaccine.py', 'vaccine.pyc', 'fuckVirus.py', 'fuckVirus.pyc',
    'userSetup.py', 'userSetup.mel'
]
BAD_FILE_PATTERNS = ['import vaccine', 'import fuckVirus', 'python("import base64; pyCode = base64.urlsafe_b64decode']

def find_bad_script_nodes():
    bad_script_nodes = []
    for node in cmds.ls(type='script'):
        for attr in ['before', 'after']:
            script_content = cmds.getAttr('.'.join([node, attr]))
            if any(pattern in script_content for pattern in BAD_SCRIPT_PATTERNS):
                bad_script_nodes.append(node)
    return bad_script_nodes

def delete_bad_script_nodes(bad_script_nodes):
    for node in bad_script_nodes:
        if cmds.referenceQuery(node, isNodeReferenced=True):
            cmds.setAttr('.'.join([node, "before"]), "", type="string")
            cmds.setAttr('.'.join([node, "after"]), "", type="string")
            cmds.setAttr('.'.join([node, "scriptType"]), 0)
        else:
            cmds.lockNode(node, lock=False)
        cmds.delete(node)

def clear_bad_scripts():
    bad_script_nodes = find_bad_script_nodes()
    delete_bad_script_nodes(bad_script_nodes)

def find_bad_script_jobs():
    return [
        job
        for job in cmds.scriptJob(listJobs=True)
        if any(bad_script in job for bad_script in BAD_JOB_SCRIPTS)
    ]

def delete_bad_script_jobs(bad_script_jobs):
    for job in bad_script_jobs:
        job_index = int(JOB_INDEX_REGEX.findall(job)[0])
        cmds.scriptJob(kill=job_index, force=True)

def clear_bad_script_jobs():
    bad_script_jobs = find_bad_script_jobs()
    delete_bad_script_jobs(bad_script_jobs)

def delete_local_files():
    for file_name in BAD_FILE_PATHS:
        file_path = os.path.join(SCRIPTS_PATH, file_name)
        if os.path.exists(file_path):
            if file_name.endswith('.py') or file_name.endswith('.mel'):
                with open(file_path, 'r') as file:
                    content = file.read()
                if any(pattern in content for pattern in BAD_FILE_PATTERNS):
                    cmds.sysFile(file_path, delete=True)
            else:
                cmds.sysFile(file_path, delete=True)

def delete_unknown_plugin_nodes():
    for node in cmds.ls(type="unknown"):
        if cmds.objExists(node) and not cmds.referenceQuery(node, isNodeReferenced=True) and not cmds.lockNode(node, query=True):
            cmds.delete(node)
    for plugin in cmds.unknownPlugin(query=True, list=True) or []:
        cmds.unknownPlugin(plugin, remove=True)

def fix_model_error():
    node = 'uiConfigurationScriptNode'
    if cmds.objExists(node):
        expression_str = cmds.getAttr('.'.join([node, "before"]))
        if '-editorChanged "onModelChange3dc"' in expression_str:
            fixed_expression = '\n'.join(line for line in expression_str.split('\n') if '-editorChanged "onModelChange3dc"' not in line)
            cmds.setAttr('.'.join([node, "before"]), fixed_expression, type='string')

def fix_callback_error():
    for model_panel in cmds.getPanel(type="modelPanel"):
        if cmds.modelEditor(model_panel, query=True, editorChanged=True) == "CgAbBlastPanelOptChangeCallback":
            cmds.modelEditor(model_panel, edit=True, editorChanged="")

def fix_look_error():
    mm.eval('outlinerEditor -edit -selectCommand "" "outlinerPanel1";')