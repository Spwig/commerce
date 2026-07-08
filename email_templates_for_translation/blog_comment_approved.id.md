---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
Komentar Anda pada "{{ post_title }}" Telah Disetujui - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ Komentar Disetujui
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Berita baik! Komentar Anda pada "{{ post_title }}" telah disetujui dan kini terlihat oleh pembaca lain.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Komentar Anda:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Lihat Komentar Anda
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Kami akan memberi tahu Anda ketika seseorang membalas komentar Anda.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ KOMENTAR DISETUJUI

Hai {{ commenter_name }},

Berita baik! Komentar Anda pada "{{ post_title }}" telah disetujui dan kini terlihat oleh pembaca lain.

KOMENTAR ANDA:
{{ comment_text }}

Lihat komentar Anda: {{ comment_url }}

Kami akan memberi tahu Anda ketika seseorang membalas komentar Anda.