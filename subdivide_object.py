import bpy
import types
from . properties import NTZQSUBD_ignitproperties
from . import misc_functions

def execute(self, context):
    
    scene = context.scene

    sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    for obj in sel_objs:

        neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)
        neltulzSubDLevelCustomProp = misc_functions.getCustomSubDProperty(self, context, obj)
        
        #update current SubD mode.  If there are any missing properties or modifiers, this will recreate them
        misc_functions.fixModifierAndCustomSubDivProp(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

        if neltulzSubD_modifier is None:
            neltulzSubD_modifier = misc_functions.getNeltulzSubD_modifier(self, context, obj)

        #Set SubD mode (1, 2, or 3)
        misc_functions.setSubDMode(self, context, self.subdMode, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
