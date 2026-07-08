---
title: Provedores de Frete
---

Os provedores de frete conectam a sua loja às APIs das transportadoras para obter tarifas de envio em tempo real, geração de etiquetas e rastreamento de encomendas.

![Provedores de frete](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Transportadoras Disponíveis

| Transportadora | Regiões | Funcionalidades Principais |
|----------------|---------|---------------------------|
| **FedEx** | Global | Tarifas em tempo real, impressão de etiquetas, rastreamento, multi-volumes |
| **UPS** | Global | Tarifas em tempo real, impressão de etiquetas, rastreamento, validação de endereço |
| **USPS** | Estados Unidos | Tarifas nacionais e internacionais, rastreamento |
| **NinjaVan** | Sudeste Asiático | Entrega de última milha, pagamento contra entrega |
| **Canada Post** | Canadá | Nacional e internacional, encomendas e cartas |
| **Australia Post** | Austrália | Nacional e internacional, encomendas e expresso |

## Conectar uma Transportadora

Assistente de 5 passos: Selecionar Provedor → Instruções de Configuração → Inserir Credenciais → Testar Conexão → Configurar e Guardar

## Zonas de Envio

Áreas geográficas para cálculo de tarifas:
- Países, Estados/Províncias, Padrões de Código Postal
- Correspondência baseada em prioridade

## Regras de Envio

| Tipo de Regra | Descrição |
|---------------|-----------|
| **Desconto %** | Reduzir a tarifa por percentagem |
| **Desconto Fixo** | Reduzir a tarifa por um valor fixo |
| **Definir Custo** | Substituir por um valor específico |
| **Frete Grátis** | Definir custo como zero |
| **Sobretaxa %** | Adicionar sobretaxa percentual |
| **Sobretaxa Fixa** | Adicionar sobretaxa fixa |

Condições: Valor do Carrinho, Peso, Quantidade de Itens, Zona, Método, Produtos, Grupo de Clientes, Intervalo de Datas

## Tabelas de Tarifas
Preços escalonados por peso, valor da encomenda ou quantidade.

## Embalagens de Envio
Tamanhos de embalagem padrão para cálculos de tarifas precisos.

## Transportadoras Manuais (Predefinições de Transportadora)
Para transportadoras sem API: nome, modelo de URL de rastreamento, prazo de entrega estimado, combinado com tabela de tarifas.

## Envio Multi-Armazém
- Armazéns específicos por país
- Cadeias de fallback
- Atribuição por produto

## Dicas
- Use tarifas em tempo real sempre que possível
- Crie uma zona "Resto do Mundo"
- Frete grátis como incentivo de vendas
- Teste os cálculos de tarifas
- Use Predefinições de Transportadora para transportadoras locais
- Defina Embalagens de Envio para peso dimensional
