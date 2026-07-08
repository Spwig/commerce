---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
Tingkatkan Penjualan Anda - {{ store_name }}

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
          Getting Started: Marketing & Growth
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Drive traffic and sales to {{ store_name }}
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
          Now that <strong>{{ store_name }}</strong> is taking shape, it's time to focus on driving traffic and growing your sales. Here are five marketing tips to get you started.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Create Your First Discount Code
        </mj-text>
        <mj-text font-size="14px">
          Offer a launch discount to attract your first customers. Go to <strong>Marketing > Discount Codes</strong> to create percentage or fixed-amount discounts with optional usage limits and expiry dates.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Set Up Abandoned Cart Recovery
        </mj-text>
        <mj-text font-size="14px">
          Recover lost sales automatically. Enable abandoned cart recovery emails under <strong>Marketing > Abandoned Carts</strong> to remind customers about items they left behind.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Connect Your Social Media Accounts
        </mj-text>
        <mj-text font-size="14px">
          Link your social media profiles to your store so customers can find and follow you. Add social links under <strong>Settings > Social Media</strong> to display them in your store footer.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Set Up Google Analytics Tracking
        </mj-text>
        <mj-text font-size="14px">
          Understand where your visitors come from and how they interact with your store. Add your Google Analytics tracking ID under <strong>Settings > Analytics</strong> to start collecting data.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Create a Newsletter Signup Form
        </mj-text>
        <mj-text font-size="14px">
          Build your email list from day one. Add a newsletter signup form to your store to capture visitor emails. Use these contacts for promotions, product launches, and customer engagement.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Getting Started: Marketing & Growth - {{ store_name }}

Hi {{ name|default:'there' }},

Now that {{ store_name }} is taking shape, it's time to focus on driving traffic and growing your sales. Here are five marketing tips to get you started.

1. Create Your First Discount Code
Offer a launch discount to attract your first customers. Go to Marketing > Discount Codes to create discounts with optional usage limits and expiry dates.

2. Set Up Abandoned Cart Recovery
Recover lost sales automatically. Enable abandoned cart recovery emails under Marketing > Abandoned Carts.

3. Connect Your Social Media Accounts
Link your social media profiles to your store. Add social links under Settings > Social Media.

4. Set Up Google Analytics Tracking
Understand where your visitors come from. Add your Google Analytics tracking ID under Settings > Analytics.

5. Create a Newsletter Signup Form
Build your email list from day one. Add a newsletter signup form to capture visitor emails for promotions and engagement.

Go to Marketing: {{ admin_url }}

Need help? Contact {{ support_email }}