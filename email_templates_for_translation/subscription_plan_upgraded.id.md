---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ Langganan Anda Telah Ditingkatkan!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Plan Upgraded!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Selamat Datang di {{ new_plan_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Langganan Anda telah berhasil ditingkatkan. Anda sekarang memiliki akses ke semua manfaat dari {{ new_plan_name }}!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Perubahan Langganan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Previous Plan:</strong> {{ old_plan_name }}<br/>
              <strong>New Plan:</strong> {{ new_plan_name }}<br/>
              <strong>Upgraded On:</strong> {{ upgrade_date }}<br/>
              <strong>Effective Immediately</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What's New:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informasi Pembayaran:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>New Price:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Next Billing Date:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>Prorated Charge Today:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Anda dikenakan biaya {{ prorated_charge }} hari ini untuk sisa periode pembayaran saat ini Anda.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Langganan Saya
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Pertanyaan? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Hubungi Dukungan</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ PLAN UPGRADED!

Selamat Datang di {{ new_plan_name }}

Hi {{ customer_name }},

Langganan Anda telah berhasil ditingkatkan. Anda sekarang memiliki akses ke semua manfaat dari {{ new_plan_name }}!

PLAN CHANGE DETAILS:
- Previous Plan: {{ old_plan_name }}
- New Plan: {{ new_plan_name }}
- Upgraded On: {{ upgrade_date }}
- Effective Immediately

WHAT'S NEW:
{{ new_features }}

BILLING INFORMATION:
- New Price: {{ new_price }} / {{ billing_period }}
- Next Billing Date: {{ next_billing_date }}
{% if prorated_charge %}- Prorated Charge Today: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 Anda dikenakan biaya {{ prorated_charge }} hari ini untuk sisa periode pembayaran saat ini Anda.
{% endif %}

View my subscription: {{ account_url }}
Questions? Contact Support: {{ support_url }}
