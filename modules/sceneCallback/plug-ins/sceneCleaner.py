#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sceneClean
import maya.api.OpenMaya as omapi


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


def after_open_callback(*args):
    sceneClean.delete_unknown_plugin_node()
    sceneClean.clear_bad_scripts()


def before_save_callback(*args):
    sceneClean.clear_bad_script_jobs()


def remove_scene_callback():
    if sceneClean.AFTER_OPEN_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.AFTER_OPEN_CALLBACK_ID)
        sceneClean.AFTER_OPEN_CALLBACK_ID = None

    if sceneClean.BEFORE_SAVE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.BEFORE_SAVE_CALLBACK_ID)
        sceneClean.BEFORE_SAVE_CALLBACK_ID = None
    
    if sceneClean.AFTER_REFERENCE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.AFTER_REFERENCE_CALLBACK_ID)
        sceneClean.AFTER_REFERENCE_CALLBACK_ID = None

    if sceneClean.BEFORE_REMOVE_REFERENCE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.BEFORE_REMOVE_REFERENCE_CALLBACK_ID)
        sceneClean.BEFORE_REMOVE_REFERENCE_CALLBACK_ID = None

    if sceneClean.AFTER_IMPORT_REFERENCE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.AFTER_IMPORT_REFERENCE_CALLBACK_ID)
        sceneClean.AFTER_IMPORT_REFERENCE_CALLBACK_ID = None

    if sceneClean.BEFORE_EXPORT_REFERENCE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.BEFORE_EXPORT_REFERENCE_CALLBACK_ID)
        sceneClean.BEFORE_EXPORT_REFERENCE_CALLBACK_ID = None
    
    if sceneClean.BEFORE_UNLOAD_REFERENCE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.BEFORE_UNLOAD_REFERENCE_CALLBACK_ID)
        sceneClean.BEFORE_UNLOAD_REFERENCE_CALLBACK_ID = None
    
    if sceneClean.AFTER_IMPORT_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.AFTER_IMPORT_CALLBACK_ID)
        sceneClean.AFTER_IMPORT_CALLBACK_ID = None
    
    if sceneClean.BEFORE_EXPORT_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.BEFORE_EXPORT_CALLBACK_ID)
        sceneClean.BEFORE_EXPORT_CALLBACK_ID = None


def add_scene_callback():
    remove_scene_callback()
    sceneClean.AFTER_OPEN_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kAfterOpen, after_open_callback
    )
    sceneClean.BEFORE_SAVE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kBeforeSave, before_save_callback
    )
    sceneClean.AFTER_REFERENCE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kAfterReference, after_open_callback
    )
    sceneClean.BEFORE_REMOVE_REFERENCE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kBeforeRemoveReference, before_save_callback
    )
    sceneClean.AFTER_IMPORT_REFERENCE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kAfterImportReference, after_open_callback
    )
    sceneClean.BEFORE_EXPORT_REFERENCE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kBeforeExportReference, before_save_callback
    )
    sceneClean.BEFORE_UNLOAD_REFERENCE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kBeforeUnloadReference, before_save_callback
    )
    sceneClean.AFTER_IMPORT_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kAfterImport, after_open_callback
    )
    sceneClean.BEFORE_EXPORT_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kBeforeExport, before_save_callback
    )


def initializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject, 'sceneCleanner', '1.2', 'panyu&andy, fix&append: wuxiaomeng')
    add_scene_callback()


def uninitializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject)
    remove_scene_callback()
