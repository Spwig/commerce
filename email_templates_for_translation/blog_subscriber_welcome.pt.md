---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
Bem-vindo ao {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Bem-vindo ao {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Obrigado por se inscrever! Estamos empolgados para compartilhar nosso conteúdo mais recente com você.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              O que esperar:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Novos posts entregues na sua caixa de entrada<br/>
              ✓ Conteúdo exclusivo apenas para assinantes<br/>
              ✓ {{ publish_frequency }} atualizações<br/>
              ✓ Nenhum spam, cancelar inscrição a qualquer momento
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Comece a ler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Confira nossos artigos mais populares:
        </mj-text>

        <mj-spacer height="15px" />

        {% for post in popular_posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.reading_time }} min read
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Ler agora →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Explorar todos os artigos
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Gerencie sua inscrição: <a href="{{ preferences_url }}">Preferências de E-mail</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 BEM-VINDO AO {{ blog_name }}!

Olá {{ subscriber_name }},

Obrigado por se inscrever! Estamos empolgados para compartilhar nosso conteúdo mais recente com você.

O QUE ESPERAR:
✓ Novos posts entregues na sua caixa de entrada
✓ Conteúdo exclusivo apenas para assinantes
✓ {{ publish_frequency }} atualizações
✓ Nenhum spam, cancelar inscrição a qualquer momento

COMEÇAR A LER - ARTIGOS POPULARES:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} min read)
  {{ post.url }}
{% endfor %}

Explorar todos os artigos: {{ blog_url }}

Gerenciar sua inscrição: {{ preferences_url }}