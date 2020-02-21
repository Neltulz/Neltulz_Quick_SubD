import bpy
        

# -----------------------------------------------------------------------------
#   Determine which mode is currently Selected (Vert, Edge, Face, etc)
#   Returned: (0=Multiple modes, 1=Vertice Mode, 2=Edge Mode, 3=Face Mode)
# -----------------------------------------------------------------------------

def getCurrentSelectMode(self, context):
    #Create empty list
    tempList = []

    #check current mesh select mode
    for bool in context.tool_settings.mesh_select_mode:
        tempList.append(bool)
    
    #convert list into a tuple
    tempTuple = tuple(tempList)

    currentSelectMode = int()

    
    if tempTuple == (True, False, False):       
        currentSelectMode = 1
    elif tempTuple == (False, True, False):
        currentSelectMode = 2
    elif tempTuple == (False, False, True):
        currentSelectMode = 3
    else:
        pass #(defaults currentSelectMode to 0)

    return currentSelectMode
# END getCurrentSelectMode(self, context)


#function setSubDMode
def setSubDMode(self, context, mode, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):

    #add-on preferences
    prefs = bpy.context.preferences.addons[__package__].preferences

    disableConflictingModifiers(self, context, obj, scene)

    if neltulzSubD_modifier is not None:

        moveNeltulzSudDModifierToBottom(self, context, obj, scene, neltulzSubD_modifier)

        #if Toggle SubD is enabled:
        if prefs.toggleSubDModes:
            

            if   prefs.subdModePreference == "ON":        toggleResultMode = 2
            elif prefs.subdModePreference == "ONPLUS":    toggleResultMode = 3
                
            if obj['Neltulz_SubD_Level'] == 1 and mode == 1:

                self.mode                   = toggleResultMode
                mode                        = toggleResultMode
                obj['Neltulz_SubD_Level']   = toggleResultMode

            elif obj['Neltulz_SubD_Level'] == 2 and mode == 2:
                self.mode                   = 1
                mode                        = 1
                obj['Neltulz_SubD_Level']   = 1

            elif obj['Neltulz_SubD_Level'] == 3 and mode == 3:
                self.mode                   = 1
                mode                        = 1
                obj['Neltulz_SubD_Level']   = 1
            

        if mode == 1:

            obj['Neltulz_SubD_Level'] = 1
            
            neltulzSubD_modifier.show_viewport = False
            neltulzSubD_modifier.show_in_editmode = False
            neltulzSubD_modifier.show_on_cage = False

            if not obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
                obj.data.use_auto_smooth = True

        elif mode == 2:

            obj['Neltulz_SubD_Level'] = 2

            neltulzSubD_modifier.show_viewport = True
            neltulzSubD_modifier.show_in_editmode = True
            neltulzSubD_modifier.show_on_cage = False

            if neltulzSubD_modifier.levels == 0:
                #increase subd level
                applyRelativeLevelChange(self, context, obj, scene, neltulzSubD_modifier, False, neltulzSubDLevelCustomProp)

            if obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
                obj.data.use_auto_smooth = False

        elif mode == 3:

            obj['Neltulz_SubD_Level'] = 3


            neltulzSubD_modifier.show_viewport = True
            neltulzSubD_modifier.show_in_editmode = True
            neltulzSubD_modifier.show_on_cage = True

            if neltulzSubD_modifier.levels == 0:
                #increase subd level
                applyRelativeLevelChange(self, context, obj, scene, neltulzSubD_modifier, False, neltulzSubDLevelCustomProp)

            if obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
                obj.data.use_auto_smooth = False

        else:
            self.report({'ERROR'}, 'error determining which SubD mode to switch to' )
        
        update_all_advanced_settings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
    else:
        self.report({'ERROR'}, 'Could not find a neltulz SubD modifier.  Failed to change SubD mode' )
#end function setSubDMode

#function getNeltulzSubD_modifier
def getNeltulzSubD_modifier(self, context, obj):
    
    for modifier in obj.modifiers:
        if modifier.type == "SUBSURF":
            if modifier.name == "Neltulz - Quick SubD":
                neltulzSubD_modifier = modifier
                return neltulzSubD_modifier
                break
            else:
                pass
        else:
            pass
