---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
İade Alındı - #{{ order_number }} Siparişi İçin Görüntüleme Gerekli

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          İade Görüntülemesi Gerekli
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bir iade paketi alınmış ve görüntüleme gerekli.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Sipariş:</strong> #{{ order_number }}<br/>
              <strong>Alındı:</strong> {{ received_at }}<br/>
              <strong>Görüntülenecek Ürün Sayısı:</strong> {{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Yönetici Panelinde İadeyi Görüntüle
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İade Görüntülemesi Gerekli

Bir iade paketi alınmış ve görüntüleme gerekli.

Sipariş: #{{ order_number }}
Alındı: {{ received_at }}
Görüntülenecek Ürün Sayısı: {{ items_count }}

{% if admin_url %}Yönetici panelinde görüntüle: {{ admin_url }}{% endif %}