import bpy
from . properties import NeltulzSubD_IgnitProperties
from . import misc_functions
from . import misc_layout

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class OBJECT_PT_NeltulzSubD(Panel):

    bl_idname = "ntz_qck_subd.subdpanel"
    bl_label = "Quick SubD v1.0.4"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        selObjs = bpy.context.selected_objects

        numSelObjs = len(selObjs)
        
        activeObj = bpy.context.view_layer.objects.active

        try:
            neltulzSubD_modifier = activeObj.modifiers["Neltulz - Quick SubD"]
        except:
            neltulzSubD_modifier = None

        # -----------------------------------------------------------------------------
        #   On/Off Button Row
        # -----------------------------------------------------------------------------

        if numSelObjs == 0:
            layout.label(text="Please select an object")
        elif numSelObjs == 1:
            if neltulzSubD_modifier is None:
                layout.label(text="Choose a mode to begin:")

            elif neltulzSubD_modifier is not None and selObjs[0] == activeObj:
                layout.label(text="Current SubD Mode:",)

            else:
                layout.label(text="Multi object mode:")

        else:
            layout.label(text="Multi object mode:")

        onOffButtonRow = layout.row(align=True)
        onOffButtonRow.scale_y = 1.5
        
        buttonOneOff_active      = False #declare
        buttonTwoOn_active       = False #declare
        buttonThreeOnPlus_active = False #declare

        if numSelObjs == 1 and neltulzSubD_modifier is not None and selObjs[0] == activeObj:

            if neltulzSubD_modifier.show_viewport == False:
                buttonOneOff_active      = True
                buttonTwoOn_active       = False
                buttonThreeOnPlus_active = False

            elif neltulzSubD_modifier.show_viewport == True and neltulzSubD_modifier.show_on_cage == False:
                buttonOneOff_active      = False
                buttonTwoOn_active       = True
                buttonThreeOnPlus_active = False

            elif neltulzSubD_modifier.show_viewport == True and neltulzSubD_modifier.show_on_cage == True:
                buttonOneOff_active      = False
                buttonTwoOn_active       = False
                buttonThreeOnPlus_active = True
            
            else:
                buttonOneOff_active      = False
                buttonTwoOn_active       = False
                buttonThreeOnPlus_active = False

        else:
            buttonOneOff_active      = False
            buttonTwoOn_active       = False
            buttonThreeOnPlus_active = False



        buttonOneOff = onOffButtonRow.column(align=True)
        op = buttonOneOff.operator('ntz_qck_subd.subdivide_obj', text="1 (Off)", depress=buttonOneOff_active)
        op.subdMode=1

        buttonTwoOn = onOffButtonRow.column(align=True)
        op = buttonTwoOn.operator('ntz_qck_subd.subdivide_obj', text="2 (On)", depress=buttonTwoOn_active)
        op.subdMode=2

        buttonThreeOnPlus = onOffButtonRow.column(align=True)
        op = buttonThreeOnPlus.operator('ntz_qck_subd.subdivide_obj', text="3 (On+)", depress=buttonThreeOnPlus_active)
        op.subdMode=3

        #END On/Off Button Row

        layout.separator()

        levelChangeSection = layout.box()

        currentSubDLevel = "N/A" #declare
        currentSubDRenderLevel = "" #declare

        renderLevelsRow = levelChangeSection.row(align=True)

        if numSelObjs == 1 and neltulzSubD_modifier is not None and selObjs[0] == activeObj:
            currentSubDLevel = f"{neltulzSubD_modifier.levels}"
            currentSubDRenderLevel = f"{neltulzSubD_modifier.render_levels}"

            renderLevelsRow.label(text=f"SubD Level: {currentSubDLevel}")
            renderLevelsRow.label(text=f"Render Level: {currentSubDRenderLevel}")

        else:
            renderLevelsRow.label(text=f"SubD Level:")

        row = levelChangeSection.row(align=True)
        
        row.prop(scene.neltulzSubD, "changeMethod", expand=True)


        col = levelChangeSection.column(align=True)

        if scene.neltulzSubD.changeMethod == "1":
            row = col.row(align=True)
            op = row.operator('ntz_qck_subd.relativelevelchange', text="-")
            op.decrease=True

            op = row.operator('ntz_qck_subd.relativelevelchange', text="+")
            op.decrease=False
        else:
            row = col.row(align=True)
            row.prop(scene.neltulzSubD, "specificSubDLevel", text="")
            op = row.operator('ntz_qck_subd.specificlevelchange', text="Set")

        #create show/hide toggle for options section
        misc_layout.createShowHide(self, context, scene, "neltulzSubD", "bShowHideOptions", None, "Options", layout)

        if scene.neltulzSubD.bShowHideOptions:

            optionsWrapper = layout.column(align=True)
            optionsRow = optionsWrapper.row(align=True)

            spacer = optionsRow.column(align=True)
            spacer.label(text="", icon="BLANK1")

            optionsSection = optionsRow.column(align=True)

            # -----------------------------------------------------------------------------
            #   Overlay Options (Wireframe, Edge colors, etc)
            # -----------------------------------------------------------------------------

            overlayOptionsWrapper = optionsSection.column(align=True)

            #create show/hide toggle for options section
            misc_layout.createShowHide(self, context, scene, "neltulzSubD", "toggleOverlayOptionsBool", None, "Display Settings", overlayOptionsWrapper)
            
            if scene.neltulzSubD.toggleOverlayOptionsBool is True:

                overlayOptionsWrapper.separator()

                overlayOptionsRow = overlayOptionsWrapper.row(align=True)

                spacer = overlayOptionsRow.column(align=True)
                spacer.label(text="", icon="BLANK1")

                overlayOptionsSection = overlayOptionsRow.column(align=True)

                boxOverlayOptions = overlayOptionsSection.box()

                col = boxOverlayOptions.column(align=True)
                col.label(text="Wireframe:")

                row = col.row(align=True)

                row.prop(context.space_data.overlay, "show_wireframes", text="Toggle Wireframe", toggle=True)

                col = boxOverlayOptions.column(align=True)
                col.label(text="SubD Wireframe:")
                row = col.row(align=True)

                subdWireframeON_active = False #declare
                subdWireframeOFF_active = False #declare

                if numSelObjs == 1 and neltulzSubD_modifier is not None and selObjs[0] == activeObj:
                    if neltulzSubD_modifier.show_only_control_edges:
                        subdWireframeON_active = False
                        subdWireframeOFF_active = True
                    else:
                        subdWireframeON_active = True
                        subdWireframeOFF_active = False


                op = row.operator('ntz_qck_subd.togglewireframe', text="ON", depress=subdWireframeON_active)
                op.subDWireframeOn=True

                op = row.operator('ntz_qck_subd.togglewireframe', text="OFF", depress=subdWireframeOFF_active)
                op.subDWireframeOn=False
                
                col.separator()

                col = boxOverlayOptions.column(align=True)
                col.label(text="Edge Colors:")
                row = col.row(align=True)
                row.prop(scene.neltulzSubD, "enableAllEdgeColorsBool", text="Enable All", toggle=True)
                row.prop(scene.neltulzSubD, "disableAllEdgeColorsBool", text="Disable All", toggle=True)
                
                
                row = col.row(align=True)
                
                row.prop(context.space_data.overlay, "show_edge_crease", text="Creases", toggle=True)
                row.prop(context.space_data.overlay, "show_edge_sharp", text="Sharp", toggle=True)
                row.prop(context.space_data.overlay, "show_edge_bevel_weight", text="Bevel", toggle=True)
                row.prop(context.space_data.overlay, "show_edge_seams", text="Seams", toggle=True)

            #END Overlay Options (Wireframe, Edge colors, etc)

            # -----------------------------------------------------------------------------
            #   Use Advanced Settings Box
            # -----------------------------------------------------------------------------

            optionsSection.separator()
            
            advancedSettingsWrapper = optionsSection.column(align=True)

            #create show/hide toggle for options section
            misc_layout.createShowHide(self, context, scene, "neltulzSubD", "showAdvancedSettings", "advancedSettings", "Use Advanced Settings", advancedSettingsWrapper)
            
            if scene.neltulzSubD.showAdvancedSettings:

                advancedSettingsWrapper.separator()

                advancedSettingsRow = advancedSettingsWrapper.row(align=True)

                spacer = advancedSettingsRow.column(align=True)
                spacer.label(text="", icon="BLANK1")


                advancedSettingsSection = advancedSettingsRow.column(align=True)

                boxAdvancedOptions = advancedSettingsRow.box()

                if scene.neltulzSubD.advancedSettings:
                    boxAdvancedOptions.enabled = True
                else:
                    boxAdvancedOptions.enabled = False

                box = boxAdvancedOptions.column(align=True)
                
                row = box.row(align=True)
                
                row.prop(scene.neltulzSubD, "useCustomRenderLevel", text="Use Custom Render Level" )

                if scene.neltulzSubD.useCustomRenderLevel:
                    col = box.column(align=True)
                    col.prop(scene.neltulzSubD, "customRenderLevel", text="" )
                
                col = box.column(align=True)
                col.separator()
                col.label(text="Misc:")

                
                col.prop(scene.neltulzSubD, "vertexQuality", text="Vertex Quality" )
                col.separator()
                col.prop(scene.neltulzSubD, "useCreases", text="Use Creases" )
                
                col.separator()

                col.label(text="UV Smoothing:")
                col.prop(scene.neltulzSubD, "uvSmoothing", text='')
                
                col.separator()

                col.label(text="SubD Algorithm:")
                col.prop(scene.neltulzSubD, "algorithms", text='')
                
                col.separator()
                
                col.prop(scene.neltulzSubD, "disableConflictingModifiersBool", text='Disable Conflicting Modifiers')
                col.prop(scene.neltulzSubD, "keepSubDatBottomBool", text='Keep SubD Modifier at Bottom')
                col.prop(scene.neltulzSubD, "pickBestShadingBool", text='Pick Best Shading')
                col.prop(scene.neltulzSubD, "showPolyCountWarningsBool", text='Show Poly Count Warnings')
                
                col.separator()

                #END Use Advanced Settings Box

            optionsSection.separator()

            delResetApplyButtons = optionsSection.row(align=True)
            delResetApplyButtons.scale_y = 1.5
            
            op = delResetApplyButtons.operator('ntz_qck_subd.deletemodifier', text="Delete Modifier")
            op = delResetApplyButtons.operator('ntz_qck_subd.applymodifier', text="Apply Modifier")

            optionsSection.separator()     

            op = optionsSection.operator('ntz_qck_subd.resetallsettings', text="Reset All Settings")
