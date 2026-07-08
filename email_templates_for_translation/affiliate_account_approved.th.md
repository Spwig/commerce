---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 ยินดีต้อนรับสู่โปรแกรมพันธมิตร {{ shop_name }}

## HTML Content
<mjml>
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
          🎉 Application Approved!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Welcome to our affiliate program
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          You're Now an Affiliate!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Start earning commissions today
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Congratulations! Your application to join the {{ shop_name }} affiliate program has been approved.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          You can now start promoting our products and earning commissions on every sale you generate.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          How It Works
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. Get your unique affiliate links from the dashboard<br/>
          2. Share these links with your audience<br/>
          3. Earn commissions when people buy through your links<br/>
          4. Receive payouts according to your payment schedule
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Access Affiliate Dashboard
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            Contact Support
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ยินดีต้อนรับสู่โปรแกรมพันธมิตร {{ shop_name }}

Hi {{ affiliate_name }},

Congratulations! Your application to join the {{ shop_name }} affiliate program has been approved.

You can now start promoting our products and earning commissions on every sale you generate.

How It Works:
1. Get your unique affiliate links from the dashboard
2. Share these links with your audience
3. Earn commissions when people buy through your links
4. Receive payouts according to your payment schedule

Access your dashboard: {{ portal_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}