# Email Templates for Translation

This document contains all English email templates that need to be translated into 16 languages:
- fr (French)
- es (Spanish)
- de (German)
- pt (Portuguese)
- ja (Japanese)
- zh-hans (Simplified Chinese)
- zh-hant (Traditional Chinese)
- ru (Russian)
- ar (Arabic)
- hi (Hindi)
- id (Indonesian)
- it (Italian)
- ko (Korean)
- th (Thai)
- tr (Turkish)
- vi (Vietnamese)

**IMPORTANT NOTES FOR TRANSLATION:**
1. Preserve all Django template variables (e.g., `{{ order.number }}`, `{{ customer_name }}`)
2. Preserve all Django template tags (e.g., `{% if %}`, `{% endif %}`, `{% for %}`, `{% endfor %}`, `{% trans %}`, `{% load i18n %}`)
3. Preserve all HTML/MJML tags and structure
4. Only translate the human-readable text content
5. Keep all URLs, variable names, and technical identifiers unchanged

---

## Category: Core E-commerce Templates (9 templates)

### Template: order_confirmation

**Subject:**
```
Order Confirmation - Order #{{ order.number }}
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Order Confirmation
        </mj-text>
        <mj-text>
          Thank you for your order! Your order #{{ order_number }} has been received and is being processed.
        </mj-text>
        <mj-text>
          <strong>Order Total:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="#4F46E5">
          View Order Details
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Order Confirmation

Thank you for your order! Your order #{{ order_number }} has been received and is being processed.

Order Total: {{ order_total }}

View order details: {{ order_url }}
```

---

### Template: payment_confirmation

**Subject:**
```
Payment Confirmed - Order #{{ order_number }}
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Payment Confirmed
        </mj-text>
        <mj-text>
          Your payment for order #{{ order_number }} has been successfully processed.
        </mj-text>
        <mj-text>
          <strong>Amount Paid:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Payment Method:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Payment Confirmed

Your payment for order #{{ order_number }} has been successfully processed.

Amount Paid: {{ amount_paid }}
Payment Method: {{ payment_method }}
```

---

### Template: shipping_confirmation

**Subject:**
```
Your Order Has Shipped - Order #{{ order_number }}
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Your Order Has Shipped!
        </mj-text>
        <mj-text>
          Great news! Your order #{{ order_number }} has been shipped.
        </mj-text>
        <mj-text>
          <strong>Tracking Number:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Carrier:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="#4F46E5">
          Track Shipment
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Your Order Has Shipped!

Great news! Your order #{{ order_number }} has been shipped.

Tracking Number: {{ tracking_number }}
Carrier: {{ carrier }}

Track your shipment: {{ tracking_url }}
```

---

### Template: delivery_confirmation

**Subject:**
```
Order Delivered - Order #{{ order_number }}
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Order Delivered
        </mj-text>
        <mj-text>
          Your order #{{ order_number }} has been delivered!
        </mj-text>
        <mj-text>
          We hope you enjoy your purchase. If you have any questions or concerns, please don't hesitate to contact us.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="#4F46E5">
          View Order
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Order Delivered

Your order #{{ order_number }} has been delivered!

We hope you enjoy your purchase. If you have any questions or concerns, please don't hesitate to contact us.

View order: {{ order_url }}
```

---

### Template: refund_notification

**Subject:**
```
Refund Processed - Order #{{ order_number }}
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Refund Processed
        </mj-text>
        <mj-text>
          A refund has been processed for order #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Refund Amount:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          The refund will appear in your account within {{ refund_days }} business days.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Refund Processed

A refund has been processed for order #{{ order_number }}.

Refund Amount: {{ refund_amount }}

The refund will appear in your account within {{ refund_days }} business days.
```

---

### Template: password_reset

**Subject:**
```
Password Reset Request
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Password Reset Request
        </mj-text>
        <mj-text>
          We received a request to reset your password. Click the button below to reset it.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="#4F46E5">
          Reset Password
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          If you didn't request this, you can safely ignore this email.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          This link will expire in {{ expiry_hours }} hours.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Password Reset Request

We received a request to reset your password. Click the link below to reset it.

{{ reset_url }}

If you didn't request this, you can safely ignore this email.
This link will expire in {{ expiry_hours }} hours.
```

---

### Template: email_verification

**Subject:**
```
Verify Your Email Address
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Verify Your Email
        </mj-text>
        <mj-text>
          Please verify your email address by clicking the button below.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="#4F46E5">
          Verify Email
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          This link will expire in {{ expiry_hours }} hours.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Verify Your Email

Please verify your email address by clicking the link below.

{{ verification_url }}

This link will expire in {{ expiry_hours }} hours.
```

---

### Template: admin_new_order

