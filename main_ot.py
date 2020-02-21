import bpy
from . properties import NTZQSUBD_ignitproperties
from . import misc_functions

from bpy.props     import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types     import (Operator)

# -----------------------------------------------------------------------------
#    Set SubD Mode
# -----------------------------------------------------------------------------    

class NTZQSUBD_OT_setsubdmode(Operator):
    """Tooltip"""
    bl_idname = "ntzqcksubd.setsubdmode"
    bl_label = "Neltulz - Quick SubD"
    bl_description = "Subdivides your object quickly"

    subdMode : IntProperty (
        name                = "Subdivision Mode",
        description         = "Which subdivision mode to use",
        default             = 1,
    )

    bUseAdvancedSettings : BoolProperty (
        name                = "Use Advanced Settings (Default: False)",
        description         = "Enables the use of advanced settings",
        default             = False,
    )

    bDisableErrorPopups : BoolProperty (
        name                = "Disable Error Popups",
        description         = 'Disables those nasty error popups that appear when using the advanced settings in the "Neltulz - Smart Sharpen" Panel.',
        default             = False,
    )

    @classmethod
    def poll(cls, context):
        return (context.selected_objects and context.object.type == 'MESH')

    def execute(self, context):

        scene = context.scene

        def subdivideObj():

            sel_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']

            for obj in sel_objs:

                neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
                neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)
                
                #update current SubD mode.  If there are any missing properties or modifiers, this will recreate them
                misc_functions.fixModifierAndCustomSubDivProp(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                if neltulzSubD_modifier is None:
                    neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)

                #Set SubD mode (1, 2, or 3)
                misc_functions.setSubDMode(self, context, self.subdMode, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

        # -----------------------------------------------------------------------------
        #   Check whether user is in "Edit Mode" or "Object Mode"
        # -----------------------------------------------------------------------------

        if context.object.mode == "EDIT":

            #Go back to Object Mode
            bpy.ops.object.editmode_toggle()

            subdivideObj()

            #Go back to Edit Mode
            bpy.ops.object.editmode_toggle()

        elif context.object.mode == "OBJECT":

            #detect if something is selected
            if context.selected_objects:

                subdivideObj()

            else:
                self.report({'ERROR'}, 'Please select an object before running the script!' )

        else:
            self.report({'ERROR'}, 'Unable to detect "object" or "edit" mode.  Canceling.' )

        return {'FINISHED'}
    # END execute()
# END Operator()





