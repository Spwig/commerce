---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ Uyum Sorunu: {{ component_name }} ve {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Uyum Uyarısı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sürüm Çakışması Tespit Edildi
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Spwig mağazanızdaki bileşenler arasında uyumluluk sorunu tespit edildi.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Çakışma Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Bileşen 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>Bileşen 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>Tespit Edildi:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Uyum Sorunu:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              Potansiyel Etki
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylem:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Uyumlu Sürümler
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Çakışmayı Çöz
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Destek ile İletişime Geç
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Mağazanız hâlâ çalışıyor, ancak bu çakışmayı yakında çözmeyi öneriyoruz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ UYUM UYARISI

Sürüm Çakışması Tespit Edildi

Spwig mağazanızdaki bileşenler arasında uyumluluk sorunu tespit edildi.

ÇAKIŞMA AYRINTILARI:
- Bileşen 1: {{ component_name }} v{{ component_version }}
- Bileşen 2: {{ conflicting_component }} v{{ conflicting_version }}
- Tespit Edildi: {{ detected_at }}

UYUM SORUNU:
{{ incompatibility_description }}

POTANSİYEL ETKİ:
{{ impact_description }}

ÖNERİLEN EYLEM:
{{ recommended_action }}

{% if compatible_versions %}UYUMLU SÜRÜMLER:
{{ compatible_versions }}{% endif %}

{% if update_url %}Çakışmayı çöz: {{ update_url }}{% endif %}
Destek ile iletişime geç: {{ support_url }}

Mağazanız hâlâ çalışıyor, ancak bu çakışmayı yakında çözmeyi öneriyoruz.