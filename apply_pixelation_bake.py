import bpy
import asyncio

async def apply_pixelation_and_bake(models, pixelation_node_name, output_directory, resolution=256, bake_resolution=512):
    scene = bpy.context.scene
    bake_settings = scene.render.bake
    
    # Starting settings
    start_render_engine = scene.render.engine
    start_pass_direct = bake_settings.use_pass_direct
    start_pass_indirect = bake_settings.use_pass_indirect
    start_pass_color = bake_settings.use_pass_color
    start_samples = scene.cycles.samples
    
    # Prepare settings for baking process
    scene.render.engine = "CYCLES"
    scene.cycles.bake_type = 'DIFFUSE'
    
    bake_settings.use_pass_direct = False
    bake_settings.use_pass_indirect = False
    bake_settings.use_pass_color = True
    
    scene.cycles.samples = 1
    
    # Loop through selected models
    for obj in models:
        # Make sure selected are valid
        if not obj.data.materials or not obj.type == 'MESH':
            continue
        
        if len(obj.data.polygons) <= 0:
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
        
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        for mat in obj.data.materials:
            if not mat.use_nodes:
                mat.use_nodes = True
            
            node_tree = mat.node_tree
            nodes = node_tree.nodes
            
            found_tex = False
            
            for node in mat.node_tree.nodes:
                # Find BSDF node
                if node.type == 'BSDF_PRINCIPLED':
                    # Get base color input socket
                    base_color_input = node.inputs['Base Color']
                    p_node = node
                    
                    if base_color_input.is_linked:
                        # Get base attached node
                        linked_node = base_color_input.links[0].from_node
                        
                        # Make sure it is a texture
                        if linked_node.type == 'TEX_IMAGE':
                            tex_image = linked_node
                            found_tex = True
                            
                            # Create a new pixel node, or store it if it already exists
                            if pixelation_node_name not in nodes:
                                pixel_node = nodes.new(type="ShaderNodeGroup")
                                pixel_node.node_tree = bpy.data.node_groups[pixelation_node_name]
                            else:
                                pixel_node = nodes[pixelation_node_name]
                            
                            # Set correct input values and attach pixel node to image texture
                            pixel_node.inputs['Resolution'].default_value = resolution
                            node_tree.links.new(pixel_node.outputs['Vector'], tex_image.inputs['Vector'])
            
            # Move on to next mesh if base color texture can't be found    
            if not found_tex:
                continue
            
            # In materials loop
            # Set up settings for a proper bake
            start_metallic = p_node.inputs['Metallic'].default_value
            p_node.inputs['Metallic'].default_value = 0
            
            # Create image and file to store result
            bake_tex = nodes.new(type="ShaderNodeTexImage")
            bake_image = bpy.data.images.new(name=f"{obj.name}_Baked", width=bake_resolution, height=bake_resolution)
            bake_tex.image = bake_image
            
            p_node.select = False
            bake_tex.select = True
            nodes.active=bake_tex
            
            bpy.ops.object.bake(type='DIFFUSE')
            
            # Bake done
            bake_image.filepath_raw = f"{output_directory}/{obj.name}_base_color.png"
            bake_image.file_format = 'PNG'
            bake_image.save()
            
            # Reset settings after bake
            p_node.inputs['Metallic'].default_value = start_metallic
            bake_tex.image = bpy.data.images.load(f"{output_directory}/{obj.name}_base_color.png")
            node_tree.links.new(bake_tex.outputs['Color'], p_node.inputs['Base Color'])
            
            # Remove old nodes
            nodes.remove(pixel_node)
            nodes.remove(tex_image)
    
    # Reset settings back to original
    scene.render.engine = start_render_engine
    bake_settings.use_pass_direct = start_pass_direct
    bake_settings.use_pass_indirect = start_pass_indirect
    bake_settings.use_pass_color = start_pass_color
    scene.cycles.samples = start_samples
    
#def split_list(input_list, batch_size):
#    return [input_list[i:i + batch_size] for i in range(0, len(input_list), batch_size)]
#
#async def bake_in_batches(objects, pixelation_node_group_name, output_dir, resolution, bake_resolution, batch_size):
#    batches = split_list(objects, batch_size)
#    
#    for batch in batches:
#        await apply_pixelation_and_bake(batch, pixelation_node_group_name, output_dir, resolution, bake_resolution)
#        
#        await asyncio.sleep(0.3)
