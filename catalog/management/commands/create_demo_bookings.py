"""
Management command to create demo booking products with sample booking data.

Creates a fully configured booking product with resources, availability rules,
and realistic sample bookings spanning several months.

Usage:
    python manage.py create_demo_bookings --booking fashion_styling
    python manage.py create_demo_bookings --booking fashion_styling --delete
"""

import random
import uuid
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import (
    Booking,
    BookingAvailabilityRule,
    BookingConfig,
    BookingPersonType,
    BookingRecurrenceRule,
    BookingResource,
    Category,
    Product,
)

# ============================================================================
# Shared pools for realistic data generation
# ============================================================================

STAFF_NAMES = [
    ("Emma", "Rodriguez"),
    ("Liam", "Chen"),
    ("Sophia", "Williams"),
    ("Noah", "Patel"),
    ("Olivia", "Kim"),
    ("James", "Martinez"),
    ("Ava", "Johnson"),
    ("Lucas", "Thompson"),
    ("Mia", "Davis"),
    ("Ethan", "Wilson"),
    ("Isabella", "Brown"),
    ("Mason", "Garcia"),
    ("Charlotte", "Lee"),
    ("Logan", "Anderson"),
    ("Amelia", "Taylor"),
    ("Alexander", "Thomas"),
    ("Harper", "Jackson"),
    ("Benjamin", "White"),
]

CUSTOMER_NAMES = [
    ("Alex", "Morgan"),
    ("Jordan", "Baker"),
    ("Taylor", "Reed"),
    ("Casey", "Brooks"),
    ("Morgan", "Foster"),
    ("Riley", "Price"),
    ("Quinn", "Hayes"),
    ("Avery", "Russell"),
    ("Jamie", "Griffin"),
    ("Drew", "Palmer"),
    ("Skyler", "Ward"),
    ("Robin", "Barnes"),
    ("Hayden", "Ross"),
    ("Parker", "Stewart"),
    ("Reese", "Collins"),
    ("Charlie", "Murphy"),
    ("Kendall", "Cooper"),
    ("Dakota", "Bell"),
    ("Emery", "Diaz"),
    ("Finley", "Hughes"),
    ("Sage", "Perry"),
    ("Rowan", "Butler"),
    ("Blair", "Long"),
    ("Cameron", "Scott"),
    ("Peyton", "Mitchell"),
    ("Addison", "Wood"),
    ("Elliot", "Gray"),
    ("Jessie", "Bennett"),
    ("Marley", "Nelson"),
    ("Sam", "Carter"),
]

CUSTOMER_NOTES_POOL = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",  # Most bookings have no notes (~70%)
    "First time visitor",
    "Returning customer",
    "Referred by a friend",
    "Seen on social media",
    "Has specific preferences - will follow up via email",
    "Prefers morning appointments",
    "Running a few minutes late",
    "Birthday gift",
    "Anniversary celebration",
    "Would like recommendations",
    "Allergies - please check notes",
    "VIP customer",
]

CANCELLATION_REASONS = [
    "Schedule conflict",
    "Something came up",
    "Feeling unwell",
    "Travel plans changed",
    "Found an alternative",
    "Budget constraints",
    "Weather concerns",
    "Family emergency",
]

EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "email.com", "icloud.com"]

# Booking-specific customer notes pools
PET_NOTES = [
    "",
    "",
    "",
    "",
    "",
    "Golden Retriever, 3 years old",
    "Nervous around dryers - please use low setting",
    "Labradoodle, needs full dematting",
    "Small Pomeranian, very friendly",
    "Cat - Maine Coon, first grooming visit",
    "German Shepherd, sheds heavily",
    "Two dogs - booking second appointment separately",
    "Puppy, 6 months old - first professional groom",
    "Senior dog, gentle handling please",
    "Has skin allergies - hypoallergenic shampoo only",
]

AUTO_NOTES = [
    "",
    "",
    "",
    "",
    "",
    "2022 Tesla Model 3 - white",
    "Black SUV, lots of dog hair inside",
    "Preparing car for sale - need full detail",
    "Ceramic coating touch-up needed",
    "Leather interior needs conditioning",
    "Just returned from a road trip - very dirty",
    "New car, first detail to protect paint",
    "Minor scratches on driver side - can these be buffed?",
    "Please pay extra attention to the wheels",
]

GAMING_NOTES = [
    "",
    "",
    "",
    "",
    "",
    "Currently Silver rank, want to reach Gold",
    "New to the game, need basics",
    "Want to improve aim and crosshair placement",
    "Returning player after a break",
    "Struggling with ranked anxiety",
    "Want to learn a new agent/champion",
    "Team captain, need shotcalling tips",
    "Console player switching to PC",
]

FARM_TOUR_NOTES = [
    "",
    "",
    "",
    "",
    "",
    "School group - 15 children + 3 adults",
    "Birthday celebration for our 6 year old",
    "Homeschool group outing",
    "Interested in the bee-keeping section",
    "Family reunion - 4 families attending",
    "Some guests have nut allergies",
    "Can we arrange extra animal feeding time?",
    "Photography club visit - will bring cameras",
    "First time on a farm - very excited!",
]

BIRTHDAY_PARTY_NOTES = [
    "",
    "",
    "",
    "",
    "",
    "Turning 7! Superhero theme please",
    "Nut-free cake required - severe allergy",
    "15 kids confirmed, expecting 20",
    "Please set up at 9:30, guests arrive at 10",
    "Princess theme decorations",
    "Will bring own cake, need a table for it",
    "Some kids are vegetarian",
    "Parents staying - need extra chairs",
    "Pirate theme - can we add treasure hunt?",
]

POTTERY_NOTES = [
    "",
    "",
    "",
    "",
    "",
    "Complete beginner, never touched clay",
    "Want to make a gift for my partner",
    "Group of friends - all beginners",
    "Have some experience, want to try wheel",
    "Date night activity - booking for 2",
    "Would like to focus on glazing techniques",
    "Birthday gift experience",
    "Corporate team building - booking additional slots",
]

FARM_STAY_NOTES = [
    "",
    "",
    "",
    "",
    "",
    "Anniversary getaway",
    "Would love early check-in if available",
    "Traveling with a small dog - is that OK?",
    "Interested in the farm tour during our stay",
    "Celebrating retirement",
    "First time visiting a working farm",
    "Will need a baby cot",
    "Late check-out requested if possible",
    "Honeymoon trip",
    "Kids are excited to see the animals",
]


# ============================================================================
# Booking definitions
# ============================================================================

