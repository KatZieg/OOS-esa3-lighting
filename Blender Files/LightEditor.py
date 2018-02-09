import bpy

from bpy.types import Menu, Panel, UIList


class ViewLightningPanel():
    # where the new panel will be accessable
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

# the new panel
class SetupSelectionPanel(ViewLightningPanel, Panel):
    bl_idname = "panel_setup_selection"
    bl_label = "Select your Setup"
    bl_context = "objectmode"
    bl_category = "LMD"

    # draw a new button, call operator on click
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.portrait_setup_operator", text="Portrait Setup")
        layout.operator("object.packshot_setup_operator", text="Packshot Setup")
        layout.operator("object.grid_setup_operator", text="Grid Setup")

class LampAdjustPanel(ViewLightningPanel, Panel):
    bl_idname = "panel_lampadjust"
    bl_label = "Lamp Adjustment"
    bl_context = "objectmode"
    bl_category = "LMD"

    # draw a new button, call operator on click
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.lamp_selection_operator", text="Select All Lamps")
        layout.operator("object.switchoffalllamps_operator", text="Switch Lamps On / Off")
        #layout.operator("object.remove_fixture_operator", text="Remove Fixture")
        layout.operator("brightness.operator", text="Change Luminosity")
        layout.operator("colour.operator", text="Change Colour")

class ColourOperator(bpy.types.Operator):
    """Color picking by RGB values"""
    bl_idname = "colour.operator"
    bl_label = "Set Colour in Red, Green, Blue"
    redValue = bpy.props.FloatProperty(name="Red", description="Red Proportion", max=1.000, min=0)
    greenValue = bpy.props.FloatProperty(name="Green", description="Green Proportion", max=1.000, min=0)
    blueValue = bpy.props.FloatProperty(name="Blue", description="Blue Proportion", max=1.000, min=0)

    def execute(self, context):
        SetColour(float(self.redValue), float(self.greenValue), float(self.blueValue))
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "redValue")
        col.prop(self, "greenValue")
        col.prop(self, "blueValue")

class BrightnessOperator(bpy.types.Operator):
    """Setting the intensity from 0 to 100"""
    bl_idname = "brightness.operator"
    bl_label = "Set Luminosity"
    defaultValue = 0
    brightnessValue = bpy.props.FloatProperty(name="Luminosity", description="the actual brightness", min=0.001, max=10.000, default=defaultValue) 

    def execute(self, context):
        self.report({'INFO'}, str(self.brightnessValue))
        sce = bpy.context.scene
        for object in sce.objects:
            if object.type != "LAMP":
                continue
            if object.type == "LAMP":
                SetLampStrength(object, float(self.brightnessValue))
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        BrightnessOperator.defaultValue = float(GetLampStrength(context.object))  # proof that the value is set correctly
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "brightnessValue")


