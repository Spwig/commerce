---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
Construisez votre catalogue - {{ store_name }}

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
          Getting Started: Your Products
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Build a great catalog for {{ store_name }}
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
          Your store <strong>{{ store_name }}</strong> is all set up. Now it's time to build your product catalog. Here are five tips to get you started.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Import Products from CSV
        </mj-text>
        <mj-text font-size="14px">
          Already have a product list? Head to <strong>Admin > Catalog > Import</strong> to bulk-import your products from a CSV file. This is the fastest way to populate your store.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Organise with Categories and Filters
        </mj-text>
        <mj-text font-size="14px">
          Create categories and attribute filters so customers can easily browse and find what they're looking for. Well-organised catalogs lead to higher conversion rates.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Write Compelling Product Descriptions
        </mj-text>
        <mj-text font-size="14px">
          Great descriptions sell products. Focus on benefits, not just features. Tell customers why they need your product and how it solves their problem.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Upload High-Quality Product Images
        </mj-text>
        <mj-text font-size="14px">
          Clear, professional images make a huge difference. Upload multiple angles and use consistent lighting. Spwig automatically optimises images for fast loading.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Set Up Product Variants
        </mj-text>
        <mj-text font-size="14px">
          If your products come in different sizes, colours, or styles, create variants so customers can select exactly what they want. Each variant can have its own price, stock level, and images.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Manage Your Products" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Getting Started: Your Products - {{ store_name }}

Hi {{ name|default:'there' }},

Your store {{ store_name }} is all set up. Now it's time to build your product catalog. Here are five tips to get you started.

1. Import Products from CSV
Already have a product list? Head to Admin > Catalog > Import to bulk-import your products from a CSV file.

2. Organise with Categories and Filters
Create categories and attribute filters so customers can easily browse and find what they're looking for.

3. Write Compelling Product Descriptions
Great descriptions sell products. Focus on benefits, not just features. Tell customers why they need your product.

4. Upload High-Quality Product Images
Clear, professional images make a huge difference. Upload multiple angles and use consistent lighting.

5. Set Up Product Variants
If your products come in different sizes, colours, or styles, create variants so customers can select exactly what they want.

Manage Your Products: {{ admin_url }}

Need help? Contact {{ support_email }}