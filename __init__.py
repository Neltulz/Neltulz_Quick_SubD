bl_info = {
    "name" : "Neltulz - Quick SubD",
    "author" : "Neil V. Moore",
    "description" : 'Quickly subdivide mesh with preset keymaps, picks best normal shading, supports multiple modes (Off, On, and On+), supports "Relative" and "Specific" Level Changing',
    "blender" : (2, 80, 0),
    "version" : (1, 0, 7),
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

from . properties                   import NTZQSUBD_ignitproperties
from . misc_ot                      import NTZQSUBD_OT_subdwireframe
from . misc_ot                      import NTZQSUBD_OT_updatealladvancedsettings
from . misc_ot                      import NTZQSUBD_OT_applymodifier
from . misc_ot                      import NTZQSUBD_OT_delmodifier
from . misc_ot                      import NTZQSUBD_OT_resetallsettings
from . main_ot                      import NTZQSUBD_OT_setsubdmode
from . relative_level_change        import NTZQSUBD_OT_relativelevelchange
from . specific_level_change        import NTZQSUBD_OT_specificlevelchange
from . addonPrefs                   import NTZQSUBD_OT_ntzaddonprefs
from . panels                       import NTZQSUBD_PT_changesubdlevel
from . panels                       import NTZQSUBD_PT_options
from . panels                       import NTZQSUBD_PT_sidebarpanel


from . import keymaps

PendingDeprecationWarning

bDebugModeActive = True
if bDebugModeActive:
    print("##################################################################################################################################################################")
    print("REMINDER: DEBUG MODE ACTIVE")
    print("##################################################################################################################################################################")

# -----------------------------------------------------------------------------
#    Store classes in List so that they can be easily registered/unregistered    
# -----------------------------------------------------------------------------  

classes = (
    NTZQSUBD_ignitproperties,
    NTZQSUBD_OT_subdwireframe,
    NTZQSUBD_OT_updatealladvancedsettings,
    NTZQSUBD_OT_applymodifier,
    NTZQSUBD_OT_delmodifier,
    NTZQSUBD_OT_resetallsettings,
    NTZQSUBD_OT_setsubdmode,
    NTZQSUBD_OT_relativelevelchange,
    NTZQSUBD_OT_specificlevelchange,
    NTZQSUBD_OT_ntzaddonprefs,
    NTZQSUBD_PT_changesubdlevel,
    NTZQSUBD_PT_options,
    NTZQSUBD_PT_sidebarpanel,
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addon_keymaps = []

#vscode pme workaround from iceythe (part 1 of 2)
def _reg():
    pme = bpy.utils._preferences.addons['pie_menu_editor'].preferences
    for pm in pme.pie_menus:
        if pm.key != 'NONE':
            pm.register_hotkey()
#END vscode pme workaround (part 1 of 2)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # update panel name
    prefs = bpy.context.preferences.addons[__name__].preferences
    addonPrefs.update_panel(prefs, bpy.context)

    #add keymaps from keymaps.py
    keymaps.neltulz_subd_register_keymaps(addon_keymaps)

    #add property group to the scene
    bpy.types.Scene.neltulzSubD = bpy.props.PointerProperty(type=NTZQSUBD_ignitproperties)

    #vscode pme workaround from iceythe (part 2 of 2)
    #must be appended to def register() so that it is the last thing that executes
    if bDebugModeActive:
        if not bpy.app.timers.is_registered(_reg):
            bpy.app.timers.register(_reg, first_interval=1)
    #END vscode pme workaround (part 2 of 2)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.neltulz_subd_unregister_keymaps(addon_keymaps)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.ntzqcksubd.setsubdmode()