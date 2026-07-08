"""
Management command to create demo 3D configurator products.

Creates a fully configured product with configuration slots, options,
3D scene config, and node mappings — ready to test on the frontend.

Usage:
    python manage.py create_demo_configurator --product porsche_wrap
    python manage.py create_demo_configurator --product porsche_wrap --delete
"""
import io
import os
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth import get_user_model
from PIL import Image

from catalog.models import Product, Category, ConfigurationSlot, ConfigurationSlotOption, StockItem, Warehouse
from configurator_3d.models import SceneConfig, NodeMapping
from configurator_3d.services.glb_parser import parse_glb_from_media_asset
from media_library.models import MediaAsset

User = get_user_model()

# ============================================================================
# Product definitions
# ============================================================================

PRODUCTS = {
    'porsche_wrap': {
        'glb_file': '.3dmodels/car_1_porche_optimized.glb',
        'product': {
            'name': 'Custom Vehicle Wrap',
            'slug': 'custom-vehicle-wrap',
            'sku': 'WRAP-PORSCHE-CUSTOM',
            'short_description': 'Design your own vehicle wrap. Choose from 10 stunning colors, customize your wheel finish, and select your preferred window tint.',
            'price': Decimal('2499.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('2499.99'),
        },
        'category_name': 'Vehicle Wraps',
        'scene': {
            'camera_orbit': '45deg 55deg 4m',
            'camera_target': '0m 0.3m 0m',
            'exposure': 1.0,
            'shadow_intensity': 0.8,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#1a1a2e',
        },
        'slots': [
            {
                'name': 'Wrap Color',
                'slug': 'wrap-color',
                'description': 'Choose the color for your vehicle wrap',
                'icon': 'fas fa-palette',
                'sort_order': 0,
                'target_node': 'Object_15',
                'material_name': 'paint',
                'options': [
                    {'name': 'Matte Black', 'sku': 'WRAP-CLR-MATTE-BLACK', 'color': '#1A1A1A', 'metallic': 0.4, 'roughness': 0.6, 'is_default': True},
                    {'name': 'Satin White', 'sku': 'WRAP-CLR-SATIN-WHITE', 'color': '#F5F5F5', 'metallic': 0.5, 'roughness': 0.35},
                    {'name': 'Gloss Red', 'sku': 'WRAP-CLR-GLOSS-RED', 'color': '#C41E3A', 'metallic': 0.6, 'roughness': 0.2},
                    {'name': 'Midnight Blue', 'sku': 'WRAP-CLR-MIDNIGHT-BLUE', 'color': '#1B2A4A', 'metallic': 0.6, 'roughness': 0.25},
                    {'name': 'Army Green', 'sku': 'WRAP-CLR-ARMY-GREEN', 'color': '#4B5320', 'metallic': 0.4, 'roughness': 0.5},
                    {'name': 'Sunset Orange', 'sku': 'WRAP-CLR-SUNSET-ORANGE', 'color': '#E8600A', 'metallic': 0.6, 'roughness': 0.2},
                    {'name': 'Deep Purple', 'sku': 'WRAP-CLR-DEEP-PURPLE', 'color': '#3D1F56', 'metallic': 0.6, 'roughness': 0.25},
                    {'name': 'Gunmetal Grey', 'sku': 'WRAP-CLR-GUNMETAL-GREY', 'color': '#53565A', 'metallic': 0.7, 'roughness': 0.3},
                    {'name': 'Neon Yellow', 'sku': 'WRAP-CLR-NEON-YELLOW', 'color': '#DFFF00', 'metallic': 0.5, 'roughness': 0.2},
                    {'name': 'Racing Green', 'sku': 'WRAP-CLR-RACING-GREEN', 'color': '#004225', 'metallic': 0.6, 'roughness': 0.25},
                ],
            },
            {
                'name': 'Wheel Finish',
                'slug': 'wheel-finish',
                'description': 'Select your preferred wheel finish',
                'icon': 'fas fa-circle-notch',
                'sort_order': 1,
                'target_node': 'Object_30',
                'material_name': 'silver',
                'options': [
                    {'name': 'Chrome Silver', 'sku': 'WRAP-WHL-CHROME', 'color': '#C0C0C0', 'metallic': 1.0, 'roughness': 0.15, 'is_default': True},
                    {'name': 'Matte Black Wheels', 'sku': 'WRAP-WHL-MATTE-BLK', 'color': '#1A1A1A', 'metallic': 0.3, 'roughness': 0.8},
                    {'name': 'Gunmetal Wheels', 'sku': 'WRAP-WHL-GUNMETAL', 'color': '#53565A', 'metallic': 0.8, 'roughness': 0.3},
                ],
            },
            {
                'name': 'Accent Trim',
                'slug': 'accent-trim',
                'description': 'Choose the finish for bumpers and exterior trim',
                'icon': 'fas fa-brush',
                'sort_order': 2,
                'target_node': 'Object_12',
                'material_name': 'plastic',
                'options': [
                    {'name': 'Factory Dark', 'sku': 'WRAP-TRIM-FACTORY', 'color': '#0A0A0A', 'metallic': 0.38, 'roughness': 0.52, 'is_default': True},
                    {'name': 'Gloss Black', 'sku': 'WRAP-TRIM-GLOSS', 'color': '#050505', 'metallic': 0.8, 'roughness': 0.12},
                    {'name': 'Carbon Look', 'sku': 'WRAP-TRIM-CARBON', 'color': '#1C1C1C', 'metallic': 0.5, 'roughness': 0.65},
                    {'name': 'Chrome Accent', 'sku': 'WRAP-TRIM-CHROME', 'color': '#C0C0C0', 'metallic': 1.0, 'roughness': 0.1},
                ],
            },
            {
                'name': 'Wrap Finish',
                'slug': 'wrap-finish',
                'description': 'Choose how your wrap finish looks — glossy, satin, or matte',
                'icon': 'fas fa-sun',
                'sort_order': 3,
                'target_node': 'Object_121',
                'material_name': 'coat',
                'options': [
                    {'name': 'High Gloss', 'sku': 'WRAP-FIN-GLOSS', 'color': '#262626', 'metallic': 1.0, 'roughness': 0.04, 'alpha': 0.46, 'is_default': True},
                    {'name': 'Satin', 'sku': 'WRAP-FIN-SATIN', 'color': '#262626', 'metallic': 0.7, 'roughness': 0.25, 'alpha': 0.46},
                    {'name': 'Matte', 'sku': 'WRAP-FIN-MATTE', 'color': '#262626', 'metallic': 0.3, 'roughness': 0.6, 'alpha': 0.46},
                ],
            },
        ],
    },

    'diamond_ring': {
        'glb_file': '.3dmodels/diamond_engagement_ring.glb',
        'product': {
            'name': 'Custom Engagement Ring',
            'slug': 'custom-engagement-ring',
            'sku': 'RING-CUSTOM-ENG',
            'short_description': 'Design your dream engagement ring. Choose from five precious metals and a selection of stunning gemstones.',
            'price': Decimal('1499.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('1499.99'),
        },
        'category_name': 'Rings',
        'scene': {
            'camera_orbit': '30deg 65deg 0.12m',
            'camera_target': '0m 0.008m 0m',
            'exposure': 1.2,
            'shadow_intensity': 0.4,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f8f7f4',
        },
        'slots': [
            {
                'name': 'Band Metal',
                'slug': 'band-metal',
                'description': 'Select the precious metal for your ring band',
                'icon': 'fas fa-ring',
                'sort_order': 0,
                'target_node': 'Object_3',
                'material_name': 'Metal',
                'options': [
                    {'name': 'Yellow Gold', 'sku': 'RING-BAND-YGOLD', 'color': '#FFD700', 'metallic': 1.0, 'roughness': 0.05, 'is_default': True},
                    {'name': 'Rose Gold', 'sku': 'RING-BAND-RGOLD', 'color': '#B76E79', 'metallic': 1.0, 'roughness': 0.05, 'price_adjustment': '100.00'},
                    {'name': 'White Gold', 'sku': 'RING-BAND-WGOLD', 'color': '#E8E8E8', 'metallic': 1.0, 'roughness': 0.05, 'price_adjustment': '150.00'},
                    {'name': 'Platinum', 'sku': 'RING-BAND-PLAT', 'color': '#E5E4E2', 'metallic': 1.0, 'roughness': 0.02, 'price_adjustment': '400.00'},
                    {'name': 'Sterling Silver', 'sku': 'RING-BAND-SILVER', 'color': '#C0C0C0', 'metallic': 1.0, 'roughness': 0.1, 'price_adjustment': '-300.00'},
                ],
            },
            {
                'name': 'Gemstone',
                'slug': 'gemstone',
                'description': 'Choose your center stone',
                'icon': 'fas fa-gem',
                'sort_order': 1,
                'target_node': 'Object_2',
                'material_name': 'Crystal',
                'options': [
                    {'name': 'Diamond', 'sku': 'RING-GEM-DIAMOND', 'color': '#FFFFFF', 'metallic': 0.8, 'roughness': 0.0, 'alpha': 0.92, 'is_default': True},
                    {'name': 'Ruby', 'sku': 'RING-GEM-RUBY', 'color': '#E0115F', 'metallic': 0.8, 'roughness': 0.0, 'alpha': 0.85, 'price_adjustment': '500.00'},
                    {'name': 'Sapphire', 'sku': 'RING-GEM-SAPPHIRE', 'color': '#0F52BA', 'metallic': 0.8, 'roughness': 0.0, 'alpha': 0.85, 'price_adjustment': '300.00'},
                    {'name': 'Emerald', 'sku': 'RING-GEM-EMERALD', 'color': '#50C878', 'metallic': 0.8, 'roughness': 0.0, 'alpha': 0.85, 'price_adjustment': '800.00'},
                    {'name': 'Pink Diamond', 'sku': 'RING-GEM-PINK', 'color': '#FFB6C1', 'metallic': 0.8, 'roughness': 0.0, 'alpha': 0.90, 'price_adjustment': '2000.00'},
                ],
            },
        ],
    },

    'serum_bottle': {
        'glb_file': '.3dmodels/cosmetic_serum_bottle.glb',
        'product': {
            'name': 'Custom Serum Bottle',
            'slug': 'custom-serum-bottle',
            'sku': 'SERUM-CUSTOM',
            'short_description': 'Design your signature serum packaging. Select your bottle color and cap finish to match your brand aesthetic.',
            'price': Decimal('39.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('39.99'),
        },
        'category_name': 'Skincare',
        'scene': {
            'camera_orbit': '25deg 75deg 0.15m',
            'camera_target': '0m 0.03m 0m',
            'exposure': 1.1,
            'shadow_intensity': 0.3,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f5f0eb',
        },
        'slots': [
            {
                'name': 'Bottle Color',
                'slug': 'bottle-color',
                'description': 'Choose the color for your serum bottle',
                'icon': 'fas fa-flask',
                'sort_order': 0,
                'target_node': 'Circle.004_Bottle.001_0',
                'material_name': 'Bottle.001',
                'options': [
                    {'name': 'Noir', 'sku': 'SERUM-BTL-NOIR', 'color': '#0A0A0A', 'metallic': 0.0, 'roughness': 0.07, 'is_default': True},
                    {'name': 'Amber', 'sku': 'SERUM-BTL-AMBER', 'color': '#B5651D', 'metallic': 0.0, 'roughness': 0.07},
                    {'name': 'Frosted White', 'sku': 'SERUM-BTL-FROST', 'color': '#E8E4DF', 'metallic': 0.0, 'roughness': 0.35},
                    {'name': 'Emerald', 'sku': 'SERUM-BTL-EMERALD', 'color': '#2E5F4A', 'metallic': 0.0, 'roughness': 0.07},
                    {'name': 'Cobalt Blue', 'sku': 'SERUM-BTL-COBALT', 'color': '#1A3A5C', 'metallic': 0.0, 'roughness': 0.07},
                ],
            },
            {
                'name': 'Cap Finish',
                'slug': 'cap-finish',
                'description': 'Select the finish for your dropper cap',
                'icon': 'fas fa-hat-wizard',
                'sort_order': 1,
                'target_node': 'Circle.004_Rubber.001_0',
                'material_name': 'Rubber.001',
                'options': [
                    {'name': 'Matte Black', 'sku': 'SERUM-CAP-MBLACK', 'color': '#0A0A0A', 'metallic': 0.0, 'roughness': 0.75, 'is_default': True},
                    {'name': 'Rose Gold', 'sku': 'SERUM-CAP-RGOLD', 'color': '#B76E79', 'metallic': 1.0, 'roughness': 0.1, 'price_adjustment': '5.00'},
                    {'name': 'Brushed Gold', 'sku': 'SERUM-CAP-BGOLD', 'color': '#D4AF37', 'metallic': 1.0, 'roughness': 0.2, 'price_adjustment': '5.00'},
                    {'name': 'Silver Chrome', 'sku': 'SERUM-CAP-CHROME', 'color': '#C0C0C0', 'metallic': 1.0, 'roughness': 0.05, 'price_adjustment': '3.00'},
                    {'name': 'Matte White', 'sku': 'SERUM-CAP-MWHITE', 'color': '#F0EDE8', 'metallic': 0.0, 'roughness': 0.75},
                ],
            },
        ],
    },

    'new_balance_997': {
        'glb_file': '.3dmodels/new_balance_997.glb',
        'product': {
            'name': 'New Balance 997 Custom',
            'slug': 'new-balance-997-custom',
            'sku': 'NB-997-CUSTOM',
            'short_description': 'Design your own New Balance 997. Choose colors for each part of the shoe.',
            'price': Decimal('149.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('149.99'),
        },
        'category_name': 'Footwear',
        'scene': {
            'camera_orbit': '45deg 75deg 2.5m',
            'camera_target': '0m 0.1m 0m',
            'exposure': 1.0,
            'shadow_intensity': 0.7,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#ffffff',
        },
        'slots': [
            {
                'name': 'Sole Color',
                'slug': 'sole-color',
                'description': 'Choose your sole color',
                'icon': 'fas fa-shoe-prints',
                'sort_order': 0,
                'target_node': 'Shoe_set_02_Sole_0',
                'material_name': 'Sole',
                'options': [
                    {'name': 'White', 'sku': 'NB997-SOLE-WHITE', 'color': '#FFFFFF', 'metallic': 0.3, 'roughness': 0.7, 'is_default': True},
                    {'name': 'Black', 'sku': 'NB997-SOLE-BLACK', 'color': '#1A1A1A', 'metallic': 0.3, 'roughness': 0.7},
                    {'name': 'Navy Blue', 'sku': 'NB997-SOLE-NAVY', 'color': '#1B2A4A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Red', 'sku': 'NB997-SOLE-RED', 'color': '#C41E3A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Forest Green', 'sku': 'NB997-SOLE-GREEN', 'color': '#2D5A27', 'metallic': 0.3, 'roughness': 0.7, 'price_adjustment': '5.00'},
                    {'name': 'Grey', 'sku': 'NB997-SOLE-GREY', 'color': '#808080', 'metallic': 0.3, 'roughness': 0.7},
                ],
            },
            {
                'name': 'Upper Color',
                'slug': 'upper-color',
                'description': 'Choose your upper/outer color',
                'icon': 'fas fa-paint-brush',
                'sort_order': 1,
                'target_node': 'Shoe_set_02_Outer_0',
                'material_name': 'Outer',
                'options': [
                    {'name': 'White', 'sku': 'NB997-UPPER-WHITE', 'color': '#FFFFFF', 'metallic': 0.3, 'roughness': 0.7, 'is_default': True},
                    {'name': 'Black', 'sku': 'NB997-UPPER-BLACK', 'color': '#1A1A1A', 'metallic': 0.3, 'roughness': 0.7},
                    {'name': 'Navy Blue', 'sku': 'NB997-UPPER-NAVY', 'color': '#1B2A4A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Red', 'sku': 'NB997-UPPER-RED', 'color': '#C41E3A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Forest Green', 'sku': 'NB997-UPPER-GREEN', 'color': '#2D5A27', 'metallic': 0.3, 'roughness': 0.7, 'price_adjustment': '5.00'},
                    {'name': 'Grey', 'sku': 'NB997-UPPER-GREY', 'color': '#808080', 'metallic': 0.3, 'roughness': 0.7},
                ],
            },
            {
                'name': 'Laces Color',
                'slug': 'laces-color',
                'description': 'Choose your laces color',
                'icon': 'fas fa-grip-lines',
                'sort_order': 2,
                'target_node': 'Shoe_set_02_Laces_0',
                'material_name': 'Laces',
                'options': [
                    {'name': 'White', 'sku': 'NB997-LACES-WHITE', 'color': '#FFFFFF', 'metallic': 0.3, 'roughness': 0.7},
                    {'name': 'Black', 'sku': 'NB997-LACES-BLACK', 'color': '#1A1A1A', 'metallic': 0.3, 'roughness': 0.7, 'is_default': True},
                    {'name': 'Navy Blue', 'sku': 'NB997-LACES-NAVY', 'color': '#1B2A4A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Red', 'sku': 'NB997-LACES-RED', 'color': '#C41E3A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Forest Green', 'sku': 'NB997-LACES-GREEN', 'color': '#2D5A27', 'metallic': 0.3, 'roughness': 0.7, 'price_adjustment': '5.00'},
                    {'name': 'Grey', 'sku': 'NB997-LACES-GREY', 'color': '#808080', 'metallic': 0.3, 'roughness': 0.7},
                ],
            },
            {
                'name': 'Lining Color',
                'slug': 'lining-color',
                'description': 'Choose your inner lining color',
                'icon': 'fas fa-layer-group',
                'sort_order': 3,
                'target_node': 'Shoe_set_02_Inner_0',
                'material_name': 'Inner',
                'options': [
                    {'name': 'White', 'sku': 'NB997-LINING-WHITE', 'color': '#FFFFFF', 'metallic': 0.3, 'roughness': 0.7, 'is_default': True},
                    {'name': 'Black', 'sku': 'NB997-LINING-BLACK', 'color': '#1A1A1A', 'metallic': 0.3, 'roughness': 0.7},
                    {'name': 'Navy Blue', 'sku': 'NB997-LINING-NAVY', 'color': '#1B2A4A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Red', 'sku': 'NB997-LINING-RED', 'color': '#C41E3A', 'metallic': 0.3, 'roughness': 0.7, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Forest Green', 'sku': 'NB997-LINING-GREEN', 'color': '#2D5A27', 'metallic': 0.3, 'roughness': 0.7, 'price_adjustment': '5.00'},
                    {'name': 'Grey', 'sku': 'NB997-LINING-GREY', 'color': '#808080', 'metallic': 0.3, 'roughness': 0.7},
                ],
            },
        ],
    },

    'coffee_mug': {
        'glb_file': '.3dmodels/classic_red_coffee_mug.glb',
        'product': {
            'name': 'Custom Coffee Mug',
            'slug': 'custom-coffee-mug',
            'sku': 'MUG-CUSTOM',
            'short_description': 'Pick your perfect mug. Choose the exterior glaze and interior finish for a look that matches your style.',
            'price': Decimal('19.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('19.99'),
        },
        'category_name': 'Drinkware',
        'scene': {
            'camera_orbit': '30deg 70deg 0.25m',
            'camera_target': '0m 0.04m 0m',
            'exposure': 1.1,
            'shadow_intensity': 0.4,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f5f5f5',
        },
        'slots': [
            {
                'name': 'Exterior Glaze',
                'slug': 'exterior-glaze',
                'description': 'Choose the color for the outside of your mug',
                'icon': 'fas fa-mug-hot',
                'sort_order': 0,
                'target_node': 'Mesh.Mug_Red_0',
                'material_name': 'material',
                'options': [
                    {'name': 'Classic Red', 'sku': 'MUG-EXT-RED', 'color': '#8B1A0A', 'metallic': 0.21, 'roughness': 0.18, 'is_default': True},
                    {'name': 'Matte Black', 'sku': 'MUG-EXT-BLACK', 'color': '#1A1A1A', 'metallic': 0.15, 'roughness': 0.4},
                    {'name': 'Navy Blue', 'sku': 'MUG-EXT-NAVY', 'color': '#1B2A4A', 'metallic': 0.21, 'roughness': 0.18},
                    {'name': 'Forest Green', 'sku': 'MUG-EXT-GREEN', 'color': '#2D5A27', 'metallic': 0.21, 'roughness': 0.18},
                    {'name': 'Mustard Yellow', 'sku': 'MUG-EXT-YELLOW', 'color': '#D4A017', 'metallic': 0.21, 'roughness': 0.18},
                    {'name': 'Pure White', 'sku': 'MUG-EXT-WHITE', 'color': '#F0F0F0', 'metallic': 0.1, 'roughness': 0.25},
                    {'name': 'Dusty Rose', 'sku': 'MUG-EXT-ROSE', 'color': '#C4858A', 'metallic': 0.21, 'roughness': 0.18, 'price_adjustment': '2.00'},
                    {'name': 'Cobalt Blue', 'sku': 'MUG-EXT-COBALT', 'color': '#0047AB', 'metallic': 0.25, 'roughness': 0.15, 'price_adjustment': '2.00'},
                ],
            },
            {
                'name': 'Interior Finish',
                'slug': 'interior-finish',
                'description': 'Choose the color for the inside of your mug',
                'icon': 'fas fa-fill-drip',
                'sort_order': 1,
                'target_node': 'Mesh.Mug_White Mug_0',
                'material_name': 'White_Mug',
                'options': [
                    {'name': 'Classic White', 'sku': 'MUG-INT-WHITE', 'color': '#CCCCCC', 'metallic': 0.0, 'roughness': 0.78, 'is_default': True},
                    {'name': 'Cream', 'sku': 'MUG-INT-CREAM', 'color': '#F5F0E1', 'metallic': 0.0, 'roughness': 0.78},
                    {'name': 'Black', 'sku': 'MUG-INT-BLACK', 'color': '#1A1A1A', 'metallic': 0.0, 'roughness': 0.78, 'price_adjustment': '1.50'},
                    {'name': 'Speckled Grey', 'sku': 'MUG-INT-SPECKLED', 'color': '#A0A0A0', 'metallic': 0.05, 'roughness': 0.85, 'price_adjustment': '2.00'},
                ],
            },
        ],
    },

    'lounge_sofa': {
        'glb_file': '.3dmodels/cinema_theater_lounge_sofa_optimized.glb',
        'product': {
            'name': 'Custom Lounge Sofa',
            'slug': 'custom-lounge-sofa',
            'sku': 'SOFA-CUSTOM-LOUNGE',
            'short_description': 'Configure your dream lounge sofa. Choose from premium leather colors and select your preferred leg finish.',
            'price': Decimal('1899.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('1899.99'),
        },
        'category_name': 'Furniture',
        'scene': {
            'camera_orbit': '35deg 65deg 3.5m',
            'camera_target': '0m 0.3m 0m',
            'exposure': 1.0,
            'shadow_intensity': 0.5,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f2f0ed',
        },
        'slots': [
            {
                'name': 'Upholstery',
                'slug': 'upholstery',
                'description': 'Choose your leather color',
                'icon': 'fas fa-couch',
                'sort_order': 0,
                'target_node': 'Mesh2_Leather_05_0',
                'material_name': 'Leather_05',
                'options': [
                    {'name': 'Charcoal', 'sku': 'SOFA-UPH-CHARCOAL', 'color': '#2C2C2C', 'metallic': 0.0, 'roughness': 0.5, 'is_default': True},
                    {'name': 'Espresso Brown', 'sku': 'SOFA-UPH-ESPRESSO', 'color': '#3C1F0E', 'metallic': 0.0, 'roughness': 0.5},
                    {'name': 'Cognac Tan', 'sku': 'SOFA-UPH-COGNAC', 'color': '#8B4513', 'metallic': 0.0, 'roughness': 0.45, 'is_popular': True, 'price_adjustment': '100.00'},
                    {'name': 'Ivory Cream', 'sku': 'SOFA-UPH-IVORY', 'color': '#EEDFCC', 'metallic': 0.0, 'roughness': 0.5, 'price_adjustment': '50.00'},
                    {'name': 'Navy Blue', 'sku': 'SOFA-UPH-NAVY', 'color': '#1B2A4A', 'metallic': 0.0, 'roughness': 0.5, 'price_adjustment': '75.00'},
                    {'name': 'Olive Green', 'sku': 'SOFA-UPH-OLIVE', 'color': '#3C4A2B', 'metallic': 0.0, 'roughness': 0.5, 'price_adjustment': '75.00'},
                    {'name': 'Burgundy', 'sku': 'SOFA-UPH-BURGUNDY', 'color': '#6B1C23', 'metallic': 0.0, 'roughness': 0.5, 'is_popular': True, 'price_adjustment': '100.00'},
                    {'name': 'Slate Grey', 'sku': 'SOFA-UPH-SLATE', 'color': '#6B7B8D', 'metallic': 0.0, 'roughness': 0.5},
                ],
            },
            {
                'name': 'Leg Finish',
                'slug': 'leg-finish',
                'description': 'Choose the finish for the sofa legs',
                'icon': 'fas fa-columns',
                'sort_order': 1,
                'target_node': 'Mesh6_Aluminum_04__Brushed_0',
                'material_name': 'Aluminum_04__Brushed',
                'options': [
                    {'name': 'Brushed Aluminum', 'sku': 'SOFA-LEG-ALUM', 'color': '#C0C0C0', 'metallic': 1.0, 'roughness': 0.19, 'is_default': True},
                    {'name': 'Matte Black', 'sku': 'SOFA-LEG-BLACK', 'color': '#1A1A1A', 'metallic': 0.8, 'roughness': 0.35, 'price_adjustment': '50.00'},
                    {'name': 'Brushed Gold', 'sku': 'SOFA-LEG-GOLD', 'color': '#D4AF37', 'metallic': 1.0, 'roughness': 0.2, 'is_popular': True, 'price_adjustment': '120.00'},
                    {'name': 'Chrome', 'sku': 'SOFA-LEG-CHROME', 'color': '#E8E8E8', 'metallic': 1.0, 'roughness': 0.05, 'price_adjustment': '80.00'},
                    {'name': 'Rose Gold', 'sku': 'SOFA-LEG-ROSE', 'color': '#B76E79', 'metallic': 1.0, 'roughness': 0.15, 'price_adjustment': '120.00'},
                ],
            },
        ],
    },

    'nintendo_switch': {
        'glb_file': '.3dmodels/nintendo_switch_console.glb',
        'product': {
            'name': 'Custom Switch Console',
            'slug': 'custom-switch-console',
            'sku': 'SWITCH-CUSTOM',
            'short_description': 'Design your own Switch console. Mix and match Joy-Con colors and choose your console body finish.',
            'price': Decimal('299.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('299.99'),
        },
        'category_name': 'Gaming Consoles',
        'scene': {
            'camera_orbit': '20deg 70deg 0.35m',
            'camera_target': '0m 0.01m 0m',
            'exposure': 1.0,
            'shadow_intensity': 0.5,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f0f0f0',
        },
        'slots': [
            {
                'name': 'Left Joy-Con',
                'slug': 'left-joycon',
                'description': 'Choose the color for the left Joy-Con',
                'icon': 'fas fa-gamepad',
                'sort_order': 0,
                'target_node': 'Object_6_Plastic (1)_0',
                'material_name': 'Plastic_1',
                'options': [
                    {'name': 'Neon Red', 'sku': 'SW-LJC-RED', 'color': '#E60012', 'metallic': 0.0, 'roughness': 0.53, 'is_default': True},
                    {'name': 'Neon Blue', 'sku': 'SW-LJC-BLUE', 'color': '#0AB9E6', 'metallic': 0.0, 'roughness': 0.53},
                    {'name': 'Neon Yellow', 'sku': 'SW-LJC-YELLOW', 'color': '#E6D000', 'metallic': 0.0, 'roughness': 0.53},
                    {'name': 'Neon Green', 'sku': 'SW-LJC-GREEN', 'color': '#1EDC62', 'metallic': 0.0, 'roughness': 0.53},
                    {'name': 'Neon Pink', 'sku': 'SW-LJC-PINK', 'color': '#E60071', 'metallic': 0.0, 'roughness': 0.53},
                    {'name': 'Neon Purple', 'sku': 'SW-LJC-PURPLE', 'color': '#B400E6', 'metallic': 0.0, 'roughness': 0.53, 'price_adjustment': '5.00'},
                    {'name': 'Pastel Pink', 'sku': 'SW-LJC-PPINK', 'color': '#F0C8D8', 'metallic': 0.0, 'roughness': 0.53, 'price_adjustment': '5.00'},
                    {'name': 'Pastel Blue', 'sku': 'SW-LJC-PBLUE', 'color': '#A8D8EA', 'metallic': 0.0, 'roughness': 0.53, 'price_adjustment': '5.00'},
                    {'name': 'White', 'sku': 'SW-LJC-WHITE', 'color': '#E8E8E8', 'metallic': 0.0, 'roughness': 0.53, 'price_adjustment': '10.00'},
                    {'name': 'Jet Black', 'sku': 'SW-LJC-BLACK', 'color': '#1A1A1A', 'metallic': 0.0, 'roughness': 0.53},
                ],
            },
            {
                'name': 'Right Joy-Con',
                'slug': 'right-joycon',
                'description': 'Choose the color for the right Joy-Con',
                'icon': 'fas fa-gamepad',
                'sort_order': 1,
                'target_node': 'Object_5_Plastic (2)_0',
                'material_name': 'Plastic_2',
                'options': [
                    {'name': 'Neon Blue', 'sku': 'SW-RJC-BLUE', 'color': '#0AB9E6', 'metallic': 0.0, 'roughness': 0.47, 'is_default': True},
                    {'name': 'Neon Red', 'sku': 'SW-RJC-RED', 'color': '#E60012', 'metallic': 0.0, 'roughness': 0.47},
                    {'name': 'Neon Yellow', 'sku': 'SW-RJC-YELLOW', 'color': '#E6D000', 'metallic': 0.0, 'roughness': 0.47},
                    {'name': 'Neon Green', 'sku': 'SW-RJC-GREEN', 'color': '#1EDC62', 'metallic': 0.0, 'roughness': 0.47},
                    {'name': 'Neon Pink', 'sku': 'SW-RJC-PINK', 'color': '#E60071', 'metallic': 0.0, 'roughness': 0.47},
                    {'name': 'Neon Purple', 'sku': 'SW-RJC-PURPLE', 'color': '#B400E6', 'metallic': 0.0, 'roughness': 0.47, 'price_adjustment': '5.00'},
                    {'name': 'Pastel Green', 'sku': 'SW-RJC-PGREEN', 'color': '#C8F0D8', 'metallic': 0.0, 'roughness': 0.47, 'price_adjustment': '5.00'},
                    {'name': 'Pastel Purple', 'sku': 'SW-RJC-PPURPLE', 'color': '#D8C8F0', 'metallic': 0.0, 'roughness': 0.47, 'price_adjustment': '5.00'},
                    {'name': 'White', 'sku': 'SW-RJC-WHITE', 'color': '#E8E8E8', 'metallic': 0.0, 'roughness': 0.47, 'price_adjustment': '10.00'},
                    {'name': 'Jet Black', 'sku': 'SW-RJC-BLACK', 'color': '#1A1A1A', 'metallic': 0.0, 'roughness': 0.47},
                ],
            },
            {
                'name': 'Console Body',
                'slug': 'console-body',
                'description': 'Choose the finish for the main console body',
                'icon': 'fas fa-tablet-alt',
                'sort_order': 2,
                'target_node': 'Object_1_Plastic_0',
                'material_name': 'Plastic',
                'options': [
                    {'name': 'Standard Black', 'sku': 'SW-BODY-BLACK', 'color': '#2A2A2A', 'metallic': 0.0, 'roughness': 0.45, 'is_default': True},
                    {'name': 'Pure White', 'sku': 'SW-BODY-WHITE', 'color': '#E8E8E8', 'metallic': 0.0, 'roughness': 0.45, 'is_popular': True, 'price_adjustment': '15.00'},
                    {'name': 'Slate Grey', 'sku': 'SW-BODY-GREY', 'color': '#505050', 'metallic': 0.0, 'roughness': 0.45, 'price_adjustment': '10.00'},
                    {'name': 'Midnight Blue', 'sku': 'SW-BODY-NAVY', 'color': '#1B2A4A', 'metallic': 0.0, 'roughness': 0.45, 'price_adjustment': '15.00'},
                ],
            },
        ],
    },

    'treasure_chest': {
        'glb_file': '.3dmodels/treasure_chest.glb',
        'product': {
            'name': 'Treasure Chest Toy Box',
            'slug': 'treasure-chest-toy-box',
            'sku': 'TOYBOX-CHEST',
            'short_description': 'A magical treasure chest toy box for little adventurers. Pick the wood stain, metal trim, and lock color to match their bedroom.',
            'price': Decimal('79.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('79.99'),
        },
        'category_name': 'Kids Furniture',
        'scene': {
            'camera_orbit': '35deg 65deg 1.8m',
            'camera_target': '0m 0.2m 0m',
            'exposure': 1.1,
            'shadow_intensity': 0.5,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f9f6f1',
        },
        'slots': [
            {
                'name': 'Wood Finish',
                'slug': 'wood-finish',
                'description': 'Choose the stain for the wooden panels',
                'icon': 'fas fa-tree',
                'sort_order': 0,
                'target_node': 'Dower chest_Wood_0',
                'material_name': 'Wood',
                'options': [
                    {'name': 'Natural Oak', 'sku': 'CHEST-WOOD-OAK', 'color': '#B8860B', 'metallic': 0.0, 'roughness': 0.82, 'is_default': True},
                    {'name': 'Honey Pine', 'sku': 'CHEST-WOOD-PINE', 'color': '#DEB887', 'metallic': 0.0, 'roughness': 0.82},
                    {'name': 'Cherry', 'sku': 'CHEST-WOOD-CHERRY', 'color': '#7B3F00', 'metallic': 0.0, 'roughness': 0.82, 'price_adjustment': '10.00'},
                    {'name': 'White Wash', 'sku': 'CHEST-WOOD-WHITE', 'color': '#E8E0D4', 'metallic': 0.0, 'roughness': 0.85, 'is_popular': True},
                    {'name': 'Sky Blue', 'sku': 'CHEST-WOOD-BLUE', 'color': '#6CA6CD', 'metallic': 0.0, 'roughness': 0.80, 'price_adjustment': '5.00'},
                    {'name': 'Soft Pink', 'sku': 'CHEST-WOOD-PINK', 'color': '#E8A0B4', 'metallic': 0.0, 'roughness': 0.80, 'price_adjustment': '5.00'},
                    {'name': 'Mint Green', 'sku': 'CHEST-WOOD-MINT', 'color': '#8FBC8F', 'metallic': 0.0, 'roughness': 0.80, 'price_adjustment': '5.00'},
                    {'name': 'Dark Walnut', 'sku': 'CHEST-WOOD-WALNUT', 'color': '#3E2723', 'metallic': 0.0, 'roughness': 0.82, 'price_adjustment': '10.00'},
                ],
            },
            {
                'name': 'Metal Trim',
                'slug': 'metal-trim',
                'description': 'Choose the color for the metal bands and straps',
                'icon': 'fas fa-shield-alt',
                'sort_order': 1,
                'target_node': 'Dower chest_Box met_0',
                'material_name': 'Box_met',
                'action_type': 'material_texture',
                'options': [
                    {'name': 'Aged Bronze', 'sku': 'CHEST-TRIM-BRONZE', 'color': '#CD9B1D', 'metallic': 1.0, 'roughness': 0.3, 'is_default': True},
                    {'name': 'Black Iron', 'sku': 'CHEST-TRIM-IRON', 'color': '#3A3A3A', 'metallic': 0.9, 'roughness': 0.4},
                    {'name': 'Polished Gold', 'sku': 'CHEST-TRIM-GOLD', 'color': '#FFD700', 'metallic': 1.0, 'roughness': 0.08, 'is_popular': True, 'price_adjustment': '10.00'},
                    {'name': 'Silver', 'sku': 'CHEST-TRIM-SILVER', 'color': '#E8E8E8', 'metallic': 1.0, 'roughness': 0.1, 'price_adjustment': '5.00'},
                    {'name': 'Rose Gold', 'sku': 'CHEST-TRIM-ROSE', 'color': '#E8A0A0', 'metallic': 1.0, 'roughness': 0.1, 'price_adjustment': '10.00'},
                ],
            },
            {
                'name': 'Lock Color',
                'slug': 'lock-color',
                'description': 'Choose the color for the chest lock',
                'icon': 'fas fa-lock',
                'sort_order': 2,
                'target_node': 'Dower chest_Zamok_0',
                'material_name': 'Zamok',
                'action_type': 'material_texture',
                'options': [
                    {'name': 'Aged Bronze', 'sku': 'CHEST-LOCK-BRONZE', 'color': '#CD9B1D', 'metallic': 1.0, 'roughness': 0.3, 'is_default': True},
                    {'name': 'Black Iron', 'sku': 'CHEST-LOCK-IRON', 'color': '#3A3A3A', 'metallic': 0.9, 'roughness': 0.4},
                    {'name': 'Polished Gold', 'sku': 'CHEST-LOCK-GOLD', 'color': '#FFD700', 'metallic': 1.0, 'roughness': 0.08, 'is_popular': True, 'price_adjustment': '5.00'},
                    {'name': 'Silver', 'sku': 'CHEST-LOCK-SILVER', 'color': '#E8E8E8', 'metallic': 1.0, 'roughness': 0.1},
                ],
            },
        ],
    },

    'cat_collar': {
        'glb_file': '.3dmodels/cat_collar_mesh_optimized.glb',
        'product': {
            'name': 'Custom Cat Collar',
            'slug': 'custom-cat-collar',
            'sku': 'PET-CAT-COLLAR',
            'short_description': 'A stylish breakaway cat collar with bell. Pick the collar color, stitch accent, and hardware finish for your feline friend.',
            'price': Decimal('14.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('14.99'),
        },
        'category_name': 'Pet Accessories',
        'scene': {
            'camera_orbit': '25deg 70deg 0.25m',
            'camera_target': '0m 0.01m 0m',
            'exposure': 1.1,
            'shadow_intensity': 0.4,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f5f5f5',
        },
        'slots': [
            {
                'name': 'Collar Color',
                'slug': 'collar-color',
                'description': 'Choose the collar band and trim color',
                'icon': 'fas fa-palette',
                'sort_order': 0,
                'targets': [
                    {'target_node': 'Collar_Collar_Pattern_0', 'material_name': 'Collar_Pattern'},
                    {'target_node': 'Collar_Collar_Trim_0', 'material_name': 'Collar_Trim'},
                ],
                'options': [
                    {'name': 'Red', 'sku': 'COLLAR-CLR-RED', 'color': '#CC2233', 'metallic': 0.0, 'roughness': 0.7, 'is_default': True},
                    {'name': 'Royal Blue', 'sku': 'COLLAR-CLR-BLUE', 'color': '#2255AA', 'metallic': 0.0, 'roughness': 0.7, 'is_popular': True},
                    {'name': 'Hot Pink', 'sku': 'COLLAR-CLR-PINK', 'color': '#E84090', 'metallic': 0.0, 'roughness': 0.7},
                    {'name': 'Purple', 'sku': 'COLLAR-CLR-PURPLE', 'color': '#6A2C8E', 'metallic': 0.0, 'roughness': 0.7},
                    {'name': 'Forest Green', 'sku': 'COLLAR-CLR-GREEN', 'color': '#2D6E3F', 'metallic': 0.0, 'roughness': 0.7},
                    {'name': 'Black', 'sku': 'COLLAR-CLR-BLACK', 'color': '#1A1A1A', 'metallic': 0.0, 'roughness': 0.7},
                    {'name': 'Orange', 'sku': 'COLLAR-CLR-ORANGE', 'color': '#E07020', 'metallic': 0.0, 'roughness': 0.7},
                    {'name': 'Turquoise', 'sku': 'COLLAR-CLR-TEAL', 'color': '#30A8A0', 'metallic': 0.0, 'roughness': 0.7, 'price_adjustment': '2.00'},
                ],
            },
            {
                'name': 'Stitch Color',
                'slug': 'stitch-color',
                'description': 'Choose the accent stitch color',
                'icon': 'fas fa-grip-lines',
                'sort_order': 1,
                'targets': [
                    {'target_node': 'Stitches_01_Collar_Stitches_0', 'material_name': 'Collar_Stitches'},
                ],
                'options': [
                    {'name': 'White', 'sku': 'COLLAR-STI-WHITE', 'color': '#F0F0F0', 'metallic': 0.0, 'roughness': 1.0, 'is_default': True},
                    {'name': 'Black', 'sku': 'COLLAR-STI-BLACK', 'color': '#1A1A1A', 'metallic': 0.0, 'roughness': 1.0},
                    {'name': 'Gold', 'sku': 'COLLAR-STI-GOLD', 'color': '#D4A855', 'metallic': 0.0, 'roughness': 0.9, 'is_popular': True},
                    {'name': 'Silver', 'sku': 'COLLAR-STI-SILVER', 'color': '#C0C0C0', 'metallic': 0.0, 'roughness': 0.9},
                ],
            },
            {
                'name': 'Hardware Finish',
                'slug': 'hardware-finish',
                'description': 'Choose the finish for the bell and D-ring',
                'icon': 'fas fa-bell',
                'sort_order': 2,
                'target_node': 'Hoop_Silver_0',
                'material_name': 'Silver',
                'options': [
                    {'name': 'Silver', 'sku': 'COLLAR-HW-SILVER', 'color': '#D0D0D0', 'metallic': 1.0, 'roughness': 0.2, 'is_default': True},
                    {'name': 'Gold', 'sku': 'COLLAR-HW-GOLD', 'color': '#FFD700', 'metallic': 1.0, 'roughness': 0.15, 'is_popular': True, 'price_adjustment': '3.00'},
                    {'name': 'Rose Gold', 'sku': 'COLLAR-HW-ROSE', 'color': '#E8A0A0', 'metallic': 1.0, 'roughness': 0.15, 'price_adjustment': '3.00'},
                    {'name': 'Black', 'sku': 'COLLAR-HW-BLACK', 'color': '#2A2A2A', 'metallic': 0.9, 'roughness': 0.3},
                ],
            },
        ],
    },

    'wicker_basket': {
        'glb_file': '.3dmodels/a_wicker_basket_with_a_handle.glb',
        'product': {
            'name': 'Wicker Storage Basket',
            'slug': 'wicker-storage-basket',
            'sku': 'BASKET-WICKER',
            'short_description': 'A beautiful hand-woven wicker basket with handle. Choose your preferred weave stain to complement any room.',
            'price': Decimal('34.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('34.99'),
        },
        'category_name': 'Home Storage',
        'scene': {
            'camera_orbit': '30deg 65deg 1.5m',
            'camera_target': '0m 0.15m 0m',
            'exposure': 1.0,
            'shadow_intensity': 0.4,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#f5f0eb',
        },
        'slots': [
            {
                'name': 'Weave Color',
                'slug': 'weave-color',
                'description': 'Choose the stain for the wicker weave',
                'icon': 'fas fa-palette',
                'sort_order': 0,
                'targets': [
                    {'target_node': 'Stereo textured mesh_Material0_0', 'material_name': 'Material0'},
                    {'target_node': 'Stereo textured mesh_Material1_0', 'material_name': 'Material1'},
                    {'target_node': 'Stereo textured mesh_Material2_0', 'material_name': 'Material2'},
                    {'target_node': 'Stereo textured mesh_Material3_0', 'material_name': 'Material3'},
                ],
                'options': [
                    {'name': 'Natural', 'sku': 'BASKET-NAT', 'color': '#FFFFFF', 'metallic': 0.0, 'roughness': 1.0, 'is_default': True},
                    {'name': 'Honey', 'sku': 'BASKET-HONEY', 'color': '#D4A855', 'metallic': 0.0, 'roughness': 1.0, 'is_popular': True},
                    {'name': 'Dark Walnut', 'sku': 'BASKET-WALNUT', 'color': '#5C3A1E', 'metallic': 0.0, 'roughness': 1.0, 'price_adjustment': '5.00'},
                    {'name': 'Grey Wash', 'sku': 'BASKET-GREY', 'color': '#A8A8A0', 'metallic': 0.0, 'roughness': 1.0},
                    {'name': 'White Wash', 'sku': 'BASKET-WHITE', 'color': '#E8E0D4', 'metallic': 0.0, 'roughness': 1.0},
                    {'name': 'Espresso', 'sku': 'BASKET-ESPRESSO', 'color': '#3B2314', 'metallic': 0.0, 'roughness': 1.0, 'price_adjustment': '5.00'},
                ],
            },
        ],
    },

    'gaming_pc': {
        'glb_file': '.3dmodels/free_gaming_pc.glb',
        'product': {
            'name': 'Custom Gaming PC',
            'slug': 'custom-gaming-pc',
            'sku': 'PC-CUSTOM-GAMING',
            'short_description': 'Build your ultimate gaming rig. Choose your case color, RGB lighting, and side panel style.',
            'price': Decimal('1299.99'),
            'configurator_pricing_strategy': 'base_plus_adjustments',
            'configurator_base_price': Decimal('1299.99'),
        },
        'category_name': 'Gaming PCs',
        'scene': {
            'camera_orbit': '220deg 70deg 0.6m',
            'camera_target': '0m 0.12m 0m',
            'exposure': 0.9,
            'shadow_intensity': 0.6,
            'auto_rotate': False,
            'ar_enabled': True,
            'background_color': '#0d1117',
        },
        'slots': [
            {
                'name': 'Case Color',
                'slug': 'case-color',
                'description': 'Select the finish for your case chassis',
                'icon': 'fas fa-desktop',
                'sort_order': 0,
                'target_node': 'case_Rough white metal_0',
                'material_name': 'Rough_white_metal',
                'options': [
                    {'name': 'Stealth Black', 'sku': 'PC-CASE-BLACK', 'color': '#1A1A1A', 'metallic': 1.0, 'roughness': 0.82, 'is_default': True},
                    {'name': 'Arctic White', 'sku': 'PC-CASE-WHITE', 'color': '#E0E0E0', 'metallic': 1.0, 'roughness': 0.82, 'price_adjustment': '30.00'},
                    {'name': 'Gunmetal', 'sku': 'PC-CASE-GUNMETAL', 'color': '#53565A', 'metallic': 1.0, 'roughness': 0.60, 'price_adjustment': '20.00'},
                    {'name': 'Racing Red', 'sku': 'PC-CASE-RED', 'color': '#8B0000', 'metallic': 1.0, 'roughness': 0.82, 'price_adjustment': '30.00'},
                    {'name': 'Midnight Blue', 'sku': 'PC-CASE-BLUE', 'color': '#1B2A4A', 'metallic': 1.0, 'roughness': 0.82, 'price_adjustment': '30.00'},
                ],
            },
            {
                'name': 'RGB Lighting',
                'slug': 'rgb-lighting',
                'description': 'Set the color for your Thermaltake fan LEDs',
                'icon': 'fas fa-lightbulb',
                'sort_order': 1,
                'target_node': 'FAN_Thermaltake_Blades_RGB_0',
                'material_name': 'material_14',
                'options': [
                    {'name': 'White', 'sku': 'PC-RGB-WHITE', 'color': '#FFFFFF', 'metallic': 0.0, 'roughness': 0.20, 'emissive': '#FFFFFF', 'emissive_strength': 10.0, 'is_default': True},
                    {'name': 'Crimson', 'sku': 'PC-RGB-RED', 'color': '#FF1A1A', 'metallic': 0.0, 'roughness': 0.20, 'emissive': '#FF1A1A', 'emissive_strength': 10.0},
                    {'name': 'Electric Blue', 'sku': 'PC-RGB-BLUE', 'color': '#1A8CFF', 'metallic': 0.0, 'roughness': 0.20, 'emissive': '#1A8CFF', 'emissive_strength': 10.0},
                    {'name': 'Neon Green', 'sku': 'PC-RGB-GREEN', 'color': '#1AFF66', 'metallic': 0.0, 'roughness': 0.20, 'emissive': '#1AFF66', 'emissive_strength': 10.0},
                    {'name': 'Purple Haze', 'sku': 'PC-RGB-PURPLE', 'color': '#9B30FF', 'metallic': 0.0, 'roughness': 0.20, 'emissive': '#9B30FF', 'emissive_strength': 10.0},
                    {'name': 'Cyan', 'sku': 'PC-RGB-CYAN', 'color': '#00FFFF', 'metallic': 0.0, 'roughness': 0.20, 'emissive': '#00FFFF', 'emissive_strength': 10.0},
                ],
            },
            {
                'name': 'Side Panel',
                'slug': 'side-panel',
                'description': 'Choose your tempered glass side panel style',
                'icon': 'fas fa-th-large',
                'sort_order': 2,
                'target_node': 'panel_Glass.001_0',
                'material_name': 'Glass.001',
                'options': [
                    {'name': 'Dark Tinted', 'sku': 'PC-PANEL-DARK', 'color': '#1F1E1B', 'metallic': 0.0, 'roughness': 0.0, 'alpha': 0.39, 'is_default': True},
                    {'name': 'Clear Glass', 'sku': 'PC-PANEL-CLEAR', 'color': '#FFFFFF', 'metallic': 0.0, 'roughness': 0.0, 'alpha': 0.15, 'price_adjustment': '25.00'},
                    {'name': 'Smoke Grey', 'sku': 'PC-PANEL-SMOKE', 'color': '#333333', 'metallic': 0.0, 'roughness': 0.0, 'alpha': 0.30},
                    {'name': 'Midnight Tint', 'sku': 'PC-PANEL-MIDNIGHT', 'color': '#0A1628', 'metallic': 0.0, 'roughness': 0.0, 'alpha': 0.35},
                ],
            },
        ],
    },
}


class Command(BaseCommand):
    help = 'Create demo 3D configurator products with full setup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--product',
            type=str,
            required=True,
            choices=PRODUCTS.keys(),
            help='Which demo product to create',
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete the product and all related objects instead of creating',
        )

    def handle(self, *args, **options):
        product_key = options['product']
        spec = PRODUCTS[product_key]

        if options['delete']:
            self._delete_product(spec)
        else:
            self._create_product(spec)

    def _create_color_texture(self, hex_color, sku):
        """Generate a 16x16 solid-color PNG and upload as a MediaAsset.

        Returns the URL path to the uploaded texture file.
        """
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        img = Image.new('RGB', (16, 16), (r, g, b))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        filename = f'texture_{sku.lower()}.png'
        file_size = buf.getbuffer().nbytes
        asset = MediaAsset.objects.create(
            title=f'Color texture {sku}',
            mime_type='image/png',
            file_size=file_size,
            is_public=True,
        )
        asset.original_file.save(filename, File(buf), save=True)
        return asset.original_file.url

    def _delete_product(self, spec):
        """Remove the demo product and all related objects."""
        sku = spec['product']['sku']
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'Product {sku} not found'))
            return

        # Collect option product IDs before deletion
        option_skus = []
        for slot_spec in spec['slots']:
            for opt in slot_spec['options']:
                option_skus.append(opt['sku'])

        # Delete scene config (cascades to mappings)
        SceneConfig.objects.filter(product=product).delete()

        # Delete the main product (cascades to slots and slot options)
        product.delete()

        # Delete option products
        result = Product.objects.filter(sku__in=option_skus).delete()
        deleted_count = result[0] if isinstance(result, tuple) else result

        # Delete media asset (GLB model)
        MediaAsset.objects.filter(title=f'3d_model_{spec["product"]["slug"]}').delete()

        # Delete generated texture assets
        texture_skus = [opt['sku'] for slot in spec['slots']
                        if slot.get('action_type') == 'material_texture'
                        for opt in slot['options']]
        if texture_skus:
            MediaAsset.objects.filter(
                title__in=[f'Color texture {sku}' for sku in texture_skus]
            ).delete()

        # Delete category if empty
        Category.objects.filter(name=spec['category_name'], products__isnull=True).delete()

        self.stdout.write(self.style.SUCCESS(
            f'Deleted product {sku} + {deleted_count} option products'
        ))

    def _create_product(self, spec):
        """Create the full demo product with all configuration."""
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stderr.write(self.style.ERROR('No superuser found'))
            return

        product_data = spec['product']

        # Check if already exists
        if Product.objects.filter(sku=product_data['sku']).exists():
            self.stderr.write(self.style.ERROR(
                f'Product {product_data["sku"]} already exists. '
                f'Use --delete first to recreate.'
            ))
            return

        # Step 1: Upload GLB as MediaAsset
        self.stdout.write('Uploading GLB model...')
        glb_path = os.path.join(settings.BASE_DIR, spec['glb_file'])
        if not os.path.exists(glb_path):
            self.stderr.write(self.style.ERROR(f'GLB file not found: {glb_path}'))
            return

        media_asset = MediaAsset(
            title=f'3d_model_{product_data["slug"]}',
            mime_type='model/gltf-binary',
            file_size=os.path.getsize(glb_path),
            uploaded_by=admin_user,
        )
        with open(glb_path, 'rb') as f:
            filename = os.path.basename(glb_path)
            media_asset.original_file.save(filename, File(f), save=True)
        self.stdout.write(f'  Media asset: {media_asset.id}')

        # Step 2: Create category
        category, _ = Category.objects.get_or_create(
            name=spec['category_name'],
            defaults={'slug': spec['category_name'].lower().replace(' ', '-')},
        )

        # Step 3: Create main configurable product
        self.stdout.write('Creating configurable product...')
        product = Product.objects.create(
            name=product_data['name'],
            slug=product_data['slug'],
            sku=product_data['sku'],
            short_description=product_data.get('short_description', ''),
            product_type='configurable',
            category=category,
            price=product_data['price'],
            price_currency='USD',
            configurator_pricing_strategy=product_data['configurator_pricing_strategy'],
            configurator_base_price=product_data['configurator_base_price'],
            configurator_base_price_currency='USD',
            status='published',
        )
        self.stdout.write(f'  Product: {product.id} - {product.name}')

        # Step 4: Create SceneConfig and parse GLB
        self.stdout.write('Creating 3D scene config...')
        scene_settings = spec['scene']
        scene = SceneConfig.objects.create(
            product=product,
            base_model=media_asset,
            **scene_settings,
        )

        # Parse the GLB to populate node_tree
        self.stdout.write('Parsing GLB scene graph...')
        node_tree = parse_glb_from_media_asset(media_asset)
        if 'error' in node_tree:
            self.stderr.write(self.style.WARNING(f'  GLB parse warning: {node_tree["error"]}'))
        scene.node_tree = node_tree
        scene.save()

        node_count = len(node_tree.get('nodes', {}))
        mat_count = len(node_tree.get('materials', {}))
        self.stdout.write(f'  Scene: {node_count} nodes, {mat_count} materials')

        # Step 5: Create slots, option products, slot options, and mappings
        total_options = 0
        total_mappings = 0

        for slot_spec in spec['slots']:
            self.stdout.write(f'Creating slot: {slot_spec["name"]}...')

            slot = ConfigurationSlot.objects.create(
                product=product,
                name=slot_spec['name'],
                slug=slot_spec['slug'],
                description=slot_spec.get('description', ''),
                icon=slot_spec.get('icon', ''),
                is_required=True,
                min_selections=1,
                max_selections=1,
                sort_order=slot_spec['sort_order'],
            )

            for i, opt_spec in enumerate(slot_spec['options']):
                # Create or reuse option product
                option_product, created = Product.objects.get_or_create(
                    sku=opt_spec['sku'],
                    defaults={
                        'name': opt_spec['name'],
                        'slug': opt_spec['sku'].lower(),
                        'product_type': 'simple',
                        'category': category,
                        'price': Decimal('0.00'),
                        'price_currency': 'USD',
                        'status': 'published',
                        'hide_from_storefront': True,
                    },
                )

                # Create slot option
                slot_option = ConfigurationSlotOption.objects.create(
                    slot=slot,
                    option_product=option_product,
                    price_adjustment=Decimal(str(opt_spec.get('price_adjustment', '0.00'))),
                    price_adjustment_currency='USD',
                    is_default=opt_spec.get('is_default', False),
                    is_popular=opt_spec.get('is_popular', False),
                    sort_order=i,
                )
                total_options += 1

                # Create node mapping(s)
                # Slots can define multiple targets via 'targets' list,
                # or a single target via 'target_node'/'material_name'.
                targets = slot_spec.get('targets') or [
                    {'target_node': slot_spec['target_node'], 'material_name': slot_spec['material_name']},
                ]
                action_type = slot_spec.get('action_type', 'material_color')

                # For material_texture, generate one texture per option (shared across targets)
                texture_url = None
                if action_type == 'material_texture':
                    texture_url = self._create_color_texture(opt_spec['color'], opt_spec['sku'])

                for t_idx, target in enumerate(targets):
                    if action_type == 'material_texture':
                        action_data = {
                            'material_name': target['material_name'],
                            'base_color_url': texture_url,
                        }
                        if opt_spec.get('metallic') is not None:
                            action_data['metallic'] = opt_spec['metallic']
                        if opt_spec.get('roughness') is not None:
                            action_data['roughness'] = opt_spec['roughness']
                    else:
                        action_data = {
                            k: v for k, v in {
                                'color': opt_spec['color'],
                                'metallic': opt_spec.get('metallic', 0.5),
                                'roughness': opt_spec.get('roughness', 0.5),
                                'material_name': target['material_name'],
                                'alpha': opt_spec.get('alpha'),
                                'emissive': opt_spec.get('emissive'),
                                'emissive_strength': opt_spec.get('emissive_strength'),
                            }.items() if v is not None
                        }

                    NodeMapping.objects.create(
                        scene_config=scene,
                        slot_option=slot_option,
                        action_type=action_type,
                        target_node=target['target_node'],
                        action_data=action_data,
                        sort_order=t_idx,
                    )
                    total_mappings += 1

            self.stdout.write(f'  {len(slot_spec["options"])} options created')

        # Step 6: Create stock for main product and all option products
        warehouse = Warehouse.objects.filter(code='MAIN-WH').first()
        if warehouse:
            all_skus = [product_data['sku']] + [
                opt['sku'] for slot in spec['slots'] for opt in slot['options']
            ]
            for sku in all_skus:
                p = Product.objects.filter(sku=sku).first()
                if p:
                    StockItem.objects.get_or_create(
                        product=p, warehouse=warehouse,
                        defaults={'on_hand': 100, 'allocated': 0},
                    )
            self.stdout.write(f'  Stock created for {len(all_skus)} products')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created "{product.name}" with '
            f'{len(spec["slots"])} slots, {total_options} options, {total_mappings} mappings'
        ))
        self.stdout.write(f'  Admin: http://localhost:8000/en/admin/catalog/product/{product.id}/change/')
        self.stdout.write(f'  3D Setup: http://localhost:8000/en/admin/product/{product.id}/3d-scene/')
        self.stdout.write(f'  Frontend: http://localhost:8000/en/product/{product.slug}/')
