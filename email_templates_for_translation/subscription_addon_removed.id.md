---
template_type: subscription_addon_removed
category: Subscriptions
---

# Email Template: subscription_addon_removed

## Subject
Add-on {{ addon_name }} telah dihapus dari langganan Anda

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Add-on Dihapus
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Add-on Dihapus
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ addon_name }} telah dihapus dari langganan {{ plan_name }} Anda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Penghapusan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Add-on:</strong> {{ addon_name }}<br/>
              <strong>Langganan:</strong> {{ plan_name }}<br/>
              <strong>Dihapus Pada:</strong> {{ removed_date }}<br/>
              <strong>Berlaku:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if access_until %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Akses Sampai {{ access_until }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Anda akan terus memiliki akses ke {{ addon_name }} hingga akhir periode pembayaran saat ini.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informasi Pembayaran:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Sebelumnya:</strong> {{ old_total }} / {{ billing_period }}<br/>
              <strong>Harga Add-on:</strong> -{{ addon_price }} / {{ billing_period }}<br/>
              <strong>Total Baru:</strong> {{ new_total }} / {{ billing_period }}<br/>
              <strong>Tanggal Berlaku:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 Kredit sebesar {{ credit_amount }} telah diterapkan ke akun Anda untuk bagian yang tidak digunakan dari add-on ini.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if data_retention_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informasi Penting:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ data_retention_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Butuh Kembali?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Anda dapat menambahkan {{ addon_name }} kembali ke langganan Anda kapan saja.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ addons_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Jelajahi Add-on
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Langganan Saya
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ADD-ON DIHAPUS

Add-on Dihapus

Hi {{ customer_name }},

{{ addon_name }} telah dihapus dari langganan {{ plan_name }} Anda.

DETAIL PENGHAPUSAN:
- Add-on: {{ addon_name }}
- Langganan: {{ plan_name }}
- Dihapus Pada: {{ removed_date }}
- Berlaku: {{ effective_date }}

{% if access_until %}
AKSES SAMPAI {{ access_until }}:
Anda akan terus memiliki akses ke {{ addon_name }} hingga akhir periode pembayaran saat ini.
{% endif %}

INFORMASI PEMBAYARAN:
- Total Sebelumnya: {{ old_total }} / {{ billing_period }}
- Harga Add-on: -{{ addon_price }} / {{ billing_period }}
- Total Baru: {{ new_total }} / {{ billing_period }}
- Tanggal Berlaku: {{ effective_date }}

{% if credit_applied %}
💰 Kredit sebesar {{ credit_amount }} telah diterapkan ke akun Anda untuk bagian yang tidak digunakan dari add-on ini.
{% endif %}

{% if data_retention_info %}
INFORMASI PENTING:
{{ data_retention_info }}
{% endif %}

BUTUH KEMBALI?
Anda dapat menambahkan {{ addon_name }} kembali ke langganan Anda kapan saja.

Jelajahi add-ons: {{ addons_url }}
Lihat langganan saya: {{ account_url }}