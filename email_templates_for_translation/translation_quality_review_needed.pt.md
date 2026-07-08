---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Detectadas traduções de baixa qualidade: {{ content_type }} - {{ low_quality_count }} itens necessitam de revisão

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alerta de Qualidade da Tradução
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Revisão Recomendada
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu trabalho de tradução foi concluído, mas {{ low_quality_count }} traduções tiveram pontuação abaixo do limite de qualidade e devem ser revisadas antes da publicação.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumo do Trabalho:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID do Trabalho:</strong> {{ job_id }}<br/>
              <strong>Tipo de Conteúdo:</strong> {{ content_type }}<br/>
              <strong>Total de Itens:</strong> {{ total_items }}<br/>
              <strong>Qualidade Média:</strong> {{ average_quality }}%<br/>
              <strong>Qualidade Baixa:</strong> {{ low_quality_count }} itens ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Quebra de Qualidade:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Excelente (95-100%):</strong> {{ excellent_count }} itens<br/>
              <strong>Bom (85-94%):</strong> {{ good_count }} itens<br/>
              <strong>Mediano (70-84%):</strong> {{ fair_count }} itens<br/>
              <strong>Péssimo (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} itens</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemas Comuns de Qualidade:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} ocorrências
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ações Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Revisar as traduções marcadas no painel de administração<br/>
          2. Editar manualmente as traduções de baixa qualidade<br/>
          3. Considere re-traduzir itens de baixa qualidade<br/>
          4. Publicar apenas após a revisão estar completa
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Revisar Traduções
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Itens de Baixa Qualidade
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Dica: Pontuações de qualidade abaixo de 85% indicam possíveis problemas com gramática, contexto ou precisão. É fortemente recomendada a revisão humana antes da publicação.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERTA DE QUALIDADE DA TRADUÇÃO

Revisão Recomendada

Seu trabalho de tradução foi concluído, mas {{ low_quality_count }} traduções tiveram pontuação abaixo do limite de qualidade e devem ser revisadas antes da publicação.

RESUMO DO TRABALHO:
- ID do Trabalho: {{ job_id }}
- Tipo de Conteúdo: {{ content_type }}
- Total de Itens: {{ total_items }}
- Qualidade Média: {{ average_quality }}%
- Qualidade Baixa: {{ low_quality_count }} itens ({{ low_quality_percentage }}%)

QUEBRA DE QUALIDADE:
- Excelente (95-100%): {{ excellent_count }} itens
- Bom (85-94%): {{ good_count }} itens
- Mediano (70-84%): {{ fair_count }} itens
- Péssimo (<70%): {{ poor_count }} itens

PROBLEMAS COMUNS DE QUALIDADE:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} ocorrências
{% endfor %}

AÇÕES RECOMENDADAS:
1. Revisar as traduções marcadas no painel de administração
2. Editar manualmente as traduções de baixa qualidade
3. Considere re-traduzir itens de baixa qualidade
4. Publicar apenas após a revisão estar completa

Revisar traduções: {{ review_url }}
Ver itens de baixa qualidade: {{ low_quality_url }}

💡 Dica: Pontuações de qualidade abaixo de 85% indicam possíveis problemas com gramática, contexto ou precisão. É fortemente recomendada a revisão humana antes da publicação.