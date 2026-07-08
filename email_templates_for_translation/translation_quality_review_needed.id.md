---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Terdeteksi terjemahan berkualitas rendah: {{ content_type }} - {{ low_quality_count }} item perlu ditinjau

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Peringatan Kualitas Terjemahan
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tinjauan Direkomendasikan
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Pekerjaan terjemahan Anda selesai, tetapi {{ low_quality_count }} terjemahan mendapat skor di bawah ambang batas kualitas dan perlu ditinjau sebelum dipublikasikan.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Ringkasan Pekerjaan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID Pekerjaan:</strong> {{ job_id }}<br/>
              <strong>Jenis Konten:</strong> {{ content_type }}<br/>
              <strong>Total Item:</strong> {{ total_items }}<br/>
              <strong>Kualitas Rata-Rata:</strong> {{ average_quality }}%<br/>
              <strong>Kualitas Rendah:</strong> {{ low_quality_count }} item ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Breakdown Kualitas:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Excellent (95-100%):</strong> {{ excellent_count }} item<br/>
              <strong>Good (85-94%):</strong> {{ good_count }} item<br/>
              <strong>Fair (70-84%):</strong> {{ fair_count }} item<br/>
              <strong>Poor (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} item</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Masalah Kualitas Umum:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} kali terjadi
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Tinjau terjemahan yang ditandai di panel admin<br/>
          2. Ubah terjemahan berkualitas rendah secara manual<br/>
          3. Pertimbangkan menterjemahkan ulang item berkualitas buruk<br/>
          4. Publikasikan hanya setelah tinjauan selesai
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tinjau Terjemahan
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Item Berkualitas Rendah
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Tips: Skor kualitas di bawah 85% menunjukkan potensi masalah dengan tata bahasa, konteks, atau akurasi. Tinjauan manusia sangat disarankan sebelum publikasi.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERINGATAN KUALITAS TERJEMAHAN

Tinjauan Direkomendasikan

Pekerjaan terjemahan Anda selesai, tetapi {{ low_quality_count }} terjemahan mendapat skor di bawah ambang batas kualitas dan perlu ditinjau sebelum dipublikasikan.

RINGKASAN PEKERJAAN:
- ID Pekerjaan: {{ job_id }}
- Jenis Konten: {{ content_type }}
- Total Item: {{ total_items }}
- Kualitas Rata-Rata: {{ average_quality }}%
- Kualitas Rendah: {{ low_quality_count }} item ({{ low_quality_percentage }}%)

BREAKDOWN KUALITAS:
- Excellent (95-100%): {{ excellent_count }} item
- Good (85-94%): {{ good_count }} item
- Fair (70-84%): {{ fair_count }} item
- Poor (<70%): {{ poor_count }} item

MASALAH KUALITAS UMUM:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} kali terjadi
{% endfor %}

TINDAKAN YANG DIREKOMENDASIKAN:
1. Tinjau terjemahan yang ditandai di panel admin
2. Ubah terjemahan berkualitas rendah secara manual
3. Pertimbangkan menterjemahkan ulang item berkualitas buruk
4. Publikasikan hanya setelah tinjauan selesai

Tinjau terjemahan: {{ review_url }}
Lihat item berkualitas rendah: {{ low_quality_url }}

💡 Tips: Skor kualitas di bawah 85% menunjukkan potensi masalah dengan tata bahasa, konteks, atau akurasi. Tinjauan manusia sangat disarankan sebelum publikasi.