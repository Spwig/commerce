---
slug: 3d-configurator
title_i18n_key: 3D Product Configurator
category: products
component: configurator_3d
keywords:
  - 3D configurator
  - 3D product viewer
  - product customization
  - 3D model
  - GLB file
  - scene configuration
  - augmented reality
  - AR product view
  - material color
  - texture swap
  - geometry swap
  - configurable product
  - product visualizer
  - 3D scene
url_patterns:
  - /admin/configurator_3d/sceneconfig/
related:
  - add-product
  - configurable-products
published: true
---

The 3D Configurator lets your customers view configurable products in an interactive 3D viewer directly on the product page. As customers select options — such as colours, materials, or component variations — the 3D model updates in real time to reflect their choices. On supported mobile devices, customers can also view the product in augmented reality (AR), placing it virtually in their own space before purchasing.

The 3D Configurator works with configurable products. Each configurable product can have one 3D scene configuration that links a GLB model file to the product's configuration options.

## Before you begin

To set up a 3D scene, you need:

- A **configurable product** already created in your catalog
- A **base 3D model** uploaded to your Media Library as a GLB file — this is the assembled model that appears by default
- Optionally, additional GLB files for geometry swaps (e.g., different collar shapes), and texture images for material variations

If you have not already created the configurable product and its configuration options, do that first before setting up the 3D scene.

## Creating a scene configuration

1. Navigate to **Catalog > 3D Scene Configurations**
2. Click **+ Add 3D Scene Configuration**
3. Select the **Product** this scene belongs to — only configurable products are available
4. Choose the **Base 3D Model** from your Media Library — this is the GLB file that loads by default
5. Configure the viewer settings (see below)
6. Save the record

After saving, the **Node Tree** field populates automatically. This is the parsed scene graph extracted from your GLB file — it lists every named node inside the model, which you will reference when adding node mappings.

## Viewer settings

These settings control how the 3D viewer appears on your product page.

### Camera and lighting

