import bpy
from . properties import NTZQSUBD_ignitproperties
from . import misc_functions
from . import misc_layout

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class NTZQSUBD_PT_changesubdlevel(Panel):
    bl_label = "Quick SubD - Change SubD Level"
    bl_idname = "NTZQSUBD_PT_changesubdlevel"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 13

        selObjs    = bpy.context.selected_objects
        numSelObjs = len(selObjs)
        activeObj  = bpy.context.view_layer.objects.active

        try:    neltulzSubD_modifier = activeObj.modifiers["Neltulz - Quick SubD"]
        except: neltulzSubD_modifier = None

        subdLevelSection = layout.column(align=True)

        misc_layout.changeSubDLevel_SectionInner(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, False, False, subdLevelSection)

    #END draw()

class NTZQSUBD_PT_options(Panel):
    bl_label = "Quick SubD - Options"
    bl_idname = "NTZQSUBD_PT_options"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 13

        selObjs    = bpy.context.selected_objects
        numSelObjs = len(selObjs)
        activeObj  = bpy.context.view_layer.objects.active

        try:    neltulzSubD_modifier = activeObj.modifiers["Neltulz - Quick SubD"]
        except: neltulzSubD_modifier = None

        optionsSection = layout.column(align=True)

        misc_layout.options_SectionInner(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, False, False, optionsSection)

    #END draw()

class NTZQSUBD_PT_sidebarpanel(Panel):

    bl_label = "Quick SubD v1.0.6"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bUseCompactSidebarPanel = BoolProperty(
        name="Use Compact Panel",
        description="Use Compact Panel",
        default = False
    )

    bUseCompactPopupAndPiePanel = BoolProperty(
        name="Use Compact Popup & Pie Panel",
        description="Use Compact Popup & Pie Panel",
        default = True
    )

    def draw(self, context):

        misc_layout.mainQuickSubDPanel(self, context, self.bUseCompactSidebarPanel, self.bUseCompactPopupAndPiePanel)
