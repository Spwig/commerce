---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Trabalho de Tradução Iniciado: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Trabalho de Tradução Iniciado
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tradução em Lote em Andamento
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu trabalho de tradução em lote foi iniciado e está sendo processado.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Trabalho:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID do Trabalho:</strong> {{ job_id }}<br/>
              <strong>Tipo de Conteúdo:</strong> {{ content_type }}<br/>
              <strong>Idioma de Origem:</strong> {{ source_language }}<br/>
              <strong>Idiomas de Destino:</strong> {{ target_languages }}<br/>
              <strong>Itens para Traduzir:</strong> {{ item_count }}<br/>
              <strong>Iniciado:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Estimativa de Conclusão:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Baseado em {{ word_count }} palavras)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O Que Acontece Depois:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. O serviço de tradução por IA processa seu conteúdo<br/>
          2. As traduções são salvas como rascunhos para revisão<br/>
          3. Você receberá um e-mail quando o trabalho estiver concluído<br/>
          4. Revise e publique as traduções no seu painel de administração
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Verificar Status do Trabalho
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Você pode fechar este e-mail. Nós o notificaremos quando a tradução estiver concluída.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 TRABALHO DE TRADUÇÃO INICIADO

Tradução em Lote em Andamento

Seu trabalho de tradução em lote foi iniciado e está sendo processado.

DETALHES DO TRABALHO:
- ID do Trabalho: {{ job_id }}
- Tipo de Conteúdo: {{ content_type }}
- Idioma de Origem: {{ source_language }}
- Idiomas de Destino: {{ target_languages }}
- Itens para Traduzir: {{ item_count }}
- Iniciado: {{ started_at }}

ESTIMATIVA DE CONCLUSÃO:
{{ estimated_completion }}
(Baseado em {{ word_count }} palavras)

O QUE ACONTECE DEPOIS:
1. O serviço de tradução por IA processa seu conteúdo
2. As traduções são salvas como rascunhos para revisão
3. Você receberá um e-mail quando o trabalho estiver concluído
4. Revise e publique as traduções no seu painel de administração

Verificar status do trabalho: {{ job_status_url }}

Você pode fechar este e-mail. Nós o notificaremos quando a tradução estiver concluída.