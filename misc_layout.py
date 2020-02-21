import bpy

def createProp(self, context, scene, bEnabled, labelText, propItem, scale_y, labelScale, propScale, labelAlign, propAlign, propText, bExpandProp, layout):

    propRow = layout.row(align=True)

    if not bEnabled:
        propRow.enabled = False

    propRow.scale_y = scale_y

    propRowLabel = propRow.row(align=True)
    propRowLabel.alignment="EXPAND"
    propRowLabel.ui_units_x = labelScale

    propRowLabel1 = propRowLabel.row(align=True)
    propRowLabel1.alignment=labelAlign
    propRowLabel1.scale_x = 1

    propRowLabel1.label(text=labelText)

    propRowItem = propRow.row(align=True)
    propRowItem.alignment=propAlign

    propRowItem1 = propRowItem.row(align=True)
    propRowItem1.alignment=propAlign
    propRowItem1.ui_units_x = propScale
    propRowItem1.scale_x = 100

    propRowItem1.prop(self, propItem, text=propText, expand=bExpandProp)

#Show hide section with arrow, optional checkbox, and text
def createShowHide(self, context, scene, properties, showHideBool, optionalCheckboxBool, text, layout):

    if scene is not None:
        data = eval( f"scene.{properties}" )
        boolThing = eval( f"scene.{properties}.{showHideBool}" )
    else:
        data = self
        boolThing = eval( f"self.{showHideBool}")

    if boolThing:
        showHideIcon = "TRIA_DOWN"
    else:
        showHideIcon = "TRIA_RIGHT"

    row = layout.row(align=True)

    downArrow = row.column(align=True)
    downArrow.alignment = "LEFT"
    downArrow.prop(data, showHideBool, text="", icon=showHideIcon, emboss=False )

    if optionalCheckboxBool is not None:
        checkbox = row.column(align=True)
        checkbox.alignment = "LEFT"
        checkbox.prop(data, optionalCheckboxBool, text="" )

    textRow = row.column(align=True)
    textRow.alignment = "LEFT"
    textRow.prop(data, showHideBool, text=text, emboss=False )

    emptySpace = row.column(align=True)
    emptySpace.alignment = "EXPAND"
    emptySpace.prop(data, showHideBool, text=" ", emboss=False)


def mainQuickSubDPanel(self, context, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel):
    layout = self.layout
    layout = layout.column(align=True)
    scene = context.scene

    #determine if panel is inside of a popop/pie menu
    panelInsidePopupOrPie = context.region.type == 'WINDOW'

    if panelInsidePopupOrPie:
        if bUseCompactPopupAndPiePanel:
            layout.ui_units_x = 8
            layout.label(text="Quick SubD")
        else:
            layout.ui_units_x = 13
            layout.label(text="Quick SubD v1.0.7")
    else:
        if bUseCompactSidebarPanel:
            layout.ui_units_x = 8
        else:
            layout.ui_units_x = 13

    selObjs = bpy.context.selected_objects
    numSelObjs = len(selObjs)
    activeObj = bpy.context.view_layer.objects.active

    try:    neltulzSubD_modifier = activeObj.modifiers["Neltulz - Quick SubD"]
    except: neltulzSubD_modifier = None

    #On / Off Section
    OffOnOnPlus_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout)

    if panelInsidePopupOrPie:
        layout.separator()
        
        if bUseCompactPopupAndPiePanel:
            changeSubDAndOptionsSection = layout.row(align=True)
        else:
            changeSubDAndOptionsSection = layout.column(align=True)

    else:
        if bUseCompactSidebarPanel:
            layout.separator()
            changeSubDAndOptionsSection = layout.row(align=True)
        else:
            changeSubDAndOptionsSection = layout.column(align=True)

    

    #Level Change Section
    changeSubDLevel_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, changeSubDAndOptionsSection)

    #Options Section
    options_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, changeSubDAndOptionsSection)

