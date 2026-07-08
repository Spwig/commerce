---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Update Tersedia: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Update Tersedia
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Versi Baru Tersedia
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Sebuah versi baru dari {{ component_name }} tersedia untuk toko Spwig Anda.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Pembaruan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Komponen:</strong> {{ component_name }}<br/>
              <strong>Versi Saat Ini:</strong> {{ current_version }}<br/>
              <strong>Versi Baru:</strong> {{ new_version }}<br/>
              <strong>Tanggal Rilis:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Baru:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Perubahan Pecah
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Pasang Pembaruan
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            Lihat Ringkasan Perubahan Lengkap
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 PEMBARUAN TERSEDIA

Versi Baru Tersedia

Sebuah versi baru dari {{ component_name }} tersedia untuk toko Spwig Anda.

DETAIL PEMBARUAN:
- Komponen: {{ component_name }}
- Versi Saat Ini: {{ current_version }}
- Versi Baru: {{ new_version }}
- Tanggal Rilis: {{ release_date }}

APA YANG BARU:
{{ changelog }}

{% if breaking_changes %}
⚠️ PERUBAHAN PECAH:
{{ breaking_changes }}
{% endif %}

Pasang pembaruan: {{ update_url }}
Lihat ringkasan perubahan lengkap: {{ changelog_url }}