**Subject:**
```
New Order Received - Order #{{ order_number }}
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          New Order Received
        </mj-text>
        <mj-text>
          A new order has been placed on your store.
        </mj-text>
        <mj-text>
          <strong>Order Number:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Customer:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Total:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="#4F46E5">
          View in Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
New Order Received

A new order has been placed on your store.

Order Number: {{ order_number }}
Customer: {{ customer_name }}
Total: {{ order_total }}

View in admin: {{ admin_order_url }}
```

---

### Template: admin_payment_failed

**Subject:**
```
Payment Failed - Order #{{ order_number }}
```

**HTML Content:**
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#DC2626">
          Payment Failed
        </mj-text>
        <mj-text>
          A payment attempt has failed for order #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Customer:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Amount:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Error:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="#DC2626">
          View in Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**Text Content:**
```
Payment Failed

A payment attempt has failed for order #{{ order_number }}.

Customer: {{ customer_name }}
Amount: {{ order_total }}
Error: {{ error_message }}

View in admin: {{ admin_order_url }}
```

---

## Category: Enhanced E-commerce Templates (3 new templates)

### Template: account_welcome

**Subject:**
```
Welcome to {{ shop_name }}!
```

**HTML Content:**
```mjml
{% load i18n %}<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          {% trans "Welcome!" %} 👋
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center" padding-top="10px">
          {% trans "We're excited to have you as part of our community" %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personalized Greeting -->
    <mj-section background-color="#e7f3ff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529" align="center">
          {% trans "Hi" %} {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="#6c757d" align="center" padding-top="10px">
          {% trans "Your account has been successfully created. You're all set to start shopping!" %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits Section -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="#212529" align="center" padding-bottom="20px">
          {% trans "Member Benefits" %}
        </mj-text>

        {% for benefit in shop_benefits %}
        <mj-text font-size="14px" color="#212529" padding="8px 0">
          <span style="color: #28a745; font-size: 18px;">✓</span> {{ benefit }}
        </mj-text>
        {% endfor %}
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="#ffffff" padding="10px 20px">
      <mj-column>
        <mj-button
          href="{{ browse_products_url }}"
          background-color="#007bff"
          color="#ffffff"
          font-size="16px"
          font-weight="600"
          border-radius="6px"
          padding="14px 32px"
        >
          {% trans "Start Shopping" %}
        </mj-button>
      </mj-column>
    </mj-section>

    <mj-section background-color="#ffffff" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button
          href="{{ account_url }}"
          background-color="#6c757d"
          color="#ffffff"
          font-size="14px"
          border-radius="6px"
          padding="12px 24px"
        >
          {% trans "Manage My Account" %}
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>
```

**Text Content:**
```
{% trans "Welcome!" %} 👋

{% trans "Hi" %} {{ customer_name }},

{% trans "Your account has been successfully created. You're all set to start shopping!" %}

{% trans "Member Benefits:" %}
{% for benefit in shop_benefits %}
✓ {{ benefit }}
{% endfor %}

{% trans "Start shopping:" %} {{ browse_products_url }}
{% trans "Manage your account:" %} {{ account_url }}

{% trans "Need Help?" %}
{% trans "Email:" %} {{ support_email }}
{% trans "Phone:" %} {{ support_phone }}
```

---

### Template: order_delay

**Subject:**
```
Update: Delay for Order #{{ order_number }}
```

**HTML Content:**
```mjml
{% load i18n %}<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#fff3cd" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#856404" align="center">
          {% trans "Order Delay Notice" %}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          {% trans "Order" %} #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Apology Message -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          {% trans "Dear" %} {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="#212529" padding-top="15px" line-height="1.8">
          {{ delay_reason }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Delivery Date Update -->
    <mj-section background-color="#e7f3ff" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="#6c757d" align="center">
          <strong>{% trans "Original Delivery Date:" %}</strong>
        </mj-text>
        <mj-text font-size="16px" color="#212529" align="center" padding-top="5px">
          <s>{{ original_delivery_date }}</s>
        </mj-text>
        <mj-text font-size="14px" color="#6c757d" align="center" padding-top="15px">
          <strong>{% trans "New Estimated Delivery:" %}</strong>
        </mj-text>
        <mj-text font-size="18px" color="#007bff" font-weight="600" align="center" padding-top="5px">
          {{ new_delivery_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Delayed Items -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="#212529" padding-bottom="15px">
          {% trans "Affected Items" %}
        </mj-text>
      </mj-column>
    </mj-section>

    {% for item in items %}
    <mj-section background-color="#ffffff" padding="10px 20px">
      <mj-column width="80px">
        <mj-image src="{{ item.product_thumbnail_url }}" alt="{{ item.name }}" width="60px" border-radius="6px" />
      </mj-column>
      <mj-column width="80%" vertical-align="middle">
        <mj-text font-size="14px" font-weight="600" color="#212529">
          {{ item.name }}
        </mj-text>
        <mj-text font-size="12px" color="#6c757d">
          {% trans "Qty:" %} {{ item.quantity }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Compensation (if offered) -->
    {% if compensation_offered %}
    <mj-section background-color="#d4edda" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="#155724" align="center">
          {% trans "As an apology..." %}
        </mj-text>
        <mj-text font-size="14px" color="#155724" align="center" padding-top="10px">
          {{ compensation_details }}
        </mj-text>
        {% if discount_code %}
        <mj-text font-size="18px" font-weight="bold" color="#155724" align="center" padding-top="10px">
          {% trans "Code:" %} {{ discount_code }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=order_url text="View Order Status" %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>
```

