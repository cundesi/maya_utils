#!/usr/bin/env python
# -*- coding: utf-8 -*-

import maya_cleanup
import maya.api.OpenMaya as omapi

def maya_useNewAPI():
    """
    Indicates the plugin uses the Maya Python API 2.0.
    """
    pass

def after_open_callback(*args):
    maya_cleanup.delete_unknown_plugin_node()
    maya_cleanup.clear_bad_scripts()

def before_save_callback(*args):
    maya_cleanup.clear_bad_script_jobs()

def remove_scene_callback():
    callback_ids = [
        'AFTER_OPEN_CALLBACK_ID', 'BEFORE_SAVE_CALLBACK_ID',
        'AFTER_REFERENCE_CALLBACK_ID', 'BEFORE_REMOVE_REFERENCE_CALLBACK_ID',
        'AFTER_IMPORT_REFERENCE_CALLBACK_ID', 'BEFORE_EXPORT_REFERENCE_CALLBACK_ID',
        'BEFORE_UNLOAD_REFERENCE_CALLBACK_ID', 'AFTER_IMPORT_CALLBACK_ID',
        'BEFORE_EXPORT_CALLBACK_ID'
    ]
    for id_name in callback_ids:
        callback_id = getattr(maya_cleanup, id_name, None)
        if callback_id:
            omapi.MSceneMessage.removeCallback(callback_id)
            setattr(maya_cleanup, id_name, None)

def add_scene_callback():
    remove_scene_callback()
    events = {
        'kAfterOpen': after_open_callback,
        'kBeforeSave': before_save_callback,
        'kAfterReference': after_open_callback,
        'kBeforeRemoveReference': before_save_callback,
        'kAfterImportReference': after_open_callback,
        'kBeforeExportReference': before_save_callback,
        'kBeforeUnloadReference': before_save_callback,
        'kAfterImport': after_open_callback,
        'kBeforeExport': before_save_callback
    }
    for event, callback in events.items():
        id_name = event.upper() + '_CALLBACK_ID'
        callback_id = omapi.MSceneMessage.addCallback(getattr(omapi.MSceneMessage, event), callback)
        setattr(maya_cleanup, id_name, callback_id)

def initializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject, 'maya_cleanuper', '1.2', 'panyu&andy, fix&append: wuxiaomeng')
    add_scene_callback()

def uninitializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject)
    remove_scene_callback()
