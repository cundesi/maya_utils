#!/usr/bin/env python
# -*- coding: utf-8 -*-

import callback
import maya.api.OpenMaya as omapi


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


def after_open_callback(*args):
    callback.clear_bad_scripts()


def before_save_callback(*args):
    callback.clear_bad_script_jobs()


def remove_scene_callback():
    if callback.AFTER_OPEN_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(callback.AFTER_OPEN_CALLBACK_ID)
        callback.AFTER_OPEN_CALLBACK_ID = None

    if callback.BEFORE_SAVE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(callback.BEFORE_SAVE_CALLBACK_ID)
        callback.BEFORE_SAVE_CALLBACK_ID = None


def add_scene_callback():
    remove_scene_callback()
    callback.AFTER_OPEN_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kAfterOpen, after_open_callback
    )
    callback.BEFORE_SAVE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kBeforeSave, before_save_callback
    )


def initializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject, 'scene_callback', '1.0', 'panyu')
    add_scene_callback()


def uninitializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject)
    remove_scene_callback()
