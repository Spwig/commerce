---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ {{ component_name }} Güncellemesi Başarısız

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Güncellemeye Başarısız Oldu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kurulum Hatası
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} için {{ target_version }} sürümüne güncelleme kurulumu başarısız oldu.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Başarısızlık Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Bileşen:</strong> {{ component_name }}<br/>
              <strong>Hedef Sürüm:</strong> {{ target_version }}<br/>
              <strong>Başarısız Oldu:</strong> {{ failed_at }}<br/>
              <strong>Hata Kodu:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hata Mesajı:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Tam Hata Günlüğü:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:50 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ne Yapmalı:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Sistem gereksinimlerini ve bağımlılıkları kontrol edin<br/>
          2. Hata günlüğünü inceleyerek ayrıntıları gözden geçirin<br/>
          3. Tekrar kurmaya çalışın veya destek ile iletişime geçin<br/>
          4. Mağazanız hâlâ {{ current_version }} sürümünde çalışıyor
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Yeniden Kur
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Destek ile İletişime Geç
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ GÜNCELLEME BAŞARISIZ

Kurulum Hatası

{{ component_name }} için {{ target_version }} sürümüne güncelleme kurulumu başarısız oldu.

BAŞARISIZLIK AYRINTILARI:
- Bileşen: {{ component_name }}
- Hedef Sürüm: {{ target_version }}
- Başarısız Oldu: {{ failed_at }}
- Hata Kodu: {{ error_code }}

HATA MESAJI:
{{ error_message }}

{% if error_log %}
TAM HATA GÜNLÜĞÜ:
{{ error_log|truncatewords:50 }}
{% endif %}

NE YAPMALI:
1. Sistem gereksinimlerini ve bağımlılıkları kontrol edin
2. Hata günlüğünü inceleyerek ayrıntıları gözden geçirin
3. Tekrar kurmaya çalışın veya destek ile iletişime geçin
4. Mağazanız hâlâ {{ current_version }} sürümünde çalışıyor

Yeniden kur: {{ retry_url }}
Destek ile iletişime geç: {{ support_url }}