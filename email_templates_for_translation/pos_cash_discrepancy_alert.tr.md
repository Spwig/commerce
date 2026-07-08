---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Nakit Fark Uyarısı: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Nakit Farkı Tespit Edildi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nakit Farkı Uyarısı
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} terminalinde shift kapatılırken {{ discrepancy_amount }} tutarında bir nakit farkı tespit edildi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Farkın Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kasayıcı:</strong> {{ cashier_name }}<br/>
              <strong>Shift Tarihi:</strong> {{ shift_date }}<br/>
              <strong>Shift Süresi:</strong> {{ shift_duration }}<br/>
              <strong>Tespit Edildi:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nakit Sayımı:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Beklenen Nakit:</strong> {{ expected_cash }}<br/>
              <strong>Sayım Yapılan Nakit:</strong> {{ counted_cash }}<br/>
              <strong>Fark:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Başlangıç Nakiti:</strong> {{ opening_cash }}<br/>
              <strong>Nakit Satışlar:</strong> {{ cash_sales }}<br/>
              <strong>Nakit İadeler:</strong> {{ cash_refunds }}<br/>
              <strong>Ödenen Nakit:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kasayıcının Notu:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Hatalar için işlem geçmişini incele<br/>
          2. Kaydedilmemiş nakit ödemeleri kontrol et<br/>
          3. Nakit sayımının doğru olduğundan emin ol<br/>
          4. Shift notlarında farkı belgele<br/>
          5. Gerekirse kasayıcı ile iletişime geç
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Shift Raporunu Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          İşlemleri İncele
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ NAKİT FARKI TESPİT EDİLDİ

Nakit Farkı Uyarısı

{{ terminal_name }} terminalinde shift kapatılırken {{ discrepancy_amount }} tutarında bir nakit farkı tespit edildi.

FARKIN AYRINTILARI:
- Terminal: {{ terminal_name }}
- Kasayıcı: {{ cashier_name }}
- Shift Tarihi: {{ shift_date }}
- Shift Süresi: {{ shift_duration }}
- Tespit Edildi: {{ detected_at }}

NAKİT SAYIMI:
- Beklenen Nakit: {{ expected_cash }}
- Sayım Yapılan Nakit: {{ counted_cash }}
- Fark: {{ discrepancy_amount }}

AÇIKLAMA:
- Başlangıç Nakiti: {{ opening_cash }}
- Nakit Satışlar: {{ cash_sales }}
- Nakit İadeler: {{ cash_refunds }}
- Ödenen Nakit: {{ cash_paid_out }}

{% if cashier_note %}
KASAYICININ NOTU:
"{{ cashier_note }}"
{% endif %}

ÖNERİLEN EYLEMLER:
1. Hatalar için işlem geçmişini incele
2. Kaydedilmemiş nakit ödemeleri kontrol et
3. Nakit sayımının doğru olduğundan emin ol
4. Shift notlarında farkı belgele
5. Gerekirse kasayıcı ile iletişime geç

Shift raporunu görüntüle: {{ shift_report_url }}
İşlemleri incele: {{ transaction_history_url }}

