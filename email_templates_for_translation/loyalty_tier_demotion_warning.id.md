---
template_type: loyalty_tier_demotion_warning
category: Loyalty Program
---

# Email Template: loyalty_tier_demotion_warning

## Subject
⚠️ Status Tier Anda Akan Segera Berakhir - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Status Tier Masa Berlaku Habis
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Jangan Kehilangan Manfaat {{ current_tier }} Anda!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Halo {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Status tier {{ current_tier }} Anda akan berakhir pada {{ expiry_date }} jika Anda tidak mempertahankan tingkat aktivitas Anda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Status Saat Ini:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Tier Saat Ini:</strong> {{ current_tier }}<br/>
              <strong>Berakhir:</strong> {{ expiry_date }} ({{ days_remaining }} hari)<br/>
              <strong>Tier Berikutnya:</strong> {{ next_tier }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cara Mempertahankan Status {{ current_tier }} Anda:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Anda perlu {{ requirement_type }} sebelum {{ expiry_date }}:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              {{ requirement_description }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              Saat Ini: {{ current_progress }} | Dibutuhkan: {{ required_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Manfaat Yang Akan Anda Kehilangkan:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% for benefit in tier_benefits %}
          • {{ benefit }}<br/>
          {% endfor %}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Belanja Sekarang & Pertahankan Status Anda
        </mj-button>

        <mj-spacer height="20px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Detail Lengkap
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ STATUS TIER AKAN HABIS

Jangan Kehilangan Manfaat {{ current_tier }} Anda!

Halo {{ customer_name }},

Status tier {{ current_tier }} Anda akan berakhir pada {{ expiry_date }} jika Anda tidak mempertahankan tingkat aktivitas Anda.

STATUS SAAT INI:
- Tier Saat Ini: {{ current_tier }}
- Berakhir: {{ expiry_date }} ({{ days_remaining }} hari)
- Tier Berikutnya: {{ next_tier }}

CARA MEMPERTAHANKAN STATUS {{ current_tier }} ANDA:
Anda perlu {{ requirement_type }} sebelum {{ expiry_date }}:

{{ requirement_description }}
Saat Ini: {{ current_progress }} | Dibutuhkan: {{ required_amount }}

MANFAAT YANG AKAN ANDA KEHILANGKAN:
{% for benefit in tier_benefits %}
• {{ benefit }}
{% endfor %}

Belanja sekarang & pertahankan status Anda: {{ shop_url }}
Lihat detail lengkap: {{ loyalty_dashboard_url }}