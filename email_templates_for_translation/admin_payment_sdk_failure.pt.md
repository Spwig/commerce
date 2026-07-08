---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Problema com Fornecedor de Pagamento - SDK do {{ provider_name }} Falhou ao Carregar

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Problema com Fornecedor de Pagamento
        </mj-text>
        <mj-text>
          O SDK de pagamento do {{ provider_name }} falhou ao carregar para um cliente durante o checkout. Isso pode indicar uma interrupção de serviço com o fornecedor.
        </mj-text>
        <mj-text>
          <strong>Fornecedor:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Tipo de Erro:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Horário:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Contagem de Falhas (última hora):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Esta notificação está limitada a uma por fornecedor por hora. Se o problema persistir, verifique o painel do fornecedor ou entre em contato com o suporte deles.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Ver Configurações de Pagamento
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Problema com Fornecedor de Pagamento

O SDK de pagamento do {{ provider_name }} falhou ao carregar para um cliente durante o checkout. Isso pode indicar uma interrupção de serviço com o fornecedor.

Fornecedor: {{ provider_name }}
Tipo de Erro: {{ error_type }}
Horário: {{ timestamp }}
Contagem de Falhas (última hora): {{ failure_count }}

Esta notificação está limitada a uma por fornecedor por hora. Se o problema persistir, verifique o painel do fornecedor ou entre em contato com o suporte deles.

Ver configurações de pagamento: {{ admin_url }}