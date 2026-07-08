---
template_type: blog_comment_reply
category: Blog
---

# Email Template: blog_comment_reply

## Subject
 {{ replier_name }} ha risposto al tuo commento su "{{ post_title }}" 

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          💬 Nuova Risposta al Tuo Commento
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ replier_name }} ha risposto al tuo commento su "{{ post_title }}".
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Il tuo commento:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ original_comment }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="15px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="#065f46">
              {{ replier_name }} ha risposto:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ reply_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ reply_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza e Rispondi
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Non vuoi ricevere notifiche di risposta? <a href="{{ unsubscribe_url }}">Annulla l'abbonamento</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💬 NUOVA RISPOSTA AL TUO COMMENTO

Hi {{ commenter_name }},

{{ replier_name }} ha risposto al tuo commento su "{{ post_title }}".

IL TUO COMMENTO:
{{ original_comment }}

{{ replier_name }} HA RISPOSTO:
{{ reply_text }}

Visualizza e rispondi: {{ reply_url }}

Non vuoi ricevere notifiche di risposta? Annulla l'abbonamento: {{ unsubscribe_url }}

