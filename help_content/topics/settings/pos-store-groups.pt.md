---
title: POS Store Groups
---

Grupos de lojas organizam múltiplas localizações de varejo com configurações compartilhadas. Em vez de configurar cada terminal individualmente, agrupe terminais por região, franquia ou tipo de localização e aplique configurações no nível do grupo. Os grupos suportam herança de configurações - moeda, idioma, fuso horário, modelos de recibos e conteúdo promocional se propagam do grupo para lojas individuais. Isso simplifica a gestão para comerciantes com múltiplas localizações, enquanto preserva a flexibilidade para substituições específicas de loja quando necessário.

Use grupos de lojas quando operar múltiplas localizações de varejo, franquias ou mercados regionais com requisitos operacionais diferentes.

![Lista de Grupos de Loja](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## O que são Grupos de Loja?

Grupos de loja são contêineres organizacionais para armazéns e terminais que compartilham características comuns:

**Estratégias de Agrupamento Comuns**:
- **Geográfico**: Região Norte, Região Sul, Costa Oeste, Costa Leste
- **Franquia**: Lojas do Franqueado A, Lojas do Franqueado B, Lojas Corporativas
- **Formato**: Localizações de Shopping, Lojas Independentes, Lojas Pop-up
- **Mercado**: Lojas Nacionais, Lojas Europeias, Lojas da Ásia-Pacífico

Os grupos não alteram a operação física dos terminais - eles fornecem uma camada de configuração que simplifica a gestão em larga escala.

## Quando Usar Grupos de Loja

**Uma Localização** - Não são necessários grupos. Configure os terminais diretamente.

**2-3 Localizações com Configurações Idênticas** - Grupos são opcionais. Pode ser mais fácil configurar os terminais diretamente.

**4+ Localizações** - Grupos fortemente recomendados. A configuração centralizada economiza tempo.

**Operações em Múltiplos Países** - Grupos essenciais. Diferentes moedas, idiomas e fusos horários exigem substituições no nível do grupo.

**Operações de Franquia** - Grupos críticos. Cada franqueado precisa de configurações independentes, enquanto mantém a consistência da marca.

## Hierarquia de Herança de Configurações

O Spwig POS usa uma cascata de 4 níveis de configurações (prioridade mais alta para mais baixa):

| Nível | Prioridade | Exemplo | Caso de Uso |
|-------|----------|---------|----------|
| **Terminal** | 1 (Mais Alta) | Terminal 5 redefine a largura do papel para 58mm | Um único terminal tem hardware de impressora único |
| **Loja** | 2 | Loja 2 redefine a moeda para GBP | Localização no Reino Unido entre lojas principalmente dos EUA |
| **Grupo** | 3 | Grupo Europeu define o fuso horário para CET | Consistência regional em múltiplas lojas |
| **Site** | 4 (Mais Baixa) | Padrão global: USD, Inglês, UTC | Padrão de fallback para todas as configurações não definidas |

**Como Funciona**:
- O sistema verifica primeiro as configurações do Terminal
- Se não definido, verifica as configurações da Loja
- Se não definido, verifica as configurações do Grupo
- Se não definido, usa os padrões do Site

**Exemplo**:
- Padrão do site: Moeda = USD, Idioma = Inglês
- Grupo "Lojas Europeias": Moeda = EUR, Idioma = não definido
- Loja "Loja de Paris": Moeda = não definido, Idioma = Francês
- Terminal "Caixa 1 de Paris": Moeda = não definido, Idioma = não definido

**Resultado para Caixa 1 de Paris**:
- Moeda: EUR (herdada do Grupo)
- Idioma: Francês (herdado da Loja)

Essa cascata permite padrões amplos com substituições cirúrgicas onde necessário.

## Criando um Grupo de Loja

Navegue até **POS > Grupos de Loja** e clique em **+ Adicionar Grupo de Loja**:

![Formulário de Adição de Grupo de Loja](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Configuração Básica

**Nome do Grupo** - Rótulo descritivo (ex.: "Lojas da Costa Oeste", "Franquias Europeias", "Localizações de Shopping")

**Código** - Identificador curto e único (ex.: "WEST", "EUR", "MALL"):
- Usado internamente para referências
- Deve ser único em todos os grupos
- 2-10 caracteres, alfanuméricos
- Maiúsculas recomendadas para consistência

**Ordem de Classificação** - Controla a ordem de exibição em listas do administrador (números mais baixos aparecem primeiro):
- Use múltiplos de 10: 10, 20, 30 (permite inserir novos grupos entre existentes)
- Ajuda a organizar grupos logicamente (ordem geográfica, ordem de tamanho, etc.)

### Substituições Regionais

**Substituição de Moeda** - Defina a moeda no nível do grupo diferente do padrão do site:
- Exemplo: Grupo europeu usa EUR, grupo da Ásia-Pacífico usa JPY
- Terminais nesse grupo usam essa moeda por padrão
- Afeta a exibição de preços, reconciliação de dinheiro, relatórios

**Substituição de Idioma** - Defina o idioma no nível do grupo diferente do padrão do site:
- Exemplo: Lojas francesas usam francês, lojas alemãs usam alemão
- Afeta o idioma da interface do POS, idioma dos recibos (se o modelo de recibo suportar)
- O pessoal vê a interface do POS nesse idioma ao fazer login em terminais do grupo

**Substituição de Fuso Horário** - Defina o fuso horário no nível do grupo diferente do padrão do site:
- Exemplo: Lojas da Costa Oeste usam America/Los_Angeles, lojas europeias usam Europe/Paris
- Afeta timestamps de turnos, programação de relatórios, programação de slides promocionais
- Garante que os relatórios de turnos estejam alinhados com os horários de funcionamento locais

**Quando Substituir**:
- **Moeda**: Substitua sempre para localizações internacionais (moedas de pagamento diferentes)
- **Idioma**: Substitua para mercados que não falam inglês (conteúdo voltado para o cliente)
- **Fuso Horário**: Substitua para localizações >2 horas do padrão do site (timestamps locais precisos)

## Associando Armazéns a Grupos

Depois de criar um grupo, associe armazéns a ele:

1. Navegue até **Catálogo > Armazéns**
2. Edite o armazém que representa uma localização de loja
3. Defina o campo **Grupo de Loja** para o grupo criado
4. Salve

Todos os terminais associados a esse armazém agora herdam as configurações do grupo.

**Configuração de Exemplo**:
- Crie grupo: "Lojas Europeias" (Moeda: EUR, Idioma: não definido, Fuso Horário: CET)
- Crie armazéns: "Loja de Paris", "Loja de Berlim", "Loja de Roma"
- Associe todos os 3 armazéns ao grupo "Lojas Europeias"
- Crie terminais: "Caixa 1 de Paris", "Caixa 1 de Berlim", "Caixa 1 de Roma"
- Cada terminal herda a moeda EUR e o fuso horário CET do grupo
- Substitua o idioma no nível da loja: Paris=Francês, Berlim=Alemão, Roma=Italiano

## Configurações Controladas por Grupos

Os grupos podem substituir essas configurações:

**Configurações Operacionais**:
- Moeda (afeta a exibição de preços e reconciliação de dinheiro)
- Idioma (afeta o idioma da interface do POS)
- Fuso Horário (afeta timestamps e programação)

**Configurações de Conteúdo** (via modelos com escopo):
- Modelos de recibo (crie designs de recibo específicos do grupo)
- Slides promocionais (direcione promoções a grupos específicos)

**Não Controladas por Grupos**:
- Configuração de hardware do terminal (configurada por terminal)
- Atribuição de funcionários (configurada por terminal)
- Níveis de estoque do armazém (configurados por armazém)
- Contas de provedores de pagamento (configuradas no site ou por provedor)

## Exemplos do Mundo Real

### Exemplo 1: Varejista de Moda Internacional

**Configuração**:
- 50 lojas em 5 países
- Cada país tem moeda, idioma e requisitos fiscais diferentes

**Estrutura de Grupo**:
- Grupo: "Lojas dos EUA" (USD, Inglês, America/New_York)
  - 20 armazéns (Nova York, Los Angeles, Chicago, etc.)
  - 60 terminais
- Grupo: "Lojas do Reino Unido" (GBP, Inglês, Europe/London)
  - 10 armazéns (Londres, Manchester, etc.)
  - 30 terminais
- Grupo: "Lojas da UE" (EUR, não definido, Europe/Paris)
  - 15 armazéns (Paris, Berlim, Roma, etc.)
  - 45 terminais
  - Idioma substituído no nível da loja (Paris=Francês, Berlim=Alemão, Roma=Italiano)
- Grupo: "Lojas do Japão" (JPY, Japonês, Asia/Tokyo)
  - 5 armazéns (Tóquio, Osaka, etc.)
  - 15 terminais

**Benefícios**:
- Uma configuração de grupo se aplica a todas as lojas em cada mercado
- Modelos de recibo com escopo para grupos (formato de IVA para UE, imposto de venda para EUA)
- Slides promocionais direcionados por região (EUA: Venda do Dia do Memorial, UE: Venda de Férias de Verão)

### Exemplo 2: Cadeia de Cafés

**Configuração**:
- 30 localizações, todas no mesmo país, mas diferentes formatos

**Estrutura de Grupo**:
- Grupo: "Localizações de Shopping" (não definido, não definido, não definido)
  - 10 lojas em shoppings
  - Slides promocionais com horários estendidos (abertos até as 21h)
  - Modelo de recibo com código QR de validação de estacionamento do shopping
- Grupo: "Lojas Independentes" (não definido, não definido, não definido)
  - 15 lojas de frente de rua
  - Slides promocionais com horários padrão
  - Modelo de recibo padrão
- Grupo: "Localizações de Aeroporto" (não definido, não definido, não definido)
  - 5 lojas de aeroporto
  - Slides promocionais com 24 horas
  - Modelo de recibo com integração de código QR de informações de voo

**Benefícios**:
- Conteúdo promocional diferente para diferentes formatos
- Personalizações de recibo específicas da localização
- Gestão simplificada (atualize um grupo em vez de atualizar 10 lojas individuais)

### Exemplo 3: Operação de Franquia

**Configuração**:
- 100 lojas, 20 diferentes franqueados

**Estrutura de Grupo**:
- Grupo: "Franqueado A" (não definido, não definido, não definido)
  - 10 lojas operadas pelo Franqueado A
  - Informações de contato do Franqueado A nos recibos (via modelo de recibo do grupo)
  - Conteúdo promocional do Franqueado A (eventos locais, ofertas)
- Grupo: "Franqueado B" (não definido, não definido, não definido)
  - 8 lojas operadas pelo Franqueado B
  - Informações de contato do Franqueado B nos recibos
  - Conteúdo promocional do Franqueado B
- (Repita para todos os franqueados)
- Grupo: "Lojas Corporativas" (não definido, não definido, não definido)
  - 5 lojas corporativas
  - Marca corporativa e promoções

**Benefícios**:
- Cada franqueado gerencia suas próprias configurações de grupo
- Consistência de marca mantida via padrões do site
- Independência do franqueado via substituições de grupo

## Gerenciando Configurações de Grupo

**Alterar Configurações de Grupo** afeta todos os terminais desse grupo:
- Alteração de moeda: Todos os terminais do grupo mudam para a nova moeda na próxima sincronização
- Alteração de idioma: Todos os terminais do grupo mudam para o novo idioma na próxima sincronização
- Alteração de fuso horário: Todos os terminais do grupo recalculam os timestamps na próxima sincronização

**Considerações sobre Impacto**:
- Teste alterações em um único terminal antes de aplicar a todo o grupo
- Informe aos funcionários sobre mudanças iminentes (ex.: troca de idioma)
- Agende alterações durante horários de baixa demanda para minimizar interrupções

**Remover um Grupo**:
- Reatribua todos os armazéns a um grupo diferente ou remova a atribuição do grupo
- Os terminais perdem as configurações do nível do grupo e recorrem aos padrões do site
- Não é possível excluir um grupo enquanto armazéns ainda estão atribuídos

## Dicas

- **Use códigos significativos** - "WEST" é mais claro que "GRP1" ao revisar configurações
- **Planeje a hierarquia antes de criar grupos** - Pense primeiro na estrutura organizacional; reestruturar depois é trabalhoso
- **Teste as configurações do grupo com um terminal** - Antes de atribuir 50 armazéns a um grupo, teste as configurações do grupo com um terminal
- **Use substituições no nível da loja com parcimônia** - Muitas substituições no nível da loja anulam o propósito dos grupos
- **Documente os propósitos dos grupos** - Anote no nome do grupo o que torna esse grupo distinto (geografia, formato, franqueado)
- **Use a ordem de classificação estrategicamente** - Ordene os grupos por importância (Lojas Corporativas primeiro) ou geografia (Oeste a Leste) para navegação mais fácil
- **Mantenha o número de grupos razoável** - 20+ grupos sugerem segmentação excessiva; considere consolidar
- **As substituições de moeda são permanentes** - Trocar a moeda de um grupo durante a operação complica a contabilidade; planeje com cuidado

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.