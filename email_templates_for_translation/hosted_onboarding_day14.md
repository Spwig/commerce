---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
Take It Further - {{ store_name }}

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
          Getting Started: Advanced Features
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Unlock the full potential of {{ store_name }}
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
          You've been running <strong>{{ store_name }}</strong> for a couple of weeks now. Here are some advanced features to help you take your store to the next level.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Set Up Automated Email Workflows
        </mj-text>
        <mj-text font-size="14px">
          Automate your customer communication with email workflows. Set up welcome sequences, post-purchase follow-ups, and re-engagement campaigns under <strong>Marketing > Email Workflows</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure Tax Rules for Your Regions
        </mj-text>
        <mj-text font-size="14px">
          Ensure you're charging the correct tax rates. Go to <strong>Settings > Tax</strong> to configure tax rules for each region you sell to. You can set up tax-inclusive or tax-exclusive pricing.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Explore the API for Integrations
        </mj-text>
        <mj-text font-size="14px">
          If your plan includes API access, you can integrate your store with external tools and services. Visit <strong>Settings > API</strong> to generate API keys and explore the documentation.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Review Your Analytics Dashboard
        </mj-text>
        <mj-text font-size="14px">
          Keep an eye on your store's performance. Your <strong>Dashboard</strong> shows key metrics including revenue, orders, top products, and customer insights to help you make data-driven decisions.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Consider Adding POS for In-Store Sales
        </mj-text>
        <mj-text font-size="14px">
          Sell in person too? Spwig's point-of-sale feature lets you process in-store transactions that sync with your online inventory and order management. Check <strong>Settings > Point of Sale</strong> to learn more.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Explore Your Dashboard" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Getting Started: Advanced Features - {{ store_name }}

Hi {{ name|default:'there' }},

You've been running {{ store_name }} for a couple of weeks now. Here are some advanced features to help you take your store to the next level.

1. Set Up Automated Email Workflows
Automate your customer communication with welcome sequences, post-purchase follow-ups, and re-engagement campaigns.

2. Configure Tax Rules for Your Regions
Ensure you're charging the correct tax rates. Go to Settings > Tax to configure rules for each region.

3. Explore the API for Integrations
If your plan includes API access, integrate your store with external tools. Visit Settings > API to get started.

4. Review Your Analytics Dashboard
Your Dashboard shows key metrics including revenue, orders, top products, and customer insights.

5. Consider Adding POS for In-Store Sales
Sell in person too? Spwig's point-of-sale feature syncs in-store transactions with your online inventory.

Explore Your Dashboard: {{ admin_url }}

Need help? Contact {{ support_email }}