#end function getNeltulzSubD_modifier

#function createNeltulzSubD_modifier
def createNeltulzSubD_modifier(self, context, obj, scene, bUseAdvancedSettings_PanelCheckbox, bUseCustomRenderLevel_PanelCheckbox, viewport_level, render_level, neltulzSubDLevelCustomProp):

    #add-on preferences
    prefs = bpy.context.preferences.addons[__package__].preferences

    if bUseAdvancedSettings_PanelCheckbox is None:
        bUseAdvancedSettings_PanelCheckbox = False

    if viewport_level is None:
        viewport_level = prefs.initialSubDLevel

    if render_level is None:
        render_level = prefs.initialSubDLevel
    
    disableConflictingModifiers(self, context, obj, scene)

    #Create the neltulz modifier
    neltulzSubD_modifier = obj.modifiers.new(name="Neltulz - Quick SubD", type='SUBSURF')

    neltulzSubD_modifier.levels = viewport_level
    neltulzSubD_modifier.render_levels = render_level
    neltulzSubD_modifier.show_expanded = False
    
    if viewport_level == 1:
            
        neltulzSubD_modifier.show_viewport = False
        neltulzSubD_modifier.show_in_editmode = False
        neltulzSubD_modifier.show_on_cage = False

        if not obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
            obj.data.use_auto_smooth = True

    elif viewport_level == 2:

        neltulzSubD_modifier.show_viewport = True
        neltulzSubD_modifier.show_in_editmode = True
        neltulzSubD_modifier.show_on_cage = False

        if obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
            obj.data.use_auto_smooth = False

    else:

        neltulzSubD_modifier.show_viewport = True
        neltulzSubD_modifier.show_in_editmode = True
        neltulzSubD_modifier.show_on_cage = True

        if obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
            obj.data.use_auto_smooth = False

    
  

    
    
    #add some necessary scene variables
    scene.neltulzSubD.advancedSettings = bUseAdvancedSettings_PanelCheckbox
    scene.neltulzSubD.useCustomRenderLevel = bUseCustomRenderLevel_PanelCheckbox
    scene.neltulzSubD.customRenderLevel = render_level

    self.report({'INFO'}, 'Could not find a Neltulz SubD Modifier.  Created one.' )
    
    fixShadingAndAutoSmooth(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)

    update_all_advanced_settings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
    
#end function createNeltulzSubD_modifier

