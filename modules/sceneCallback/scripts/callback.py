#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import maya.cmds as cmds

JOB_INDEX_REGEX = re.compile(r'^(\d+):')

BAD_JOD_SCRIPTS = ['leukocyte.antivirus()']

AFTER_OPEN_CALLBACK_ID = None
BEFORE_SAVE_CALLBACK_ID = None


def find_bad_scripts():
    bad_script_nodes = []
    script_nodes = cmds.ls(type='script')
    for script_node in script_nodes:
        if cmds.referenceQuery(script_node, isNodeReferenced=True):
            continue
        script_before_string = cmds.getAttr('{}.before'.format(script_node))
        script_after_string = cmds.getAttr('{}.after'.format(script_node))
        for script_string in [script_before_string, script_after_string]:
            if not script_string:
                continue
            if 'internalVar' in script_string or 'userSetup' in script_string:
                bad_script_nodes.append(script_node)
    return bad_script_nodes


def del_bad_scripts(bad_script_nodes):
    for bad_script_node in bad_script_nodes:
        cmds.lockNode(bad_script_node, l=False)
        cmds.delete(bad_script_node)


def clear_bad_scripts():
    bad_script_nodes = find_bad_scripts()
    if not bad_script_nodes:
        return
    reply = cmds.confirmDialog(
        title='Found these suspicious nodes!',
        message='Delete these Script nodes:\n    {}'.format('\n    '.join(bad_script_nodes)),
        button=['Yes', 'No'],
        defaultButton='Yes',
        cancelButton='No',
        dismissString='No')
    if reply == 'Yes':
        del_bad_scripts(bad_script_nodes)


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
    reply = cmds.confirmDialog(
        title='Found these suspicious jobs!',
        message='Delete these Script jobs:\n    {}'.format('\n    '.join(bad_script_jobs)),
        button=['Yes', 'No'],
        defaultButton='Yes',
        cancelButton='No',
        dismissString='No')
    if reply == 'Yes':
        del_bad_script_jobs(bad_script_jobs)
