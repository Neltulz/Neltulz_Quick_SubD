import bpy
from . properties import NTZQSUBD_ignitproperties
from . import misc_functions

# -----------------------------------------------------------------------------
#    SubD Wireframe
# -----------------------------------------------------------------------------    

class NTZQSUBD_OT_subdwireframe(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_qck_subd.togglewireframe"
    bl_label = "Neltulz - Quick SubD : Toggle Wireframe ON/OFF"
    bl_description = "Toggles the wireframe ON/OFF"

    subDWireframeOn: bpy.props.BoolProperty \
    (
        name="SubD Wireframe ON",
        description="Turn SubD Wireframe ON",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return (context.selected_objects and context.object.type == 'MESH' and bpy.context.space_data.overlay.show_wireframes)
        #return context.selected_objects
        #return context.active_object is not None

    def execute(self, context):

        scene = context.scene
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        for obj in sel_objs:

            neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
            neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)
            
            if neltulzSubD_modifier is None or neltulzSubDLevelCustomProp is None:
                #update current SubD mode.  If there are any missing properties or modifiers, this will recreate them
                misc_functions.fixModifierAndCustomSubDivProp(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
                neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)

            #when toggling subd wireframe on, make sure overlay wireframe is enabled
            if not bpy.context.space_data.overlay.show_wireframes and self.subDWireframeOn:
                bpy.context.space_data.overlay.show_wireframes = True
            
            if self.subDWireframeOn:
                neltulzSubD_modifier.show_only_control_edges = False
                if neltulzSubDLevelCustomProp == 1:
                    misc_functions.setSubDMode(self, context, 3, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
            else:
                neltulzSubD_modifier.show_only_control_edges = True

            misc_functions.update_all_advanced_settings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)




        return {'FINISHED'}


    # END execute()
# END Operator()



# -----------------------------------------------------------------------------
#    Update All Advanced Settings
# -----------------------------------------------------------------------------  


class NTZQSUBD_OT_updatealladvancedsettings(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_qck_subd.updatealladvsettings"
    bl_label = "Neltulz - Quick SubD : Update Advanced Settings"
    bl_description = "Updates the advanced settings"

    @classmethod
    def poll(cls, context):
        return (context.selected_objects and context.object.type == 'MESH')
        #return context.active_object is not None

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

                
                misc_functions.update_all_advanced_settings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
                misc_functions.fixShadingAndAutoSmooth(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                #Go back to Edit Mode
                bpy.ops.object.editmode_toggle()

            elif bpy.context.object.mode == "OBJECT":

                #detect if something is selected
                if bpy.context.selected_objects:
                    
                    misc_functions.update_all_advanced_settings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
                    misc_functions.fixShadingAndAutoSmooth(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                else:
                    self.report({'ERROR'}, 'Please select an object before running the script!' )

            else:
                self.report({'ERROR'}, 'Unable to detect "object" or "edit" mode.  Canceling.' )


        return {'FINISHED'}
    # END execute()
# END Operator()




# -----------------------------------------------------------------------------
#    Apply Modifier
# -----------------------------------------------------------------------------  


class NTZQSUBD_OT_applymodifier(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_qck_subd.applymodifier"
    bl_label = "Neltulz - Quick SubD : Apply Modifier"
    bl_description = "Applies the modifier as data (Destructive operation)"

    @classmethod
    def poll(cls, context):
        return (context.selected_objects and context.object.type == 'MESH')

    def execute(self, context):

        scene = context.scene
        
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        #deselect each object (works better while in edit mode)
        for obj in sel_objs:
            obj.select_set(state=False)

        for obj in sel_objs:

            obj.select_set(state=True)
            #bpy.ops.object.select_pattern(pattern=obj.name)
            bpy.context.view_layer.objects.active = obj

            neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
            neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)

            if bpy.context.object.mode == "EDIT":

                #Go back to Object Mode
                bpy.ops.object.editmode_toggle()

                misc_functions.applyModifier(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                #Go back to Edit Mode
                bpy.ops.object.editmode_toggle()

            elif bpy.context.object.mode == "OBJECT":

                #detect if something is selected
                if bpy.context.selected_objects:

                    misc_functions.applyModifier(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                else:
                    self.report({'ERROR'}, 'Please select an object before running the script!' )

            else:
                self.report({'ERROR'}, 'Unable to detect "object" or "edit" mode.  Canceling.' )
            



        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        col = self.layout.column(align = True)
        col.label(text="Are you sure you want to apply the modifier?")
        col.label(text="This is a destructive operation.")
    # END execute()
# END Operator()




# -----------------------------------------------------------------------------
#    Delete Modifier
# -----------------------------------------------------------------------------  


class NTZQSUBD_OT_delmodifier(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_qck_subd.deletemodifier"
    bl_label = "Neltulz - Quick SubD : Delete Modifier"
    bl_description = "Deletes the modifier"

    @classmethod
    def poll(cls, context):
        return (context.selected_objects and context.object.type == 'MESH')
        #return context.selected_objects
        #return context.active_object is not None

    def execute(self, context):

        scene = context.scene

        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        for obj in sel_objs:
            
            neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
            neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)

            if bpy.context.object.mode == "EDIT":

                #Go back to Object Mode
                bpy.ops.object.editmode_toggle()

                misc_functions.deleteModifier(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                #Go back to Edit Mode
                bpy.ops.object.editmode_toggle()

            elif bpy.context.object.mode == "OBJECT":

                #detect if something is selected
                if bpy.context.selected_objects:

                    misc_functions.deleteModifier(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                else:
                    self.report({'ERROR'}, 'Please select an object before running the script!' )

            else:
                self.report({'ERROR'}, 'Unable to detect "object" or "edit" mode.  Canceling.' )
            



        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        col = self.layout.column(align = True)
        col.label(text="Are you sure you want to delete the SubD")
        col.label(text="modifier from the currently selected object?")
    # END execute()
# END Operator()

#NEIL - IGNORE or delete later
#return context.window_manager.invoke_confirm(self, event)





# -----------------------------------------------------------------------------
#    Reset All Settings
# -----------------------------------------------------------------------------  


class NTZQSUBD_OT_resetallsettings(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_qck_subd.resetallsettings"
    bl_label = "Neltulz - Quick SubD : Reset All Settings"
    bl_description = "Resets all settings"

    @classmethod
    def poll(cls, context):
        #return (context.selected_objects and context.object.type == 'MESH')
        return context.active_object is not None

    def execute(self, context):

        scene = context.scene

        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        for obj in sel_objs:
            
            neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
            neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)

            if bpy.context.object.mode == "EDIT":

                #Go back to Object Mode
                bpy.ops.object.editmode_toggle()

                misc_functions.resetAllSettings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                #Go back to Edit Mode
                bpy.ops.object.editmode_toggle()

            elif bpy.context.object.mode == "OBJECT":

                #detect if something is selected
                if bpy.context.selected_objects:

                    misc_functions.resetAllSettings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

                else:
                    misc_functions.resetAllSettings(self, context, None, scene, None, None)

            else:
                self.report({'ERROR'}, 'Unable to detect "object" or "edit" mode.  Canceling.' )
            



        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        col = self.layout.column(align = True)
        col.label(text="Are you sure you want to reset all settings?")
    # END execute()
# END Operator()