from django.urls import path

from . import api_views

app_name = "customizable_product_api"

urlpatterns = [
    # Editor configuration for a product
    path(
        "<int:product_id>/config/",
        api_views.editor_config,
        name="editor_config",
    ),
    # Customer image upload
    path(
        "upload-image/",
        api_views.upload_image,
        name="upload_image",
    ),
    # Clipart browsing
    path(
        "clipart/",
        api_views.clipart_list,
        name="clipart_list",
    ),
    # Font list
    path(
        "fonts/",
        api_views.font_list,
        name="font_list",
    ),
    # Design templates for a product
    path(
        "templates/<int:product_id>/",
        api_views.template_list,
        name="template_list",
    ),
    # Saved designs (registered users)
    path(
        "designs/",
        api_views.saved_design_list,
        name="saved_design_list",
    ),
    path(
        "designs/save/",
        api_views.save_design,
        name="save_design",
    ),
    path(
        "designs/<int:design_id>/",
        api_views.saved_design_detail,
        name="saved_design_detail",
    ),
    path(
        "designs/<int:design_id>/delete/",
        api_views.delete_saved_design,
        name="delete_saved_design",
    ),
    # Price calculation
    path(
        "calculate-price/",
        api_views.calculate_price,
        name="calculate_price",
    ),
    # Prepare design for cart (validate + create draft + thumbnails)
    path(
        "prepare-for-cart/",
        api_views.prepare_for_cart,
        name="prepare_for_cart",
    ),
]
