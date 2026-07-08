"""
GLB/glTF parser service for extracting scene graph structure.

Uses pygltflib to parse GLB files server-side and extract node names,
material names, and hierarchy. This information is stored in SceneConfig.node_tree
and used by the admin mapping UI to let merchants map configurator options
to 3D scene nodes.
"""
import logging
import tempfile
import os

logger = logging.getLogger(__name__)


def parse_glb(file_obj):
    """
    Parse a GLB/glTF file and extract the scene graph.

    Args:
        file_obj: A file-like object (Django FieldFile, InMemoryUploadedFile, etc.)

    Returns:
        dict: Parsed scene graph structure:
        {
            "version": 1,
            "root_nodes": ["Scene"],
            "nodes": {
                "NodeName": {
                    "children": ["ChildName1"],
                    "mesh": "mesh_name" or null,
                    "materials": ["mat_name1"]
                }
            },
            "materials": {
                "mat_name": {
                    "index": 0,
                    "base_color": [1.0, 1.0, 1.0, 1.0],
                    "metallic": 0.0,
                    "roughness": 1.0
                }
            }
        }
    """
    try:
        from pygltflib import GLTF2
    except ImportError:
        logger.error("pygltflib not installed. Run: pip install pygltflib")
        return {"error": "pygltflib not installed", "version": 1, "root_nodes": [], "nodes": {}, "materials": {}}

    # Write to temp file if needed (pygltflib needs a file path for GLB)
    tmp_path = None
    try:
        if hasattr(file_obj, 'path'):
            # Direct file on disk
            file_path = file_obj.path
        elif hasattr(file_obj, 'temporary_file_path'):
            # Django temp upload
            file_path = file_obj.temporary_file_path()
        else:
            # In-memory file — write to temp
            suffix = '.glb'
            if hasattr(file_obj, 'name') and file_obj.name:
                _, ext = os.path.splitext(file_obj.name)
                if ext:
                    suffix = ext
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            file_obj.seek(0)
            for chunk in _iter_chunks(file_obj):
                tmp.write(chunk)
            tmp.close()
            tmp_path = tmp.name
            file_path = tmp_path

        gltf = GLTF2().load(file_path)
        return _extract_scene_graph(gltf)

    except Exception as e:
        logger.error(f"Error parsing GLB file: {e}")
        return {"error": str(e), "version": 1, "root_nodes": [], "nodes": {}, "materials": {}}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def _iter_chunks(file_obj, chunk_size=8192):
    """Iterate over file-like object in chunks."""
    if hasattr(file_obj, 'chunks'):
        yield from file_obj.chunks()
    else:
        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break
            yield chunk


