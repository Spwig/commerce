"""
Product Image API endpoints
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from catalog.models import Product, ProductImage


@staff_member_required
@require_http_methods(["GET"])
def get_product_images(request, product_id):
    """
    Get all images for a product.

    Returns:
        {
            "success": true,
            "images": [
                {
                    "id": 1,
                    "media_id": 123,
                    "url": "/media/products/image.jpg",
                    "thumbnail_url": "/media/products/image_thumb.jpg",
                    "alt_text": "Product image",
                    "display_order": 0,
                    "is_primary": true
                },
                ...
            ]
        }
    """
    try:
        product = Product.objects.get(pk=product_id)
        images = product.images.select_related("media_asset").order_by("position")

        image_data = []
        for img in images:
            data = {
                "id": img.id,
                "position": img.position,
                "is_primary": img.is_primary,
                "alt_text": img.alt_text or "",
                "show_in_gallery": img.show_in_gallery,
                "show_in_listing": img.show_in_listing,
            }

            # Add media information if available
            if img.media_asset:
                data["media_id"] = img.media_asset.id
                data["title"] = img.media_asset.title
                data["alt_text"] = img.media_asset.alt_text or img.alt_text or ""

                # Use webp if available, otherwise original file
                if img.media_asset.webp_file:
                    data["url"] = img.media_asset.webp_file.url
                elif img.media_asset.original_file:
                    data["url"] = img.media_asset.original_file.url
                else:
                    data["url"] = None

                # Get thumbnail - check if thumbnails exist
                thumbnails = (
                    img.media_asset.thumbnails.all()
                    if hasattr(img.media_asset, "thumbnails")
                    else []
                )
                if thumbnails:
                    # Use first thumbnail
                    data["thumbnail_url"] = (
                        thumbnails[0].file.url if thumbnails[0].file else data["url"]
                    )
                else:
                    # Fallback to main image
                    data["thumbnail_url"] = data["url"]
            else:
                data["media_id"] = None
                data["url"] = None
                data["thumbnail_url"] = None

            image_data.append(data)

        return JsonResponse({"success": True, "images": image_data})

    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def update_image_order(request, product_id):
    """
    Update the display order of product images.

    POST data:
        {
            "image_ids": [3, 1, 2]  // Array of image IDs in desired order
        }
    """
    try:
        product = Product.objects.get(pk=product_id)

        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)

        image_ids = data.get("image_ids", [])

        if not isinstance(image_ids, list):
            return JsonResponse(
                {"success": False, "error": "image_ids must be an array"}, status=400
            )

        # Update position for each image
        for order, image_id in enumerate(image_ids):
            try:
                img = ProductImage.objects.get(id=image_id, product=product)
                img.position = order
                img.save(update_fields=["position"])
            except ProductImage.DoesNotExist:
                pass  # Skip invalid image IDs

        return JsonResponse({"success": True, "message": "Image order updated"})

    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def set_primary_image(request, product_id, image_id):
    """
    Set an image as the primary product image.
    """
    try:
        product = Product.objects.get(pk=product_id)
        image = ProductImage.objects.get(id=image_id, product=product)

        # Unset all other primary images for this product
        ProductImage.objects.filter(product=product).update(is_primary=False)

        # Set this image as primary
        image.is_primary = True
        image.save(update_fields=["is_primary"])

        return JsonResponse({"success": True, "message": "Primary image updated"})

    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)
    except ProductImage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Image not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["DELETE"])
def delete_product_image(request, product_id, image_id):
    """
    Delete a product image.
    """
    try:
        product = Product.objects.get(pk=product_id)
        image = ProductImage.objects.get(id=image_id, product=product)

        image.delete()

        return JsonResponse({"success": True, "message": "Image deleted"})

    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)
    except ProductImage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Image not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
