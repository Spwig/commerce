---
slug: media-library
title_i18n_key: Media Library
category: store-config
component: media_library
keywords:
  - media library
  - image
  - upload
  - media
  - photo
  - video
  - file
  - gallery
  - folder
  - tag
  - thumbnail
  - WebP
  - image preset
  - media asset
  - upload queue
  - recycle bin
  - focal point
url_patterns:
  - /admin/media_library/mediaasset/
  - /admin/media_library/imagesizepreset/
related:
  - add-product
  - page-builder
  - blog-management
published: true
---

The Media Library is the central hub for managing all images, videos, 3D models, and files used across your store. Upload files by dragging them in, organize with folders and tags, and let the system automatically optimize images for fast loading.

![Media Gallery](/static/core/admin/img/help/media-library/media-gallery.webp)

## Gallery Interface

Navigate to **Media Library** in the sidebar to open the gallery. The interface has three areas:

| Area | Location | Purpose |
|------|----------|---------|
| **Upload Zone** | Left sidebar, top | Drag and drop files to upload (images, videos, 3D models up to 100MB) |
| **Folders & Tags** | Left sidebar, below | Browse folders, filter by tags, access Recycle Bin |
| **Media Grid** | Main area | Search, filter, browse, and manage all your assets |

### Toolbar Controls

The toolbar above the media grid provides:

- **Search** — find assets by title, alt text, description, or tag name
- **Type filter** — show only Images, Videos, or 3D Models
- **Size filter** — filter by file size (Small, Medium, Large)
- **Bulk actions** — Select Items, Edit Details, Delete Selected
- **View modes** — Grid (large), Small Grid, or List view (persisted across sessions)

## Uploading Files

Drag one or more files onto the **Upload** zone in the left sidebar, or click the zone to open a file picker.

### Supported Formats

| Type | Formats |
|------|---------|
| **Images** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Videos** | MP4, WebM, MOV, MKV, AVI |
| **3D Models** | GLB, glTF |

### Upload Queue

When uploading multiple files, a queue manager appears showing:

- Each file's name and upload progress bar
- Concurrent uploads (up to 2 at a time for performance)
- Processing status as files are optimized after upload
- Option to cancel individual uploads or clear completed items

The queue is draggable and can be minimized so you can continue working while uploads finish.

## Automatic Image Optimization

Every image you upload is automatically optimized:

- **WebP conversion** — a WebP version is generated alongside the original (quality 85%) for faster loading
- **Thumbnail generation** — multiple sized versions are created based on your image presets
- **EXIF orientation** — images are automatically rotated to the correct orientation

### System Image Presets

The platform includes 21 built-in presets that cover common use cases:

| Preset | Dimensions | Crop | Used For |
|--------|-----------|------|---------|
| **Thumbnail** | 150 x 150 | Cover | Admin lists, quick previews |
| **Small** | 300 x 300 | Cover | Small product cards |
| **Medium** | 600 x 600 | Contain | Product cards, blog thumbnails |
| **Large** | 1200 x 1200 | Contain | Product detail pages |
| **Gallery** | 800 x 800 | Contain | Image galleries |
| **Hero** | 1920 x 1080 | Cover | Hero sections, page banners |
| **Banner** | 1200 x 400 | Cover | Promotion banners |
| **Card** | 400 x 300 | Cover | Feature cards, content cards |
| **Avatar** | 200 x 200 | Crop | Customer and staff avatars |
| **Product Listing** | 400 x 400 | Cover | Product grid cards |
| **Product Detail** | 1200 x 1200 | Cover | Full product images |
| **Product Thumbnail** | 100 x 100 | Cover | Variant selectors, mini carts |
| **Category Banner** | 1920 x 480 | Cover | Category page headers |
| **Category Thumbnail** | 300 x 200 | Cover | Category cards |
| **Logo Header** | 300 x 80 | Pad | Site header logo |
| **Logo Footer** | 200 x 60 | Pad | Site footer logo |
| **Logo Email** | 400 x 100 | Pad | Email template logos |
| **Logo Square** | 160 x 160 | Pad | Square logo placements |
| **Brand Logo** | 200 x 100 | Pad | Brand/partner logos |
| **Announcement Banner** | 800 x 300 | Cover | Announcement images |
| **Announcement Background** | 1200 x 800 | Cover | Announcement backgrounds |

