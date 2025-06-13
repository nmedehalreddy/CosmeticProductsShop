import bpy
import sys

argv = sys.argv[sys.argv.index("--") + 1:]
input_file = argv[0]
output_file = argv[1]

bpy.ops.wm.read_factory_settings(use_empty=True)

# Auto-detect format
if input_file.endswith(".fbx"):
    bpy.ops.import_scene.fbx(filepath=input_file)
elif input_file.endswith(".stl"):
    bpy.ops.import_mesh.stl(filepath=input_file)
elif input_file.endswith(".gltf") or input_file.endswith(".glb"):
    bpy.ops.import_scene.gltf(filepath=input_file)
else:
    raise Exception("Unsupported format")

bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB')