BOOKINGS = {
    # ------------------------------------------------------------------
    # 1. Fashion Styling - Basic appointment, customer-selected stylists
    # ------------------------------------------------------------------
    "fashion_styling": {
        "product": {
            "name": "Personal Styling Consultation",
            "slug": "personal-styling-consultation",
            "sku": "BK-FASHION-STYLE",
            "short_description": (
                "Book a 30-minute video call with one of our professional stylists. "
                "Get personalized outfit recommendations, wardrobe advice, and styling "
                "tips tailored to your body type, lifestyle, and budget."
            ),
            "price": Decimal("49.99"),
        },
        "category_name": "Styling Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "fixed",
            "duration": 30,
            "duration_unit": "minute",
            "buffer_before": 5,
            "buffer_after": 10,
            "min_advance": 24,
            "min_advance_unit": "hour",
            "max_advance": 2,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 24,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": True,
            "deposit_enabled": False,
            "reminder_enabled": True,
            "reminder_hours_before": [1, 24],
        },
        "resources": [
            {
                "name": "Emma Rodriguez",
                "description": "Senior stylist specializing in womenswear and casual looks",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "emma.rodriguez@example.com",
                "is_per_night": False,
                "tags": ["womenswear", "casual", "workwear"],
            },
            {
                "name": "Liam Chen",
                "description": "Menswear specialist with expertise in smart-casual and formal styling",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "liam.chen@example.com",
                "is_per_night": False,
                "tags": ["menswear", "formal", "smart-casual"],
            },
            {
                "name": "Sophia Williams",
                "description": "Personal shopper and styling expert for all occasions",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "sophia.williams@example.com",
                "is_per_night": False,
                "tags": ["womenswear", "menswear", "occasionwear"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4],  # Mon-Fri
                "start_time": "09:00",
                "end_time": "17:00",
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5],  # Saturday
                "start_time": "10:00",
                "end_time": "14:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 70,
            "months_back": 3,
            "months_forward": 2,
        },
    },
    # ------------------------------------------------------------------
    # 2. Jewelry Showroom - Deposit required, confirmation required
    # ------------------------------------------------------------------
    "jewelry_showroom": {
        "product": {
            "name": "Private Showroom Appointment",
            "slug": "private-showroom-appointment",
            "sku": "BK-JEWELRY-SHOW",
            "short_description": (
                "Book a 45-minute private session with one of our expert jewelers. "
                "View our exclusive collection in a one-on-one setting and receive "
                "personalized guidance on the perfect piece for any occasion."
            ),
            "price": Decimal("75.00"),
        },
        "category_name": "Showroom Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "fixed",
            "duration": 45,
            "duration_unit": "minute",
            "buffer_before": 10,
            "buffer_after": 15,
            "min_advance": 48,
            "min_advance_unit": "hour",
            "max_advance": 3,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": True,
            "cancellation_allowed": True,
            "cancellation_deadline": 48,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": False,
            "deposit_enabled": True,
            "deposit_type": "fixed",
            "deposit_amount": Decimal("50.00"),
            "reminder_enabled": True,
            "reminder_hours_before": [2, 24, 48],
        },
        "resources": [
            {
                "name": "Marcus Blackwell",
                "description": "Master jeweler with 20+ years in diamond selection and custom design",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "marcus.blackwell@example.com",
                "tags": ["diamonds", "engagement", "custom-design"],
            },
            {
                "name": "Priya Sharma",
                "description": "GIA-certified gemologist specializing in colored gemstones and vintage pieces",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "priya.sharma@example.com",
                "tags": ["gemstones", "vintage", "estate-jewelry"],
            },
            {
                "name": "Isabella Fontaine",
                "description": "Bridal jewelry specialist and fine jewelry consultant",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "isabella.fontaine@example.com",
                "tags": ["bridal", "fine-jewelry", "gifts"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [1, 2, 3, 4, 5],  # Tue-Sat (closed Mon)
                "start_time": "10:00",
                "end_time": "18:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 65,
            "months_back": 3,
            "months_forward": 2,
        },
    },
    # ------------------------------------------------------------------
    # 3. Beauty Analysis - Auto-assigned resource, short duration
    # ------------------------------------------------------------------
    "beauty_analysis": {
        "product": {
            "name": "Virtual Skin Analysis",
            "slug": "virtual-skin-analysis",
            "sku": "BK-BEAUTY-SKIN",
            "short_description": (
                "Book a 20-minute video consultation with a certified aesthetician. "
                "Get a personalized skin assessment, product recommendations, and a "
                "custom skincare routine tailored to your skin type and concerns."
            ),
            "price": Decimal("29.99"),
        },
        "category_name": "Beauty Consultations",
        "config": {
            "booking_type": "appointment",
            "duration_type": "fixed",
            "duration": 20,
            "duration_unit": "minute",
            "buffer_before": 5,
            "buffer_after": 5,
            "min_advance": 12,
            "min_advance_unit": "hour",
            "max_advance": 1,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 6,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "date_picker",
            "customer_timezone_enabled": True,
            "deposit_enabled": False,
            "reminder_enabled": True,
            "reminder_hours_before": [1, 12],
        },
        "resources": [
            {
                "name": "Dr. Amara Obi",
                "description": "Board-certified dermatologist with 10+ years in clinical skincare",
                "resource_type": "staff",
                "assignment_type": "automatic",
                "email": "amara.obi@example.com",
                "tags": ["dermatology", "anti-aging", "acne"],
            },
            {
                "name": "Yuki Tanaka",
                "description": "Licensed aesthetician specializing in sensitive skin and K-beauty routines",
                "resource_type": "staff",
                "assignment_type": "automatic",
                "email": "yuki.tanaka@example.com",
                "tags": ["sensitive-skin", "k-beauty", "natural"],
            },
            {
                "name": "Claire Dubois",
                "description": "Skincare specialist focused on hyperpigmentation and sun damage repair",
                "resource_type": "staff",
                "assignment_type": "automatic",
                "email": "claire.dubois@example.com",
                "tags": ["pigmentation", "sun-care", "clinical"],
            },
            {
                "name": "Fatima Al-Rashid",
                "description": "Holistic beauty advisor blending traditional and modern approaches",
                "resource_type": "staff",
                "assignment_type": "automatic",
                "email": "fatima.alrashid@example.com",
                "tags": ["holistic", "organic", "wellness"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4],  # Mon-Fri
                "start_time": "08:00",
                "end_time": "20:00",
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5, 6],  # Sat-Sun
                "start_time": "09:00",
                "end_time": "17:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 80,
            "months_back": 3,
            "months_forward": 2,
        },
    },
    # ------------------------------------------------------------------
    # 4. Farm Tour - Event, group booking with person types, max capacity
    # ------------------------------------------------------------------
    "farm_tour": {
        "product": {
            "name": "Farm & Orchard Tour",
            "slug": "farm-orchard-tour",
            "sku": "BK-FARM-TOUR",
            "short_description": (
                "Join a half-day guided tour of our organic farm and orchard. "
                "Feed the animals, pick seasonal fruit, and enjoy a farm-fresh "
                "picnic lunch. Perfect for families and school groups."
            ),
            "price": Decimal("45.00"),
        },
        "category_name": "Farm Experiences",
        "config": {
            "booking_type": "event",
            "duration_type": "fixed",
            "duration": 4,
            "duration_unit": "hour",
            "buffer_before": 0,
            "buffer_after": 30,
            "min_advance": 2,
            "min_advance_unit": "day",
            "max_advance": 2,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 20,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 48,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": False,
            "deposit_enabled": False,
            "reminder_enabled": True,
            "reminder_hours_before": [24, 48],
        },
        "resources": [
            {
                "name": "Farmer Tom",
                "description": "Farm owner and lead tour guide with expertise in organic farming",
                "resource_type": "staff",
                "assignment_type": "automatic",
                "email": "tom@example.com",
                "tags": ["organic", "animals", "orchard"],
            },
            {
                "name": "Farmer Sarah",
                "description": "Animal care specialist and children-friendly tour guide",
                "resource_type": "staff",
                "assignment_type": "automatic",
                "email": "sarah@example.com",
                "tags": ["animals", "kids", "education"],
            },
        ],
        "person_types": [
            {
                "name": "Adult",
                "cost_adjustment": 0,
                "min_persons": 1,
                "max_persons": 10,
                "is_counted_for_capacity": True,
                "is_per_night": False,
            },
            {
                "name": "Child (3-12)",
                "cost_adjustment": -20,
                "min_persons": 0,
                "max_persons": 8,
                "is_counted_for_capacity": True,
                "is_per_night": False,
            },
            {
                "name": "Infant (0-2)",
                "cost_adjustment": -45,
                "min_persons": 0,
                "max_persons": 3,
                "is_counted_for_capacity": False,
                "is_per_night": False,
            },
        ],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4, 5, 6],  # Every day
                "start_time": "09:00",
                "end_time": "13:00",  # Morning tour
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4, 5, 6],
                "start_time": "13:00",
                "end_time": "17:00",  # Afternoon tour
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 90,
            "months_back": 3,
            "months_forward": 2,
            "per_person_pricing": True,
            "notes_pool": FARM_TOUR_NOTES,
        },
    },
    # ------------------------------------------------------------------
    # 4b. Farm Stay - Accommodation, nightly, check-in/check-out
    # ------------------------------------------------------------------
    "farm_stay": {
        "product": {
            "name": "Farm Stay Experience",
            "slug": "farm-stay-experience",
            "sku": "BK-FARM-STAY",
            "short_description": (
                "Escape to the countryside with our farm stay accommodation. "
                "Wake up to rooster calls, collect fresh eggs for breakfast, "
                "and enjoy the tranquil rural lifestyle. Check-in 2pm, checkout 10am."
            ),
            "price": Decimal("175.00"),
        },
        "category_name": "Farm Experiences",
        "config": {
            "booking_type": "accommodation",
            "duration_type": "customer_selected",
            "duration": 2,
            "duration_unit": "night",
            "min_duration": 2,
            "max_duration": 14,
            "standard_occupancy": 2,
            "min_stay": 2,
            "max_stay": 14,
            "buffer_before": 0,
            "buffer_after": 0,
            "min_advance": 3,
            "min_advance_unit": "day",
            "max_advance": 3,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": True,
            "cancellation_allowed": True,
            "cancellation_deadline": 1,
            "cancellation_deadline_unit": "week",
            "calendar_display": "date_range",
            "customer_timezone_enabled": False,
            "deposit_enabled": True,
            "deposit_type": "percentage",
            "deposit_amount": Decimal("50.00"),
            "check_in_time": "14:00",
            "check_out_time": "10:00",
            "reminder_enabled": True,
            "reminder_hours_before": [24, 72],
        },
        "resources": [
            {
                "name": "Sunflower Cottage",
                "description": "Cozy 1-bedroom cottage with fireplace, sleeps 2, garden view",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "is_per_night": True,
                "tags": ["cottage", "couples", "romantic"],
            },
            {
                "name": "Orchard Cabin",
                "description": "Spacious 2-bedroom cabin surrounded by apple trees, sleeps 4",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "base_cost_adjustment": 50,
                "is_per_night": True,
                "tags": ["cabin", "family", "spacious"],
            },
            {
                "name": "Barn Loft Suite",
                "description": "Converted barn loft with rustic charm, king bed, and hot tub",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "base_cost_adjustment": 85,
                "is_per_night": True,
                "tags": ["loft", "luxury", "hot-tub"],
            },
        ],
        "person_types": [
            {
                "name": "Adult",
                "cost_adjustment": 0,
                "min_persons": 1,
                "max_persons": 4,
                "is_counted_for_capacity": True,
                "is_per_night": True,
            },
            {
                "name": "Child",
                "cost_adjustment": -50,
                "min_persons": 0,
                "max_persons": 3,
                "is_counted_for_capacity": True,
                "is_per_night": True,
            },
        ],
        "availability_rules": [
            # Base: available every day
            {
                "rule_type": "available",
                "scope": "all_dates",
                "priority": 10,
            },
            # Weekend surcharge: Fri+Sat nights +15%
            {
                "rule_type": "custom_cost",
                "scope": "days_of_week",
                "days_of_week": [4, 5],
                "cost_adjustment": Decimal("15"),
                "cost_adjustment_type": "percentage",
                "priority": 20,
            },
            # Peak summer: July-August override $225/night, min 3 nights
            {
                "rule_type": "custom_cost",
                "scope": "date_range",
                "start_date": "CURRENT_YEAR-07-01",
                "end_date": "CURRENT_YEAR-08-31",
                "cost_override": Decimal("225.00"),
                "min_stay_override": 3,
                "priority": 30,
            },
            # Long stay discount: 5+ nights → 10% off
            {
                "rule_type": "custom_cost",
                "scope": "all_dates",
                "length_of_stay_min": 5,
                "length_of_stay_discount_percent": Decimal("10.00"),
                "priority": 40,
            },
            # Early bird: 30+ days ahead → $10/night off
            {
                "rule_type": "custom_cost",
                "scope": "all_dates",
                "cost_adjustment": Decimal("-10.00"),
                "cost_adjustment_type": "flat",
                "lead_time_min_days": 30,
                "priority": 15,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 50,
            "months_back": 3,
            "months_forward": 2,
            "notes_pool": FARM_STAY_NOTES,
        },
    },
    # ------------------------------------------------------------------
    # 5. Tech Consultation - Customer-selected duration (30/60/90min)
    # ------------------------------------------------------------------
    "tech_consultation": {
        "product": {
            "name": "Tech Setup Consultation",
            "slug": "tech-setup-consultation",
            "sku": "BK-TECH-CONSULT",
            "short_description": (
                "Book a remote screen-share session with one of our tech experts. "
                "Get help setting up your new device, troubleshooting issues, "
                "optimizing performance, or learning advanced features. "
                "Choose 30, 60, or 90 minutes based on your needs."
            ),
            "price": Decimal("59.99"),
        },
        "category_name": "Tech Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "customer_selected",
            "duration": 60,
            "duration_unit": "minute",
            "min_duration": 30,
            "max_duration": 90,
            "buffer_before": 5,
            "buffer_after": 10,
            "min_advance": 4,
            "min_advance_unit": "hour",
            "max_advance": 2,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 12,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": True,
            "deposit_enabled": False,
            "reminder_enabled": True,
            "reminder_hours_before": [1, 24],
        },
        "resources": [
            {
                "name": "Raj Patel",
                "description": "Hardware specialist covering PCs, laptops, and peripherals",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "raj.patel@example.com",
                "tags": ["hardware", "pc", "troubleshooting"],
            },
            {
                "name": "Sarah Kim",
                "description": "Apple ecosystem expert - Mac, iPhone, iPad, and smart home setup",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "sarah.kim@example.com",
                "tags": ["apple", "mac", "smart-home"],
            },
            {
                "name": "Mike Torres",
                "description": "Networking and security specialist for home and small business",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "mike.torres@example.com",
                "tags": ["networking", "security", "smart-home"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4],  # Mon-Fri
                "start_time": "09:00",
                "end_time": "21:00",
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5],  # Saturday
                "start_time": "10:00",
                "end_time": "18:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 75,
            "months_back": 3,
            "months_forward": 2,
        },
    },
    # ------------------------------------------------------------------
    # 6. Personal Training - Recurring booking, resource tags for matching
    # ------------------------------------------------------------------
    "personal_training": {
        "product": {
            "name": "Personal Training Session",
            "slug": "personal-training-session",
            "sku": "BK-FITNESS-PT",
            "short_description": (
                "Book a 1-hour personal training session with a certified trainer. "
                "Whether in-person at our facility or via live video, get a customized "
                "workout plan and real-time coaching to reach your fitness goals."
            ),
            "price": Decimal("79.99"),
        },
        "category_name": "Training Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "fixed",
            "duration": 1,
            "duration_unit": "hour",
            "buffer_before": 10,
            "buffer_after": 15,
            "min_advance": 12,
            "min_advance_unit": "hour",
            "max_advance": 2,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 24,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": False,
            "deposit_enabled": False,
            "recurrence_enabled": True,
            "reminder_enabled": True,
            "reminder_hours_before": [1, 24],
        },
        "resources": [
            {
                "name": "Jake Morrison",
                "description": "NASM-certified trainer specializing in strength training and HIIT",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "jake.morrison@example.com",
                "tags": ["strength", "hiit", "weight-loss"],
            },
            {
                "name": "Ana Costa",
                "description": "Yoga and flexibility specialist with Pilates certification",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "ana.costa@example.com",
                "tags": ["yoga", "pilates", "flexibility"],
            },
            {
                "name": "Devon Clarke",
                "description": "Sports performance coach for endurance and functional fitness",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "devon.clarke@example.com",
                "tags": ["endurance", "functional", "sports"],
            },
            {
                "name": "Mei Lin Wu",
                "description": "Rehabilitation and mobility specialist with physical therapy background",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "mei.wu@example.com",
                "tags": ["rehab", "mobility", "senior-fitness"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4],  # Mon-Fri
                "start_time": "06:00",
                "end_time": "21:00",
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5, 6],  # Sat-Sun
                "start_time": "07:00",
                "end_time": "18:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [
            {
                "frequency": "weekly",
                "day_of_week": 0,  # Monday
                "start_time": "06:00",
                "end_time": "21:00",
                "auto_create_days_ahead": 60,
            },
            {
                "frequency": "weekly",
                "day_of_week": 3,  # Thursday
                "start_time": "06:00",
                "end_time": "21:00",
                "auto_create_days_ahead": 60,
            },
        ],
        "booking_generation": {
            "count": 80,
            "months_back": 3,
            "months_forward": 2,
        },
    },
    # ------------------------------------------------------------------
    # 7. Interior Design - Higher price, deposit percentage, weekends
    # ------------------------------------------------------------------
    "interior_design": {
        "product": {
            "name": "Interior Design Consultation",
            "slug": "interior-design-consultation",
            "sku": "BK-HOME-DESIGN",
            "short_description": (
                "Book a 1-hour video consultation with a professional interior designer. "
                "Share your space, discuss your vision, and receive a personalized mood board "
                "with product recommendations within 48 hours of your session."
            ),
            "price": Decimal("149.00"),
        },
        "category_name": "Design Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "fixed",
            "duration": 1,
            "duration_unit": "hour",
            "buffer_before": 10,
            "buffer_after": 15,
            "min_advance": 2,
            "min_advance_unit": "day",
            "max_advance": 3,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 48,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": True,
            "deposit_enabled": True,
            "deposit_type": "percentage",
            "deposit_amount": Decimal("25.00"),
            "reminder_enabled": True,
            "reminder_hours_before": [2, 24, 48],
        },
        "resources": [
            {
                "name": "Olivia Harper",
                "description": "Contemporary and minimalist design specialist",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "olivia.harper@example.com",
                "base_cost_adjustment": 25,
                "tags": ["contemporary", "minimalist", "scandinavian"],
            },
            {
                "name": "Daniel Keane",
                "description": "Traditional and transitional interiors with a focus on living spaces",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "daniel.keane@example.com",
                "tags": ["traditional", "transitional", "living-room"],
            },
            {
                "name": "Zara Ahmadi",
                "description": "Bohemian and eclectic style specialist with sustainable sourcing expertise",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "zara.ahmadi@example.com",
                "base_cost_adjustment": 15,
                "tags": ["bohemian", "eclectic", "sustainable"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4],  # Mon-Fri
                "start_time": "09:00",
                "end_time": "18:00",
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5, 6],  # Sat-Sun (weekend availability)
                "start_time": "10:00",
                "end_time": "16:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 60,
            "months_back": 3,
            "months_forward": 2,
        },
    },
    # ------------------------------------------------------------------
    # 8. Birthday Party - Event, rooms, person types, weekend-only
    # ------------------------------------------------------------------
    "birthday_party": {
        "product": {
            "name": "Birthday Party Package",
            "slug": "birthday-party-package",
            "sku": "BK-PARTY-BDAY",
            "short_description": (
                "Celebrate your special day with our all-inclusive party package! "
                "2-hour private party room with decorations, cake, party host, "
                "games, and loot bags for all guests."
            ),
            "price": Decimal("299.00"),
        },
        "category_name": "Party Packages",
        "config": {
            "booking_type": "event",
            "duration_type": "fixed",
            "duration": 2,
            "duration_unit": "hour",
            "buffer_before": 30,
            "buffer_after": 30,
            "min_advance": 1,
            "min_advance_unit": "week",
            "max_advance": 3,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": True,
            "cancellation_allowed": True,
            "cancellation_deadline": 1,
            "cancellation_deadline_unit": "week",
            "calendar_display": "calendar",
            "customer_timezone_enabled": False,
            "deposit_enabled": True,
            "deposit_type": "fixed",
            "deposit_amount": Decimal("100.00"),
            "reminder_enabled": True,
            "reminder_hours_before": [24, 72],
        },
        "resources": [
            {
                "name": "Galaxy Room",
                "description": "Space-themed party room with LED ceiling, capacity 30 guests",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "tags": ["large", "themed", "indoor"],
            },
            {
                "name": "Jungle Room",
                "description": "Tropical jungle-themed room with climbing wall, capacity 25 guests",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "base_cost_adjustment": 25,
                "tags": ["medium", "themed", "active"],
            },
            {
                "name": "Garden Pavilion",
                "description": "Outdoor covered pavilion with BBQ area, capacity 40 guests",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "base_cost_adjustment": 50,
                "tags": ["large", "outdoor", "bbq"],
            },
        ],
        "person_types": [
            {
                "name": "Child",
                "cost_adjustment": 15,
                "min_persons": 5,
                "max_persons": 25,
                "is_counted_for_capacity": True,
            },
            {
                "name": "Adult",
                "cost_adjustment": 0,
                "min_persons": 1,
                "max_persons": 10,
                "is_counted_for_capacity": True,
            },
        ],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5, 6],  # Sat-Sun only
                "start_time": "10:00",
                "end_time": "18:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 50,
            "months_back": 3,
            "months_forward": 2,
            "notes_pool": BIRTHDAY_PARTY_NOTES,
        },
    },
    # ------------------------------------------------------------------
    # 9. Pottery Workshop - Class, max 6 people, person types
    # ------------------------------------------------------------------
    "pottery_workshop": {
        "product": {
            "name": "Pottery & Ceramics Workshop",
            "slug": "pottery-ceramics-workshop",
            "sku": "BK-CRAFT-POTTERY",
            "short_description": (
                "Join a 2-hour hands-on pottery workshop led by an experienced ceramicist. "
                "Learn wheel throwing or hand-building techniques. All materials and firing "
                "included - take home your finished piece in 2 weeks."
            ),
            "price": Decimal("65.00"),
        },
        "category_name": "Creative Workshops",
        "config": {
            "booking_type": "class",
            "duration_type": "fixed",
            "duration": 2,
            "duration_unit": "hour",
            "buffer_before": 15,
            "buffer_after": 15,
            "min_advance": 2,
            "min_advance_unit": "day",
            "max_advance": 2,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 6,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 48,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": False,
            "deposit_enabled": False,
            "reminder_enabled": True,
            "reminder_hours_before": [24, 48],
        },
        "resources": [
            {
                "name": "Studio A - Wheel Throwing",
                "description": "Equipped with 6 pottery wheels for wheel throwing classes",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "tags": ["wheel", "beginner", "intermediate"],
            },
            {
                "name": "Studio B - Hand Building",
                "description": "Open workspace for hand-building, sculpting, and glazing",
                "resource_type": "room",
                "assignment_type": "customer_selected",
                "tags": ["hand-building", "sculpting", "all-levels"],
            },
        ],
        "person_types": [
            {
                "name": "Adult",
                "cost_adjustment": 0,
                "min_persons": 1,
                "max_persons": 6,
                "is_counted_for_capacity": True,
            },
            {
                "name": "Student (16-21)",
                "cost_adjustment": -20,
                "min_persons": 0,
                "max_persons": 6,
                "is_counted_for_capacity": True,
            },
        ],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [2, 3, 4, 5, 6],  # Wed-Sun
                "start_time": "10:00",
                "end_time": "12:00",  # Morning class
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [2, 3, 4, 5, 6],  # Wed-Sun
                "start_time": "14:00",
                "end_time": "16:00",  # Afternoon class
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 70,
            "months_back": 3,
            "months_forward": 2,
            "per_person_pricing": True,
            "notes_pool": POTTERY_NOTES,
        },
    },
    # ------------------------------------------------------------------
    # 10. Gaming Coaching - Evening/weekend availability, low price
    # ------------------------------------------------------------------
    "gaming_coaching": {
        "product": {
            "name": "1-on-1 Gaming Coaching Session",
            "slug": "gaming-coaching-session",
            "sku": "BK-GAMING-COACH",
            "short_description": (
                "Book a 1-hour live coaching session with a ranked competitive player. "
                "Get gameplay analysis, strategy tips, and real-time guidance to "
                "improve your skills and climb the ladder."
            ),
            "price": Decimal("24.99"),
        },
        "category_name": "Coaching Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "fixed",
            "duration": 1,
            "duration_unit": "hour",
            "buffer_before": 5,
            "buffer_after": 5,
            "min_advance": 2,
            "min_advance_unit": "hour",
            "max_advance": 2,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 6,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": True,
            "deposit_enabled": False,
            "reminder_enabled": True,
            "reminder_hours_before": [1],
        },
        "resources": [
            {
                "name": "NightOwl (Tyler Ross)",
                "description": "Top 500 FPS player - Valorant, CS2, and Overwatch specialist",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "tyler.ross@example.com",
                "tags": ["fps", "valorant", "cs2", "overwatch"],
            },
            {
                "name": "Zenith (Hana Park)",
                "description": "Diamond-ranked MOBA coach - League of Legends and Dota 2",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "hana.park@example.com",
                "tags": ["moba", "league", "dota2", "strategy"],
            },
            {
                "name": "Blitz (Marcus Cole)",
                "description": "Battle royale specialist - Fortnite, Apex Legends, Warzone",
                "resource_type": "staff",
                "assignment_type": "customer_selected",
                "email": "marcus.cole@example.com",
                "tags": ["battle-royale", "fortnite", "apex", "warzone"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4],  # Mon-Fri (evenings)
                "start_time": "16:00",
                "end_time": "23:00",
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5, 6],  # Sat-Sun (all day)
                "start_time": "10:00",
                "end_time": "23:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 85,
            "months_back": 3,
            "months_forward": 2,
            "notes_pool": GAMING_NOTES,
        },
    },
    # ------------------------------------------------------------------
    # 11. Auto Detailing - Customer-selected duration (2-8hr), vehicle resources
    # ------------------------------------------------------------------
    "auto_detailing": {
        "product": {
            "name": "Professional Auto Detailing",
            "slug": "professional-auto-detailing",
            "sku": "BK-AUTO-DETAIL",
            "short_description": (
                "Book a professional detailing appointment for your vehicle. "
                "Select your preferred service duration from 2 to 8 hours for a "
                "thorough exterior wash, interior cleaning, and protective coating."
            ),
            "price": Decimal("149.99"),
        },
        "category_name": "Detailing Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "customer_selected",
            "duration": 4,
            "duration_unit": "hour",
            "min_duration": 2,
            "max_duration": 8,
            "buffer_before": 15,
            "buffer_after": 30,
            "min_advance": 2,
            "min_advance_unit": "day",
            "max_advance": 1,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": True,
            "cancellation_allowed": True,
            "cancellation_deadline": 48,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "date_picker",
            "customer_timezone_enabled": False,
            "deposit_enabled": True,
            "deposit_type": "percentage",
            "deposit_amount": Decimal("30.00"),
            "reminder_enabled": True,
            "reminder_hours_before": [2, 24],
        },
        "resources": [
            {
                "name": "Bay 1 - Standard",
                "description": "Standard detailing bay for sedans and compact vehicles",
                "resource_type": "equipment",
                "assignment_type": "automatic",
                "tags": ["sedan", "compact", "standard"],
            },
            {
                "name": "Bay 2 - Standard",
                "description": "Standard detailing bay for sedans and mid-size vehicles",
                "resource_type": "equipment",
                "assignment_type": "automatic",
                "tags": ["sedan", "mid-size", "standard"],
            },
            {
                "name": "Bay 3 - Large Vehicle",
                "description": "Oversized bay for SUVs, trucks, and vans",
                "resource_type": "equipment",
                "assignment_type": "automatic",
                "base_cost_adjustment": 50,
                "tags": ["suv", "truck", "van", "large"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4, 5],  # Mon-Sat
                "start_time": "07:00",
                "end_time": "17:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 55,
            "months_back": 3,
            "months_forward": 2,
            "notes_pool": AUTO_NOTES,
        },
    },
    # ------------------------------------------------------------------
    # 12. Pet Grooming - Variable duration, equipment resources, cost tiers
    # ------------------------------------------------------------------
    "pet_grooming": {
        "product": {
            "name": "Pet Grooming Appointment",
            "slug": "pet-grooming-appointment",
            "sku": "BK-PET-GROOM",
            "short_description": (
                "Book a grooming appointment for your furry friend. Choose from "
                "bath & brush, full groom, or premium spa packages. Our certified "
                "groomers handle dogs and cats of all sizes with gentle care."
            ),
            "price": Decimal("45.00"),
        },
        "category_name": "Grooming Services",
        "config": {
            "booking_type": "appointment",
            "duration_type": "customer_selected",
            "duration": 60,
            "duration_unit": "minute",
            "min_duration": 30,
            "max_duration": 120,
            "buffer_before": 10,
            "buffer_after": 15,
            "min_advance": 24,
            "min_advance_unit": "hour",
            "max_advance": 1,
            "max_advance_unit": "month",
            "max_bookings_per_slot": 1,
            "confirmation_required": False,
            "cancellation_allowed": True,
            "cancellation_deadline": 24,
            "cancellation_deadline_unit": "hour",
            "calendar_display": "calendar",
            "customer_timezone_enabled": False,
            "deposit_enabled": False,
            "reminder_enabled": True,
            "reminder_hours_before": [2, 24],
        },
        "resources": [
            {
                "name": "Grooming Station A",
                "description": "Full-service grooming station with hydraulic table - small/medium pets",
                "resource_type": "equipment",
                "assignment_type": "automatic",
                "tags": ["small", "medium", "dogs", "cats"],
            },
            {
                "name": "Grooming Station B",
                "description": "Full-service grooming station with large tub - all pet sizes",
                "resource_type": "equipment",
                "assignment_type": "automatic",
                "base_cost_adjustment": 15,
                "tags": ["large", "xl", "dogs"],
            },
            {
                "name": "Spa Suite",
                "description": "Premium private suite with aromatherapy bath and blueberry facial",
                "resource_type": "equipment",
                "assignment_type": "customer_selected",
                "base_cost_adjustment": 35,
                "tags": ["spa", "premium", "all-sizes"],
            },
        ],
        "person_types": [],
        "availability_rules": [
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [0, 1, 2, 3, 4],  # Mon-Fri
                "start_time": "08:00",
                "end_time": "18:00",
                "priority": 10,
            },
            {
                "rule_type": "available",
                "scope": "days_of_week",
                "days_of_week": [5],  # Saturday
                "start_time": "09:00",
                "end_time": "16:00",
                "priority": 10,
            },
        ],
        "recurrence_rules": [],
        "booking_generation": {
            "count": 75,
            "months_back": 3,
            "months_forward": 2,
            "notes_pool": PET_NOTES,
        },
    },
}


