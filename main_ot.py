import bpy
from . properties import NTZQSUBD_ignitproperties
from . import misc_functions
from . import subdivide_object

# -----------------------------------------------------------------------------
#    Main Addon Operator
# -----------------------------------------------------------------------------    

class NTZQSUBD_OT_subdmainoperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_qck_subd.subdivide_obj"
    bl_label = "Neltulz - Quick SubD"
    bl_description = "Subdivides your object quickly"

    subdMode: bpy.props.IntProperty \
    (
        name="Subdivision Mode",
        description="Which subdivision mode to use",
        default=1
    )

    bUseAdvancedSettings: bpy.props.BoolProperty \
    (
        name="Use Advanced Settings (Default: False)",
        description="Enables the use of advanced settings",
        default=False
    )

    bDisableErrorPopups: bpy.props.BoolProperty \
    (
        name="Disable Error Popups",
        description='Disables those nasty error popups that appear when using the advanced settings in the "Neltulz - Smart Sharpen" Panel.',
        default=False
    )

    @classmethod
    def poll(cls, context):
        return (context.selected_objects and context.object.type == 'MESH')

    def execute(self, context):

        # -----------------------------------------------------------------------------
        #   Check whether user is in "Edit Mode" or "Object Mode"
        # -----------------------------------------------------------------------------

        if bpy.context.object.mode == "EDIT":

            #Go back to Object Mode
            bpy.ops.object.editmode_toggle()

            subdivide_object.execute(self, context)

            #Go back to Edit Mode
            bpy.ops.object.editmode_toggle()

        elif bpy.context.object.mode == "OBJECT":

            #detect if something is selected
            if bpy.context.selected_objects:

                subdivide_object.execute(self, context)

            else:
                self.report({'ERROR'}, 'Please select an object before running the script!' )

        else:
            self.report({'ERROR'}, 'Unable to detect "object" or "edit" mode.  Canceling.' )

        return {'FINISHED'}
    # END execute()
# END Operator()