System presets cannot be renamed or deleted. You can create additional custom presets under **Media Library > Image Size Presets** if you need sizes not covered by the defaults.

### Crop Modes

| Mode | Behavior |
|------|----------|
| **Cover** | Fills the entire area, cropping edges if needed — good for cards and banners |
| **Contain** | Fits the full image within the area, adding transparent space if needed — good for product images |
| **Crop** | Center-crops to exact dimensions |
| **Pad** | Fits the image and adds padding (transparent, white, or black) — good for logos |

## Organizing Files

### Folders

Create folders to organize your media into logical groups. Folders can be nested to any depth. Click a folder in the left sidebar to show only the assets inside it. The **All Files** link shows everything.

### Tags

Add tags to assets for flexible cross-folder organization. Tags appear in a cloud in the left sidebar. Click a tag to filter assets by that tag. Assets can have multiple tags.

### Search

The search bar finds assets by title, alt text, description, or tag name. Combine search with type and size filters for precise results.

## Asset Detail

Click an asset to open its detail view with a large preview and full metadata.

![Asset Detail](/static/core/admin/img/help/media-library/media-detail.webp)

The detail view shows:

- **Preview** — large image preview with the original dimensions
- **File info** — type, dimensions, file size, upload date
- **Tabs** for editing:

| Tab | Fields |
|-----|--------|
| **General** | Title, Alt Text, Description (all translatable for multi-language stores) |
| **Technical** | MIME type, file hash, original filename, WebP version status |
| **Organization** | Folder assignment, tags, public/private toggle |
| **Advanced** | Focal point coordinates, external ID, metadata JSON |

### Translatable Fields

Title, alt text, and description support translations. Click the translate icon next to each field to add translations for your enabled languages. This ensures images have properly localized alt text and descriptions for SEO and accessibility.

### Usage Tracking

The system tracks where each asset is used across the platform. The **Media usages** section at the bottom shows every model and field that references this asset, helping you understand the impact before making changes or deleting.

## Video Support

Videos uploaded to the media library are automatically analyzed:

- **Metadata extraction** — duration, resolution, frame rate, bitrate, and codecs are captured
- **Poster image** — a thumbnail is generated from the video for preview
- **Streaming** — videos support range requests for seeking without downloading the full file
- **Optional conversion** — videos can be converted to optimized WebM/AV1 format for faster delivery

## Recycle Bin

Deleting an asset moves it to the **Recycle Bin** rather than permanently removing it. This protects against accidental deletion.

| Action | What It Does |
|--------|-------------|
| **Delete** | Moves asset to Recycle Bin (soft delete) |
| **Restore** | Returns a deleted asset to its original location |
| **Permanent Delete** | Removes the asset and all its thumbnails from storage permanently |
| **Empty Recycle Bin** | Permanently deletes all items in the Recycle Bin |

Click **Recycle Bin** in the left sidebar to view and manage deleted assets.

## Where Media Library Is Used

The media library is integrated across the entire platform:

| Feature | How It Uses Media |
|---------|------------------|
| **Product catalog** | Product images, variant images, category banners |
| **Blog** | Featured images, in-content images via CKEditor |
| **Page Builder** | Image elements, hero backgrounds, gallery components |
| **Header/Footer Builder** | Logo images, background images |
| **Site Settings** | Site logo and favicon |
| **Announcements** | Announcement images and backgrounds |
| **CKEditor** | All rich text image uploads route through the media library |
| **Loyalty Program** | Reward and tier images |

When you select an image in any of these features, the media library gallery opens as a modal for easy browsing and selection.

## Tips

- **Use descriptive titles and alt text** — good metadata improves SEO and accessibility. The system uses alt text in image tags throughout the storefront.
- **Organize with folders early** — create a folder structure (e.g., Products, Blog, Banners, Logos) before uploading many files. It is much easier to organize as you go than to reorganize later.
- **Use tags for cross-cutting categories** — tags like "seasonal", "sale", or "lifestyle" help you find assets that span multiple folders.
- **Check usage before deleting** — the usage tracking section shows where an asset is referenced. Deleting a used asset may leave broken images on your storefront.
- **Let WebP do the work** — the automatic WebP conversion typically reduces file sizes by 25-35% compared to JPEG with no visible quality loss. You do not need to manually convert images before uploading.
- **Create custom presets** — if you have a unique layout that needs a specific image size, create a custom preset rather than manually resizing images.
