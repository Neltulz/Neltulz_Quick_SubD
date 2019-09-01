bl_info = {
    "name" : "Neltulz - Quick SubD",
    "author" : "Neil V. Moore",
    "description" : 'Quickly subdivide mesh with preset hotkeys, picks best normal shading, supports multiple modes (Off, On, and On+), supports "Relative" and "Specific" Level Changing',
    "blender" : (2, 80, 0),
    "version" : (1, 0, 3),
    "location" : "View3D",
    "warning" : "",
    "category" : "3D View",
    "tracker_url": "mailto:neilvmoore@gmail.com",
    "wiki_url": "https://www.logichaos.com/neltulz_blender_addons/neltulz_quick_subd_readme/README_Neltulz_Quick_SubD.html"
}

# -----------------------------------------------------------------------------
#   Import Classes and/or functions     
# -----------------------------------------------------------------------------  

import bpy

from . properties import NeltulzSubD_IgnitProperties
from . misc_ot import OBJECT_OT_NeltulzSubD_SubDWireframe
from . misc_ot import OBJECT_OT_NeltulzSubD_UpdateAllAdvancedSettings
from . misc_ot import OBJECT_OT_NeltulzSubD_ApplyModifier
from . misc_ot import OBJECT_OT_NeltulzSubD_DeleteModifier
from . misc_ot import OBJECT_OT_NeltulzSubD_ResetAllSettings
from . main_ot import OBJECT_OT_NeltulzSubD
from . relative_level_change import OBJECT_OT_NeltulzSubD_Relative_LevelChange
from . specific_level_change import OBJECT_OT_NeltulzSubD_Specific_LevelChange
from . addon_preferences import OBJECT_OT_NeltulzSubD_Preferences
from . panels import OBJECT_PT_NeltulzSubD


from . import keymaps

PendingDeprecationWarning


# -----------------------------------------------------------------------------
#    Store classes in List so that they can be easily registered/unregistered    
# -----------------------------------------------------------------------------  

classes = (
    NeltulzSubD_IgnitProperties,
    OBJECT_OT_NeltulzSubD_SubDWireframe,
    OBJECT_OT_NeltulzSubD_UpdateAllAdvancedSettings,
    OBJECT_OT_NeltulzSubD_ApplyModifier,
    OBJECT_OT_NeltulzSubD_DeleteModifier,
    OBJECT_OT_NeltulzSubD_ResetAllSettings,
    OBJECT_OT_NeltulzSubD,
    OBJECT_OT_NeltulzSubD_Relative_LevelChange,
    OBJECT_OT_NeltulzSubD_Specific_LevelChange,
    OBJECT_OT_NeltulzSubD_Preferences,
    OBJECT_PT_NeltulzSubD,
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addon_keymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # update panel name
    addon_preferences.update_panel(None, bpy.context)

    #add keymaps from keymaps.py
    keymaps.neltulz_subd_register_keymaps(addon_keymaps)

    #add property group to the scene
    bpy.types.Scene.neltulzSubD = bpy.props.PointerProperty(type=NeltulzSubD_IgnitProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.neltulz_subd_unregister_keymaps(addon_keymaps)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.neltulz_subd()