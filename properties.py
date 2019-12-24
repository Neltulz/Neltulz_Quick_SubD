import bpy
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

def neltulzSubD_setSpecificSubDLevel(self, context):
    if bpy.context.selected_objects:
        bpy.ops.ntz_qck_subd.specificlevelchange()

def neltulzSubD_UpdateAdvancedSettings(self, context):
    
    if bpy.context.selected_objects:
        
        # when mass updating advanced settings, they will try to loop and update a lot.  
        # This condition prevents this from happening
        if not context.scene.neltulzSubD.busyUpdatingAdvancedSettings:
            
            bpy.ops.ntz_qck_subd.updatealladvsettings()
            
        else:
            pass
            #Loop prevented

def neltulzSubD_useAdvancedSettings_toggled(self, context):
    # when mass updating advanced settings, they will try to loop and update a lot.  
    # This condition prevents this from happening
    if not context.scene.neltulzSubD.busyUpdatingAdvancedSettings:
        scene = context.scene

        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        foundModifierOrCustomProp = False

        # loop through all of the selected objects, if a modifier or custom prop is found, then when the user
        # clicks the "Use Advanced Settings" checkbox, update all of the settings on the SubD modifier.
        # Otherwise, if NOTHING is found, then merely toggle the advanced settings menu without doing anything.
        
        # Limitation: If multiple objects are selected and a SubD Modifier or custom prop is found, then any
        # other objects in the selection (without subd modifiers and props) will have theirs recreated.
        for obj in sel_objs:

            neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
            neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)

            if neltulzSubD_modifier is not None:
                foundModifierOrCustomProp = True
                break
            elif neltulzSubDLevelCustomProp is not None:
                foundModifierOrCustomProp = True
                break

        if foundModifierOrCustomProp:
            neltulzSubD_UpdateAdvancedSettings(self, context)
    
    else:
        pass
        #Loop prevented
        

def neltulzSubD_DisableAllEdgeColorsFunc(self, context):
    if context.scene.neltulzSubD.disableAllEdgeColorsBool:
        bpy.context.space_data.overlay.show_edge_crease = False
        bpy.context.space_data.overlay.show_edge_sharp = False
        bpy.context.space_data.overlay.show_edge_bevel_weight = False
        bpy.context.space_data.overlay.show_edge_seams = False
        context.scene.neltulzSubD.disableAllEdgeColorsBool = False

def neltulzSubD_EnableAllEdgeColorsFunc(self, context):
    if context.scene.neltulzSubD.enableAllEdgeColorsBool:
        bpy.context.space_data.overlay.show_edge_crease = True
        bpy.context.space_data.overlay.show_edge_sharp = True
        bpy.context.space_data.overlay.show_edge_bevel_weight = True
        bpy.context.space_data.overlay.show_edge_seams = True
        context.scene.neltulzSubD.enableAllEdgeColorsBool = False

