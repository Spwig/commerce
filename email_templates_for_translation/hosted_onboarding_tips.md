---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Tips to Get the Most Out of {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Getting Started Tips
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Make the most of your Spwig store
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Now that <strong>{{ store_name }}</strong> is up and running, here are some tips to help you get the most out of your store.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Customise Your Look
        </mj-text>
        <mj-text font-size="14px">
          Visit <strong>Design > Theme Settings</strong> to pick a theme, upload your logo, and set your brand colours. Your storefront updates instantly so you can preview changes in real time.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Add Your Products
        </mj-text>
        <mj-text font-size="14px">
          Head to <strong>Catalog > Products</strong> to start adding your items. You can create product variants (size, colour), set pricing, manage inventory, and upload high-quality images.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Set Up Payments
        </mj-text>
        <mj-text font-size="14px">
          Go to <strong>Settings > Payment Providers</strong> to connect Stripe, PayPal, or another payment method. You can enable multiple providers so your customers can pay however they prefer.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure Shipping
        </mj-text>
        <mj-text font-size="14px">
          Under <strong>Settings > Shipping</strong>, set up your shipping zones and rates. You can create flat-rate, weight-based, or free shipping rules for different regions.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Boost Your SEO
        </mj-text>
        <mj-text font-size="14px">
          Spwig automatically generates sitemaps and meta tags. Visit <strong>Settings > SEO</strong> to customise your page titles, descriptions, and social sharing images to help customers find your store.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Getting Started Tips - {{ store_name }}

Hi {{ name|default:'there' }},

Now that {{ store_name }} is up and running, here are some tips to help you get the most out of your store.

1. Customise Your Look
Visit Design > Theme Settings to pick a theme, upload your logo, and set your brand colours.

2. Add Your Products
Head to Catalog > Products to start adding your items with variants, pricing, and images.

3. Set Up Payments
Go to Settings > Payment Providers to connect Stripe, PayPal, or another payment method.

4. Configure Shipping
Under Settings > Shipping, set up your shipping zones and rates for different regions.

5. Boost Your SEO
Visit Settings > SEO to customise your page titles, descriptions, and social sharing images.

Go to Admin Panel: {{ admin_url }}

Need help? Contact {{ support_email }}