def OffOnOnPlus_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout):

    onOffButtonSection = layout.column(align=True)

    def labelInfoText():
        if numSelObjs == 0:
            onOffButtonSection.label(text="Please select an object")

        elif numSelObjs == 1:
            if neltulzSubD_modifier is None:
                
                if not bUseCompactSidebarPanel: onOffButtonSection.label(text="Choose a mode to begin:")

            elif neltulzSubD_modifier is not None and selObjs[0] == activeObj:
                onOffButtonSection.label(text="Current SubD Mode:",)

            else:
                onOffButtonSection.label(text="Multi object mode:")

        else:
            onOffButtonSection.label(text="Multi object mode:")

        onOffButtonSection.separator()

    if panelInsidePopupOrPie:

        if not bUseCompactPopupAndPiePanel:
            labelInfoText()

    else:

        if not bUseCompactSidebarPanel:
            labelInfoText()


    

    onOffButtonRow = onOffButtonSection.row(align=True)


    if panelInsidePopupOrPie:
        if bUseCompactPopupAndPiePanel: onOffButtonRow.scale_y = 1
        else:                           onOffButtonRow.scale_y = 1.5

    else:
        if bUseCompactSidebarPanel: onOffButtonRow.scale_y = 1
        else:                       onOffButtonRow.scale_y = 1.5


   

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
    op = buttonOneOff.operator('ntzqcksubd.setsubdmode', text="1 (Off)", depress=buttonOneOff_active)
    op.subdMode=1

    buttonTwoOn = onOffButtonRow.column(align=True)
    op = buttonTwoOn.operator('ntzqcksubd.setsubdmode', text="2 (On)", depress=buttonTwoOn_active)
    op.subdMode=2

    buttonThreeOnPlus = onOffButtonRow.column(align=True)
    op = buttonThreeOnPlus.operator('ntzqcksubd.setsubdmode', text="3 (On+)", depress=buttonThreeOnPlus_active)
    op.subdMode=3

def changeSubDLevel_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout):
    
    levelChangeSection = layout.column(align=True)
    
    if panelInsidePopupOrPie:

        if bUseCompactPopupAndPiePanel:
            changeLevelPopover_Enum = "changeLevel_CompactPopoverEnum"
        else:
            changeLevelPopover_Enum = "changeLevel_PopoverEnum"
        
        changeLevelPopover = levelChangeSection.prop_with_popover( scene.neltulzSubD, changeLevelPopover_Enum, text="", icon="NONE", icon_only=False, panel="NTZQSUBD_PT_changesubdlevel" )

    else:

        if bUseCompactSidebarPanel:
            
            changeLevelPopover = levelChangeSection.prop_with_popover( scene.neltulzSubD, "changeLevel_CompactPopoverEnum", text="", icon="NONE", icon_only=False, panel="NTZQSUBD_PT_changesubdlevel" )

            levelChangeSection.separator()

        else:
            
            levelChangeSection.separator()

            #create show/hide toggle for options section
            createShowHide(self, context, scene, "neltulzSubD", "bShowHideLevelChangeOptions", None, "Change SubD Level", levelChangeSection)

            if scene.neltulzSubD.bShowHideLevelChangeOptions:

                levelChangeSection.separator()

                changeSubDLevel_SectionInner(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, True, True, levelChangeSection)

            levelChangeSection.separator()

def changeSubDLevel_SectionInner(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, bIndent, bWrapInBox, layout):

    if bIndent:

        levelChangeRow = layout.row(align=True)
        spacer = levelChangeRow.column(align=True)
        spacer.label(text="", icon="BLANK1")


        if bWrapInBox:

            levelChangeCol = levelChangeRow.box()

        else:

            levelChangeCol = levelChangeRow.column(align=True)

            levelChangeCol.separator()

    
    else:
        levelChangeCol = layout


    currentSubDLevel = "N/A" #declare
    currentSubDRenderLevel = "" #declare

    renderLevelsRow = levelChangeCol.row(align=True)

    if numSelObjs == 1 and neltulzSubD_modifier is not None and selObjs[0] == activeObj:
        currentSubDLevel = f"{neltulzSubD_modifier.levels}"
        currentSubDRenderLevel = f"{neltulzSubD_modifier.render_levels}"

        renderLevelsRow.label(text=f"View Lvl: {currentSubDLevel}")
        renderLevelsRow.label(text=f"Render Lvl: {currentSubDRenderLevel}")

    else:
        renderLevelsRow.label(text=f"View Lvl:")

    row = levelChangeCol.row(align=True)
    
    row.prop(scene.neltulzSubD, "changeMethod", expand=True)


    col = levelChangeCol.column(align=True)

    if scene.neltulzSubD.changeMethod == "1":
        row = col.row(align=True)
        op = row.operator('ntzqcksubd.relativelevelchange', text="-")
        op.decrease=True

        op = row.operator('ntzqcksubd.relativelevelchange', text="+")
        op.decrease=False
    else:
        row = col.row(align=True)
        row.prop(scene.neltulzSubD, "specificSubDLevel", text="")
        op = row.operator('ntzqcksubd.specificlevelchange', text="Set")

