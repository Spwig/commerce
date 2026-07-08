---
title: Campos Personalizados
---

Campos personalizados permitem que você adicione dados extras a Produtos, Categorias, Pedidos e Perfis de Clientes sem modificar qualquer código. Use-os para armazenar informações específicas do seu negócio, como IDs de APIs externas, localizações de armazéns, dados de conformidade ou qualquer atributo que sua loja precise.

## Acessando Campos Personalizados

Navegue até **Configurações > Campos Personalizados** no menu lateral do administrador.

![Página de Campos Personalizados](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Conceitos Principais

### Grupos de Campo

Os campos são organizados em **grupos** — coleções lógicas que aparecem juntos como uma seção. Por exemplo, um grupo "Informações de Envio" pode conter campos para localização do armazém, dimensões do pacote e classificação de materiais perigosos.

### Definições de Campo

Cada definição de campo controla:
- **Nome**: O rótulo mostrado nos formulários
- **Slug**: A chave legível por máquina usada no armazenamento JSON e nas respostas da API
- **Tipo de Campo**: O tipo de entrada renderizado (texto, número, dropdown, etc.)
- **Validação**: Regras como min/max, comprimento máximo, expressão regular ou escolhas permitidas
- **Visibilidade**: Se o campo aparece na loja virtual

### Tipos de Campo Suportados

| Tipo | Descrição | Uso Exemplo |
|------|-------------|-------------|
| **Texto** | Entrada de texto em uma linha | ID da API externa, código da marca |
| **Área de Texto** | Texto em múltiplas linhas | Notas de tratamento especial |
| **Número** | Valores inteiros | Quantidade mínima de pedido |
| **Decimal** | Valores decimais | Sobrescrita de peso, dimensão personalizada |
| **Sim/Não** | Alternância de caixa de seleção | É frágil, requer assinatura |
| **Data** | Seletor de data | Data de lançamento, data de validade |
| **Data e Hora** | Seletor de data e hora | Disponibilidade agendada |
| **URL** | Endereço web | Link do fornecedor, URL da folha de especificações |
| **Email** | Endereço de e-mail | Contato do fabricante |
| **Dropdown** | Lista de seleção única | Tipo de material, país de origem |
| **Multi-seleção** | Lista de múltiplas seleções | Certificações, tags |
| **Cor** | Seletor de cor | Cor da marca, cor do rótulo |

## Gerenciando Campos Personalizados

### Criando um Grupo de Campo

1. Abra **Configurações > Campos Personalizados**
2. Selecione a guia do modelo (Produtos, Categorias, Pedidos ou Perfis de Clientes)
3. Clique em **Adicionar Grupo**
4. Insira um **Nome do Grupo** (ex: "Integrações Externas")
5. Ative opcionalmente **Mostrar na loja virtual** se os clientes devem ver esses campos
6. Clique em **Salvar Grupo**

### Adicionando um Campo a um Grupo

1. Na carta do grupo, clique em **Adicionar Campo**
2. Insira um **Nome do Campo** — o slug é gerado automaticamente
3. Escolha o **Tipo de Campo**
4. Defina opcionalmente um **Texto de Ajuda** e **Valor Padrão**
5. Configure as opções de validação (varia conforme o tipo de campo):
   - Texto: comprimento máximo, padrão de expressão regular
   - Número/Decimal: valores mínimos e máximos
   - Dropdown: defina a lista de escolhas
6. Defina as opções do campo:
   - **Obrigatório**: Os vendedores devem preencher este campo ao salvar
   - **Mostrar na loja virtual**: Exiba o valor na página voltada para o cliente
   - **Traduzível**: Permita que o valor seja traduzido (apenas texto/área de texto)
7. Clique em **Salvar Campo**

### Editando e Reordenando

- Clique no ícone de **caneta** em qualquer grupo ou campo para editá-lo
- Arraste o **manete** para reordenar grupos ou campos dentro de um grupo
- As alterações têm efeito imediatamente em todos os formulários relevantes

### Excluindo Grupos e Campos

- Clique no ícone de **lixo** em um grupo ou campo para excluí-lo
- As exclusões são **exclusões suaves** — os dados são preservados no banco de dados, mas ocultos dos formulários
- Isso protege os dados existentes contra perda acidental

## Usando Campos Personalizados em Formulários

Uma vez que você definiu campos personalizados para um modelo, uma **aba Campos Personalizados** aparece automaticamente na forma de edição correspondente.

### Produtos e Categorias

1. Abra qualquer produto ou categoria para edição
2. Clique na **aba Campos Personalizados**
3. Preencha os campos conforme necessário
4. Clique em **Salvar** — os valores são armazenados junto com o registro

### Pedidos

Valores de campos personalizados para pedidos são exibidos como uma **seção somente leitura** na página de detalhes do pedido. Campos personalizados de pedidos são normalmente definidos via a API ou no checkout.

### Perfis de Clientes

1. Abra um perfil de cliente
2. Clique na **aba Campos Personalizados**
3. Preencha os campos e salve

## Acesso à API

### Listando Definições de Campo

Recuperar todas as definições de campo personalizado para um modelo:

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Resposta:**
```json
[
  {
    "id": 1,
    "name": "External API ID",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "External Integrations" }
  }
]
```

### Lendo Valores de Campo Personalizado

Valores de campo personalizado são incluídos no objeto JSON `custom_fields` nas respostas da API do modelo:

```json
{
  "id": 42,
  "name": "Blue Widget",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Escrevendo Valores de Campo Personalizado

Inclua `custom_fields` ao criar ou atualizar um registro via a API:

```json
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

Os valores são validados contra as definições de campo. Valores inválidos retornam um erro `400` com detalhes.

### Consultando por Campos Personalizados

Campos personalizados são indexados para consultas rápidas no banco de dados. Filtrar registros usando filtros de consulta do banco de dados:

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Exibição na Loja Virtual

### Para Desenvolvedores de Temas

Use a tag de modelo `render_custom_fields` para exibir campos personalizados na loja virtual:

```python
{% load custom_fields_tags %}

{# Renderizar todos os campos visíveis na loja virtual #}
{% render_custom_fields product %}

{# Obter um valor de campo específico #}
{% get_custom_field product "warehouse_location" as location %}
<p>Envia de: {{ location }}</p>
```

Apenas campos com **Mostrar na loja virtual** habilitado tanto no nível do grupo quanto do campo serão renderizados.

## Boas Práticas

- **Use nomes descritivos** — os nomes dos campos aparecem nos formulários e na loja virtual
- **Defina texto de ajuda** — oriente os vendedores sobre o que inserir em cada campo
- **Agrupe campos relacionados** — mantenha os formulários organizados e intuitivos
- **Use valores padrão** — defina valores sensíveis para reduzir a entrada de dados
- **Seja seletivo com a visibilidade na loja virtual** — mostre apenas campos que sejam significativos para os clientes
- **Use slugs em integrações** — slugs são identificadores estáveis; os nomes dos campos podem mudar

## Solução de Problemas

**A aba Campos Personalizados não está aparecendo:**
- Verifique se pelo menos um grupo de campo ativo existe para esse modelo
- Confira se a classe de administração inclui o `CustomFieldsAdminMixin`
- Limpe o cache e atualize a página

**Valores de campo não estão sendo salvos:**
- Certifique-se de que os campos obrigatórios estão preenchidos
- Verifique as regras de validação (min/max, padrões de expressão regular, escolhas permitidas)
- Confirme se o campo está ativo e não foi excluído softmente

**API retornando custom_fields vazios:**
- Confirme se o modelo possui o `CustomFieldsMixin`
- Verifique se as definições de campo existem para o tipo de conteúdo correto
- Certifique-se de que o serializador inclui `CustomFieldsSerializerMixin`

## Tópicos Relacionados

- [Adicionando Produtos](#)
- [Configurações da Loja](#)