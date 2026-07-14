from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from vouchers.models import VoucherCode

from .models import Order, OrderItem, OrderNote

User = get_user_model()


class OrderEditForm(forms.ModelForm):
    """
    Main form for editing order header information
    """

    class Meta:
        model = Order
        fields = [
            "status",
            "email",
            "phone",
            "notes",
            "special_instructions",
            "tracking_number",
            "carrier",
            "payment_status",
        ]
        widgets = {
            "status": forms.Select(attrs={"class": "status-select"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "special_instructions": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "tracking_number": forms.TextInput(attrs={"class": "form-control"}),
            "payment_status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields optional for manual order creation
        if not self.instance.pk:
            self.fields["tracking_number"].required = False
            self.fields["carrier"].required = False


class OrderItemInlineForm(forms.ModelForm):
    """
    Form for editing individual order items inline
    """

    product_search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control product-search-input",
                "placeholder": _("Search products..."),
                "autocomplete": "off",
            }
        ),
        help_text=_("Search for a product by name or SKU"),
    )

    override_price = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "price-override-checkbox"}),
        help_text=_("Allow manual price override"),
    )

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "variant",
            "quantity",
            "unit_price",
            "base_price",
            "discount_type",
            "discount_value",
            "discount_reason",
            "exclude_from_vouchers",
            "customizations",
        ]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control product-select"}),
            "variant": forms.Select(attrs={"class": "form-control variant-select"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control quantity-input", "min": "1", "step": "1"}
            ),
            "unit_price": forms.TextInput(attrs={"class": "form-control price-input"}),
            "base_price": forms.TextInput(attrs={"class": "form-control base-price-input"}),
            "discount_type": forms.Select(attrs={"class": "form-control discount-type-select"}),
            "discount_value": forms.NumberInput(
                attrs={"class": "form-control discount-value-input", "min": "0", "step": "0.01"}
            ),
            "discount_reason": forms.TextInput(
                attrs={
                    "class": "form-control discount-reason-input",
                    "placeholder": _("Optional: Reason for discount"),
                }
            ),
            "exclude_from_vouchers": forms.CheckboxInput(
                attrs={"class": "exclude-vouchers-checkbox"}
            ),
            "customizations": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["variant"].required = False
        self.fields["customizations"].required = False

        # Make discount fields optional (they have model defaults)
        self.fields["base_price"].required = False
        self.fields["discount_type"].required = False
        self.fields["discount_value"].required = False
        self.fields["discount_reason"].required = False
        self.fields["exclude_from_vouchers"].required = False

        # Populate product name and variant name if editing existing item
        if self.instance.pk:
            self.fields["product"].initial = self.instance.product
            if self.instance.variant:
                self.fields["variant"].initial = self.instance.variant

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity and quantity < 1:
            raise ValidationError(_("Quantity must be at least 1"))
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data.get("unit_price")
        override_price = self.cleaned_data.get("override_price", False)

        if unit_price and unit_price.amount < 0:
            raise ValidationError(_("Price cannot be negative"))

        # If not overriding, validate against product price
        if not override_price and self.instance.pk:
            product = self.cleaned_data.get("product")
            if product and unit_price:
                # Check if price matches product price (allow some flexibility for variants)
                pass  # Additional validation can be added here

        return unit_price

    def clean_discount_value(self):
        discount_value = self.cleaned_data.get("discount_value")
        discount_type = self.cleaned_data.get("discount_type")

        if discount_value and discount_value < 0:
            raise ValidationError(_("Discount value cannot be negative"))

        if discount_type == "percentage" and discount_value and discount_value > 100:
            raise ValidationError(_("Percentage discount cannot exceed 100%"))

        return discount_value

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        variant = cleaned_data.get("variant")
        unit_price = cleaned_data.get("unit_price")
        base_price = cleaned_data.get("base_price")
        discount_type = cleaned_data.get("discount_type")
        discount_value = cleaned_data.get("discount_value")

        # Validate variant belongs to product
        if variant and product and variant.product_id != product.id:
            raise ValidationError(_("Selected variant does not belong to this product"))

        # Validate discount pricing
        if base_price and unit_price and unit_price.amount > base_price.amount:
            raise ValidationError(_("Unit price cannot exceed base price"))

        # Validate fixed discount doesn't exceed base price
        if discount_type == "fixed" and discount_value and base_price:
            if discount_value > base_price.amount:
                raise ValidationError(_("Fixed discount cannot exceed base price"))

        return cleaned_data


class OrderAddressInlineForm(forms.Form):
    """
    Form for editing shipping and billing addresses inline
    """

    ADDRESS_TYPES = [
        ("shipping", _("Shipping")),
        ("billing", _("Billing")),
    ]

    address_type = forms.ChoiceField(choices=ADDRESS_TYPES, widget=forms.HiddenInput())

    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Full Name"),
    )

    address1 = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Address Line 1"),
    )

    address2 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Address Line 2"),
    )

    city = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}), label=_("City")
    )

    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("State / Province"),
    )

    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Postal Code"),
    )

    country = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}), label=_("Country")
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "type": "tel", "placeholder": "+1 (555) 123-4567"}
        ),
        label=_("Phone Number"),
    )

    save_to_customer = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "save-to-customer-checkbox"}),
        label=_("Save this address to customer profile"),
        help_text=_("Update customer's saved addresses with these changes"),
    )

    def __init__(self, *args, **kwargs):
        order = kwargs.pop("order", None)
        address_type = kwargs.pop("address_type", "shipping")
        super().__init__(*args, **kwargs)

        self.fields["address_type"].initial = address_type

        # Pre-populate with order data if provided
        if order and address_type == "shipping":
            self.fields["name"].initial = order.shipping_name
            self.fields["address1"].initial = order.shipping_address1
            self.fields["address2"].initial = order.shipping_address2
            self.fields["city"].initial = order.shipping_city
            self.fields["state"].initial = order.shipping_state
            self.fields["postal_code"].initial = order.shipping_postal_code
            self.fields["country"].initial = order.shipping_country
            self.fields["phone"].initial = order.shipping_phone
        elif order and address_type == "billing":
            self.fields["name"].initial = order.billing_name
            self.fields["address1"].initial = order.billing_address1
            self.fields["address2"].initial = order.billing_address2
            self.fields["city"].initial = order.billing_city
            self.fields["state"].initial = order.billing_state
            self.fields["postal_code"].initial = order.billing_postal_code
            self.fields["country"].initial = order.billing_country
            self.fields["phone"].initial = order.billing_phone


