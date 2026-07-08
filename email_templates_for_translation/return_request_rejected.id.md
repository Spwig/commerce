---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Pembaruan Permintaan Pengembalian - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Pembaruan Permintaan Pengembalian
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kami telah meninjau permintaan pengembalian Anda untuk pesanan <strong>#{{ order_number }}</strong> dan saat ini kami tidak dapat menyetujui permintaan tersebut.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Alasan:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Jika Anda memiliki pertanyaan mengenai keputusan ini atau percaya bahwa terjadi kesalahan, silakan hubungi tim dukungan kami.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembaruan Permintaan Pengembalian - Pesanan #{{ order_number }}

Hai {{ customer_name }},

Kami telah meninjau permintaan pengembalian Anda untuk pesanan #{{ order_number }} dan saat ini kami tidak dapat menyetujui permintaan tersebut.

{% if rejection_reason %}Alasan: {{ rejection_reason }}{% endif %}

Jika Anda memiliki pertanyaan mengenai keputusan ini atau percaya bahwa terjadi kesalahan, silakan hubungi tim dukungan kami.