class SelectPortraitSetup(bpy.types.Operator):
    """Classic 3-point-lighting portrait setup"""
    bl_idname = "object.portrait_setup_operator"
    bl_label = "Portrait Setup Selection Operator"

    def execute(self, context):
        #add a standin
        #bpy.ops.mesh.primitive_monkey_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

        # add a standin
        bpy.ops.object.lamp_add(type='AREA', radius=1, view_align=False, location=(-2.75, -2.00, 2.3), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        #bpy.context.active_object.name = 'portrait_keylight'
        bpy.context.object.data.distance = 15
        bpy.context.object.data.energy = 0.2
        bpy.context.object.data.color = (1, 0.828055, 0.649111)

        # add a fill
        bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(3.11, -2.02, 1.35), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        bpy.context.object.data.distance = 15
        bpy.context.object.data.energy = 0.1
        bpy.context.object.data.color = (1, 0.828055, 0.649111)

        # backlight
        bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(-3.85, 2.44, 2.26), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        #bpy.context.active_object.name = 'portrait_backlight'
        bpy.context.object.data.distance = 15
        bpy.context.object.data.energy = 0.1
        bpy.context.object.data.color = (1, 0.828055, 0.649111)
        return {'FINISHED'}

class SelectGritSetup(bpy.types.Operator):
    """10 by 10 fixture grid"""
    bl_idname = "object.grid_setup_operator"
    bl_label = "Grid Setup Selection Operator"

    def execute(self, context):
        # make a plane for setting up a table top
        #bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #bpy.ops.transform.resize(value=(-5.0, -5.0, -5.0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(10):
            for j in range(10):
                bpy.ops.object.lamp_add(type='AREA', radius=1, view_align=False, location=(i * 2, -j * 2, 10.0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False, False))
                bpy.context.object.data.distance = 15
                bpy.context.object.data.energy = 0.2
                bpy.context.object.data.color = (1, 0.828055, 0.649111)
        return {'FINISHED'}

class SelectPackshotSetup(bpy.types.Operator):
    """Classic table top packshot setup"""
    bl_idname = "object.packshot_setup_operator"
    bl_label = "Packshot Setup Selection Operator"

    def execute(self, context):
        # make a plane for setting up a table top
        #bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        #bpy.ops.transform.resize(value=(-5.0, -5.0, -5.0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        # make the sides
        bpy.ops.object.lamp_add(type='AREA', radius=1, view_align=False, location=(0, -10, 2.3), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        bpy.context.object.data.distance = 15
        bpy.context.object.data.energy = 0.2
        bpy.context.object.data.color = (1, 0.828055, 0.649111)
        bpy.ops.object.lamp_add(type='AREA', radius=1, view_align=False, location=(0, 10, 2.3), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        bpy.context.object.data.distance = 15
        bpy.context.object.data.energy = 0.2
        bpy.context.object.data.color = (1, 0.828055, 0.649111)

        # make the backlight
        bpy.ops.object.lamp_add(type='AREA', radius=1, view_align=False, location=(-6, 0, 8), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        bpy.context.object.data.distance = 15
        bpy.context.object.data.energy = 0.15
        bpy.context.object.data.color = (1, 0.828055, 0.649111)

        # make some accents
        bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(5, 3, 5), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False))
        bpy.context.object.data.distance = 15
        bpy.context.object.data.energy = 0.15
        bpy.context.object.data.color = (1, 0.828055, 0.649111)
        return {'FINISHED'}

#remove selected fixture
# class RemoveFixtureOperator(bpy.types.Operator):
#     """Removes the selected fixtures"""
#     bl_idname = "object.remove_fixture_operator"
#     bl_label = "Remove Fixture Operator"
#
#     def execute(self, context):
#         remove_fixture= bpy.ops.object.delete(use_global=False)
#         return {'FINISHED'}

class SwitchOffAllLampsOperator(bpy.types.Operator):
    """Switches off all fixtures"""
    bl_idname = "object.switchoffalllamps_operator"
    bl_label = "Simple Lamp Switch Off Operator"
    oldLampStrength = 200
        
    def execute(self, context):
        sce = bpy.context.scene
        for object in sce.objects:
            if object.type != "LAMP":
                continue
        
            if object.type == "LAMP":
                currentLampStrength = float(GetLampStrength(context.object))

                if currentLampStrength != 0:
                    if SwitchOffAllLampsOperator.oldLampStrength != currentLampStrength:
                        SwitchOffAllLampsOperator.oldLampStrength = currentLampStrength
        
                    SetLampStrength(object, 0)
                elif currentLampStrength == 0:
        
                    SetLampStrength(object, SwitchOffAllLampsOperator.oldLampStrength)
      
        return {'FINISHED'}

def SetColour(red, green, blue):
    sce = bpy.context.scene
    for object in sce.objects:
        if object.type != "LAMP":
                continue
        if object.type == "LAMP":
            object.data.color = (red, green, blue)
    return {'FINISHED'}

def SetLampStrength(object, lampStrength):
    helligkeit = lampStrength
    object.data.energy = helligkeit
    return {'FINISHED'}

def GetLampStrength(lamp):
    return lamp.data.energy
    return {'FINISHED'}

# operator for button
class SelectAllLampsOperator(bpy.types.Operator):
    """Selects all fixtures"""
    bl_idname = "object.lamp_selection_operator"
    bl_label = "Simple Lamp Selection Operator"

    def execute(self, context):
        SelectAllLamps(context)
        return {'FINISHED'}

# function for operator
def SelectAllLamps(context):
    sce = bpy.context.scene
    for object in sce.objects:
        if object.type != "LAMP":
            object.select = False
        else:
            object.select = True

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()