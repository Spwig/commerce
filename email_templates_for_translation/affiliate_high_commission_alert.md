---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Unusual Commission Activity Detected - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ High Commission Alert
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Unusual Activity Detected
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          An unusually high commission has been earned by affiliate {{ affiliate_name }}. This requires review for fraud prevention.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Alert Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Affiliate:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Commission Amount:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Order Value:</strong> {{ order_value }}<br/>
              <strong>Order ID:</strong> {{ order_number }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Why This Was Flagged:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Review the order details for legitimacy<br/>
          • Check affiliate's referral history<br/>
          • Verify customer is not affiliated with referrer<br/>
          • Approve or reject commission in admin panel
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Review Commission
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Affiliate Details
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          This commission is pending review and will not be paid until approved.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ HIGH COMMISSION ALERT

Unusual Activity Detected

An unusually high commission has been earned by affiliate {{ affiliate_name }}. This requires review for fraud prevention.

ALERT DETAILS:
- Affiliate: {{ affiliate_name }} ({{ affiliate_id }})
- Commission Amount: {{ commission_amount }}
- Order Value: {{ order_value }}
- Order ID: {{ order_number }}
- Detected: {{ detected_at }}

WHY THIS WAS FLAGGED:
{{ flag_reason }}

RECOMMENDED ACTIONS:
• Review the order details for legitimacy
• Check affiliate's referral history
• Verify customer is not affiliated with referrer
• Approve or reject commission in admin panel

Review commission: {{ review_commission_url }}
View affiliate details: {{ affiliate_details_url }}

This commission is pending review and will not be paid until approved.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affiliate_name | Affiliate's name | John Smith |
| affiliate_id | Affiliate ID | AFF-12345 |
| commission_amount | Commission earned | $547.50 |
| order_value | Total order value | $5,475.00 |
| order_number | Order number | #2026-001234 |
| detected_at | When detected | February 15, 2026 at 3:45 PM |
| flag_reason | Why flagged | Commission amount exceeds $500 threshold (10x normal average of $47.32) |
| review_commission_url | Commission review page | https://shop.com/en/admin/affiliate/commissions/12345 |
| affiliate_details_url | Affiliate profile | https://shop.com/en/admin/affiliate/partners/AFF-12345 |

## Notes

- ADMIN ONLY notification
- Fraud prevention alert
- Sent when commission exceeds threshold (e.g., 5x average or >$500)
- Commission automatically held pending review
- Helps prevent affiliate fraud
- Transactional email
