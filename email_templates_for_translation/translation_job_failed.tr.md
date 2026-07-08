---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Çeviri Görevi Başarısız Oldu: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Çeviri Görevi Başarısız Oldu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Çeviri Hatası
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Toplu çeviri görevinizde bir hata oluştu ve tamamlanamadı.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Görev Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Görev Kimliği:</strong> {{ job_id }}<br/>
              <strong>İçerik Türü:</strong> {{ content_type }}<br/>
              <strong>Hedef Diller:</strong> {{ target_languages }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Kısmi Tamamlama
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Hata oluşmadan önce {{ items_completed }}/{{ total_items }} öğe başarıyla çevrildi.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ortak Nedenler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Çeviri hizmeti API bağlantısı sorunları<br/>
          • Yetersiz çeviri kredisi<br/>
          • Geçersiz veya bozuk kaynak içeriği<br/>
          • Desteklenmeyen diller çifti
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Çeviri hizmeti ayarlarınızı kontrol edin<br/>
          2. Çeviri kredisinin mevcut olduğunu doğrulayın<br/>
          3. Hata mesajını özel sorunlar için inceleyin<br/>
          4. Çeviri görevini tekrar deneyin
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Çeviriyi Tekrar Deneyin
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ayarları Kontrol Et
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sorun devam ederse, {{ error_code }} hata kodu ile destek ile iletişime geçin.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ÇEVİRİ GÖREVİ BAŞARISIZ OLDU

Çeviri Hatası

Toplu çeviri görevinizde bir hata oluştu ve tamamlanamadı.

GÖREV DETAYLARI:
- Görev Kimliği: {{ job_id }}
- İçerik Türü: {{ content_type }}
- Hedef Diller: {{ target_languages }}
- Başarısız Oldu: {{ failed_at }}
- Hata Kodu: {{ error_code }}

HATA MESAJI:
{{ error_message }}

{% if partial_completion %}
KISMI TAMAMLAMA:
{{ items_completed }}/{{ total_items }} öğe, hata oluşmadan önce başarıyla çevrildi.
{% endif %}

ORTAK NEDENLER:
• Çeviri hizmeti API bağlantısı sorunları
• Yetersiz çeviri kredisi
• Geçersiz veya bozuk kaynak içeriği
• Desteklenmeyen diller çifti

ÖNERİLEN EYLEMLER:
1. Çeviri hizmeti ayarlarınızı kontrol edin
2. Çeviri kredisinin mevcut olduğunu doğrulayın
3. Hata mesajını özel sorunlar için inceleyin
4. Çeviri görevini tekrar deneyin

Çeviriyi tekrar deneyin: {{ retry_url }}
Ayarları kontrol edin: {{ settings_url }}

Sorun devam ederse, {{ error_code }} hata kodu ile destek ile iletişime geçin.