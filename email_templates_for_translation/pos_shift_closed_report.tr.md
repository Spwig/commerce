---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 {{ terminal_name }} - {{ shift_date }} için Shift Raporu

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Shift Kapatıldı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Shift Özeti Raporu
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} terminalinde {{ cashier_name }} tarafından shift kapatıldı.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Shift Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kasiyer:</strong> {{ cashier_name }}<br/>
              <strong>Başlatıldı:</strong> {{ shift_started }}<br/>
              <strong>Bitti:</strong> {{ shift_ended }}<br/>
              <strong>Süre:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Satış Özeti:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Toplam Satış:</strong> {{ total_sales }}<br/>
              <strong>İşlemler:</strong> {{ transaction_count }}<br/>
              <strong>Satın Alınan Ürünler:</strong> {{ items_sold }}<br/>
              <strong>Ortalama Satış:</strong> {{ average_sale }}<br/>
              <strong>Koleksiyon Vergisi:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ödeme Ayrıntıları:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} işlem)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nakit Rekabeti:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Başlangıç Nakit:</strong> {{ opening_cash }}<br/>
              <strong>Nakit Satışlar:</strong> {{ cash_sales }}<br/>
              <strong>Beklenen Nakit:</strong> {{ expected_cash }}<br/>
              <strong>Sayılan Nakit:</strong> {{ counted_cash }}<br/>
              <strong>Fark:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Nakit Farkı: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Not: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Raporu Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 SHIFT KAPATILDI

Shift Özeti Raporu

{{ terminal_name }} terminalinde {{ cashier_name }} tarafından shift kapatıldı.

SHIFT AYRINTILARI:
- Terminal: {{ terminal_name }}
- Kasiyer: {{ cashier_name }}
- Başlatıldı: {{ shift_started }}
- Bitti: {{ shift_ended }}
- Süre: {{ shift_duration }}

SATIŞ ÖZETİ:
- Toplam Satış: {{ total_sales }}
- İşlemler: {{ transaction_count }}
- Satın Alınan Ürünler: {{ items_sold }}
- Ortalama Satış: {{ average_sale }}
- Koleksiyon Vergisi: {{ tax_collected }}

ÖDEME AYRINTILARI:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} işlem)
{% endfor %}

NAKİT REKABETİ:
- Başlangıç Nakit: {{ opening_cash }}
- Nakit Satışlar: {{ cash_sales }}
- Beklenen Nakit: {{ expected_cash }}
- Sayılan Nakit: {{ counted_cash }}
- Fark: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ NAKİT FARKI: {{ discrepancy_amount }}
{% if discrepancy_note %}Not: {{ discrepancy_note }}{% endif %}
{% endif %}

Raporu Görüntüle: {{ shift_report_url }}