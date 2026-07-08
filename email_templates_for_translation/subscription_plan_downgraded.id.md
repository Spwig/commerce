---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
Rencana langganan Anda telah diubah ke {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Rencana Berubah
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Rencana Langganan Diperbarui
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Rencana langganan Anda telah diubah ke {{ new_plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Perubahan Rencana:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Rencana Sebelumnya:</strong> {{ old_plan_name }}<br/>
              <strong>Rencana Baru:</strong> {{ new_plan_name }}<br/>
              <strong>Diperbarui Pada:</strong> {{ downgrade_date }}<br/>
              <strong>Berlaku:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa Perubahan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Fitur yang Tidak Tersedia Lagi:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
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
              <strong>Harga Baru:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Tanggal Berlaku:</strong> {{ effective_date }}<br/>
              <strong>Tanggal Pemrosesan Berikutnya:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 Kredit sebesar {{ credit_amount }} telah diterapkan pada akun Anda untuk bagian yang tidak digunakan dari rencana sebelumnya.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Berubah Pikiran?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          Anda dapat meningkatkan kembali ke {{ old_plan_name }} kapan saja.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tingkatkan Rencana
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
RENCANA BERUBAH

Rencana Langganan Diperbarui

Hi {{ customer_name }},

Rencana langganan Anda telah diubah ke {{ new_plan_name }}.

DETAIL PERUBAHAN RENCANA:
- Rencana Sebelumnya: {{ old_plan_name }}
- Rencana Baru: {{ new_plan_name }}
- Diperbarui Pada: {{ downgrade_date }}
- Berlaku: {{ effective_date }}

APA PERUBAHAN:
{{ plan_changes }}

{% if features_lost %}
FITUR YANG TIDAK TERSEDIA LAGI:
{{ features_lost }}
{% endif %}

INFORMASI PEMBAYARAN:
- Harga Baru: {{ new_price }} / {{ billing_period }}
- Tanggal Berlaku: {{ effective_date }}
- Tanggal Pemrosesan Berikutnya: {{ next_billing_date }}

{% if credit_applied %}
💰 Kredit sebesar {{ credit_amount }} telah diterapkan pada akun Anda untuk bagian yang tidak digunakan dari rencana sebelumnya.
{% endif %}

BERUBAH PIKIRAN?
Anda dapat meningkatkan kembali ke {{ old_plan_name }} kapan saja.

Tingkatkan rencana: {{ upgrade_url }}
Lihat langganan saya: {{ account_url }}