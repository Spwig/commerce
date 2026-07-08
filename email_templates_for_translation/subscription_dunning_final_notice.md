---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ FINAL NOTICE: Your subscription will be cancelled in {{ days_until_cancellation }} days

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ FINAL NOTICE
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Subscription Cancellation Imminent
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          This is your final notice. We've been unable to process payment for your {{ plan_name }} subscription. If we don't receive payment within {{ days_until_cancellation }} days, your subscription will be cancelled.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Payment Failed - Action Required
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Subscription:</strong> {{ plan_name }}<br/>
              <strong>Amount Due:</strong> {{ amount_due }}<br/>
              <strong>Failed Attempts:</strong> {{ retry_count }}<br/>
              <strong>Last Attempt:</strong> {{ last_retry_date }}<br/>
              <strong>Cancellation Date:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Payment Error:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What Will Happen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          If payment is not received by {{ cancellation_date }}:<br/>
          • Your subscription will be cancelled<br/>
          • You'll lose access to all subscription benefits<br/>
          • Your data may be deleted (see retention policy)<br/>
          • You'll need to re-subscribe to regain access
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Update Your Payment Method Now
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Update Payment Method
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Common Issues & Solutions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Expired card:</strong> Update with a current credit card<br/>
          • <strong>Insufficient funds:</strong> Ensure sufficient balance<br/>
          • <strong>Card declined:</strong> Contact your bank or use different card<br/>
          • <strong>Address mismatch:</strong> Verify billing address matches card
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Need Help?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              If you're experiencing payment issues or need assistance, please contact our support team immediately.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contact Support
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          If you wish to cancel your subscription, you can do so in your account settings.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ FINAL NOTICE

Subscription Cancellation Imminent

Hi {{ customer_name }},

This is your final notice. We've been unable to process payment for your {{ plan_name }} subscription. If we don't receive payment within {{ days_until_cancellation }} days, your subscription will be cancelled.

⚠️ PAYMENT FAILED - ACTION REQUIRED:
- Subscription: {{ plan_name }}
- Amount Due: {{ amount_due }}
- Failed Attempts: {{ retry_count }}
- Last Attempt: {{ last_retry_date }}
- Cancellation Date: {{ cancellation_date }}

PAYMENT ERROR:
{{ payment_error_message }}

WHAT WILL HAPPEN:
If payment is not received by {{ cancellation_date }}:
• Your subscription will be cancelled
• You'll lose access to all subscription benefits
• Your data may be deleted (see retention policy)
• You'll need to re-subscribe to regain access

UPDATE YOUR PAYMENT METHOD NOW

Common Issues & Solutions:
• Expired card: Update with a current credit card
• Insufficient funds: Ensure sufficient balance
• Card declined: Contact your bank or use different card
• Address mismatch: Verify billing address matches card

NEED HELP?
If you're experiencing payment issues or need assistance, please contact our support team immediately.

Update payment method: {{ update_payment_url }}
Contact support: {{ support_url }}

If you wish to cancel your subscription, you can do so in your account settings.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | John |
| plan_name | Subscription plan name | Premium Plan |
| amount_due | Amount owed | $49.99 |
| retry_count | Number of failed attempts | 4 |
| last_retry_date | Last payment attempt | February 14, 2026 |
| days_until_cancellation | Days remaining | 3 |
| cancellation_date | When subscription cancels | February 18, 2026 |
| payment_error_message | Payment gateway error | Your card was declined. Please contact your bank. |
| update_payment_url | Payment method update page | https://shop.com/en/account/subscription/payment |
| support_url | Support contact | https://shop.com/en/contact |

## Notes

- CRITICAL customer notification
- Final warning before automatic cancellation
- Part of dunning sequence (after multiple retry failures)
- Urgent tone with clear deadline
- Explains consequences of non-payment
- Provides troubleshooting guidance
- Clear call-to-action to update payment
- Transactional email (must be sent)
