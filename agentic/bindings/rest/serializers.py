"""
Documentation serializers for the UCP catalog responses.

These describe the JSON shape the catalog views return so drf-spectacular can
document the response bodies (and stop emitting "unable to guess serializer"
warnings). They are NOT used to build the responses — the views assemble UCP
dicts via `catalog_service` — they exist purely so the published API contract
carries a real response schema, per the API-docs rules.
"""

from rest_framework import serializers


class UCPPriceSerializer(serializers.Serializer):
    amount = serializers.IntegerField(help_text="Price in integer minor units (e.g. cents).")
    currency = serializers.CharField(help_text="ISO 4217 currency code.")


class UCPPriceRangeSerializer(serializers.Serializer):
    min = UCPPriceSerializer()
    max = UCPPriceSerializer()


class UCPAvailabilitySerializer(serializers.Serializer):
    available = serializers.BooleanField()
    status = serializers.CharField(help_text="in_stock | backorder | out_of_stock")


class UCPVariantSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = UCPPriceSerializer(allow_null=True)
    availability = UCPAvailabilitySerializer()
    sku = serializers.CharField(allow_blank=True)


class UCPProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price_range = UCPPriceRangeSerializer(allow_null=True)
    variants = UCPVariantSerializer(many=True)
    availability = UCPAvailabilitySerializer()
    condition = serializers.CharField(help_text="new | refurbished | used")
    url = serializers.URLField(required=False)
    brand = serializers.CharField(required=False)


class UCPSearchResponseSerializer(serializers.Serializer):
    products = UCPProductSerializer(many=True)
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total = serializers.IntegerField()


class UCPErrorSerializer(serializers.Serializer):
    error = serializers.CharField()
    message = serializers.CharField()
    messages = serializers.ListField(
        child=serializers.CharField(), required=False, help_text="Validation detail, when present."
    )


# --- Checkout session ---------------------------------------------------------


class UCPCheckoutLineItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    product_id = serializers.CharField(allow_null=True)
    variant_id = serializers.CharField(allow_null=True, required=False)
    title = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = UCPPriceSerializer(allow_null=True)
    total = UCPPriceSerializer(allow_null=True)


class UCPBuyerSerializer(serializers.Serializer):
    email = serializers.CharField(allow_null=True)
    name = serializers.CharField(allow_null=True)


class UCPFulfillmentOptionSerializer(serializers.Serializer):
    id = serializers.CharField()
    label = serializers.CharField()
    description = serializers.CharField(required=False)
    price = UCPPriceSerializer(allow_null=True)
    estimated_delivery = serializers.CharField(allow_null=True, required=False)
    min_days = serializers.IntegerField(allow_null=True, required=False)
    max_days = serializers.IntegerField(allow_null=True, required=False)


class UCPFulfillmentSerializer(serializers.Serializer):
    selected_option_id = serializers.CharField(allow_null=True)
    options = UCPFulfillmentOptionSerializer(many=True)


class UCPCheckoutTotalsSerializer(serializers.Serializer):
    subtotal = UCPPriceSerializer(allow_null=True)
    shipping = UCPPriceSerializer(allow_null=True)
    tax = UCPPriceSerializer(allow_null=True)
    discount = UCPPriceSerializer(allow_null=True)
    total = UCPPriceSerializer(allow_null=True)
    amount_due = UCPPriceSerializer(allow_null=True)


class UCPCheckoutPaymentSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="requires_payment | requires_action | completed")
    continue_url = serializers.URLField(
        allow_null=True, help_text="Storefront URL a human can use to finish checkout."
    )


class UCPCheckoutOrderSerializer(serializers.Serializer):
    id = serializers.CharField()
    number = serializers.CharField()
    status = serializers.CharField()


class UCPCheckoutSessionSerializer(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.CharField(
        help_text="not_ready_for_payment | ready_for_payment | completed | canceled"
    )
    currency = serializers.CharField()
    line_items = UCPCheckoutLineItemSerializer(many=True)
    buyer = UCPBuyerSerializer(allow_null=True)
    fulfillment = UCPFulfillmentSerializer(allow_null=True)
    totals = UCPCheckoutTotalsSerializer()
    payment = UCPCheckoutPaymentSerializer()
    messages = serializers.ListField(child=serializers.CharField())
    order = UCPCheckoutOrderSerializer(required=False, allow_null=True)


# --- Checkout request bodies (documentation only) -----------------------------


class UCPCheckoutLineItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    variant_id = serializers.IntegerField(required=False, allow_null=True)


class UCPCheckoutCreateRequestSerializer(serializers.Serializer):
    line_items = UCPCheckoutLineItemInputSerializer(many=True)
    buyer = serializers.DictField(
        required=False, help_text="email, name, shipping_address, billing_address."
    )


class UCPCheckoutUpdateRequestSerializer(serializers.Serializer):
    buyer = serializers.DictField(required=False)
    fulfillment_option_id = serializers.IntegerField(required=False, allow_null=True)


class UCPCheckoutCompleteRequestSerializer(serializers.Serializer):
    payment = serializers.DictField(help_text="The agent's payment credential (gateway-specific).")
    attested_total = UCPPriceSerializer(
        required=False, allow_null=True, help_text="Checkout-time price lock."
    )
    return_url = serializers.URLField(required=False)
    cancel_url = serializers.URLField(required=False)