def options_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout):

    if panelInsidePopupOrPie:
        if bUseCompactPopupAndPiePanel:
            optionsSection = layout.row(align=True)
        else:
            optionsSection = layout.column(align=True)
    else:
        if bUseCompactSidebarPanel:
            optionsSection = layout.row(align=True)
        else:
            optionsSection = layout.column(align=True)

    def createPopover(bIconOnly):
        if bIconOnly:
            icon = "SETTINGS"
        else:
            icon = "NONE"

        optionsSection.separator()

        optionsPopover = optionsSection.prop_with_popover( scene.neltulzSubD, "options_PopoverEnum", text="", icon=icon, icon_only=bIconOnly, panel="NTZQSUBD_PT_options" )

    if panelInsidePopupOrPie:

        if bUseCompactPopupAndPiePanel:
            createPopover(True)
        else:
            createPopover(False)

    else:
        if bUseCompactSidebarPanel:
            createPopover(True)
        else:
            #create show/hide toggle for options section
            createShowHide(self, context, scene, "neltulzSubD", "bShowHideOptions", None, "Options", optionsSection)

            if scene.neltulzSubD.bShowHideOptions:

                optionsSection.separator()

                options_SectionInner(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, True, False, layout)

def options_SectionInner(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, bIndent, bWrapInBox, layout):

    if bIndent:

        optionsRow = layout.row(align=True)
        indent = optionsRow.column(align=True)
        indent.label(text="", icon="BLANK1")

        if bWrapInBox: optionsCol = optionsRow.box()
        else:          optionsCol = optionsRow.column(align=True)

    else:
        if bWrapInBox: optionsCol = layout.box()
        else:          optionsCol = layout
        

    # -----------------------------------------------------------------------------
    #   SubD Options
    # -----------------------------------------------------------------------------

    generalOptionsWrapper = optionsCol.box().column(align=True)

    #create show/hide toggle for options section
    createShowHide(self, context, scene, "neltulzSubD", "toggleGeneralOptionsBool", None, "SubD", generalOptionsWrapper)
    

    if scene.neltulzSubD.toggleGeneralOptionsBool is True:
        generalOptionsWrapper.separator()

        options_general_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, False, False, generalOptionsWrapper)

    #END General Options (Wireframe, Edge colors, etc)

    optionsCol.separator()

    # -----------------------------------------------------------------------------
    #   Overlay Options (Wireframe, Edge colors, etc)
    # -----------------------------------------------------------------------------

    overlayOptionsWrapper = optionsCol.box().column(align=True)

    #create show/hide toggle for options section
    createShowHide(self, context, scene, "neltulzSubD", "toggleOverlayOptionsBool", None, "Display", overlayOptionsWrapper)
    

    if scene.neltulzSubD.toggleOverlayOptionsBool is True:
        overlayOptionsWrapper.separator()

        options_wireframeAndEdgeDisplay_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, False, False, overlayOptionsWrapper)

    #END Overlay Options (Wireframe, Edge colors, etc)

    # -----------------------------------------------------------------------------
    #   Use Advanced Settings Box
    # -----------------------------------------------------------------------------

    optionsCol.separator()
    
    advancedSettingsWrapper = optionsCol.box().column(align=True)

    #create show/hide toggle for options section
    createShowHide(self, context, scene, "neltulzSubD", "showAdvancedSettings", "advancedSettings", "Use Advanced", advancedSettingsWrapper)

    
    if scene.neltulzSubD.showAdvancedSettings:
        advancedSettingsWrapper.separator()

        advancedSettingsWrapper.separator()

        options_advancedSettings_Section(self, context, scene, False, False, advancedSettingsWrapper)

        #END Use Advanced Settings Box

    optionsCol.separator()

    delResetApplyButtons = optionsCol.row(align=True)
    delResetApplyButtons.scale_y = 1.5
    
    op = delResetApplyButtons.operator('ntzqcksubd.deletemodifier', text="Delete", icon="X")
    op = delResetApplyButtons.operator('ntzqcksubd.applymodifier', text="Apply", icon="CHECKMARK")

    optionsCol.separator()     

    op = optionsCol.operator('ntzqcksubd.resetallsettings', text="Reset All Settings", icon="LOOP_BACK")

