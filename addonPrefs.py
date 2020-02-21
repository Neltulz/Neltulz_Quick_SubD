# Update "Tab Category Name" inspired by "Meta-Androcto's" "Edit Mesh Tools" Add-on
# recommended by "cytoo"

import bpy
from . panels import NTZQSUBD_PT_sidebarpanel

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# Define Panel classes for updating
panels = (
        NTZQSUBD_PT_sidebarpanel,
        )

        

def update_panel(self, context):

    sidebarPanelSize_PropVal        = context.preferences.addons[__package__].preferences.sidebarPanelSize
    category_PropVal                = context.preferences.addons[__package__].preferences.category
    popupAndPiePanelSize_PropVal    = context.preferences.addons[__package__].preferences.popupAndPiePanelSize

    message = "Neltulz QuickSubD: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        #Whatever the user typed into the text box in the add-ons settings, set that as the addon's tab category name
        for panel in panels:
            

            if sidebarPanelSize_PropVal == "HIDE":
                panel.bl_category = ""
                panel.bl_region_type = "WINDOW"

            else:
                if self.sidebarPanelSize == "DEFAULT":
                    panel.bUseCompactSidebarPanel = False
                else:
                    panel.bUseCompactSidebarPanel = True

                panel.bl_category = category_PropVal
                panel.bl_region_type = "UI"

            if self.popupAndPiePanelSize == "DEFAULT":
                panel.bUseCompactPopupAndPiePanel = False
            else:
                panel.bUseCompactPopupAndPiePanel = True

            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__package__, message, e))
        pass


class NTZQSUBD_OT_ntzaddonprefs(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    
    navTabs_List = [
        ("UILAY",      "UI Layout",  "", "", 0),
        ("SUBD",       "SubD",       "", "", 1),
    ]

    navTabs : EnumProperty (
        items       = navTabs_List,
        name        = "Navigation Tabs",
        default     = "UILAY"
    )

    category: StringProperty(
        name="Tab Category",
        description="Choose a name for the category of the panel",
        default="Neltulz",
        update=update_panel,
    )
        
    sidebarpanelSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        ("COMPACT", "Compact", "", "", 1),
        ("HIDE",    "Hide",    "", "", 2),
    ]

    popupAndPiePanelSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        ("COMPACT", "Compact", "", "", 1),
    ]

    sidebarPanelSize : EnumProperty (
        items       = sidebarpanelSize_List,
        name        = "Sidebar Panel Size",
        description = "Sidebar Panel Size",
        default     = "DEFAULT",
        update=update_panel,
    )

    popupAndPiePanelSize : EnumProperty (
        items       = popupAndPiePanelSize_List,
        name        = "Popup & Pie Panel Size",
        description = "Popup & Pie Panel Size",
        default     = "COMPACT",

        update=update_panel,
    )

    toggleSubDModes : BoolProperty (
        name                = 'Toggle SubD',
        description         = 'Toggle the SubD Modes instead of setting them',
        default             =  False
    )

    subdModePreference_List = [
        ("ON",      "2 (On)",  "", "", 0),
        ("ONPLUS", "3 (On+)", "", "", 1),
    ]

    subdModePreference : EnumProperty (
        items       = subdModePreference_List,
        name        = "SubD Mode Preference",
        description = 'Which "On" method you prefer?',
        default     = "ONPLUS"
    )

    initialSubDLevel : IntProperty(
        name="",
        description="Initial SubD Level when enabling subdivision modifier",
        default = 1,
        min = 1,
        max = 11,
        soft_max = 5,
    )




    def draw(self, context):

        from . misc_layout import createProp
        layout = self.layout

        labelWidth = 8
        labelJustify = "RIGHT"
        propJustify = "LEFT"
        propWidth = 15
        propHeight = 1.25

        if self.sidebarPanelSize == "HIDE":
            bTabCatEnabled = False
        else:
            bTabCatEnabled = True

        navRow = layout.row(align=True)
        navRow.prop(self, 'navTabs', expand=True)


        if self.navTabs == "UILAY":
        
            createProp(self, context, None, True,           "Sidebar Panel",         "sidebarPanelSize",     propHeight, labelWidth, propWidth, labelJustify, propJustify, None,  True, layout)
            createProp(self, context, None, bTabCatEnabled, "Tab Category",          "category",             propHeight, labelWidth, propWidth, labelJustify, propJustify, "",    True, layout)
            createProp(self, context, None, True,           "Popup & Pie Panel",     "popupAndPiePanelSize", propHeight, labelWidth, propWidth, labelJustify, propJustify, None,  True, layout)

        elif self.navTabs == "SUBD":

            createProp(self, context, None, True,           "SubD Mode Preference",  "subdModePreference",   1, labelWidth, propWidth, labelJustify, propJustify, None,  True, layout)
            createProp(self, context, None, True,           "",                      "toggleSubDModes",      1, labelWidth, propWidth, labelJustify, propJustify, None,  True, layout)
            createProp(self, context, None, True,           "Initial SubD Level",    "initialSubDLevel",     1, labelWidth, propWidth, labelJustify, propJustify, None,  True, layout)