#function fixModifierAndCustomSubDivProp
def fixModifierAndCustomSubDivProp(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):

    #add-on preferences
    prefs = bpy.context.preferences.addons[__package__].preferences

    localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp

    if localNeltulzSubDLevelCustomProp is None:
        localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)

    localNeltulzSubD_modifier = neltulzSubD_modifier

    # if neltulzSubD_modifier wasn't specified when running the function, check to see if one exists on the selected object.
    if neltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)
    
    
    #Check if neltulzSubD modifier is at the bottom of the stack, if not, move it to the bottom
    if localNeltulzSubD_modifier is not None:
        moveNeltulzSudDModifierToBottom(self, context, obj, scene, localNeltulzSubD_modifier)

    #custom prop does NOT exist
    if localNeltulzSubDLevelCustomProp is None:

        if localNeltulzSubD_modifier is not None:

            if localNeltulzSubD_modifier.show_viewport and not localNeltulzSubD_modifier.show_on_cage:
                #detected SubD mode 2
                obj['Neltulz_SubD_Level'] = 2
                self.report({'INFO'}, 'FIXED: Custom SubD Mode Prop missing, recreated it from existing neltulzSubD_modifier (SubD Mode 2)' )
            
            elif localNeltulzSubD_modifier.show_viewport and localNeltulzSubD_modifier.show_on_cage:
                #detected SubD mode 3
                obj['Neltulz_SubD_Level'] = 3
                self.report({'INFO'}, 'FIXED: Custom SubD Mode Prop missing, recreated it from existing neltulzSubD_modifier (SubD Mode 3)' )

            else:
                #detected SubD mode 1
                obj['Neltulz_SubD_Level'] = 1
                self.report({'INFO'}, 'FIXED: Custom SubD Mode Prop missing, recreated it from existing neltulzSubD_modifier (SubD Mode 1)' )
        
        else:
            #Missing Custom prop name AND missing neltulz SubD modifier
            self.report({'WARNING'}, 'Missing both the Custom Prop & the neltulz SubD modifier.  Creating them!' )
            createNeltulzSubD_modifier(self, context, obj, scene, scene.neltulzSubD.advancedSettings, scene.neltulzSubD.useCustomRenderLevel, prefs.initialSubDLevel, prefs.initialSubDLevel, neltulzSubDLevelCustomProp)
    
    #custom prop EXISTS
    else:
        
        if localNeltulzSubD_modifier is not None:
            if obj['Neltulz_SubD_Level'] == 1:
                if not localNeltulzSubD_modifier.show_viewport:
                    pass
                else:
                    setSubDMode(self, context, 1, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
                    self.report({'INFO'}, 'FIXED: Custom SubD Prop Found (Level 1) - Force Setting SubD Mode 1' )
                    

            elif obj['Neltulz_SubD_Level'] == 2:
                if localNeltulzSubD_modifier.show_viewport and not localNeltulzSubD_modifier.show_on_cage:
                    pass
                else:
                    setSubDMode(self, context, 2, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
                    self.report({'INFO'}, 'FIXED: Custom SubD Prop Found (Level 2) - Force Setting SubD Mode 2' )
                    
            elif obj['Neltulz_SubD_Level'] == 3:
                if localNeltulzSubD_modifier.show_viewport and localNeltulzSubD_modifier.show_on_cage:
                    pass
                else:
                    setSubDMode(self, context, 3, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
                    self.report({'INFO'}, 'FIXED: Custom SubD Prop Found (Level 3) - Force Setting SubD Mode 3' )

        else:
            #Custom prop EXISTS but we're a missing neltulz SubD modifier
            self.report({'WARNING'}, 'Custom Prop exists, but were missing the neltulz SubD modifier.  Creating them!' )
            
            createNeltulzSubD_modifier(self, context, obj, scene, scene.neltulzSubD.advancedSettings, scene.neltulzSubD.useCustomRenderLevel, prefs.initialSubDLevel, prefs.initialSubDLevel, localNeltulzSubDLevelCustomProp)
            
            if neltulzSubD_modifier is None:
                localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

            if localNeltulzSubD_modifier is not None:
                setSubDMode(self, context, obj['Neltulz_SubD_Level'], obj, scene, localNeltulzSubD_modifier, localNeltulzSubDLevelCustomProp)
            

 
#end function fixModifierAndCustomSubDivProp

#function fixShadingAndAutoSmooth
def fixShadingAndAutoSmooth(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):
    if scene.neltulzSubD.pickBestShadingBool:
        if obj is not None:

            localNeltulzSubD_modifier = neltulzSubD_modifier
            localNeltulzSubD_modifier = neltulzSubDLevelCustomProp

            #Force Smooth Shading
            if context.object.mode == "EDIT":
                bpy.ops.object.editmode_toggle() #Go back to Object Mode
                bpy.ops.object.shade_smooth() #smooth shade
                bpy.ops.object.editmode_toggle() #Go back to Edit Mode
            else:
                bpy.ops.object.shade_smooth() #smooth shade
            
            if localNeltulzSubD_modifier is None:
                if localNeltulzSubD_modifier is None:
                    localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)
                fixModifierAndCustomSubDivProp(self, context, obj, scene, localNeltulzSubD_modifier, None)

            if neltulzSubDLevelCustomProp is not None:

                if obj['Neltulz_SubD_Level'] == 1:
                    if not obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
                        obj.data.use_auto_smooth = True
                        self.report({'WARNING'}, 'FIXED: Auto Smooth Re-enabled (SubD mode 1)' )

                elif obj['Neltulz_SubD_Level'] == 2:
                    if obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
                        obj.data.use_auto_smooth = False
                        self.report({'WARNING'}, 'FIXED: Auto Smooth DISABLED (SubD mode 2)' )

                elif obj['Neltulz_SubD_Level'] == 3:
                    if obj.data.use_auto_smooth and scene.neltulzSubD.pickBestShadingBool:
                        obj.data.use_auto_smooth = False
                        self.report({'WARNING'}, 'FIXED: Auto Smooth DISABLED (SubD mode 3)' )
                else:
                    self.report({'ERROR'}, 'Could not fix shading.  The "Neltulz_SubD_Level" custom property has an unsupported value. Detected: ' + str(obj['Neltulz_SubD_Level']) )

            else:
                pass
                #Could not find the custom SubD prop on the selected object
#END fixShadingAndAutoSmooth function

#function applyRelativeLevelChange
def applyRelativeLevelChange(self, context, obj, scene, neltulzSubD_modifier, decrease, neltulzSubDLevelCustomProp):

    #add-on preferences
    prefs = bpy.context.preferences.addons[__package__].preferences

    disableConflictingModifiers(self, context, obj, scene)

    localNeltulzSubD_modifier = neltulzSubD_modifier
    localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp
    
    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    preventDoubleLevelChange = False
    if localNeltulzSubD_modifier is None:
        preventDoubleLevelChange = True
        fixModifierAndCustomSubDivProp(self, context, obj, scene, localNeltulzSubD_modifier, None)

    localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubDLevelCustomProp is None:
        localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)    

    if localNeltulzSubDLevelCustomProp is None:
        fixModifierAndCustomSubDivProp(self, context, obj, scene, None, localNeltulzSubDLevelCustomProp)

    localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)

    if localNeltulzSubD_modifier is not None:

        moveNeltulzSudDModifierToBottom(self, context, obj, scene, localNeltulzSubD_modifier)

        if decrease:
            if localNeltulzSubD_modifier.levels > 0:

                localNeltulzSubD_modifier.levels -= 1

                self.report({'INFO'}, 'Decreased SubD level to: ' + str(localNeltulzSubD_modifier.levels) )

                if localNeltulzSubD_modifier.levels <= 0:
                    setSubDMode(self, context, 1, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
                else:
                    pass
            else:
                pass
                

        else:
            if obj['Neltulz_SubD_Level'] == 1:
                if   prefs.subdModePreference == "ON":     preferredMode = 2
                elif prefs.subdModePreference == "ONPLUS": preferredMode = 3

                setSubDMode(self, context, preferredMode, obj, scene, localNeltulzSubD_modifier, localNeltulzSubDLevelCustomProp)
                self.report({'INFO'}, 'Increased SubD level to: ' + str(localNeltulzSubD_modifier.levels) )

            elif localNeltulzSubD_modifier.levels <= 11:
                if not preventDoubleLevelChange:
                    localNeltulzSubD_modifier.levels += 1
                    self.report({'INFO'}, 'Increased SubD level to: ' + str(localNeltulzSubD_modifier.levels) )
                else:
                    self.report({'INFO'}, 'NeltulzSubD had to be recreated, which caused the level to be reset.  Prevented double level change.' )

        fixShadingAndAutoSmooth(self, context, obj, scene, neltulzSubD_modifier, localNeltulzSubDLevelCustomProp)





    else:
        self.report({'WARNING'}, 'FAILED TO CHANGE LEVEL!' )

    update_all_advanced_settings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp)   
