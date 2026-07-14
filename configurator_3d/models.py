from django.db import models
from django.utils.translation import gettext_lazy as _


class SceneConfig(models.Model):
    """
    One-to-one link from a configurable Product to its 3D scene configuration.
    Stores the base GLB model, parsed scene graph, viewer settings, and
    references to geometry/texture assets.
    """

    product = models.OneToOneField(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="scene_3d",
        verbose_name=_("Product"),
        limit_choices_to={"product_type": "configurable"},
    )
    base_model = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scene_configs",
        verbose_name=_("Base 3D Model"),
        help_text=_("The main GLB file containing the assembled 3D model."),
    )
    node_tree = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Node Tree"),
        help_text=_("Parsed scene graph from the GLB file (auto-populated)."),
    )

    # Viewer settings
    camera_orbit = models.CharField(
        max_length=100,
        default="0deg 75deg 2m",
        verbose_name=_("Camera Orbit"),
        help_text=_("model-viewer camera-orbit attribute."),
    )
    camera_target = models.CharField(
        max_length=100,
        default="0m 0m 0m",
        verbose_name=_("Camera Target"),
        help_text=_("model-viewer camera-target attribute."),
    )
    environment_image = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Environment Image"),
        help_text=_("HDR environment map for image-based lighting."),
    )
    exposure = models.FloatField(
        default=1.0,
        verbose_name=_("Exposure"),
    )
    shadow_intensity = models.FloatField(
        default=0.5,
        verbose_name=_("Shadow Intensity"),
    )
    shadow_softness = models.FloatField(
        default=0.5,
        verbose_name=_("Shadow Softness"),
        help_text=_("Shadow blur amount. 0 = sharp, 1 = soft."),
    )
    tone_mapping = models.CharField(
        max_length=20,
        default="commerce",
        verbose_name=_("Tone Mapping"),
        help_text=_(
            "Color grading algorithm. Commerce = vibrant, Neutral = accurate, ACES = cinematic."
        ),
    )
    bloom_strength = models.FloatField(
        default=0.0,
        verbose_name=_("Bloom Strength"),
        help_text=_("Glow intensity for emissive materials. 0 = off, 1-5 = subtle to dramatic."),
    )
    auto_rotate = models.BooleanField(
        default=True,
        verbose_name=_("Auto Rotate"),
    )
    ar_enabled = models.BooleanField(
        default=True,
        verbose_name=_("AR Enabled"),
        help_text=_("Enable augmented reality viewing on supported devices."),
    )
    background_color = models.CharField(
        max_length=512,
        default="#ffffff",
        verbose_name=_("Background"),
        help_text=_("Solid hex color or CSS gradient."),
    )
    thumbnail = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Thumbnail"),
        help_text=_("Preview screenshot captured from the 3D viewer."),
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Enabled"),
        help_text=_("When disabled, the product uses the standard 2D configurator."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("3D Scene Configuration")
        verbose_name_plural = _("3D Scene Configurations")

    def __str__(self):
        return f"3D Scene: {self.product.name}"


class NodeMapping(models.Model):
    """
    Maps a ConfigurationSlotOption to a 3D visual action.
    Multiple mappings per option are allowed (e.g., change color + hide node).
    """

    ACTION_TYPES = [
        ("material_color", _("Material Color")),
        ("material_texture", _("Material Texture")),
        ("geometry_swap", _("Geometry Swap")),
        ("visibility", _("Visibility")),
    ]

    scene_config = models.ForeignKey(
        SceneConfig,
        on_delete=models.CASCADE,
        related_name="mappings",
        verbose_name=_("Scene Config"),
    )
    slot_option = models.ForeignKey(
        "catalog.ConfigurationSlotOption",
        on_delete=models.CASCADE,
        related_name="visual_mappings",
        verbose_name=_("Slot Option"),
    )
    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
        verbose_name=_("Action Type"),
    )
    target_node = models.CharField(
        max_length=200,
        verbose_name=_("Target Node"),
        help_text=_("Scene graph node name from the parsed node tree."),
    )
    action_data = models.JSONField(
        default=dict,
        verbose_name=_("Action Data"),
        help_text=_("Action-specific payload (color, texture URLs, GLB URL, visibility)."),
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Node Mapping")
        verbose_name_plural = _("Node Mappings")
        ordering = ["sort_order", "pk"]
        indexes = [
            models.Index(fields=["scene_config", "slot_option"]),
        ]

    def __str__(self):
        return f"{self.slot_option} → {self.action_type} on {self.target_node}"


class GeometryAsset(models.Model):
    """
    Separate GLB file for geometry swaps (e.g., different collar shapes).
    """

    scene_config = models.ForeignKey(
        SceneConfig,
        on_delete=models.CASCADE,
        related_name="geometry_assets",
        verbose_name=_("Scene Config"),
    )
    label = models.CharField(
        max_length=200,
        verbose_name=_("Label"),
        help_text=_('e.g., "V-Neck Collar"'),
    )
    media_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="geometry_usages",
        verbose_name=_("GLB File"),
    )
    target_node = models.CharField(
        max_length=200,
        verbose_name=_("Target Node"),
        help_text=_("Which base model node to replace."),
    )
    node_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Node Data"),
        help_text=_("Parsed node names from this GLB."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Geometry Asset")
        verbose_name_plural = _("Geometry Assets")

    def __str__(self):
        return f"{self.label} ({self.target_node})"


class TextureAsset(models.Model):
    """
    Texture image for material mappings.
    """

    TEXTURE_TYPES = [
        ("base_color", _("Base Color")),
        ("normal", _("Normal Map")),
        ("roughness", _("Roughness Map")),
        ("metalness", _("Metalness Map")),
        ("ao", _("Ambient Occlusion")),
        ("emissive", _("Emissive Map")),
    ]

    scene_config = models.ForeignKey(
        SceneConfig,
        on_delete=models.CASCADE,
        related_name="textures",
        verbose_name=_("Scene Config"),
    )
    label = models.CharField(
        max_length=200,
        verbose_name=_("Label"),
        help_text=_('e.g., "Red Leather"'),
    )
    media_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="texture_usages",
        verbose_name=_("Texture Image"),
    )
    texture_type = models.CharField(
        max_length=20,
        choices=TEXTURE_TYPES,
        verbose_name=_("Texture Type"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Texture Asset")
        verbose_name_plural = _("Texture Assets")

    def __str__(self):
        return f"{self.label} ({self.get_texture_type_display()})"
