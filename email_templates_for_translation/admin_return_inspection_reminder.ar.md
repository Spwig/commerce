---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
استلام المرتجع - مطلوب فحص للطلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          مطلوب فحص المرتجع
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم استلام حزمة مرتجعة وتحتاج إلى فحص.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الطلب:</strong> #{{ order_number }}<br/>
              <strong>الاستلام:</strong> {{ received_at }}<br/>
              <strong>العناصر للفحص:</strong> {{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض المرتجع في الإدارة
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
فحص المرتجع مطلوب

تم استلام حزمة مرتجعة وتحتاج إلى فحص.

الطلب: #{{ order_number }}
الاستلام: {{ received_at }}
العناصر للفحص: {{ items_count }}

{% if admin_url %}عرض في الإدارة: {{ admin_url }}{% endif %}