#end function applyRelativeLevelChange

#function applySpecificLevelChange
def applySpecificLevelChange(self, context, obj, scene, forceLevel, neltulzSubD_modifier, neltulzSubDLevelCustomProp):

    #add-on preferences
    prefs = bpy.context.preferences.addons[__package__].preferences

    if   prefs.subdModePreference == "ON":     preferredMode = 2
    elif prefs.subdModePreference == "ONPLUS": preferredMode = 3

    disableConflictingModifiers(self, context, obj, scene)

    localNeltulzSubD_modifier = neltulzSubD_modifier
    localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp

    if localNeltulzSubD_modifier is None or localNeltulzSubDLevelCustomProp is None:
        fixModifierAndCustomSubDivProp(self, context, obj, scene, localNeltulzSubD_modifier, localNeltulzSubDLevelCustomProp)

    localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubD_modifier is not None:
        moveNeltulzSudDModifierToBottom(self, context, obj, scene, localNeltulzSubD_modifier)

        if forceLevel is None:
            localNeltulzSubD_modifier.levels = scene.neltulzSubD.specificSubDLevel
        else:
            localNeltulzSubD_modifier.levels = forceLevel

        fixShadingAndAutoSmooth(self, context, obj, scene, localNeltulzSubD_modifier, localNeltulzSubDLevelCustomProp)
    else:
        self.report({'WARNING'}, 'FAILED TO CHANGE LEVEL!' )


    if forceLevel is None:
        #This is most likely used when the specific level is set from the "Quick SubD" panel
        if scene.neltulzSubD.specificSubDLevel <= 0:
            if obj['Neltulz_SubD_Level'] != 1:
                setSubDMode(self, context, 1, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
        else:
            if obj['Neltulz_SubD_Level'] == 1:
                setSubDMode(self, context, preferredMode, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
    else:
        #This is most likely used when the keyboard shortcut (CTRL+1) to set specific level is used
        if forceLevel <= 0:
            if obj['Neltulz_SubD_Level'] != 1:
                setSubDMode(self, context, 1, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
        else:
            if obj['Neltulz_SubD_Level'] == 1:
                setSubDMode(self, context, preferredMode, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)

    update_all_advanced_settings(self, context, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
#end function applySpecificLevelChange

#function update_render_level
def update_render_level(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):

    localNeltulzSubD_modifier = neltulzSubD_modifier
    localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp
    
    #fix localNeltulzSubDLevelCustomProp

    if localNeltulzSubDLevelCustomProp is None:
        localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)
    
    if localNeltulzSubDLevelCustomProp is None:
        fixModifierAndCustomSubDivProp(self, context, obj, scene, None, localNeltulzSubDLevelCustomProp)

    if localNeltulzSubDLevelCustomProp is None:
        localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)

    #fix localNeltulzSubD_modifier

    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubD_modifier is None:
        #update current SubD mode.  If there are any missing properties or modifiers, this will recreate them
        fixModifierAndCustomSubDivProp(self, context, obj, scene, None, neltulzSubDLevelCustomProp)
        
    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)
    

    #begin

    newLevel = scene.neltulzSubD.customRenderLevel

    if localNeltulzSubD_modifier is not None:

        moveNeltulzSudDModifierToBottom(self, context, obj, scene, localNeltulzSubD_modifier)
    
        if scene.neltulzSubD.advancedSettings:

            if scene.neltulzSubD.useCustomRenderLevel:

                if localNeltulzSubD_modifier.render_levels == 0:
                    localNeltulzSubD_modifier.show_render = False
                else:
                    localNeltulzSubD_modifier.show_render = True

                localNeltulzSubD_modifier.render_levels = newLevel

            else:
                localNeltulzSubD_modifier.render_levels = localNeltulzSubD_modifier.levels

                if obj['Neltulz_SubD_Level'] == 1:
                    localNeltulzSubD_modifier.show_render = False
                else:
                    localNeltulzSubD_modifier.show_render = True
        
        else:
            localNeltulzSubD_modifier.render_levels = localNeltulzSubD_modifier.levels

            if obj['Neltulz_SubD_Level'] == 1:
                localNeltulzSubD_modifier.show_render = False
            else:
                localNeltulzSubD_modifier.show_render = True
    else:
        self.report({'ERROR'}, 'Could not update the render level, could not find a neltulz SubD modifier' )
#end function update_render_level

#function moveNeltulzSudDModifierToBottom
def moveNeltulzSudDModifierToBottom(self, context, obj, scene, neltulzSubD_modifier):
    if scene.neltulzSubD.keepSubDatBottomBool:
        if neltulzSubD_modifier is not None:

            #Determine number of modifiers in the stack
            modifierLength = len(obj.modifiers)

            neltulzSubD_modifierIndex = obj.modifiers.find("Neltulz - Quick SubD")

            if neltulzSubD_modifierIndex != (modifierLength - 1):
                #the existing neltulz modifier needs to be moved to the bottom of the stack
                while neltulzSubD_modifierIndex != (modifierLength - 1):
                    bpy.ops.object.modifier_move_down(modifier="Neltulz - Quick SubD")
                    neltulzSubD_modifierIndex += 1
                self.report({'INFO'}, 'Neltulz SubD Modifier moved to the bottom of the stack')
            else:
                pass
#end function move


#function update_vertex_quality
def update_vertex_quality(self, context, obj, scene, neltulzSubD_modifier):
    localNeltulzSubD_modifier = neltulzSubD_modifier

    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubD_modifier is not None:
        if scene.neltulzSubD.advancedSettings == True:
            localNeltulzSubD_modifier.quality = scene.neltulzSubD.vertexQuality
        else:
            localNeltulzSubD_modifier.quality = 3
        self.report({'DEBUG'}, 'Updated Neltulz SubD Vertex Quality' )
    else:
        self.report({'WARNING'}, 'FAILED to update Neltulz SubD Vertex Quality' )
#end function update_vertex_quality


#function update_use_creases
def update_use_creases(self, context, obj, scene, neltulzSubD_modifier):
    localNeltulzSubD_modifier = neltulzSubD_modifier

    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubD_modifier is not None:
        if scene.neltulzSubD.advancedSettings == True:
            localNeltulzSubD_modifier.use_creases = scene.neltulzSubD.useCreases
        else:
            localNeltulzSubD_modifier.use_creases = True
        self.report({'DEBUG'}, 'Updated Neltulz SubD Creases' )
    else:
        self.report({'WARNING'}, 'FAILED to update Neltulz SubD Creases' )
#end function update_use_creases

#function update_uv_smoothing
def update_uv_smoothing(self, context, obj, scene, neltulzSubD_modifier):
    localNeltulzSubD_modifier = neltulzSubD_modifier

    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubD_modifier is not None:
        if scene.neltulzSubD.advancedSettings == True:
            if scene.neltulzSubD.uvSmoothing == "1":
                localNeltulzSubD_modifier.uv_smooth = 'NONE'
            else:
                localNeltulzSubD_modifier.uv_smooth = 'PRESERVE_CORNERS'
        else:
            localNeltulzSubD_modifier.uv_smooth = 'PRESERVE_CORNERS'
        self.report({'DEBUG'}, 'Updated Neltulz SubD UV Smoothing' )
    else:
        self.report({'WARNING'}, 'FAILED to update Neltulz SubD UV Smoothing' )
#end function update_uv_smoothing

#function update_subdiv_algorithm
def update_subdiv_algorithm(self, context, obj, scene, neltulzSubD_modifier):
    localNeltulzSubD_modifier = neltulzSubD_modifier

    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubD_modifier is not None:
        if scene.neltulzSubD.advancedSettings == True:
            if scene.neltulzSubD.algorithms == "1":
                localNeltulzSubD_modifier.subdivision_type = 'CATMULL_CLARK'
            else:
                localNeltulzSubD_modifier.subdivision_type = 'SIMPLE'
        else:
            localNeltulzSubD_modifier.subdivision_type = 'CATMULL_CLARK'
        self.report({'DEBUG'}, 'Updated Neltulz Subdivision Type' )
    else:
        self.report({'WARNING'}, 'FAILED to update Neltulz Subdivision Type' )
#end function update_subdiv_algorithm


#function update_all_advanced_settings
def update_all_advanced_settings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):
    disableConflictingModifiers(self, context, obj, scene)

    localNeltulzSubD_modifier = neltulzSubD_modifier
    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp
    if localNeltulzSubDLevelCustomProp is None:
        localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)

    update_render_level(self, context, obj, scene, localNeltulzSubD_modifier, localNeltulzSubDLevelCustomProp)
    update_vertex_quality(self, context, obj, scene, localNeltulzSubD_modifier)
    update_use_creases(self, context, obj, scene, localNeltulzSubD_modifier)
    update_uv_smoothing(self, context, obj, scene, localNeltulzSubD_modifier)
    update_subdiv_algorithm(self, context, obj, scene, localNeltulzSubD_modifier)

    fixShadingAndAutoSmooth(self, context, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
#end update_all_advanced_settings


#function getCustomSubDProperty
def getCustomSubDProperty(self, context, obj):
    #check to see if the custom SubD level prop exists on the selected object
    localCustomPropName = None
    for key in obj.keys():
        if key not in '_RNA_UI':
            if key == 'Neltulz_SubD_Level':
                localCustomPropName = str(key)
                break
    if localCustomPropName is not None:
        return obj[localCustomPropName]


#function applyModifier
def applyModifier(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):

    localNeltulzSubD_modifier = neltulzSubD_modifier
    localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp

    if localNeltulzSubD_modifier is None or localNeltulzSubDLevelCustomProp is None:
        fixModifierAndCustomSubDivProp(self, context, obj, scene, localNeltulzSubDLevelCustomProp, localNeltulzSubDLevelCustomProp)

    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubDLevelCustomProp is None:
        localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)

    if localNeltulzSubD_modifier is not None:

        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Neltulz - Quick SubD")

        if localNeltulzSubDLevelCustomProp is not None:
            del obj["Neltulz_SubD_Level"]
    else:
        self.report({'ERROR'}, 'Could not apply modifier, could not find the Neltulz - Quick SubD Modifier.' )
