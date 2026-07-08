---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 Yüksek Değerli İşlem: {{ transaction_amount }} - {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 Yüksek Değerli İşlem
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Büyük Bir İşlem İşlendi
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} terminalinde {{ transaction_amount }} tutarında bir işlem işlendi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              İşlem Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tutar:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kasayıcı:</strong> {{ cashier_name }}<br/>
              <strong>Zaman Damgası:</strong> {{ transaction_time }}<br/>
              <strong>İşlem Kimliği:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ödeme Bilgileri:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ürünler Özeti:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Toplam Ürünler:</strong> {{ item_count }}<br/>
              <strong>Ara Toplam:</strong> {{ subtotal }}<br/>
              <strong>Vergi:</strong> {{ tax_amount }}<br/>
              <strong>Toplam:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Müşteri Bilgileri:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
          Tüm {{ threshold_amount }} tutarını geçen işlemler için dolandırıcılık önleme ve izleme amaçlı bu bildirim gönderilmektedir.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          İşlemi Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Faturayı Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 YÜKSEK DEĞERLİ İŞLEM

Büyük Bir İşlem İşlendi

{{ terminal_name }} terminalinde {{ transaction_amount }} tutarında bir işlem işlendi.

İŞLEM DETAYLARI:
- Tutar: {{ transaction_amount }}
- Terminal: {{ terminal_name }}
- Kasayıcı: {{ cashier_name }}
- Zaman Damgası: {{ transaction_time }}
- İşlem Kimliği: {{ transaction_id }}

ÖDEME BİLGİLERİ:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

ÜRÜNLER ÖZETİ:
- Toplam Ürünler: {{ item_count }}
- Ara Toplam: {{ subtotal }}
- Vergi: {{ tax_amount }}
- Toplam: {{ transaction_amount }}

{% if customer_info %}
MÜŞTERİ BİLGİLERİ:
{{ customer_info }}
{% endif %}

Tüm {{ threshold_amount }} tutarını geçen işlemler için dolandırıcılık önleme ve izleme amaçlı bu bildirim gönderilmektedir.

İşlemi Görüntüle: {{ transaction_url }}
Faturayı Görüntüle: {{ receipt_url }}