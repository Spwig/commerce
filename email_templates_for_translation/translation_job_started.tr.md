---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Çeviri işi başlatıldı: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Çeviri İş Başlatıldı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Toplu Çeviri İşlemi Devam Ediyor
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Toplu çeviri işiniz başlatıldı ve şu anda işleniyor.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              İş Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>İş Kimliği:</strong> {{ job_id }}<br/>
              <strong>İçerik Türü:</strong> {{ content_type }}<br/>
              <strong>Kaynak Dili:</strong> {{ source_language }}<br/>
              <strong>Hedef Diller:</strong> {{ target_languages }}<br/>
              <strong>Çevirilecek Öğeler:</strong> {{ item_count }}<br/>
              <strong>Başlatıldı:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tahmini Tamamlanma:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              ({{ word_count }} kelime temelinde)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sonraki Adımlar:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. AI çeviri hizmeti içeriğinizi işler<br/>
          2. Çeviriler inceleme için taslak olarak kaydedilir<br/>
          3. İş tamamlandığında size bir e-posta gönderilecektir<br/>
          4. Yönetici panelinizden çevirileri inceleyip yayınlayabilirsiniz
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          İş Durumunu Görüntüle
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bu e-postayı kapatabilirsiniz. Çeviri tamamlandığında size bildirilecektir.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 ÇEVİRİ İŞİ BAŞLATILDI

Toplu Çeviri İşlemi Devam Ediyor

Toplu çeviri işiniz başlatıldı ve şu anda işleniyor.

İŞ DETAYLARI:
- İş Kimliği: {{ job_id }}
- İçerik Türü: {{ content_type }}
- Kaynak Dili: {{ source_language }}
- Hedef Diller: {{ target_languages }}
- Çevirilecek Öğeler: {{ item_count }}
- Başlatıldı: {{ started_at }}

Tahmini Tamamlanma:
{{ estimated_completion }}
({{ word_count }} kelime temelinde)

SONRAKİ ADIMLAR:
1. AI çeviri hizmeti içeriğinizi işler
2. Çeviriler inceleme için taslak olarak kaydedilir
3. İş tamamlandığında size bir e-posta gönderilecektir
4. Yönetici panelinizden çevirileri inceleyip yayınlayabilirsiniz

İş durumunu görüntüleyin: {{ job_status_url }}

Bu e-postayı kapatabilirsiniz. Çeviri tamamlandığında size bildirilecektir.