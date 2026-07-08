---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Güncelleme Mevcut: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Güncelleştirme Mevcut
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yeni Bir Sürüm Mevcut
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Spwig mağazanız için {{ component_name }} için yeni bir sürüm mevcut.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Güncelleştirme Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Bileşen:</strong> {{ component_name }}<br/>
              <strong>Mevcut Sürüm:</strong> {{ current_version }}<br/>
              <strong>Yeni Sürüm:</strong> {{ new_version }}<br/>
              <strong>Yayın Tarihi:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ne Yeni?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Kırıcı Değişiklikler
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Güncelleştirme Yükle
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            Tam Değişiklik Kaydı'na Bak
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 GÜNCELLEME MEVCUT

Yeni Bir Sürüm Mevcut

Spwig mağazanız için {{ component_name }} için yeni bir sürüm mevcut.

GÜNCELLEME DETAYLARI:
- Bileşen: {{ component_name }}
- Mevcut Sürüm: {{ current_version }}
- Yeni Sürüm: {{ new_version }}
- Yayın Tarihi: {{ release_date }}

NE YENİ:
{{ changelog }}

{% if breaking_changes %}
⚠️ KIRICI DEĞİŞİKLİKLER:
{{ breaking_changes }}
{% endif %}

Güncelleme yükle: {{ update_url }}
Tam değişiklik kaydı'na bak: {{ changelog_url }}