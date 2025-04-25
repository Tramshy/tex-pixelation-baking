import bpy
import os

PIXELATION = "Pixelation"

def is_pixelation_group_missing():
    return PIXELATION not in bpy.data.node_groups

def append_from_asset():
    if not is_pixelation_group_missing():
        return
    
    addon_dir = os.path.dirname(__file__)
    blend_path = os.path.join(addon_dir, "assets/pixelation_assets.blend")
    node_group_path = os.path.join(blend_path, "NodeTree")
    
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if PIXELATION in data_from.node_groups:
            data_to.node_groups = [PIXELATION]
