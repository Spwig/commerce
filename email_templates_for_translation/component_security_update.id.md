---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 PENTING: Pembaruan Keamanan Tersedia untuk {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 PEMBARUAN KEAMANAN DIBUTUHKAN
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Perbaikan Keamanan Penting
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kerentanan keamanan telah ditemukan dalam {{ component_name }}. Silakan perbarui segera untuk melindungi toko Anda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Informasi Keamanan
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Komponen:</strong> {{ component_name }}<br/>
              <strong>Versi Saat Ini:</strong> {{ current_version }}<br/>
              <strong>Versi yang Diperbaiki:</strong> {{ patched_version }}<br/>
              <strong>Keparahan:</strong> {{ severity_level }}<br/>
              <strong>ID CVE:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Detail Kerentanan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dampak Potensial:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Mitigasi Sementara
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Tindakan yang Diperlukan: Pasang Pembaruan Segera
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Pasang Perbaikan Keamanan
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Baca Petunjuk Keamanan
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Jika Anda memerlukan bantuan, segera hubungi dukungan Spwig.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 PEMBARUAN KEAMANAN DIBUTUHKAN

Perbaikan Keamanan Penting

Kerentanan keamanan telah ditemukan dalam {{ component_name }}. Silakan perbarui segera untuk melindungi toko Anda.

⚠️ INFORMASI KEAMANAN:
- Komponen: {{ component_name }}
- Versi Saat Ini: {{ current_version }}
- Versi yang Diperbaiki: {{ patched_version }}
- Keparahan: {{ severity_level }}
- ID CVE: {{ cve_id }}

DETAIL KERENTANAN:
{{ vulnerability_description }}

DAMPAK POTENSIAL:
{{ impact_description }}

{% if mitigation_steps %}
MITIGASI SEMENTARA:
{{ mitigation_steps }}
{% endif %}

TINDAKAN YANG DIPERLUKAN: PASANG PEMBARUAN SEGERA

Pasang perbaikan keamanan: {{ update_url }}
Baca petunjuk keamanan: {{ advisory_url }}

Jika Anda memerlukan bantuan, segera hubungi dukungan Spwig.