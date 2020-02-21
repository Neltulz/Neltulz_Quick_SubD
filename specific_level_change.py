import bpy

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

from . properties import NTZQSUBD_ignitproperties
from . import misc_functions



# -----------------------------------------------------------------------------
#    Level Change Operator
# -----------------------------------------------------------------------------    

class NTZQSUBD_OT_specificlevelchange(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntzqcksubd.specificlevelchange"
    bl_label = "Neltulz - Quick SubD - Specific Level Change"
    bl_description = "Changes the Specific subdivision level"

    

    useShortcutKeySpecificLevel: bpy.props.BoolProperty \
    (
        name="Use Operator Specific Level",
        description="Use Operator Specific Level",
        default=False
    )

    shortcutKeySpecificLevel: bpy.props.IntProperty \
    (
        name="Specific Level",
        description="Which SubD Level to use",
        default=0
    )

    @classmethod
    def poll(cls, context):
        return (context.selected_objects and context.object.type == 'MESH')

    def execute(self, context):

        scene = context.scene

        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        for obj in sel_objs:

            neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
            neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)

            # -----------------------------------------------------------------------------
            #   Check whether user is in "Edit Mode" or "Object Mode"
            # -----------------------------------------------------------------------------


            if bpy.context.object.mode == "EDIT":

                #Go back to Object Mode
                bpy.ops.object.editmode_toggle()

                if self.useShortcutKeySpecificLevel:
                    #Use the specific SubD level for the pressed keymap (CTRL+Shift+1 etc)
                    misc_functions.applySpecificLevelChange(self, context, obj, scene, self.shortcutKeySpecificLevel, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
                else:
                    #Use the Specific SubD level in the "Quick SubD panel"
                    misc_functions.applySpecificLevelChange(self, context, obj, scene, None, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                #Go back to Edit Mode
                bpy.ops.object.editmode_toggle()

            elif bpy.context.object.mode == "OBJECT":

                #detect if something is selected
                if bpy.context.selected_objects:

                    if self.useShortcutKeySpecificLevel:
                        #Use the specific SubD level for the pressed keymap (CTRL+Shift+1 etc)
                        misc_functions.applySpecificLevelChange(self, context, obj, scene, self.shortcutKeySpecificLevel, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
                    else:
                        #Use the Specific SubD level in the "Quick SubD panel"
                        misc_functions.applySpecificLevelChange(self, context, obj, scene, None, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                else:
                    self.report({'ERROR'}, 'Please select an object before running the script!' )

            else:
                self.report({'ERROR'}, 'Unable to detect "object" or "edit" mode.  Canceling.' )



        return {'FINISHED'}


    
    def invoke(self, context, event):

        scene = context.scene

        if scene.neltulzSubD.showPolyCountWarningsBool:

            sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
            detectedHighPolyCount = False

            for obj in sel_objs:

                #Calculate approximate polycount of the resulting SubD so that it can be used to display warnings in the operator's invoke
                # the poly count is stored in a neltulzSubD scene variable.

                neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
                
                resultingLevel = 0

                if self.useShortcutKeySpecificLevel:
                    #Use the specific level from the pressed keymap shortcut
                    resultingLevel = self.shortcutKeySpecificLevel

                else:
                    #Use the specific level from the "Quick SubD" Panel
                    resultingLevel = scene.neltulzSubD.specificSubDLevel

                misc_functions.calculateSubDPolyCount(self, context, obj, scene, resultingLevel)

                polycount = scene.neltulzSubD.resultingPolyCount

                if polycount >= 2000000:
                    detectedHighPolyCount = True
                    break
                
            if detectedHighPolyCount:
                return context.window_manager.invoke_props_dialog(self, width=300)
            else:
                return self.execute(context)
        
        else:
            return self.execute(context)
        
    
    
    def draw(self, context):
        col = self.layout.column(align = True)
        col.label(text="One or more objects has a high poly count!")
        col.label(text="Approximate poly count: " + context.scene.neltulzSubD.resultingPolyCountString )
        col.label(text="Are you sure you want to subdivide?")
    # END execute()
# END Operator()


