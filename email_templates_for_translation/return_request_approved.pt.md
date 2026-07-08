---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Sua Devolução Foi Aprovada - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Devolução Aprovada
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Pedido #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sua solicitação de devolução para o pedido <strong>#{{ order_number }}</strong> foi aprovada.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Próximos passos:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Baixe e imprima o rótulo de devolução abaixo<br/>
          2. Empacote os itens de forma segura em seu embalagem original, se possível<br/>
          3. Coloque o rótulo de devolução no exterior do pacote<br/>
          4. Entregue no local de envio mais próximo
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Baixar Rótulo de Devolução
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Número de Rastreamento da Devolução:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Importante:</strong> Por favor, envie a devolução dentro de 7 dias para garantir o processamento rápido do seu reembolso.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Após recebermos e inspecionarmos sua devolução, processaremos seu reembolso para o método de pagamento original.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Devolução Aprovada - Pedido #{{ order_number }}

Olá {{ customer_name }},

Sua solicitação de devolução para o pedido #{{ order_number }} foi aprovada.

Próximos passos:
1. Baixe e imprima o rótulo de devolução
2. Empacote os itens de forma segura em seu embalagem original, se possível
3. Coloque o rótulo de devolução no exterior do pacote
4. Entregue no local de envio mais próximo

{% if return_label_url %}Baixe seu rótulo de devolução: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Número de Rastreamento da Devolução: {{ return_tracking_number }}{% endif %}

Importante: Por favor, envie a devolução dentro de 7 dias para garantir o processamento rápido do seu reembolso.

Após recebermos e inspecionarmos sua devolução, processaremos seu reembolso para o método de pagamento original.