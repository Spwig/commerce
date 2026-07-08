---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
Seu comentário sobre "{{ post_title }}" foi aprovado - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ Comentário Aprovado
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grande noticia! Seu comentário sobre "{{ post_title }}" foi aprovado e agora está visível para outros leitores.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Seu Comentário:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Ver Seu Comentário
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Nós notificaremos você quando alguém responder ao seu comentário.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ COMENTÁRIO APROVADO

Olá {{ commenter_name }},

Grande noticia! Seu comentário sobre "{{ post_title }}" foi aprovado e agora está visível para outros leitores.

SEU COMENTÁRIO:
{{ comment_text }}

Ver seu comentário: {{ comment_url }}

Nós notificaremos você quando alguém responder ao seu comentário.