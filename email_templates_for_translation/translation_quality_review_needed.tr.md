---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Kaliteli çeviri bulunamadı: {{ content_type }} - {{ low_quality_count }} öğe incelemeye ihtiyaç duyuyor

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Çeviri Kalitesi Uyarısı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          İnceleme Önerilir
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Çeviri işiniz tamamlandı, ancak {{ low_quality_count }} çeviri kalite eşiğini geçemedi ve yayın yapmadan önce incelemeye tabi olmalıdır.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              İş Özeti:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>İş Kimliği:</strong> {{ job_id }}<br/>
              <strong>İçerik Türü:</strong> {{ content_type }}<br/>
              <strong>Toplam Öğeler:</strong> {{ total_items }}<br/>
              <strong>Ortalama Kalite:</strong> {{ average_quality }}%<br/>
              <strong>Düşük Kalite:</strong> {{ low_quality_count }} öğe ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kalite Dağılımı:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Mükemmel (95-100%):</strong> {{ excellent_count }} öğe<br/>
              <strong>İyi (85-94%):</strong> {{ good_count }} öğe<br/>
              <strong>Fair (70-84%):</strong> {{ fair_count }} öğe<br/>
              <strong>Kötü (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} öğe</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ortak Kalite Sorunları:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} kez
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Yönetici panelinde işaretlenmiş çevirileri inceleyin<br/>
          2. Düşük kaliteli çevirileri elle düzenleyin<br/>
          3. Kötü kaliteli öğelerin tekrar çevirisini düşünün<br/>
          4. İnceleme tamamlandıktan sonra yalnızca yayınlayın
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Çevirileri İnceleyin
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Düşük Kaliteli Öğeleri Görüntüle
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 İpucu: 85% altındaki kalite puanları, dilbilgisi, bağlam veya doğrulukla ilgili potansiyel sorunları gösterir. Yayın yapmadan önce insan incelemesi güçlü şekilde önerilir.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ÇEVİRİ KALİTESİ UYARISI

İnceleme Önerilir

Çeviri işiniz tamamlandı, ancak {{ low_quality_count }} çeviri kalite eşiğini geçemedi ve yayın yapmadan önce incelemeye tabi olmalıdır.

İŞ ÖZETİ:
- İş Kimliği: {{ job_id }}
- İçerik Türü: {{ content_type }}
- Toplam Öğeler: {{ total_items }}
- Ortalama Kalite: {{ average_quality }}%
- Düşük Kalite: {{ low_quality_count }} öğe ({{ low_quality_percentage }}%)

KALİTE DAĞILIMI:
- Mükemmel (95-100%): {{ excellent_count }} öğe
- İyi (85-94%): {{ good_count }} öğe
- Fair (70-84%): {{ fair_count }} öğe
- Kötü (<70%): {{ poor_count }} öğe

ORTAK KALİTE SORUNLARI:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} kez
{% endfor %}

ÖNERİLEN EYLEMLER:
1. Yönetici panelinde işaretlenmiş çevirileri inceleyin
2. Düşük kaliteli çevirileri elle düzenleyin
3. Kötü kaliteli öğelerin tekrar çevirisini düşünün
4. İnceleme tamamlandıktan sonra yalnızca yayınlayın

Çevirileri inceleyin: {{ review_url }}
Düşük kaliteli öğeleri görüntüleyin: {{ low_quality_url }}

💡 İpucu: 85% altındaki kalite puanları, dilbilgisi, bağlam veya doğrulukla ilgili potansiyel sorunları gösterir. Yayın yapmadan önce insan incelemesi güçlü şekilde önerilir.