#END applyModifier function


#function deleteModifier
def deleteModifier(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):

    localNeltulzSubD_modifier = neltulzSubD_modifier
    localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp

    if localNeltulzSubD_modifier is None or localNeltulzSubDLevelCustomProp is None:
        fixModifierAndCustomSubDivProp(self, context, obj, scene, localNeltulzSubDLevelCustomProp, localNeltulzSubDLevelCustomProp)

    if localNeltulzSubD_modifier is None:
        localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

    if localNeltulzSubDLevelCustomProp is None:
        localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)

    if localNeltulzSubD_modifier is not None:
        
        obj.modifiers.remove(localNeltulzSubD_modifier)
        
        if localNeltulzSubDLevelCustomProp is not None:

            del obj["Neltulz_SubD_Level"]

    else:
        self.report({'ERROR'}, 'Could not apply modifier, could not find the Neltulz - Quick SubD Modifier.' )
#END deleteModifier function

#function resetAllSettings
def resetAllSettings(self, context, obj, scene, neltulzSubD_modifier, neltulzSubDLevelCustomProp):

    #add-on preferences
    prefs = bpy.context.preferences.addons[__package__].preferences

    if obj is not None:
        localNeltulzSubD_modifier = neltulzSubD_modifier
        localNeltulzSubDLevelCustomProp = neltulzSubDLevelCustomProp

        if localNeltulzSubD_modifier is None or localNeltulzSubDLevelCustomProp is None:
            fixModifierAndCustomSubDivProp(self, context, obj, scene, localNeltulzSubDLevelCustomProp, localNeltulzSubDLevelCustomProp)

        if localNeltulzSubD_modifier is None:
            localNeltulzSubD_modifier = getNeltulzSubD_modifier(self, context, obj)

        if localNeltulzSubDLevelCustomProp is None:
            localNeltulzSubDLevelCustomProp = getCustomSubDProperty(self, context, obj)

    
    
    scene.neltulzSubD.busyUpdatingAdvancedSettings = True #Prevent scene properties from trying to update
    
    prefs.toggleSubDModes = False
    prefs.subdModePreference = 'ONPLUS'
    prefs.initialSubDLevel = 1
    scene.neltulzSubD.specificSubDLevel = 1
    scene.neltulzSubD.changeMethod = '1'
    scene.neltulzSubD.advancedSettings = False
    scene.neltulzSubD.useCustomRenderLevel = False
    scene.neltulzSubD.customRenderLevel = 3
    scene.neltulzSubD.vertexQuality = 3
    scene.neltulzSubD.useCreases = True
    scene.neltulzSubD.uvSmoothing = '2'
    scene.neltulzSubD.algorithms = '1'
    scene.neltulzSubD.disableConflictingModifiersBool = True
    scene.neltulzSubD.keepSubDatBottomBool = True
    scene.neltulzSubD.pickBestShadingBool = True
    scene.neltulzSubD.showPolyCountWarningsBool = True

    scene.neltulzSubD.busyUpdatingAdvancedSettings = False #Reset

    if obj is not None:
        applySpecificLevelChange(self, context, obj, scene, 1, neltulzSubD_modifier, neltulzSubDLevelCustomProp)
        setSubDMode(self, context, 3, obj, scene, localNeltulzSubD_modifier, neltulzSubDLevelCustomProp)
