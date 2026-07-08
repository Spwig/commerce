---
template_type: order_confirmation
category: Core E-commerce
---

# Email Template: order_confirmation

## Subject
注文確認 #{{ order_number }} - ありがとうございます！

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ご注文ありがとうございます！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          注文 #{{ order_number }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ order_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Timeline -->
    {% include 'email_system/mjml_components/order_timeline.mjml' with stages=timeline_stages %}

    <!-- Order Items -->
    {% include 'email_system/mjml_components/order_items_table.mjml' with items=items %}

    <!-- Payment Summary -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        {% include 'email_system/mjml_components/payment_summary.mjml' with subtotal=subtotal shipping=shipping tax=tax total=total %}
      </mj-column>
    </mj-section>

    <!-- Delivery Estimate -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          <strong>予想到着日:</strong> {{ estimated_delivery_start }} - {{ estimated_delivery_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Shipping Address -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        {% include 'email_system/mjml_components/address_block.mjml' with address=shipping_address title="Shipping Address" %}
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=order_url text="View Order Status" %}

    {% if activation_url %}
    <!-- Guest Account Creation CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          アカウントを作成する
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          注文を追跡し、次回からより早くチェックアウトし、ご希望に応じて設定を管理できます。
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ご注文ありがとうございます！

注文 #{{ order_number }}
{{ order_date }}

予想到着日: {{ estimated_delivery_start }} - {{ estimated_delivery_end }}

注文商品:
{% for item in items %}
- {{ item.name }} (数量: {{ item.quantity }}) - {{ item.subtotal }}
{% endfor %}

小計: {{ subtotal }}
送料: {{ shipping }}
税: {{ tax }}
合計: {{ total }}

配送先住所:
{{ shipping_address.full_address }}

注文状況を確認: {{ order_url }}
{% if activation_url %}

アカウントを作成する
注文を追跡し、次回からより早くチェックアウトし、ご希望に応じて設定を管理できます。
アカウントを作成: {{ activation_url }}
{% endif %}

お手伝いが必要ですか？
メール: {{ support_email }}
電話: {{ support_phone }}