def options_general_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, bIndent, bWrapInBox, layout):

    #add-on preferences
    prefs = bpy.context.preferences.addons[__package__].preferences

    if bIndent:

        overlayOptionsRow = layout.row(align=True)

        spacer = overlayOptionsRow.column(align=True)
        spacer.label(text="", icon="BLANK1")

        if bWrapInBox: overlayOptionsCol = overlayOptionsRow.box()
        else:          overlayOptionsCol = overlayOptionsRow.column(align=True)

    else:

        if bWrapInBox: overlayOptionsCol = layout.box()
        else:          overlayOptionsCol = layout
        

    subdModePreference = overlayOptionsCol.column(align=True)
    subdModePreference.label(text="SubD Mode Preference:")
    subdModePreference.prop(prefs, 'subdModePreference', text="")

    overlayOptionsCol.separator()
    
    overlayOptionsCol.prop(prefs, 'toggleSubDModes')

    overlayOptionsCol.separator()

    overlayOptionsCol.prop(prefs, 'initialSubDLevel', slider=False, text="Initial SubD Level")
    

def options_wireframeAndEdgeDisplay_Section(self, context, scene, activeObj, selObjs, numSelObjs, neltulzSubD_modifier, bIndent, bWrapInBox, layout):

    if bIndent:

        overlayOptionsRow = layout.row(align=True)

        spacer = overlayOptionsRow.column(align=True)
        spacer.label(text="", icon="BLANK1")

        if bWrapInBox: overlayOptionsCol = overlayOptionsRow.box()
        else:          overlayOptionsCol = overlayOptionsRow.column(align=True)

    else:

        if bWrapInBox: overlayOptionsCol = layout.box()
        else:          overlayOptionsCol = layout
        

    col = overlayOptionsCol.column(align=True)
    col.label(text="Wireframe:")

    row = col.row(align=True)

    row.prop(context.space_data.overlay, "show_wireframes", text="Toggle Wireframe", toggle=True)

    col = overlayOptionsCol.column(align=True)
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


    op = row.operator('ntzqcksubd.togglewireframe', text="ON", depress=subdWireframeON_active)
    op.subDWireframeOn=True

    op = row.operator('ntzqcksubd.togglewireframe', text="OFF", depress=subdWireframeOFF_active)
    op.subDWireframeOn=False
    
    col.separator()

    col = overlayOptionsCol.column(align=True)
    col.label(text="Edge Colors:")
    row = col.row(align=True)
    row.prop(scene.neltulzSubD, "enableAllEdgeColorsBool", text="Enable All", toggle=True)
    row.prop(scene.neltulzSubD, "disableAllEdgeColorsBool", text="Disable All", toggle=True)
    
    
    row = col.row(align=True)
    
    row.prop(context.space_data.overlay, "show_edge_crease", text="Creases", toggle=True)
    row.prop(context.space_data.overlay, "show_edge_sharp", text="Sharp", toggle=True)
    row.prop(context.space_data.overlay, "show_edge_bevel_weight", text="Bevel", toggle=True)
    row.prop(context.space_data.overlay, "show_edge_seams", text="Seams", toggle=True)

def options_advancedSettings_Section(self, context, scene, bIndent, bWrapInBox, layout):

    if bIndent:

        advancedSettingsRow = layout.row(align=True)
        indent = advancedSettingsRow.column(align=True)
        indent.label(text="", icon="BLANK1")

        if bWrapInBox: advancedSettingsCol = advancedSettingsRow.box()
        else:          advancedSettingsCol = advancedSettingsRow.column(align=True)

    else:
        if bWrapInBox: advancedSettingsCol = layout.box()
        else:          advancedSettingsCol = layout.column(align=True)
        


    if scene.neltulzSubD.advancedSettings:
        advancedSettingsCol.enabled = True
    else:
        advancedSettingsCol.enabled = False
    
    row = advancedSettingsCol.row(align=True)
    
    row.prop(scene.neltulzSubD, "useCustomRenderLevel", text="Use Custom Render Level" )

    if scene.neltulzSubD.useCustomRenderLevel:
        col = advancedSettingsCol.column(align=True)
        col.prop(scene.neltulzSubD, "customRenderLevel", text="" )
    
    col = advancedSettingsCol.column(align=True)
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