class OrderVoucherApplicationForm(forms.Form):
    """
    Form for applying voucher codes to orders
    """

    voucher_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control voucher-code-input",
                "placeholder": _("Enter voucher code"),
                "autocomplete": "off",
            }
        ),
        label=_("Voucher Code"),
    )

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop("order", None)
        super().__init__(*args, **kwargs)

    def clean_voucher_code(self):
        code = self.cleaned_data.get("voucher_code", "").strip().upper()

        if not code:
            raise ValidationError(_("Please enter a voucher code"))

        # Check if voucher exists
        try:
            voucher = VoucherCode.objects.get(code=code)
        except VoucherCode.DoesNotExist:
            raise ValidationError(_("Invalid voucher code"))

        # Validate voucher is active
        from django.utils import timezone

        now = timezone.now()

        if voucher.start_date and voucher.start_date > now:
            raise ValidationError(_("This voucher is not yet active"))

        if voucher.end_date and voucher.end_date < now:
            raise ValidationError(_("This voucher has expired"))

        # Check usage limits
        if voucher.max_uses_total and voucher.current_uses >= voucher.max_uses_total:
            raise ValidationError(_("This voucher has reached its usage limit"))

        # Check customer-specific usage limits
        if self.order and self.order.user and voucher.max_uses_per_customer:
            from vouchers.models import VoucherUsage

            customer_uses = VoucherUsage.objects.filter(
                voucher=voucher, user=self.order.user
            ).count()
            if customer_uses >= voucher.max_uses_per_customer:
                raise ValidationError(
                    _("You have already used this voucher the maximum number of times")
                )

        # Check minimum order value
        if voucher.min_order_value:
            if self.order and self.order.subtotal < voucher.min_order_value:
                raise ValidationError(
                    _("Minimum order value of %(amount)s required for this voucher")
                    % {"amount": voucher.min_order_value}
                )

        self.cleaned_data["voucher"] = voucher
        return code


class OrderCustomerChangeForm(forms.Form):
    """
    Form for changing the customer associated with an order
    """

    CUSTOMER_TYPE_CHOICES = [
        ("existing", _("Existing Customer")),
        ("guest", _("Guest Checkout")),
    ]

    customer_type = forms.ChoiceField(
        choices=CUSTOMER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "customer-type-radio"}),
        initial="existing",
        label=_("Customer Type"),
    )

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={"class": "form-control customer-select"}),
        label=_("Select Customer"),
        help_text=_("Search for existing customer"),
    )

    guest_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("guest@example.com")}
        ),
        label=_("Guest Email"),
    )

    guest_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("+1234567890")}),
        label=_("Guest Phone"),
    )

    def clean(self):
        cleaned_data = super().clean()
        customer_type = cleaned_data.get("customer_type")

        if customer_type == "existing":
            if not cleaned_data.get("user"):
                raise ValidationError(_("Please select a customer"))
        elif customer_type == "guest" and not cleaned_data.get("guest_email"):
            raise ValidationError(_("Guest email is required"))

        return cleaned_data


class OrderManualDiscountForm(forms.Form):
    """
    Form for applying manual discounts to orders (admin override)
    """

    discount_type = forms.ChoiceField(
        choices=[
            ("percentage", _("Percentage")),
            ("fixed", _("Fixed Amount")),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Discount Type"),
    )

    discount_value = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        label=_("Discount Value"),
    )

    reason = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Reason for discount (optional)")}
        ),
        label=_("Reason"),
    )

    def clean_discount_value(self):
        discount_value = self.cleaned_data.get("discount_value")
        discount_type = self.cleaned_data.get("discount_type")

        if discount_type == "percentage" and discount_value > 100:
            raise ValidationError(_("Percentage discount cannot exceed 100%"))

        return discount_value


class OrderNoteForm(forms.ModelForm):
    """
    Form for adding notes to orders
    """

    class Meta:
        model = OrderNote
        fields = ["note", "is_customer_note"]
        widgets = {
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": _("Add a note about this order..."),
                }
            ),
            "is_customer_note": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "note": _("Note"),
            "is_customer_note": _("Visible to customer"),
        }


class OrderCreateForm(OrderEditForm):
    """
    Extended form for creating manual orders
    Inherits from OrderEditForm and adds creation-specific fields
    """

    # Override to make user selection required
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Customer"),
        help_text=_("Select the customer for this order"),
    )

    class Meta(OrderEditForm.Meta):
        fields = OrderEditForm.Meta.fields + ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set source to 'manual' for manually created orders
        self.initial["status"] = "pending"
        self.initial["payment_status"] = "unpaid"


class QuickOrderStatusForm(forms.Form):
    """
    Quick form for changing order status (for HTMX updates)
    """

    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control status-select"}),
    )

    send_notification = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label=_("Send customer notification"),
        help_text=_("Email customer about status change"),
    )