class Command(BaseCommand):
    help = "Create demo booking products with sample booking data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--booking",
            type=str,
            required=True,
            choices=BOOKINGS.keys(),
            help="Which demo booking to create",
        )
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete the booking product and all related objects",
        )

    def handle(self, *args, **options):
        spec = BOOKINGS[options["booking"]]
        if options["delete"]:
            self._delete_booking(spec)
        else:
            self._create_booking(spec)

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    def _create_booking(self, spec):
        product_data = spec["product"]
        sku = product_data["sku"]

        # Check for existing product (including soft-deleted)
        if Product.all_objects.filter(sku=sku).exists():
            self.stderr.write(
                self.style.ERROR(f"Product {sku} already exists. Use --delete first to recreate.")
            )
            return

        # Step 1: Category
        self.stdout.write("Creating category...")
        category, _ = Category.objects.get_or_create(
            name=spec["category_name"],
            defaults={"slug": spec["category_name"].lower().replace(" ", "-")},
        )

        # Step 2: Product
        self.stdout.write("Creating booking product...")
        product = Product.objects.create(
            name=product_data["name"],
            slug=product_data["slug"],
            sku=sku,
            short_description=product_data.get("short_description", ""),
            product_type="booking",
            category=category,
            price=product_data["price"],
            price_currency="USD",
            status="published",
            track_inventory=False,
        )
        self.stdout.write(f"  Product: {product.id} - {product.name}")

        # Step 3: BookingConfig
        self.stdout.write("Creating booking configuration...")
        config_data = spec["config"]
        config = BookingConfig.objects.create(
            product=product,
            booking_type=config_data["booking_type"],
            duration_type=config_data.get("duration_type", "fixed"),
            duration=config_data["duration"],
            duration_unit=config_data["duration_unit"],
            min_duration=config_data.get("min_duration"),
            max_duration=config_data.get("max_duration"),
            buffer_before=config_data.get("buffer_before", 0),
            buffer_after=config_data.get("buffer_after", 0),
            min_advance=config_data.get("min_advance", 1),
            min_advance_unit=config_data.get("min_advance_unit", "hour"),
            max_advance=config_data.get("max_advance", 3),
            max_advance_unit=config_data.get("max_advance_unit", "month"),
            max_bookings_per_slot=config_data.get("max_bookings_per_slot", 1),
            confirmation_required=config_data.get("confirmation_required", False),
            cancellation_allowed=config_data.get("cancellation_allowed", True),
            cancellation_deadline=config_data.get("cancellation_deadline", 24),
            cancellation_deadline_unit=config_data.get("cancellation_deadline_unit", "hour"),
            calendar_display=config_data.get("calendar_display", "calendar"),
            customer_timezone_enabled=config_data.get("customer_timezone_enabled", False),
            deposit_enabled=config_data.get("deposit_enabled", False),
            deposit_type=config_data.get("deposit_type", "fixed"),
            deposit_amount=config_data.get("deposit_amount", Decimal("0.00")),
            check_in_time=self._parse_time(config_data.get("check_in_time")),
            check_out_time=self._parse_time(config_data.get("check_out_time")),
            standard_occupancy=config_data.get("standard_occupancy", 2),
            min_stay=config_data.get("min_stay", 1),
            max_stay=config_data.get("max_stay", 365),
            recurrence_enabled=config_data.get("recurrence_enabled", False),
            reminder_enabled=config_data.get("reminder_enabled", True),
            reminder_hours_before=config_data.get("reminder_hours_before", [1, 24]),
        )
        self.stdout.write(
            f"  Config: {config.booking_type} / {config.duration}{config.duration_unit[0]}"
        )

        # Step 4: Resources
        resources = []
        for i, res_spec in enumerate(spec.get("resources", [])):
            resource = BookingResource.objects.create(
                product=product,
                name=res_spec["name"],
                description=res_spec.get("description", ""),
                resource_type=res_spec.get("resource_type", "staff"),
                quantity=res_spec.get("quantity", 1),
                base_cost_adjustment=Decimal(str(res_spec.get("base_cost_adjustment", 0))),
                assignment_type=res_spec.get("assignment_type", "customer_selected"),
                email=res_spec.get("email", ""),
                tags=res_spec.get("tags", []),
                is_per_night=res_spec.get("is_per_night", True),
                sort_order=i,
                is_active=True,
            )
            resources.append(resource)
        if resources:
            self.stdout.write(f"  Resources: {len(resources)} created")

        # Step 5: Person types
        person_types = []
        for i, pt_spec in enumerate(spec.get("person_types", [])):
            pt = BookingPersonType.objects.create(
                product=product,
                name=pt_spec["name"],
                cost_adjustment=Decimal(str(pt_spec.get("cost_adjustment", 0))),
                min_persons=pt_spec.get("min_persons", 0),
                max_persons=pt_spec.get("max_persons", 10),
                is_counted_for_capacity=pt_spec.get("is_counted_for_capacity", True),
                is_per_night=pt_spec.get("is_per_night", True),
                sort_order=i,
            )
            person_types.append(pt)
        if person_types:
            self.stdout.write(f"  Person types: {len(person_types)} created")

        # Step 6: Availability rules
        rules = []
        current_year = str(timezone.now().year)
        for rule_spec in spec.get("availability_rules", []):
            # Resolve dynamic CURRENT_YEAR placeholders in date strings
            raw_start = rule_spec.get("start_date")
            raw_end = rule_spec.get("end_date")
            if isinstance(raw_start, str) and "CURRENT_YEAR" in raw_start:
                raw_start = raw_start.replace("CURRENT_YEAR", current_year)
            if isinstance(raw_end, str) and "CURRENT_YEAR" in raw_end:
                raw_end = raw_end.replace("CURRENT_YEAR", current_year)

            rule = BookingAvailabilityRule.objects.create(
                product=product,
                resource=None,  # product-level rules
                rule_type=rule_spec["rule_type"],
                scope=rule_spec["scope"],
                start_date=raw_start,
                end_date=raw_end,
                start_time=self._parse_time(rule_spec.get("start_time")),
                end_time=self._parse_time(rule_spec.get("end_time")),
                days_of_week=rule_spec.get("days_of_week", []),
                specific_dates=rule_spec.get("specific_dates", []),
                cost_override=rule_spec.get("cost_override"),
                cost_adjustment=rule_spec.get("cost_adjustment"),
                cost_adjustment_type=rule_spec.get("cost_adjustment_type", "flat"),
                min_stay_override=rule_spec.get("min_stay_override"),
                length_of_stay_min=rule_spec.get("length_of_stay_min"),
                length_of_stay_discount_percent=rule_spec.get("length_of_stay_discount_percent"),
                lead_time_min_days=rule_spec.get("lead_time_min_days"),
                lead_time_max_days=rule_spec.get("lead_time_max_days"),
                priority=rule_spec.get("priority", 10),
            )
            rules.append(rule)
        if rules:
            self.stdout.write(f"  Availability rules: {len(rules)} created")

        # Step 7: Recurrence rules
        rec_rules = []
        for rec_spec in spec.get("recurrence_rules", []):
            rec = BookingRecurrenceRule.objects.create(
                product=product,
                frequency=rec_spec["frequency"],
                day_of_week=rec_spec.get("day_of_week"),
                day_of_month=rec_spec.get("day_of_month"),
                start_time=self._parse_time(rec_spec["start_time"]),
                end_time=self._parse_time(rec_spec["end_time"]),
                start_date=rec_spec.get("start_date", timezone.now().date()),
                end_date=rec_spec.get("end_date"),
                auto_create_days_ahead=rec_spec.get("auto_create_days_ahead", 90),
                is_active=True,
            )
            rec_rules.append(rec)
        if rec_rules:
            self.stdout.write(f"  Recurrence rules: {len(rec_rules)} created")

        # Step 8: Generate sample bookings
        gen_spec = spec.get("booking_generation", {})
        count = gen_spec.get("count", 70)
        if count > 0:
            self.stdout.write(f"Generating {count} sample bookings...")
            booking_count = self._generate_bookings(
                product,
                config,
                resources,
                person_types,
                spec,
            )
            self.stdout.write(f"  Bookings: {booking_count} created")

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone! Created "{product.name}" with '
                f"{len(resources)} resources, {len(rules)} rules, "
                f"{Booking.objects.filter(product=product).count()} bookings"
            )
        )
        self.stdout.write(
            f"  Admin: http://localhost:8000/en/admin/catalog/product/{product.id}/change/"
        )
        self.stdout.write(
            f"  Bookings: http://localhost:8000/en/admin/catalog/booking/?product__id__exact={product.id}"
        )
        self.stdout.write(
            "  Calendar: http://localhost:8000/en/admin/catalog/booking/?view=calendar"
        )

    # ------------------------------------------------------------------
    # Deletion
    # ------------------------------------------------------------------

    def _delete_booking(self, spec):
        sku = spec["product"]["sku"]
        products = Product.all_objects.filter(sku=sku)
        if not products.exists():
            self.stdout.write(self.style.WARNING(f"Product {sku} not found"))
            return

        total_bookings = 0
        total_resources = 0
        product_name = products.first().name

        for product in products:
            total_bookings += Booking.objects.filter(product=product).count()
            total_resources += BookingResource.objects.filter(product=product).count()
            # Hard delete (cascades to BookingConfig, Resources, Rules, Bookings)
            # Must use hard_delete() because Product.delete() only soft-deletes
            product.hard_delete()

        # Clean up empty category
        Category.objects.filter(
            name=spec["category_name"],
            products__isnull=True,
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Deleted "{product_name}" ({sku}) + '
                f"{total_resources} resources, {total_bookings} bookings"
            )
        )

    # ------------------------------------------------------------------
    # Booking generation
    # ------------------------------------------------------------------

    def _generate_bookings(self, product, config, resources, person_types, spec):
        """Generate realistic sample bookings spanning several months."""
        # Route accommodation bookings to specialized generator
        if config.booking_type == "accommodation":
            return self._generate_accommodation_bookings(
                product,
                config,
                resources,
                person_types,
                spec,
            )

        gen = spec.get("booking_generation", {})
        count = gen.get("count", 70)
        months_back = gen.get("months_back", 3)
        months_forward = gen.get("months_forward", 2)

        # Use spec-specific notes pool if provided, otherwise default
        notes_pool = gen.get("notes_pool", CUSTOMER_NOTES_POOL)

        now = timezone.now()
        start_date = (now - timedelta(days=months_back * 30)).date()
        end_date = (now + timedelta(days=months_forward * 30)).date()

        # Collect valid time windows from availability rules
        time_windows = self._get_time_windows(spec)

        # Check if duration is variable (customer-selected)
        is_variable_duration = (
            config.duration_type == "customer_selected"
            and config.min_duration
            and config.max_duration
        )
        base_duration_minutes = self._get_duration_minutes(config)

        bookings_created = 0
        attempts = 0
        max_attempts = count * 5  # Avoid infinite loops

        while bookings_created < count and attempts < max_attempts:
            attempts += 1

            # Pick a random date
            days_range = (end_date - start_date).days
            random_date = start_date + timedelta(days=random.randint(0, days_range))

            # Find a matching time window for this day of week
            dow = random_date.weekday()  # 0=Mon
            valid_windows = [w for w in time_windows if dow in w["days"]]
            if not valid_windows:
                continue

            window = random.choice(valid_windows)

            # Determine duration for this booking
            if is_variable_duration:
                duration_minutes = self._get_random_duration_minutes(config)
            else:
                duration_minutes = base_duration_minutes

            # Pick a random start time within the window
            window_start = window["start"]
            window_end = window["end"]
            # Ensure there's room for the booking duration
            latest_start_minutes = window_end.hour * 60 + window_end.minute - duration_minutes
            earliest_start_minutes = window_start.hour * 60 + window_start.minute
            if latest_start_minutes < earliest_start_minutes:
                continue

            # Snap to slot boundaries (e.g., every 15 or 30 minutes)
            slot_interval = 15 if duration_minutes <= 30 else 30
            possible_starts = list(
                range(
                    earliest_start_minutes,
                    latest_start_minutes + 1,
                    slot_interval,
                )
            )
            if not possible_starts:
                continue

            start_minutes = random.choice(possible_starts)
            start_hour = start_minutes // 60
            start_min = start_minutes % 60

            start_dt = timezone.make_aware(
                datetime(
                    random_date.year, random_date.month, random_date.day, start_hour, start_min
                ),
            )
            end_dt = start_dt + timedelta(minutes=duration_minutes)

            # Determine status based on whether past or future
            is_past = start_dt < now
            if is_past:
                status = random.choices(
                    ["completed", "cancelled", "no_show", "confirmed"],
                    weights=[60, 15, 10, 15],
                )[0]
            else:
                status = random.choices(
                    ["confirmed", "pending_confirmation"],
                    weights=[70, 30],
                )[0]

            # Pick a resource
            resource = random.choice(resources) if resources else None

            # Pick a customer
            first, last = random.choice(CUSTOMER_NAMES)
            customer_name = f"{first} {last}"
            customer_email = f"{first.lower()}.{last.lower()}@{random.choice(EMAIL_DOMAINS)}"
            customer_phone = f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

            # Person counts
            persons = {}
            if person_types:
                for pt in person_types:
                    lo = pt.min_persons or 1
                    hi = min(pt.max_persons, max(lo, 4))
                    persons[pt.name] = random.randint(lo, hi)

            # Calculate total cost
            base_price = float(product.price.amount)
            # Scale price by duration for customer-selected bookings
            if is_variable_duration and base_duration_minutes > 0:
                base_price = base_price * (duration_minutes / base_duration_minutes)
            per_person = gen.get("per_person_pricing", False)
            if persons and person_types and per_person:
                # Per-person pricing: each person pays (base + adjustment)
                total_cost = 0
                for pt in person_types:
                    pcount = persons.get(pt.name, 0)
                    per_person = base_price + float(pt.cost_adjustment)
                    total_cost += max(per_person, 0) * pcount
            else:
                # Flat base + per-person surcharges (appointments)
                total_cost = base_price
                if persons and person_types:
                    for pt in person_types:
                        pcount = persons.get(pt.name, 0)
                        total_cost += float(pt.cost_adjustment) * pcount
            if resource and resource.base_cost_adjustment:
                total_cost += float(resource.base_cost_adjustment)
            total_cost = max(total_cost, 0)

            # Deposit
            deposit = Decimal("0.00")
            if config.deposit_enabled:
                if config.deposit_type == "percentage":
                    deposit = Decimal(str(total_cost)) * config.deposit_amount / 100
                else:
                    deposit = config.deposit_amount

            # Notes and cancellation reason
            customer_notes = random.choice(notes_pool)
            cancellation_reason = ""
            if status == "cancelled":
                cancellation_reason = random.choice(CANCELLATION_REASONS)

            Booking.objects.create(
                product=product,
                resource=resource,
                start_datetime=start_dt,
                end_datetime=end_dt,
                status=status,
                persons=persons,
                total_cost=Decimal(str(round(total_cost, 2))),
                deposit_amount=deposit,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                customer_notes=customer_notes,
                customer_timezone="America/New_York",
                cancellation_reason=cancellation_reason,
                ical_uid=f"{uuid.uuid4()}@demo.spwig.com",
                is_recurring=False,
            )
            bookings_created += 1

        return bookings_created

    def _generate_accommodation_bookings(self, product, config, resources, person_types, spec):
        """Generate accommodation bookings with per-night pricing engine."""
        import json

        from catalog.services.booking_service import BookingAvailabilityService

        gen = spec.get("booking_generation", {})
        count = gen.get("count", 50)
        months_back = gen.get("months_back", 3)
        months_forward = gen.get("months_forward", 2)
        notes_pool = gen.get("notes_pool", CUSTOMER_NOTES_POOL)

        now = timezone.now()
        start_date = (now - timedelta(days=months_back * 30)).date()
        end_date = (now + timedelta(days=months_forward * 30)).date()

        check_in = config.check_in_time or time(14, 0)
        check_out = config.check_out_time or time(10, 0)

        # Use min_stay/max_stay for night range (hotel pricing fields)
        min_nights = config.min_stay or 1
        max_nights = min(config.max_stay or 14, 14)  # Cap at 14 for demo realism

        bookings_created = 0
        attempts = 0
        max_attempts = count * 5

        while bookings_created < count and attempts < max_attempts:
            attempts += 1

            # Pick a random check-in date
            days_range = (end_date - start_date).days
            check_in_date = start_date + timedelta(days=random.randint(0, days_range))

            # Pick a random number of nights (weighted towards shorter stays)
            nights = random.choices(
                list(range(min_nights, max_nights + 1)),
                weights=[max(1, max_nights - n + 1) for n in range(min_nights, max_nights + 1)],
            )[0]
            check_out_date = check_in_date + timedelta(days=nights)

            # Don't let check-out exceed our range by too much
            if check_out_date > end_date + timedelta(days=7):
                continue

            start_dt = timezone.make_aware(
                datetime(
                    check_in_date.year,
                    check_in_date.month,
                    check_in_date.day,
                    check_in.hour,
                    check_in.minute,
                ),
            )
            end_dt = timezone.make_aware(
                datetime(
                    check_out_date.year,
                    check_out_date.month,
                    check_out_date.day,
                    check_out.hour,
                    check_out.minute,
                ),
            )

            # Status
            is_past = start_dt < now
            if is_past:
                status = random.choices(
                    ["completed", "cancelled", "no_show", "confirmed"],
                    weights=[60, 15, 10, 15],
                )[0]
            else:
                status = random.choices(
                    ["confirmed", "pending_confirmation"],
                    weights=[70, 30],
                )[0]

            # Resource (room)
            resource = random.choice(resources) if resources else None

            # Customer
            first, last = random.choice(CUSTOMER_NAMES)
            customer_name = f"{first} {last}"
            customer_email = f"{first.lower()}.{last.lower()}@{random.choice(EMAIL_DOMAINS)}"
            customer_phone = f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

            # Person counts
            persons = {}
            if person_types:
                for pt in person_types:
                    lo = pt.min_persons or 1
                    hi = min(pt.max_persons, max(lo, 4))
                    persons[pt.name] = random.randint(lo, hi)

            # Use the real pricing engine for accurate per-night breakdown
            try:
                calc_total, breakdown = (
                    BookingAvailabilityService.calculate_booking_price_with_breakdown(
                        product,
                        start_dt,
                        end_dt,
                        resource.id if resource else None,
                        persons,
                    )
                )
                total_cost = float(calc_total)
                price_breakdown = json.loads(json.dumps(breakdown, default=str))
            except Exception:
                # Fallback: simple multiplication
                total_cost = float(product.price.amount) * nights
                if resource and resource.base_cost_adjustment:
                    total_cost += float(resource.base_cost_adjustment) * nights
                total_cost = max(total_cost, 0)
                price_breakdown = {}

            # Deposit
            deposit = Decimal("0.00")
            if config.deposit_enabled:
                if config.deposit_type == "percentage":
                    deposit = Decimal(str(total_cost)) * config.deposit_amount / 100
                else:
                    deposit = config.deposit_amount

            # Notes
            customer_notes = random.choice(notes_pool)
            cancellation_reason = ""
            if status == "cancelled":
                cancellation_reason = random.choice(CANCELLATION_REASONS)

            Booking.objects.create(
                product=product,
                resource=resource,
                start_datetime=start_dt,
                end_datetime=end_dt,
                status=status,
                persons=persons,
                total_cost=Decimal(str(round(total_cost, 2))),
                deposit_amount=deposit,
                price_breakdown=price_breakdown,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                customer_notes=customer_notes,
                customer_timezone="America/New_York",
                cancellation_reason=cancellation_reason,
                ical_uid=f"{uuid.uuid4()}@demo.spwig.com",
                is_recurring=False,
            )
            bookings_created += 1

        return bookings_created

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_time_windows(self, spec):
        """Extract time windows from availability rules for booking generation."""
        windows = []
        for rule in spec.get("availability_rules", []):
            if rule["rule_type"] != "available":
                continue
            start = self._parse_time(rule.get("start_time", "09:00"))
            end = self._parse_time(rule.get("end_time", "17:00"))
            if rule["scope"] == "days_of_week":
                days = rule.get("days_of_week", [0, 1, 2, 3, 4])
            elif rule["scope"] == "all_dates":
                days = [0, 1, 2, 3, 4, 5, 6]
            else:
                days = [0, 1, 2, 3, 4]  # Default to weekdays
            windows.append({"days": days, "start": start, "end": end})
        return windows

    def _get_duration_minutes(self, config):
        """Get the default/base booking duration in minutes from config."""
        duration = config.duration
        unit = config.duration_unit
        if unit == "hour":
            return duration * 60
        elif unit == "day":
            return duration * 60 * 8  # 8-hour working day
        elif unit == "night":
            return duration * 60 * 12
        return duration  # minutes

    def _get_random_duration_minutes(self, config):
        """Get a random duration for customer-selected duration bookings."""
        unit = config.duration_unit
        min_d = config.min_duration or config.duration
        max_d = config.max_duration or config.duration

        if unit == "minute":
            # Snap to 30-min increments for minute-based
            step = 30
            possible = list(range(min_d, max_d + 1, step))
            if not possible:
                possible = [min_d]
            duration = random.choice(possible)
            return duration
        elif unit == "hour":
            # Snap to 1-hour increments for hour-based
            possible = list(range(min_d, max_d + 1))
            if not possible:
                possible = [min_d]
            duration = random.choice(possible)
            return duration * 60
        elif unit == "night":
            possible = list(range(min_d, max_d + 1))
            if not possible:
                possible = [min_d]
            return random.choice(possible)  # nights handled differently
        else:
            return config.duration  # fallback

    @staticmethod
    def _parse_time(time_str):
        """Parse 'HH:MM' string to time object, or return None."""
        if not time_str:
            return None
        parts = time_str.split(":")
        return time(int(parts[0]), int(parts[1]))
