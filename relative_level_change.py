import bpy

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

from . properties import NeltulzSubD_IgnitProperties
from . import misc_functions



# -----------------------------------------------------------------------------
#    Level Change Operator
# -----------------------------------------------------------------------------    

class OBJECT_OT_NeltulzSubD_Relative_LevelChange(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_qck_subd.relativelevelchange"
    bl_label = "Neltulz - Quick SubD - Level Change"
    bl_description = "Changes the subdivision level"

    decrease: bpy.props.BoolProperty \
    (
        name="Decrease Level",
        description="Decrease level",
        default=False
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

                misc_functions.applyRelativeLevelChange(self, context, obj, scene, neltulzSubD_modifier, self.decrease, neltulzSubDLevelCustomProp)

                #Go back to Edit Mode
                bpy.ops.object.editmode_toggle()

            elif bpy.context.object.mode == "OBJECT":

                #detect if something is selected
                if bpy.context.selected_objects:

                    misc_functions.applyRelativeLevelChange(self, context, obj, scene, neltulzSubD_modifier, self.decrease, neltulzSubDLevelCustomProp)

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
                resultingLevel = 0
                plusOrMinus = 1
                if self.decrease:
                    plusOrMinus = -1

                neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
                
                if neltulzSubD_modifier is not None:
                    
                    resultingLevel = neltulzSubD_modifier.levels + plusOrMinus

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





        
