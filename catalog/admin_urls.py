"""
Catalog Admin URL Configuration
Separate from API URLs - these are for admin interface AJAX endpoints
"""

from django.urls import path

from catalog import admin_views, views
from catalog.views import (
    ProviderWizardStep1View,
    ProviderWizardStep2View,
    ProviderWizardStep3View,
    ProviderWizardStep4View,
)

app_name = "catalog_admin"

urlpatterns = [
    # Admin AJAX Endpoints
    path("category/filter/", views.filter_categories, name="filter_categories"),
    path("promotion/filter/", views.filter_promotions, name="filter_promotions"),
    path("license-key/filter/", views.filter_license_keys, name="filter_license_keys"),
    path("license-pool/filter/", views.filter_license_pools, name="filter_license_pools"),
    path("external-sync/filter/", views.filter_external_sync, name="filter_external_sync"),
    path("digital-asset/filter/", views.filter_digital_assets, name="filter_digital_assets"),
    path("product/filter/", views.filter_products, name="filter_products"),
    path("giftcard/filter/", admin_views.filter_gift_cards, name="filter_gift_cards"),
    path(
        "giftcardtransaction/filter/",
        admin_views.filter_gift_card_transactions,
        name="filter_gift_card_transactions",
    ),
    path("stockitem/filter/", admin_views.filter_stock_items, name="filter_stock_items"),
    path("warehouse/filter/", admin_views.filter_warehouses, name="filter_warehouses"),
    path("salesregion/filter/", admin_views.filter_sales_regions, name="filter_sales_regions"),
    path("productreview/filter/", admin_views.filter_reviews, name="filter_reviews"),
    path("booking/filter/", admin_views.filter_bookings, name="filter_bookings"),
    # Variation Builder
    path(
        "product/<int:product_id>/variation-builder/",
        admin_views.variation_builder,
        name="variation_builder",
    ),
    path(
        "product/<int:product_id>/generate-variations/",
        admin_views.generate_variations,
        name="generate_variations",
    ),
    # Digital Products Analytics Dashboard
    path(
        "digital-products-analytics/",
        admin_views.digital_products_analytics_dashboard,
        name="digital_products_analytics",
    ),
    # Quick Add Attribute (AJAX)
    path("quick-add-attribute/", admin_views.quick_add_attribute, name="quick_add_attribute"),
    # License Provider Wizard
    path(
        "license-provider/wizard/step1/",
        ProviderWizardStep1View.as_view(),
        name="license_provider_wizard_step1",
    ),
    path(
        "license-provider/wizard/step2/",
        ProviderWizardStep2View.as_view(),
        name="license_provider_wizard_step2",
    ),
    path(
        "license-provider/wizard/step3/",
        ProviderWizardStep3View.as_view(),
        name="license_provider_wizard_step3",
    ),
    path(
        "license-provider/wizard/step4/",
        ProviderWizardStep4View.as_view(),
        name="license_provider_wizard_step4",
    ),
    # License Provider Product Mapping
    path(
        "license-provider/<int:provider_id>/mappings/",
        admin_views.get_product_mappings,
        name="license_provider_mappings",
    ),
    path(
        "license-provider/<int:provider_id>/mappings/save/",
        admin_views.save_product_mapping,
        name="license_provider_mapping_save",
    ),
    path(
        "license-provider/<int:provider_id>/mappings/delete/",
        admin_views.delete_product_mapping,
        name="license_provider_mapping_delete",
    ),
    path(
        "license-provider/search-products/",
        admin_views.search_digital_products,
        name="license_provider_search_products",
    ),
    # License Template Preview
    path(
        "license-template-preview/<int:template_id>/",
        admin_views.get_license_template_preview,
        name="license_template_preview",
    ),
    # Bundle Item Variant Lookup
    path(
        "product/<int:product_id>/variants/",
        admin_views.get_product_variants,
        name="get_product_variants",
    ),
    # Bundle Component Product Autocomplete (excludes bundle products)
    path(
        "autocomplete/component-products/",
        admin_views.autocomplete_component_products,
        name="autocomplete_component_products",
    ),
    # Product Variant AJAX Deletion
    path(
        "variant/<int:variant_id>/delete/",
        admin_views.delete_product_variant,
        name="delete_product_variant",
    ),
    # Product Variant Cards AJAX Endpoints
    path(
        "product/<int:product_id>/variants/list/", admin_views.list_variants, name="list_variants"
    ),
    path(
        "product/<int:product_id>/variants/create/",
        admin_views.create_variant,
        name="create_variant",
    ),
    path(
        "product/<int:product_id>/variants/form-context/",
        admin_views.variant_form_context,
        name="variant_form_context",
    ),
    path("variant/<int:variant_id>/detail/", admin_views.variant_detail, name="variant_detail"),
    path("variant/<int:variant_id>/update/", admin_views.update_variant, name="update_variant"),
    path(
        "variant/<int:variant_id>/stock/update/",
        admin_views.update_variant_stock,
        name="update_variant_stock",
    ),
    path(
        "variant/<int:variant_id>/images/update/",
        admin_views.update_variant_images,
        name="update_variant_images",
    ),
    path(
        "attribute-value/<int:value_id>/color/",
        admin_views.update_attribute_color,
        name="update_attribute_color",
    ),
    # Product Configurator Management
    path(
        "slot/<int:slot_id>/options/", admin_views.slot_options_manager, name="slot_options_manager"
    ),
    path(
        "slot/<int:slot_id>/options/search/",
        admin_views.slot_options_search_products,
        name="slot_options_search",
    ),
    path(
        "product/<int:product_id>/compatibility/",
        admin_views.compatibility_matrix_manager,
        name="compatibility_matrix",
    ),
    path(
        "product/<int:product_id>/compatibility/api/",
        admin_views.compatibility_rule_api,
        name="compatibility_rule_api",
    ),
    # Configuration Slot AJAX CRUD
    path("product/<int:product_id>/slots/list/", admin_views.list_slots, name="list_slots"),
    path("product/<int:product_id>/slots/create/", admin_views.create_slot, name="create_slot"),
    path("slot/<int:slot_id>/detail/", admin_views.slot_detail, name="slot_detail"),
    path("slot/<int:slot_id>/update/", admin_views.update_slot, name="update_slot"),
    path("slot/<int:slot_id>/delete/", admin_views.delete_slot, name="delete_slot"),
    # Configuration Preset AJAX CRUD
    path("product/<int:product_id>/presets/list/", admin_views.list_presets, name="list_presets"),
    path(
        "product/<int:product_id>/presets/create/", admin_views.create_preset, name="create_preset"
    ),
    path("preset/<int:preset_id>/detail/", admin_views.preset_detail, name="preset_detail"),
    path("preset/<int:preset_id>/update/", admin_views.update_preset, name="update_preset"),
    path("preset/<int:preset_id>/delete/", admin_views.delete_preset, name="delete_preset"),
    # Product Recycle Bin
    path(
        "product/recycle-bin/", admin_views.product_recycle_bin, name="catalog_product_recycle_bin"
    ),
    # Booking Calendar API
    path("booking/calendar-api/", admin_views.booking_calendar_api, name="booking_calendar_api"),
    # Booking Reschedule Check (AJAX)
    path(
        "booking/<int:booking_id>/check-reschedule/",
        admin_views.booking_check_reschedule,
        name="booking_check_reschedule",
    ),
    # Booking AJAX CRUD
    # BookingConfig (singleton)
    path(
        "product/<int:product_id>/booking-config/",
        admin_views.booking_config_detail,
        name="booking_config_detail",
    ),
    path(
        "product/<int:product_id>/booking-config/save/",
        admin_views.booking_config_save,
        name="booking_config_save",
    ),
    # BookingResource CRUD
    path(
        "product/<int:product_id>/booking-resources/list/",
        admin_views.list_booking_resources,
        name="list_booking_resources",
    ),
    path(
        "product/<int:product_id>/booking-resources/create/",
        admin_views.create_booking_resource,
        name="create_booking_resource",
    ),
    path(
        "booking-resource/<int:resource_id>/detail/",
        admin_views.booking_resource_detail,
        name="booking_resource_detail",
    ),
    path(
        "booking-resource/<int:resource_id>/update/",
        admin_views.update_booking_resource,
        name="update_booking_resource",
    ),
    path(
        "booking-resource/<int:resource_id>/delete/",
        admin_views.delete_booking_resource,
        name="delete_booking_resource",
    ),
    # BookingPersonType CRUD
    path(
        "product/<int:product_id>/booking-person-types/list/",
        admin_views.list_booking_person_types,
        name="list_booking_person_types",
    ),
    path(
        "product/<int:product_id>/booking-person-types/create/",
        admin_views.create_booking_person_type,
        name="create_booking_person_type",
    ),
    path(
        "booking-person-type/<int:person_type_id>/detail/",
        admin_views.booking_person_type_detail,
        name="booking_person_type_detail",
    ),
    path(
        "booking-person-type/<int:person_type_id>/update/",
        admin_views.update_booking_person_type,
        name="update_booking_person_type",
    ),
    path(
        "booking-person-type/<int:person_type_id>/delete/",
        admin_views.delete_booking_person_type,
        name="delete_booking_person_type",
    ),
    # BookingAvailabilityRule CRUD
    path(
        "product/<int:product_id>/booking-availability-rules/list/",
        admin_views.list_booking_availability_rules,
        name="list_booking_availability_rules",
    ),
    path(
        "product/<int:product_id>/booking-availability-rules/create/",
        admin_views.create_booking_availability_rule,
        name="create_booking_availability_rule",
    ),
    path(
        "booking-availability-rule/<int:rule_id>/detail/",
        admin_views.booking_availability_rule_detail,
        name="booking_availability_rule_detail",
    ),
    path(
        "booking-availability-rule/<int:rule_id>/update/",
        admin_views.update_booking_availability_rule,
        name="update_booking_availability_rule",
    ),
    path(
        "booking-availability-rule/<int:rule_id>/delete/",
        admin_views.delete_booking_availability_rule,
        name="delete_booking_availability_rule",
    ),
    # BookingRecurrenceRule CRUD
    path(
        "product/<int:product_id>/booking-recurrence-rules/list/",
        admin_views.list_booking_recurrence_rules,
        name="list_booking_recurrence_rules",
    ),
    path(
        "product/<int:product_id>/booking-recurrence-rules/create/",
        admin_views.create_booking_recurrence_rule,
        name="create_booking_recurrence_rule",
    ),
    path(
        "booking-recurrence-rule/<int:rule_id>/detail/",
        admin_views.booking_recurrence_rule_detail,
        name="booking_recurrence_rule_detail",
    ),
    path(
        "booking-recurrence-rule/<int:rule_id>/update/",
        admin_views.update_booking_recurrence_rule,
        name="update_booking_recurrence_rule",
    ),
    path(
        "booking-recurrence-rule/<int:rule_id>/delete/",
        admin_views.delete_booking_recurrence_rule,
        name="delete_booking_recurrence_rule",
    ),
]