| Field | Description | Default |
|-------|-------------|---------|
| **Camera Orbit** | Starting camera position in the format `angle elevation distance` (e.g., `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Camera Target** | The point the camera looks at, in metres from the model centre (e.g., `0m 0m 0m`) | `0m 0m 0m` |
| **Environment Image** | An HDR image from your Media Library used for image-based lighting — gives more realistic reflections and shadows | None |
| **Exposure** | Overall brightness of the scene — lower values are darker, higher values are brighter | `1.0` |

### Shadows

| Field | Description | Default |
|-------|-------------|---------|
| **Shadow Intensity** | How strong the shadow cast beneath the model appears — `0` is no shadow, `1` is full intensity | `0.5` |
| **Shadow Softness** | How blurred the shadow edges are — `0` is sharp, `1` is very soft | `0.5` |

### Colour grading

| Field | Description |
|-------|-------------|
| **Tone Mapping** | The colour grading algorithm applied to the scene. **Commerce** produces vibrant, product-friendly colours. **Neutral** is colour-accurate. **ACES** gives a cinematic film look. |
| **Bloom Strength** | Adds a glow effect to emissive (self-lit) parts of the model. `0` disables bloom. Values between `1` and `5` produce subtle to dramatic glow. |

### Behaviour and background

| Field | Description | Default |
|-------|-------------|---------|
| **Auto Rotate** | Whether the model slowly spins on load to catch the customer's attention | On |
| **AR Enabled** | Whether customers on supported devices see an **View in AR** button | On |
| **Background** | The viewer's background colour or CSS gradient — enter a hex colour (e.g., `#f5f5f5`) or a CSS gradient value | `#ffffff` |

### Thumbnail

The **Thumbnail** field holds a preview screenshot of the 3D viewer, shown before the viewer loads. You can capture a screenshot from the live product page and upload it to your Media Library, then link it here for a smoother page load experience.

## Enabling and disabling the 3D viewer

The **Enabled** toggle controls whether the 3D viewer is shown on the product page. When disabled, the product falls back to the standard 2D image configurator. This lets you prepare a scene configuration before making it visible to customers.

## Connecting configuration options to 3D actions

Once the base scene is configured, you can link each configuration slot option to a visual change in the 3D model. These links are called **Node Mappings** and are added in the **Node Mappings** section at the bottom of the scene configuration form.

### Node mapping fields

| Field | Description |
|-------|-------------|
| **Slot Option** | The configuration option that triggers this change (e.g., "Red Leather") |
| **Action Type** | What visual change happens (see action types below) |
| **Target Node** | The name of the scene graph node that changes — choose from the names listed in your **Node Tree** |
| **Action Data** | Action-specific data such as a colour hex code, texture URL, or GLB file URL |
| **Sort Order** | Controls the order in which multiple mappings for the same option are applied |

### Action types

| Action | What it does |
|--------|-------------|
| **Material Color** | Changes the colour of a material on the target node — provide a hex colour in **Action Data** |
| **Material Texture** | Swaps the texture applied to a material — link to a texture image asset in **Action Data** |
| **Geometry Swap** | Replaces a part of the model with a different GLB file — useful for structural changes like a different handle shape |
| **Visibility** | Shows or hides a node in the scene — set `visible: true` or `visible: false` in **Action Data** |

Multiple mappings can be added for a single slot option. For example, selecting "Blue Denim" might change the material colour *and* hide a leather trim node at the same time.

## Geometry assets

If your configuration includes **Geometry Swap** actions, you need to register the replacement GLB files as Geometry Assets. These are added in the **Geometry Assets** section of the scene configuration form.

| Field | Description |
|-------|-------------|
| **Label** | Descriptive name for this geometry asset, e.g., "V-Neck Collar" |
| **GLB File** | The replacement GLB file from your Media Library |
| **Target Node** | Which node in the base model this geometry replaces |

After saving a Geometry Asset, its node names are parsed from the GLB and stored in **Node Data**, making them available as target nodes in your mappings.

## Texture assets

Texture images used in **Material Texture** mappings can be registered as Texture Assets for easier reference. These are added in the **Texture Assets** section.

| Field | Description |
|-------|-------------|
| **Label** | Descriptive name, e.g., "Red Leather" |
| **Texture Image** | The texture image from your Media Library |
| **Texture Type** | The PBR channel this texture applies to — Base Color, Normal Map, Roughness Map, Metalness Map, Ambient Occlusion, or Emissive Map |

## Example: configurable jacket with colour options

**Scenario:** A jacket that can be ordered in Black, Navy, or Burgundy, with each colour applied to the jacket body mesh.

**Setup:**

1. Create a scene configuration for the jacket product with the assembled jacket GLB as the base model
2. Set **Tone Mapping** to Commerce and **Auto Rotate** to on
3. In Node Mappings, add three entries — one per colour option:

| Slot Option | Action Type | Target Node | Action Data |
|-------------|-------------|-------------|-------------|
| Black | Material Color | JacketBody | `{"color": "#1a1a1a"}` |
| Navy | Material Color | JacketBody | `{"color": "#1b2a4a"}` |
| Burgundy | Material Color | JacketBody | `{"color": "#6b2737"}` |

When a customer selects Navy on the product page, the viewer instantly updates the JacketBody material to the navy colour.

## Tips

- Name your GLB nodes clearly when creating your 3D model — node names like "JacketBody" or "CollarMesh" are much easier to work with than auto-generated names like "Mesh_023"
- Use the **Commerce** tone mapping for most products — it is tuned for vibrant, appealing product presentation
- Disable **Auto Rotate** for products where the default camera angle already shows the most important features, to avoid disorienting the customer on load
- Test the AR button on an actual mobile device before promoting it — AR availability depends on the customer's device and browser (iOS Safari and Android Chrome with WebXR support are the most reliable)
- Upload a **Thumbnail** image for every scene configuration — this prevents a blank white box from flashing while the 3D viewer loads
- If the 3D viewer is not ready yet, disable it with the **Enabled** toggle so customers see the standard image configurator instead
