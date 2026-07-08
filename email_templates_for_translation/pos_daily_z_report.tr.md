---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 Günlük Z Raporu - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Günlük Z Raporu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gün Sonu Bakiye Raporu
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ location_name }} için {{ report_date }} tarihli günlük özet.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Satış Özeti:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Toplam Satış:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>İşlemler:</strong> {{ transaction_count }}<br/>
              <strong>Satın Alınan Ürünler:</strong> {{ items_sold }}<br/>
              <strong>Ortalama Satış:</strong> {{ average_sale }}<br/>
              <strong>Kolekte Edilen Vergi:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ödeme Yöntemleri:
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
          Vardiya Özeti:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Toplam Vardiya Sayısı:</strong> {{ shift_count }}<br/>
              <strong>Kullanılan Terminal Sayısı:</strong> {{ terminal_count }}<br/>
              <strong>Aktif Kasiyer Sayısı:</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Satışlar: {{ terminal.sales }} | İşlemler: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Düzeltilmeler & İndirimler:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Verilen İndirimler:</strong> {{ discounts_total }}<br/>
              <strong>İade Edilen Tutar:</strong> {{ refunds_total }}<br/>
              <strong>Göze Çarpanlar:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Toplam Nakit Farkı: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          En Çok Satılan Ürünler:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} satıldı ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Raporu Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 GÜNLÜK Z RAPORU

Gün Sonu Bakiye Raporu

{{ location_name }} için {{ report_date }} tarihli günlük özet.

SATIŞ ÖZETİ:
- Toplam Satış: {{ total_sales }}
- İşlemler: {{ transaction_count }}
- Satın Alınan Ürünler: {{ items_sold }}
- Ortalama Satış: {{ average_sale }}
- Kolekte Edilen Vergi: {{ tax_collected }}

ÖDEME YÖNTEMLERİ:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} işlem)
{% endfor %}

VARDİYA ÖZETİ:
- Toplam Vardiya: {{ shift_count }}
- Kullanılan Terminal Sayısı: {{ terminal_count }}
- Aktif Kasiyer Sayısı: {{ cashier_count }}

TERMINAL AYRINTILARI:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} işlem
{% endfor %}

DÜZELTİLMELER & İNDİRİMLER:
- Verilen İndirimler: {{ discounts_total }}
- İade Edilen Tutar: {{ refunds_total }}
- Göze Çarpanlar: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ TOPLAM NAKİT FARKI: {{ cash_variance }}
{{ variance_note }}
{% endif %}

EN ÇOK SATILAN ÜRÜNLER:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} satıldı ({{ product.revenue }})
{% endfor %}

Raporu Görüntüle: {{ full_report_url }}