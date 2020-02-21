import bpy
from . properties import NTZQSUBD_ignitproperties

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def neltulz_subd_register_keymaps(addon_keymaps):

    wm = bpy.context.window_manager

    def createSubD_mode_keymaps():
        #Setup keymaps for Mode Switching (1, 2, 3)
        keymapConfig = [
            #type       subdMode
            ("ONE",     1           ),
            ("TWO",     2           ),
            ("THREE",   3           )
        ]

        for keymap in keymapConfig:
            kmi = km.keymap_items.new("ntzqcksubd.setsubdmode", type=keymap[0], ctrl=False, shift=False, alt=False, value = "PRESS")
            kmi.properties.subdMode = keymap[1]



    #------------------------------ 3D View Generic ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="3D View Generic", space_type="VIEW_3D")

    #Setup keymaps for Relative changing using "Page Up" and "Page Down" keys
    keymapConfig = [
        #type               oskey   decreaseLevel
        ("PAGE_UP",         False,  False           ),
        ("PAGE_DOWN",       False,  True            ),
        ("WHEELUPMOUSE",    True,   False           ),
        ("WHEELDOWNMOUSE",  True,   True            )
    ]

    for keymap in keymapConfig:

        kmi = km.keymap_items.new("ntzqcksubd.relativelevelchange", type=keymap[0], ctrl=False, shift=False, alt=False, oskey=keymap[1], value = "PRESS")
        kmi.properties.decrease = keymap[2]


    #Setup keymaps for Specific Level Change (1-0)

    keymapConfig = [
        #type       specificLevel
        ("ONE",     1               ),
        ("TWO",     2               ),
        ("THREE",   3               ),
        ("FOUR",    4               ),
        ("FIVE",    5               ),
        ("SIX",     6               ),
        ("SEVEN",   7               ),
        ("EIGHT",   8               ),
        ("NINE",    9               ),
        ("ZERO",    0               ),
    ]

    for keymap in keymapConfig:

        kmi = km.keymap_items.new("ntzqcksubd.specificlevelchange", type=keymap[0], ctrl=True, shift=False, alt=False, value = "PRESS")
        kmi.properties.useShortcutKeySpecificLevel = True
        kmi.properties.shortcutKeySpecificLevel = keymap[1]

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Object Mode  ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")

    createSubD_mode_keymaps()

    #kmi = km.keymap_items.new("ntzqcksubd.togglesubdmode", type="FOUR", ctrl=False, shift=False, alt=False, oskey=False, value = "PRESS")

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Edit Mode  ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Mesh", space_type="EMPTY")

    createSubD_mode_keymaps()

    #kmi = km.keymap_items.new("ntzqcksubd.togglesubdmode", type="FOUR", ctrl=False, shift=False, alt=False, oskey=False, value = "PRESS")
    
    #add list of keymaps
    addon_keymaps.append(km)


def neltulz_subd_unregister_keymaps(addon_keymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()