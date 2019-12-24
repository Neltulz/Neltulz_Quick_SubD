import bpy
from . properties import NeltulzSubD_IgnitProperties

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def neltulz_subd_register_keymaps(addon_keymaps):

    wm = bpy.context.window_manager

    def createSubD_mode_hotkeys():
        #Setup Hotkeys for Mode Switching (1, 2, 3)
        keymapConfig = [("ONE", 1), ("TWO", 2), ("THREE", 3)]

        for keymap in keymapConfig:
            kmi = km.keymap_items.new("ntz_qck_subd.subdivide_obj", type = keymap[0], ctrl=False, shift=False, alt=False, value = "PRESS")
            kmi.properties.subdMode = keymap[1]

    def createRelativeSpecific_mode_hotkeys():
        #Setup Hotkeys for Relative / Specific changing
        keymapConfig = [("PAGE_UP", False), ("PAGE_DOWN", True)]

        for keymap in keymapConfig:
            kmi = km.keymap_items.new("ntz_qck_subd.relativelevelchange", type = keymap[0], ctrl=False, shift=False, alt=False, value = "PRESS")
            kmi.properties.decrease = keymap[1]

    def createSpecificLevelChange_hotkeys():
        #Setup Hotkeys for Specific Level Change (1-0)
        keymapConfig =  [   ("ONE",     1),
                            ("TWO",     2),
                            ("THREE",   3),
                            ("FOUR",    4),
                            ("FIVE",    5),
                            ("SIX",     6),
                            ("SEVEN",   7),
                            ("EIGHT",   8),
                            ("NINE",    9),
                            ("ZERO",    0)
                        ]

        for keymap in keymapConfig:
            kmi = km.keymap_items.new("ntz_qck_subd.specificlevelchange", type = keymap[0], ctrl=True, shift=False, alt=False, value = "PRESS")
            kmi.properties.useShortcutKeySpecificLevel = True
            kmi.properties.shortcutKeySpecificLevel = keymap[1]

    #------------------------------Object Mode----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")

    createSubD_mode_hotkeys()
    createRelativeSpecific_mode_hotkeys()
    createSpecificLevelChange_hotkeys()

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------Mesh Mode----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name = "Mesh", space_type="EMPTY")

    createSubD_mode_hotkeys()
    createRelativeSpecific_mode_hotkeys()
    createSpecificLevelChange_hotkeys()


    #add list of keymaps
    addon_keymaps.append(km)

def neltulz_subd_unregister_keymaps(addon_keymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()