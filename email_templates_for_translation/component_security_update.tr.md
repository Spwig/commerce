---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 ACİL: {{ component_name }} için Güvenlik Güncellemesi Mevcut

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 GÜVENLİK GÜNCELLEMESİ GEREKLİ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kritik Güvenlik Yaması
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} bileşeninde bir güvenlik açıklaması bulundu. Mağazanızı korumak için hemen güncelleyin.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Güvenlik Bilgisi
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Bileşen:</strong> {{ component_name }}<br/>
              <strong>Mevcut Sürüm:</strong> {{ current_version }}<br/>
              <strong>Yamalanan Sürüm:</strong> {{ patched_version }}<br/>
              <strong>Ciddiyet:</strong> {{ severity_level }}<br/>
              <strong>CVE Kimliği:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Açıklamanın Ayrıntıları:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Potansiyel Etki:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Geçici Çözüm
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Yapılacak İşlem: Güncellemeyi Hemen Kurun
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Güvenlik Yamasını Kur
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Güvenlik Danışmanlığını Oku
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Yardım gerekiyorsa, Spwig desteğiyle hemen iletişime geçin.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 GÜVENLİK GÜNCELLEMESİ GEREKLİ

Kritik Güvenlik Yaması

{{ component_name }} bileşeninde bir güvenlik açıklaması bulundu. Mağazanızı korumak için hemen güncelleyin.

⚠️ GÜVENLİK BİLGİSİ:
- Bileşen: {{ component_name }}
- Mevcut Sürüm: {{ current_version }}
- Yamalanan Sürüm: {{ patched_version }}
- Ciddiyet: {{ severity_level }}
- CVE Kimliği: {{ cve_id }}

AÇIKLAMANIN AYRINTILARI:
{{ vulnerability_description }}

POTANSİYEL ETKİ:
{{ impact_description }}

{% if mitigation_steps %}
GEÇİCİ ÇÖZÜM:
{{ mitigation_steps }}
{% endif %}

YAPILACAK İŞLEM: GÜNCELLEMEYİ HEMEN KURUN

Güvenlik yamasını kur: {{ update_url }}
Güvenlik danışmanlığını oku: {{ advisory_url }}

Yardım gerekiyorsa, Spwig desteğiyle hemen iletişime geçin.