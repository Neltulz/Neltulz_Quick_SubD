import bpy
from . properties import NeltulzSubD_IgnitProperties
from . import misc_functions

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class OBJECT_PT_NeltulzSubD(Panel):

    bl_idname = "object.neltulz_subd_panel"
    bl_label = "Quick SubD v1.0.3"
    bl_category = "Quick SubD"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    



    def draw(self, context):

        layout = self.layout
        scene = context.scene




        col = layout.column(align=True)
        col.label(text="Subdivision Mode:")
        row = col.row(align=True)


        op = row.operator('object.neltulz_subd', text="1 (Off)")
        op.subdMode=1

        op = row.operator('object.neltulz_subd', text="2 (On)")
        op.subdMode=2

        op = row.operator('object.neltulz_subd', text="3. (On+)")
        op.subdMode=3

        col = layout.column(align=True)
        col.label(text="Subdivision Level:")
        row = col.row(align=True)

        
        row = col.row(align=True)
        row.prop(context.scene.neltulzSubD, "changeMethod", expand=True)


        col = layout.column(align=True)

        if scene.neltulzSubD.changeMethod == "1":
            row = col.row(align=True)
            op = row.operator('object.neltulz_subd_relative_level_change', text="-")
            op.decrease=True

            op = row.operator('object.neltulz_subd_relative_level_change', text="+")
            op.decrease=False
        else:
            row = col.row(align=True)
            row.prop(context.scene.neltulzSubD, "specificSubDLevel", text="")
            op = row.operator('object.neltulz_subd_specific_level_change', text="Set")


        col = layout.column(align=True)

        col.prop(context.scene.neltulzSubD, "toggleOverlayOptionsBool", text="Toggle Overlay Options")
        
        # -----------------------------------------------------------------------------
        #   Overlay Options (Wireframe, Edge colors, etc)
        # -----------------------------------------------------------------------------

        if scene.neltulzSubD.toggleOverlayOptionsBool is True:

            boxOverlayOptions = layout.box()

            col = boxOverlayOptions.column(align=True)
            col.label(text="Wireframe:")

            row = col.row(align=True)

            row.prop(context.space_data.overlay, "show_wireframes", text="Toggle Wireframe", toggle=True)

            col = boxOverlayOptions.column(align=True)
            col.label(text="SubD Wireframe:")
            row = col.row(align=True)
            op = row.operator('object.neltulz_subd_toggle_wireframe', text="ON")
            op.subDWireframeOn=True

            op = row.operator('object.neltulz_subd_toggle_wireframe', text="OFF")
            op.subDWireframeOn=False
            
            col.separator()

            col = boxOverlayOptions.column(align=True)
            col.label(text="Edge Colors:")
            row = col.row(align=True)
            row.prop(context.scene.neltulzSubD, "enableAllEdgeColorsBool", text="Enable All", toggle=True)
            row.prop(context.scene.neltulzSubD, "disableAllEdgeColorsBool", text="Disable All", toggle=True)
            
            
            row = col.row(align=True)
            
            row.prop(context.space_data.overlay, "show_edge_crease", text="Creases", toggle=True)
            row.prop(context.space_data.overlay, "show_edge_sharp", text="Sharp", toggle=True)
            row.prop(context.space_data.overlay, "show_edge_bevel_weight", text="Bevel", toggle=True)
            row.prop(context.space_data.overlay, "show_edge_seams", text="Seams", toggle=True)

        #END Overlay Options (Wireframe, Edge colors, etc)

        # -----------------------------------------------------------------------------
        #   Use Advanced Settings Box
        # -----------------------------------------------------------------------------

        col = layout.column(align=True)
        row = col.row(align=True)
        col.prop(context.scene.neltulzSubD, "advancedSettings", text="Use Advanced Settings" )

        if scene.neltulzSubD.advancedSettings:

            boxAdvancedOptions = layout.box()
            boxAdvancedOptions.label(text="Advanced Settings:")

            box = boxAdvancedOptions.column(align=True)
            
            row = box.row(align=True)
            
            row.prop(context.scene.neltulzSubD, "useCustomRenderLevel", text="Use Custom Render Level" )

            if scene.neltulzSubD.useCustomRenderLevel:
                col = box.column(align=True)
                col.prop(context.scene.neltulzSubD, "customRenderLevel", text="" )
            
            col = box.column(align=True)
            col.separator()
            col.label(text="Misc:")

            
            col.prop(context.scene.neltulzSubD, "vertexQuality", text="Vertex Quality" )
            col.separator()
            col.prop(context.scene.neltulzSubD, "useCreases", text="Use Creases" )
            
            col.separator()

            col.label(text="UV Smoothing:")
            col.prop(context.scene.neltulzSubD, "uvSmoothing", text='')
            
            col.separator()

            col.label(text="SubD Algorithm:")
            col.prop(context.scene.neltulzSubD, "algorithms", text='')
            
            col.separator()
            
            col.prop(context.scene.neltulzSubD, "disableConflictingModifiersBool", text='Disable Conflicting Modifiers')
            col.prop(context.scene.neltulzSubD, "keepSubDatBottomBool", text='Keep SubD Modifier at Bottom')
            col.prop(context.scene.neltulzSubD, "pickBestShadingBool", text='Pick Best Shading')
            col.prop(context.scene.neltulzSubD, "showPolyCountWarningsBool", text='Show Poly Count Warnings')
            
            col.separator()

            row = col.row(align=True)
            
            op = row.operator('object.neltulz_subd_delete_modifier', text="Delete Modifier")
            op = row.operator('object.neltulz_reset_all_settings', text="Reset Settings")

            col.separator()     
            col = box.column(align=True)
            op = col.operator('object.neltulz_subd_apply_modifier', text="Apply Modifier")

        #END Use Advanced Settings Box