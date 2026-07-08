---
template_type: component_update_installed
category: Component Updates
---

# Email Template: component_update_installed

## Subject
✓ {{ component_name }} v{{ new_version }}'a güncellendi

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Update Installed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Update Successful
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} has been successfully updated to version {{ new_version }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Installation Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Previous Version:</strong> {{ old_version }}<br/>
              <strong>New Version:</strong> {{ new_version }}<br/>
              <strong>Installed:</strong> {{ installed_at }}<br/>
              <strong>Duration:</strong> {{ installation_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if post_install_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Important Information:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ post_install_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if requires_configuration %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚙️ Configuration Required
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ configuration_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if configuration_url %}
        <mj-button href="{{ configuration_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Configure Component
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ component_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Component Details
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ GÜNCELLEME YÜKLENDİ

Güncelleme Başarılı

{{ component_name }} başarıyla v{{ new_version }} sürümüne güncellendi.

YÜKLEME DETAYLARI:
- Bileşen: {{ component_name }}
- Önceki Sürüm: {{ old_version }}
- Yeni Sürüm: {{ new_version }}
- Yüklendi: {{ installed_at }}
- Süre: {{ installation_duration }}

{% if post_install_message %}
ÖNEMLİ BİLGİ:
{{ post_install_message }}
{% endif %}

{% if requires_configuration %}
⚙️ YÜKLEME GEREKLİ:
{{ configuration_message }}
{% endif %}

{% if configuration_url %}Bileşeni yapılandır: {{ configuration_url }}{% endif %}
Bileşen detaylarını gör: {{ component_url }}