#END resetAllSettings function


#function disableConflictingModifiers
def disableConflictingModifiers(self, context, obj, scene):
    if scene.neltulzSubD.disableConflictingModifiersBool:
        for modifier in obj.modifiers:
            if modifier.type == "SUBSURF":
                if modifier.name != "Neltulz - Quick SubD":
                    #Found an existing SUBSURF modifier, it needs to be disabled.
                    if "(Disabled) " not in modifier.name:
                        modifier.name = "(Disabled) " + modifier.name
                        self.report({'INFO'}, 'Found an existing SUBSURF modifier.  It could interfere with the subd preview.  Disabled it just to be safe.' )
                        
                    modifier.show_expanded = False
                    modifier.show_render = False
                    modifier.show_viewport = False
                    modifier.show_in_editmode = False
                    modifier.show_on_cage = False

            elif modifier.type =="WEIGHTED_NORMAL":
                #Found an existing WEIGHTED_NORMAL modifier, it needs to be disabled.
                if "(Disabled) " not in modifier.name:
                    modifier.name = "(Disabled) " + modifier.name
                    self.report({'INFO'}, 'Found an existing WEIGHTED_NORMAL modifier. It could interfere with the subd preview.  Disabled it just to be safe.' )

                modifier.show_expanded = False
                modifier.show_render = False
                modifier.show_viewport = False
                modifier.show_in_editmode = False
                modifier.show_on_cage = False
                
                    
            elif modifier.type =="NORMAL_EDIT":
                #Found an existing NORMAL_EDIT modifier, it needs to be disabled.
                if "(Disabled) " not in modifier.name:
                    modifier.name = "(Disabled) " + modifier.name
                    self.report({'INFO'}, 'Found an existing NORMAL_EDIT modifier. It could interfere with the subd preview.  Disabled it just to be safe.' )

                modifier.show_expanded = False
                modifier.show_render = False
                modifier.show_viewport = False
                modifier.show_in_editmode = False
                modifier.show_on_cage = False
                

            else:
                pass
                #modifier.show_in_editmode = False #Disabled 2019-08-19 - Was causing problems with mirror modifier, and possibly more.
#END disableConflictingModifiers function

#Begin getPolyCount Function
def calculateSubDPolyCount(self, context, obj, scene, level):
    if obj is not None:
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US')

        data = obj.data
        total_triangles = 0

        for face in data.polygons:
            vertices = face.vertices
            triangles = len(vertices) - 2
            total_triangles += triangles

        powerList = (1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304)
        
        resultingPolyCount = total_triangles * powerList[max(min(level, 11), 0)]

        #put commas in number
        resultingPolyCountString = locale.format("%d", resultingPolyCount, grouping=True)

        scene.neltulzSubD.resultingPolyCount = resultingPolyCount
        scene.neltulzSubD.resultingPolyCountString = resultingPolyCountString
    else:
        self.report({'WARNING'}, 'Failed to get poly count.  Object was undefined.' )

#END getPolyCount Function