def _extract_scene_graph(gltf):
    """Extract scene graph from a parsed GLTF2 object."""
    result = {
        "version": 2,
        "root_nodes": [],
        "nodes": {},
        "materials": {},
    }

    # Known glTF extensions to detect on materials
    _KNOWN_EXTENSIONS = {
        'KHR_materials_clearcoat',
        'KHR_materials_transmission',
        'KHR_materials_ior',
        'KHR_materials_unlit',
        'KHR_materials_sheen',
        'KHR_materials_specular',
        'KHR_materials_iridescence',
        'KHR_materials_anisotropy',
        'KHR_materials_volume',
        'KHR_materials_emissive_strength',
    }

    # Parse materials
    if gltf.materials:
        for idx, mat in enumerate(gltf.materials):
            mat_name = mat.name or f"material_{idx}"
            mat_data = {
                "index": idx,
                # PBR metallic-roughness
                "base_color": [1.0, 1.0, 1.0, 1.0],
                "metallic": 1.0,
                "roughness": 1.0,
                # Emissive
                "emissive_color": [0.0, 0.0, 0.0],
                "emissive_strength": 0.0,
                # Alpha
                "alpha_mode": "OPAQUE",
                "alpha_cutoff": 0.5,
                "double_sided": False,
                # Texture flags
                "has_base_color_texture": False,
                "has_metallic_roughness_texture": False,
                "has_normal_texture": False,
                "has_occlusion_texture": False,
                "has_emissive_texture": False,
                # Extensions present
                "extensions": [],
            }

            # PBR metallic-roughness properties
            if mat.pbrMetallicRoughness:
                pbr = mat.pbrMetallicRoughness
                if pbr.baseColorFactor:
                    mat_data["base_color"] = list(pbr.baseColorFactor)
                if pbr.metallicFactor is not None:
                    mat_data["metallic"] = pbr.metallicFactor
                if pbr.roughnessFactor is not None:
                    mat_data["roughness"] = pbr.roughnessFactor
                mat_data["has_base_color_texture"] = pbr.baseColorTexture is not None
                mat_data["has_metallic_roughness_texture"] = pbr.metallicRoughnessTexture is not None

            # Emissive properties
            if mat.emissiveFactor and any(c > 0 for c in mat.emissiveFactor):
                mat_data["emissive_color"] = list(mat.emissiveFactor)
            mat_data["has_emissive_texture"] = mat.emissiveTexture is not None

            # KHR_materials_emissive_strength extension
            mat_ext = mat.extensions or {}
            if 'KHR_materials_emissive_strength' in mat_ext:
                ext = mat_ext['KHR_materials_emissive_strength']
                if isinstance(ext, dict) and 'emissiveStrength' in ext:
                    mat_data["emissive_strength"] = float(ext['emissiveStrength'])

            # Alpha properties
            if mat.alphaMode:
                mat_data["alpha_mode"] = mat.alphaMode
            if mat.alphaCutoff is not None:
                mat_data["alpha_cutoff"] = mat.alphaCutoff
            mat_data["double_sided"] = bool(mat.doubleSided)

            # Texture flags
            mat_data["has_normal_texture"] = mat.normalTexture is not None
            mat_data["has_occlusion_texture"] = mat.occlusionTexture is not None

            # Detect known extensions
            if mat_ext:
                mat_data["extensions"] = sorted(
                    ext_name for ext_name in mat_ext if ext_name in _KNOWN_EXTENSIONS
                )

            result["materials"][mat_name] = mat_data

    # Build node lookup (index → name)
    node_names = {}
    if gltf.nodes:
        for idx, node in enumerate(gltf.nodes):
            node_names[idx] = node.name or f"node_{idx}"

    # Parse nodes
    if gltf.nodes:
        for idx, node in enumerate(gltf.nodes):
            name = node_names[idx]
            node_data = {
                "children": [],
                "mesh": None,
                "materials": [],
            }

            # Children
            if node.children:
                node_data["children"] = [node_names.get(c, f"node_{c}") for c in node.children]

            # Mesh and materials
            if node.mesh is not None and gltf.meshes:
                mesh = gltf.meshes[node.mesh]
                node_data["mesh"] = mesh.name or f"mesh_{node.mesh}"

                # Collect materials used by this mesh's primitives
                seen_mats = set()
                if mesh.primitives:
                    for prim in mesh.primitives:
                        if prim.material is not None and gltf.materials:
                            mat = gltf.materials[prim.material]
                            mat_name = mat.name or f"material_{prim.material}"
                            if mat_name not in seen_mats:
                                seen_mats.add(mat_name)
                                node_data["materials"].append(mat_name)

            result["nodes"][name] = node_data

    # Find root nodes from scenes
    if gltf.scenes:
        for scene in gltf.scenes:
            if scene.nodes:
                for root_idx in scene.nodes:
                    root_name = node_names.get(root_idx, f"node_{root_idx}")
                    result["root_nodes"].append(root_name)

    return result


def parse_glb_from_media_asset(media_asset):
    """
    Parse a GLB file from a MediaAsset instance.

    Args:
        media_asset: MediaAsset instance with a GLB file

    Returns:
        dict: Parsed scene graph (same as parse_glb)
    """
    if not media_asset or not media_asset.original_file:
        return {"error": "No file", "version": 1, "root_nodes": [], "nodes": {}, "materials": {}}

    return parse_glb(media_asset.original_file)