class NeltulzSubD_IgnitProperties(bpy.types.PropertyGroup):

    bShowHideOptions : BoolProperty (
        name="Show/Hide Options",
        description="Reveals options.",
        default = False,
    )

    subd_change_method = [
        ("1", "Relative", "RELATIVE_CHANGE"),
        ("2", "Specific", "SPECIFIC_CHANGE"),
    ]

    changeMethod : EnumProperty(
        items=subd_change_method,
        description="Default: Relative: Determines whether to change subdivision levels relative to the selected object's current level, or Specific: Set the level specifically to the one you want.",
        default="1"
    )

    specificSubDLevel : IntProperty(
        name="Specific SubD Level",
        description="Set the SubD of your object to a specific level",
        default = 1,
        min = 0,
        max = 11
    )

    toggleOverlayOptionsBool : BoolProperty(
        name="Toggle Overlay options (Wireframe, Edge colors, etc)",
        description="Default: True: Toggle Overlay options (Wireframe, Edge colors, etc)",
        default = True
    )
    
    disableAllEdgeColorsBool : BoolProperty(
        name="Disable all Edge Colors",
        description="Default: False: Disables all edge colors to make SubD easier to visualize",
        default = False,
        update=neltulzSubD_DisableAllEdgeColorsFunc
    )

    enableAllEdgeColorsBool : BoolProperty(
        name="Disable all Edge Colors",
        description="Default: False: Enables all edge colors",
        default = False,
        update=neltulzSubD_EnableAllEdgeColorsFunc
    )

    showAdvancedSettings : BoolProperty(
        name="Show Advanced Settings",
        description="Show Advanced Settings",
        default = True
    )

    advancedSettings : BoolProperty(
        name="Checkbox Name",
        description="Default: Off: Use advanced settings",
        default = False,
        update=neltulzSubD_useAdvancedSettings_toggled
    )

        
    busyUpdatingAdvancedSettings : BoolProperty(
        name="Busy updating advanced settings",
        description="Default: False: Prevents lots of looping",
        default = False
    )

    useCustomRenderLevel : BoolProperty(
        name="Default: Off: Use Custom Render Level (Checkbox)",
        description="Allows you to set a custom subdivision render level.  Use this to make your render higher quality!  Caution: values greater than 6 can result in extreme lag, or program instability",
        default = False,
        update=neltulzSubD_UpdateAdvancedSettings
    )

    customRenderLevel : IntProperty(
        name="Custom Render Level",
        description="Default: 3: Allows you to set a custom subdivision render level.  Use this to make your render higher quality!  Caution: values greater than 6 can result in extreme lag, or program instability.  (Max: 11)",
        default = 3,
        min = 0,
        max = 11,
        soft_max = 6,
        update=neltulzSubD_UpdateAdvancedSettings
    )

    vertexQuality : IntProperty(
        name="Quality",
        description="Default: 3: Accuracy of vertex positions, lower value is faster but less precise.  (Max: 10)",
        default = 3,
        min = 0,
        max = 10,
        soft_max = 6,
        update=neltulzSubD_UpdateAdvancedSettings
    )

    
    useCreases : BoolProperty(
        name="Use Creases",
        description="Default: True: Use mesh edge crease information to sharpen edges",
        default = True,
        update=neltulzSubD_UpdateAdvancedSettings
    )

    uvsmooth_items = [
        ("1", "Sharp", "NONE"),
        ("2", "Smooth, Keep Corners", "PRESERVE_CORNERS"),
    ]

    uvSmoothing : EnumProperty(
        items=uvsmooth_items,
        description="Default: Smooth: Controls how smoothing is applied to UVs",
        default="2",
        update=neltulzSubD_UpdateAdvancedSettings
    )

    subd_algorithims = [
        ("1", "Catmull-Clark", "CATMULL CLARK"),
        ("2", "Simple", "SIMPLE"),
    ]

    algorithms : EnumProperty(
        items=subd_algorithims,
        description="Default: Catmull-Clark: Type of subdivision algorithm",
        default="1",
        update=neltulzSubD_UpdateAdvancedSettings
    )

    disableConflictingModifiersBool : BoolProperty(
        name="Disable Conflicting Modifiers",
        description="Default: True: Automatically disables any conflicting modifiers",
        default = False
    )

    keepSubDatBottomBool : BoolProperty(
        name="Keep SubD Modifier at Bottom",
        description="Default: True: Automatically moves the Neltulz SubD modifier to the bottom of the modifier stack so that it can smooth the object after other modifiers",
        default = True
    )
    
    pickBestShadingBool : BoolProperty(
        name="Pick Best Shading",
        description='Default: True: Automatically picks the best shading (Smooth shade or Flat shade) based on which SubD mode is active, and also enables/disables "Normal Auto smooth" based on which subD mode is active.',
        default = True
    )

    showPolyCountWarningsBool : BoolProperty(
        name="Show Poly Count Warnings",
        description='Default: True: Shows warnings if your poly count is very high before subdividing further to help prevent program instability and very long freezes.',
        default = True
    )

    resultingPolyCount : FloatProperty(
        name = "Resulting Poly Count",
        description = "The resulting poly count of the getPolyCount function",
        default = 0
    )

    resultingPolyCountString : StringProperty(
        name = "Resulting Poly Count String",
        description = "The resulting poly count of the getPolyCount function as string form with commas",
        default = ""
    )