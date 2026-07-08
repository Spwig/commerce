---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
İade Talebi Güncellemesi - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          İade Talebi Güncellemesi
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
          Sipariş #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişinize <strong>#{{ order_number }}</strong> için yapılan iade talebinizi inceledik ve şu anda onaylayamayız.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Neden:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bu kararla ilgili sorularınız varsa veya bir hata olduğunu düşünüyorsanız, lütfen destek ekibimizle iletişime geçin.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İade Talebi Güncellemesi - Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

Sipariş #{{ order_number }} için yapılan iade talebinizi inceledik ve şu anda onaylayamayız.

{% if rejection_reason %}Neden: {{ rejection_reason }}{% endif %}

Bu kararla ilgili sorularınız varsa veya bir hata olduğunu düşünüyorsanız, lütfen destek ekibimizle iletişime geçin.