bl_info = {
    "name": "Pixelation Baking",
    "author": "Trashy aka Simon",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > N",
    "description": "Pixelates and bakes base color of selected objects",
    "category": "UV"
}

import bpy
import time
import asyncio
from bpy.types import (Panel, Operator)
from bpy.props import StringProperty, IntProperty, BoolProperty, PointerProperty
from bpy.utils import register_class, unregister_class
from . import apply_pixelation_bake
from .append_pixelation_group import append_from_asset

class ButtonOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "pixelation.1"
    bl_label = "Pixelation Operator"

    def execute(self, context):
        # From AddonProperties
        properties = context.scene.pixelation_bake_settings
        
        # Define parameters
        models_to_process = bpy.context.selected_objects
        pixelation_node_group_name = "Pixelation"
        output_dir = properties.directory_path
        p_res = properties.pixel_resolution
        t_res = properties.texture_resolution
        
        # Make sure directory has been picked
        if not output_dir:
            self.report({'ERROR'}, "No save directory selected. Please pick a path to save baked textures.")
            
            return {'CANCELLED'}
        
        start_time = time.time()
        
        # Run the function
        asyncio.run(apply_pixelation_bake.apply_pixelation_and_bake(models_to_process, pixelation_node_group_name, output_dir, p_res, t_res))
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        self.report({'INFO'}, f"Baking complete after: {round(elapsed_time, 2)} seconds! Textures saved at: " + output_dir)
        
        return {'FINISHED'}

class PixelationPanel(bpy.types.Panel):
    bl_label = "Pixelation Baking Panel"
    bl_idname = "OBJECT_PT_pixelation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        properties = context.scene.pixelation_bake_settings
        
        layout.prop(properties, "directory_path")
        layout.label(text="Settings")
        
        layout.prop(properties, "pixel_resolution")
        layout.prop(properties, "texture_resolution")
        layout.separator()
        
        row = layout.row()
        row.operator(ButtonOperator.bl_idname, text="Pixelate and Bake")

class AddonProperties(bpy.types.PropertyGroup):
    directory_path: StringProperty(
        name="Texture Path",
        description="The folder to store the baked pixelated color textures.",
        subtype='DIR_PATH'
    )

    pixel_resolution: IntProperty(
        name="Pixelation Resolution",
        description="The new visual resolution of the base color.",
        default=256,
        min=1
    )

    texture_resolution: IntProperty(
        name="Texture Resolution",
        description="The size of the baked texture image.",
        default=1024,
        min=1
    )

_classes = [
    ButtonOperator,
    PixelationPanel,
    AddonProperties
]

def register():
    for cls in _classes:
        register_class(cls)
        
    bpy.types.Scene.pixelation_bake_settings = PointerProperty(type=AddonProperties)
    
    # Wait to let main Blender thread load node_groups in bpy.data.
    bpy.app.timers.register(append_from_asset)

def unregister():
    for cls in _classes:
        unregister_class(cls)
        
    del bpy.types.Scene.pixelation_bake_settings

if __name__ == "__main__":
    register()
