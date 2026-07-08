"""
Frontend serialization for 3D scene data.

Builds an optimized structure keyed by ConfigurationSlotOption.id
for O(1) lookup on the frontend when selections change.
"""


def serialize_scene_3d(scene):
    """
    Serialize a SceneConfig into a frontend-optimized dict.

    Args:
        scene: SceneConfig instance (with prefetched mappings, geometry_assets, textures)

    Returns:
        dict: Serialized scene data for frontend consumption:
        {
            "base_model_url": "/media/.../model.glb",
            "camera_orbit": "0deg 75deg 2m",
            "camera_target": "0m 0m 0m",
            "exposure": 1.0,
            "shadow_intensity": 0.5,
            "auto_rotate": true,
            "ar_enabled": true,
            "background_color": "#ffffff",
            "environment_url": null,
            "node_tree": {...},
            "mappings": {
                "42": [  // keyed by slot_option_id
                    {"action": "material_color", "node": "Body", "data": {...}}
                ]
            },
            "geometry_assets": {
                "uuid": {"url": "/media/.../collar.glb", "label": "V-Neck"}
            }
        }
    """
    if not scene or not scene.base_model:
        return None

    # Base model URL
    base_model_url = scene.base_model.original_file.url if scene.base_model.original_file else None

    # Environment image URL
    environment_url = None
    if scene.environment_image and scene.environment_image.original_file:
        environment_url = scene.environment_image.original_file.url

    # Mappings keyed by slot_option_id
    mappings = {}
    for mapping in scene.mappings.all():
        option_id = str(mapping.slot_option_id)
        if option_id not in mappings:
            mappings[option_id] = []
        mappings[option_id].append({
            "action": mapping.action_type,
            "node": mapping.target_node,
            "data": mapping.action_data,
        })

    # Geometry assets keyed by media_asset UUID
    geometry_assets = {}
    for ga in scene.geometry_assets.all():
        if ga.media_asset and ga.media_asset.original_file:
            geometry_assets[str(ga.media_asset_id)] = {
                "url": ga.media_asset.original_file.url,
                "label": ga.label,
                "target_node": ga.target_node,
            }

    # Texture assets keyed by media_asset UUID
    textures = {}
    for ta in scene.textures.all():
        if ta.media_asset and ta.media_asset.original_file:
            textures[str(ta.media_asset_id)] = {
                "url": ta.media_asset.original_file.url,
                "label": ta.label,
                "texture_type": ta.texture_type,
            }

    return {
        "base_model_url": base_model_url,
        "camera_orbit": scene.camera_orbit,
        "camera_target": scene.camera_target,
        "exposure": scene.exposure,
        "shadow_intensity": scene.shadow_intensity,
        "shadow_softness": scene.shadow_softness,
        "tone_mapping": scene.tone_mapping,
        "bloom_strength": scene.bloom_strength,
        "auto_rotate": scene.auto_rotate,
        "ar_enabled": scene.ar_enabled,
        "background_color": scene.background_color,
        "environment_url": environment_url,
        "node_tree": scene.node_tree,
        "mappings": mappings,
        "geometry_assets": geometry_assets,
        "textures": textures,
    }
