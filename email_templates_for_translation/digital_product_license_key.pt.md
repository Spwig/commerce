---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Sua Chave de Licença - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Sua Chave de Licença Está Pronta
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ customer_name }},
        </mj-text>
        <mj-text>
          Obrigado por sua compra de {{ product_name }}! Aqui está sua chave de licença para ativação.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          SUA CHAVE DE LICENÇA
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Clique para copiar ou anote-a com cuidado
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Detalhes da Licença:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Produto: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Versão: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Tipo de Licença: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Máximo de Ativações: {{ max_activations }} dispositivo(s)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Validade: Licença Vitalícia
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Válida até: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Como Ativar:
        </mj-text>
        <mj-text font-size="14px">
          1. Faça o download e instale o software
        </mj-text>
        <mj-text font-size="14px">
          2. Abra o aplicativo
        </mj-text>
        <mj-text font-size="14px">
          3. Insira sua chave de licença quando solicitado
        </mj-text>
        <mj-text font-size="14px">
          4. Clique em "Ativar" para concluir o processo
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Baixar Software
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Importante:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Mantenha este e-mail seguro - você precisará da chave de licença para reinstalação
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Não compartilhe sua chave de licença com outras pessoas
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Você pode desativar dispositivos no painel de controle da sua conta
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Precisa de ajuda com a ativação? Entre em contato com {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sua Chave de Licença Está Pronta

Olá {{ customer_name }},

Obrigado por sua compra de {{ product_name }}! Aqui está sua chave de licença para ativação.

SUAS CHAVE DE LICENÇA:
{{ license_key }}

Detalhes da Licença:
• Produto: {{ product_name }}
• Versão: {{ product_version }}
• Tipo de Licença: {{ license_type }}
• Máximo de Ativações: {{ max_activations }} dispositivo(s)
{% if is_lifetime %}• Validade: Licença Vitalícia{% else %}• Válida até: {{ expiration_date }}{% endif %}

Como Ativar:
1. Faça o download e instale o software
2. Abra o aplicativo
3. Insira sua chave de licença quando solicitado
4. Clique em "Ativar" para concluir o processo

{% if download_url %}Baixar Software: {{ download_url }}

{% endif %}IMPORTANTE:
• Mantenha este e-mail seguro - você precisará da chave de licença para reinstalação
• Não compartilhe sua chave de licença com outras pessoas
• Você pode desativar dispositivos no painel de controle da sua conta

Precisa de ajuda com a ativação? Entre em contato com {{ support_email }}