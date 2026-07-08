---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Çeviri tamamlandı: {{ content_type }} ({{ language_count }} dil)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Çeviri Tamamlandı!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Çevirileriniz Hazır
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Harika haber! Toplu çeviri işiniz başarıyla tamamlandı.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              İş Özeti:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>İş Kimliği:</strong> {{ job_id }}<br/>
              <strong>İçerik Türü:</strong> {{ content_type }}<br/>
              <strong>Diller:</strong> {{ target_languages }}<br/>
              <strong>Çevrilen Öğeler:</strong> {{ items_translated }}<br/>
              <strong>Toplam Kelime Sayısı:</strong> {{ word_count }}<br/>
              <strong>Tamamlandı:</strong> {{ completed_at }}<br/>
              <strong>Süre:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Çeviri Kalitesi:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Ortalama Kalite Puanı:</strong> {{ quality_score }}%<br/>
              <strong>Yüksek Kalite:</strong> {{ high_quality_count }} öğe<br/>
              <strong>İnceleme Önerilir:</strong> {{ review_needed_count }} öğe
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ İnceleme Önerilir
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} çeviri, 85% altında puan aldı ve yayına alma öncesi incelemeye tabi tutulmalıdır.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sonraki Adımlar:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Yönetici panelinizde çevirileri inceleyin<br/>
          2. İyileştirme gereken çevirileri düzenleyin<br/>
          3. Çevirileri yayına almak için yayınlayın<br/>
          4. Çevrimiçi içerikleriniz müşterilere ulaşabilir hale gelecektir
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Çevirileri İncele
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Tümünü Yayınla
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ÇEVİRİ TAMAMLANDI!

Çevirileriniz Hazır

Harika haber! Toplu çeviri işiniz başarıyla tamamlandı.

İŞ ÖZETİ:
- İş Kimliği: {{ job_id }}
- İçerik Türü: {{ content_type }}
- Diller: {{ target_languages }}
- Çevrilen Öğeler: {{ items_translated }}
- Toplam Kelime Sayısı: {{ word_count }}
- Tamamlandı: {{ completed_at }}
- Süre: {{ job_duration }}

ÇEVİRİ KALİTESİ:
- Ortalama Kalite Puanı: {{ quality_score }}%
- Yüksek Kalite: {{ high_quality_count }} öğe
- İnceleme Önerilir: {{ review_needed_count }} öğe

{% if review_needed_count > 0 %}
⚠️ İNCELEME ÖNERİLMİŞ:
{{ review_needed_count }} çeviri, 85% altında puan aldı ve yayına alma öncesi incelemeye tabi tutulmalıdır.
{% endif %}

SONRAKİ ADIMLAR:
1. Yönetici panelinizde çevirileri inceleyin
2. İyileştirme gereken çevirileri düzenleyin
3. Çevirileri yayına almak için yayınlayın
4. Çevrimiçi içerikleriniz müşterilere ulaşabilir hale gelecektir

Çevirileri inceleyin: {{ review_url }}
{% if can_publish_all %}Tümünü yayınla: {{ publish_all_url }}{% endif %}