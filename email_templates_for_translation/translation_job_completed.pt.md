---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Traduções concluídas: {{ content_type }} ({{ language_count }} idiomas)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Tradução Concluída!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Suas Traduções Estão Prontas
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Boa notícia! Seu trabalho de tradução em lote foi concluído com sucesso.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumo do Trabalho:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID do Trabalho:</strong> {{ job_id }}<br/>
              <strong>Tipo de Conteúdo:</strong> {{ content_type }}<br/>
              <strong>Idiomas:</strong> {{ target_languages }}<br/>
              <strong>Itens Traduzidos:</strong> {{ items_translated }}<br/>
              <strong>Total de Palavras:</strong> {{ word_count }}<br/>
              <strong>Concluído:</strong> {{ completed_at }}<br/>
              <strong>Duração:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qualidade da Tradução:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Pontuação Média de Qualidade:</strong> {{ quality_score }}%<br/>
              <strong>Alta Qualidade:</strong> {{ high_quality_count }} itens<br/>
              <strong>Revisão Recomendada:</strong> {{ review_needed_count }} itens
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Revisão Recomendada
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} traduções obtiveram uma pontuação abaixo de 85% e devem ser revisadas antes de publicar.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Próximos Passos:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Revise as traduções no seu painel de administração<br/>
          2. Edite quaisquer traduções que precisem de refinamento<br/>
          3. Publique as traduções para torná-las visíveis<br/>
          4. Seu conteúdo multilíngue estará disponível para os clientes
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Revisar Traduções
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Publicar Tudo
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ TRADUÇÃO CONCLUIDA!

Suas Traduções Estão Prontas

Boa notícia! Seu trabalho de tradução em lote foi concluído com sucesso.

RESUMO DO TRABALHO:
- ID do Trabalho: {{ job_id }}
- Tipo de Conteúdo: {{ content_type }}
- Idiomas: {{ target_languages }}
- Itens Traduzidos: {{ items_translated }}
- Total de Palavras: {{ word_count }}
- Concluído: {{ completed_at }}
- Duração: {{ job_duration }}

QUALIDADE DA TRADUÇÃO:
- Pontuação Média de Qualidade: {{ quality_score }}%
- Alta Qualidade: {{ high_quality_count }} itens
- Revisão Recomendada: {{ review_needed_count }} itens

{% if review_needed_count > 0 %}
⚠️ REVISÃO RECOMENDADA:
{{ review_needed_count }} traduções obtiveram uma pontuação abaixo de 85% e devem ser revisadas antes de publicar.
{% endif %}

PRÓXIMOS PASSOS:
1. Revise as traduções no seu painel de administração
2. Edite quaisquer traduções que precisem de refinamento
3. Publique as traduções para torná-las visíveis
4. Seu conteúdo multilíngue estará disponível para os clientes

Revisar traduções: {{ review_url }}
{% if can_publish_all %}Publicar tudo: {{ publish_all_url }}{% endif %}