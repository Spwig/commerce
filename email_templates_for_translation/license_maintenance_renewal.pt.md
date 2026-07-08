---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Manutenção Renovada - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Manutenção Renovada!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Pedido #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ customer_name }},
        </mj-text>
        <mj-text>
          Sua assinatura de manutenção Spwig foi renovada com sucesso. Você continuará recebendo atualizações da plataforma, patches de segurança e novas funcionalidades.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Resumo da Renovação
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Chave de Licença: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Manutenção Válida Até: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Número do Pedido: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          O Que Está Incluído
        </mj-text>
        <mj-text font-size="14px">
          Sua manutenção ativa lhe dá acesso a:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Atualizações e melhorias de funcionalidades da plataforma
        </mj-text>
        <mj-text font-size="14px">
          - Patches de segurança e correções de bugs
        </mj-text>
        <mj-text font-size="14px">
          - Novas liberações de componentes via servidor de atualização
        </mj-text>
        <mj-text font-size="14px">
          - Suporte técnico
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Nenhuma ação é necessária por sua parte. As atualizações continuarão a estar disponíveis através do sistema de atualização de componentes do seu painel de administração.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Manutenção Renovada!

Pedido #{{ order_number }}

Olá {{ customer_name }},

Sua assinatura de manutenção Spwig foi renovada com sucesso. Você continuará recebendo atualizações da plataforma, patches de segurança e novas funcionalidades.

Resumo da Renovação:
- Chave de Licença: {{ license_key }}
- Manutenção Válida Até: {{ renewal_expires_at }}
- Número do Pedido: {{ order_number }}

O Que Está Incluído:
- Atualizações e melhorias de funcionalidades da plataforma
- Patches de segurança e correções de bugs
- Novas liberações de componentes via servidor de atualização
- Suporte técnico

Nenhuma ação é necessária por sua parte. As atualizações continuarão a estar disponíveis através do sistema de atualização de componentes do seu painel de administração.

Precisa de ajuda? Entre em contato com {{ support_email }}