**Text Content:**
```
{% trans "Order Delay Notice" %}

{% trans "Order" %} #{{ order_number }}

{% trans "Dear" %} {{ customer_name }},

{{ delay_reason }}

{% trans "Original Delivery Date:" %} {{ original_delivery_date }}
{% trans "New Estimated Delivery:" %} {{ new_delivery_date }}

{% trans "Affected Items:" %}
{% for item in items %}
- {{ item.name }} ({% trans "Qty:" %} {{ item.quantity }})
{% endfor %}

{% if compensation_offered %}
{% trans "As an apology..." %}
{{ compensation_details }}
{% if discount_code %}{% trans "Code:" %} {{ discount_code }}{% endif %}
{% endif %}

{% trans "View order status:" %} {{ order_url }}

{% trans "Need Help?" %}
{% trans "Email:" %} {{ support_email }}
{% trans "Phone:" %} {{ support_phone }}
```

---

### Template: review_request

**Subject:**
```
How Was Your Purchase? Leave a Review
```

**HTML Content:**
```mjml
{% load i18n %}<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#212529" align="center">
          {% trans "We'd Love Your Feedback!" %}
        </mj-text>
        <mj-text font-size="16px" color="#6c757d" align="center" padding-top="10px">
          {% trans "Order" %} #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="#212529" line-height="1.8">
          {% trans "Hi" %} {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="#212529" padding-top="10px" line-height="1.8">
          {% trans "We hope you're enjoying your recent purchase! Your feedback helps us improve and helps other customers make informed decisions." %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Products to Review -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="600" color="#212529" padding-bottom="15px">
          {% trans "Review Your Purchase" %}
        </mj-text>
      </mj-column>
    </mj-section>

    {% for item in items %}
    <mj-section background-color="#ffffff" padding="15px 20px" css-class="review-item">
      <mj-column width="100px">
        <mj-image src="{{ item.product_thumbnail_url }}" alt="{{ item.name }}" width="80px" border-radius="6px" />
      </mj-column>
      <mj-column width="60%" vertical-align="middle">
        <mj-text font-size="14px" font-weight="600" color="#212529">
          {{ item.name }}
        </mj-text>
        <mj-text font-size="12px" color="#6c757d" padding-top="5px">
          {% trans "Qty:" %} {{ item.quantity }}
        </mj-text>
      </mj-column>
      <mj-column width="30%" vertical-align="middle">
        <mj-button
          href="{{ item.review_url }}"
          background-color="#007bff"
          color="#ffffff"
          font-size="12px"
          border-radius="4px"
          padding="8px 16px"
          inner-padding="8px 16px"
        >
          {% trans "Write Review" %}
        </mj-button>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Incentive (if offered) -->
    {% if incentive_offered %}
    <mj-section background-color="#e7f3ff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="#212529" align="center">
          🎁 {% trans "Bonus Reward" %}
        </mj-text>
        <mj-text font-size="14px" color="#212529" align="center" padding-top="10px">
          {{ incentive_details }}
        </mj-text>
        {% if incentive_code %}
        <mj-text font-size="18px" font-weight="bold" color="#007bff" align="center" padding-top="10px">
          {% trans "Code:" %} {{ incentive_code }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>
```

**Text Content:**
```
{% trans "We'd Love Your Feedback!" %}

{% trans "Order" %} #{{ order_number }}

{% trans "Hi" %} {{ customer_name }},

{% trans "We hope you're enjoying your recent purchase! Your feedback helps us improve and helps other customers make informed decisions." %}

{% trans "Review Your Purchase:" %}
{% for item in items %}
- {{ item.name }} ({% trans "Qty:" %} {{ item.quantity }})
  {% trans "Write review:" %} {{ item.review_url }}
{% endfor %}

{% if incentive_offered %}
🎁 {% trans "Bonus Reward" %}
{{ incentive_details }}
{% if incentive_code %}{% trans "Code:" %} {{ incentive_code }}{% endif %}
{% endif %}

{% trans "Need Help?" %}
{% trans "Email:" %} {{ support_email }}
{% trans "Phone:" %} {{ support_phone }}
```

---

**NOTE:** This markdown document is becoming very large. To make it manageable for your translation service, I can either:

1. **Continue in this same file** with all ~60 templates (file will be ~50,000+ lines)
2. **Split into multiple files** by category (e.g., core_templates.md, loyalty_templates.md, etc.)
3. **Create a JSON format** instead if that's easier for your translation service to process

Which format would work best for your translation service?
