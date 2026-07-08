---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
Yorumunuz "{{ post_title }}" için onaylandı - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ Yorum Onaylandı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Harika haber! "{{ post_title }}" üzerine yorumunuz onaylandı ve artık diğer okuyucilardan görülebilir.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Yorumunuz:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Yorumunuzu Görün
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Yorumunuza kimse yanıt verdiğinde size bildireceğiz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ Yorum Onaylandı

Merhaba {{ commenter_name }},

Harika haber! "{{ post_title }}" üzerine yorumunuz onaylandı ve artık diğer okuyucilardan görülebilir.

Yorumunuz:
{{ comment_text }}

Yorumunuzu Görün: {{ comment_url }}

Yorumunuza kimse yanıt verdiğinde size bildireceğiz.