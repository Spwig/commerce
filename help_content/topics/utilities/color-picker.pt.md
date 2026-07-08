---
title: Seletor de Cor
---

O seletor de cor avançado permite que você escolha cores usando vários métodos de entrada e presets conscientes de tema. Ele aparece em qualquer lugar onde uma propriedade de cor é usada em toda a plataforma — no construtor de páginas, construtor de cabeçalho/rodapé, construtor de menu e no administrador do catálogo. Clique em qualquer amostra de cor ou campo de entrada de cor para abrir o seletor.

![Seletor de Cor](/static/core/admin/img/help/color-picker/color-picker.webp)

## Métodos de Entrada de Cor

O seletor suporta várias formas de definir uma cor:

| Método | Descrição | Exemplo |
|--------|-------------|---------|
| **Hex** | Insira um código hex de 6 dígitos diretamente | `#FF5733` |
| **RGB** | Ajuste os sliders de Vermelho, Verde e Azul (0-255 cada um) | `rgb(255, 87, 51)` |
| **HSL** | Defina a tonalidade (0-360), saturação (0-100%) e luminosidade (0-100%) | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB com um canal de transparência alfa | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL com um canal de transparência alfa | `hsla(14, 100%, 60%, 0.8)` |
| **Espectro Visual** | Clique ou arraste na área do espectro de cor para selecionar visualmente | Seleção por clique e arrasto |

Você também pode digitar um valor diretamente no campo de texto no fundo do seletor.

## Seletor de Formato

Um menu suspenso no topo do seletor permite alternar entre os modos de saída **HEX**, **RGB**, **RGBA**, **HSL** e **HSLA**. Ao alternar os formatos, a cor atual é automaticamente convertida — nenhum valor é perdido. Escolha o formato que melhor se adapta ao seu fluxo de trabalho ou aos requisitos do seu sistema de design.

## Preset de Cores

Abaixo da área do espectro, uma linha de amostras de cor de acesso rápido fornece uma seleção de um clique para cores comuns. Essas amostras são **conscientes de tema**: elas refletem automaticamente as cores primárias, secundárias, de destaque e neutras do tema ativo. Isso torna fácil manter a consistência com sua marca sem memorizar códigos hex.

Para aplicar um preset, clique na amostra. O seletor é atualizado imediatamente para mostrar a cor selecionada no espectro e nos campos de entrada.

## Opacidade / Alfa

Ao usar o modo RGBA ou HSLA, um **slider de alfa** aparece horizontalmente abaixo do espectro. Arraste-o para definir a transparência de 0% (totalmente transparente) a 100% (totalmente opaco). O valor de opacidade também pode ser editado como uma entrada numérica ao lado do slider para controle preciso.

Cores semi-transparentes são úteis para overlays, efeitos de hover e elementos de design em camadas.

## Cor Atual vs. Nova Pré-visualização

No fundo do seletor, duas caixas lado a lado exibem a **cor atual** aplicada e a **nova** cor selecionada. Essa comparação permite que você avalie a mudança antes de confirmar. Clique em **Aplicar** para aceitar a nova cor, ou clique fora do seletor para cancelar e manter o valor atual.

## Onde Ele Aparece

O seletor de cor é uma utilidade compartilhada usada em toda a área de administração:

- **Construtor de Páginas** — Cor do texto, cor de fundo, cor de borda e estados de hover na guia Estilo
- **Construtor de Cabeçalho/Rodapé** — Cores de texto, fundo, ícone e link dos widgets
- **Construtor de Menu** — Cores de links de itens de menu e estados de hover/ativo
- **Admin do Catálogo** — Cores de selos de produto e cores de destaque de categoria

Qualquer campo que aceite um valor de cor abre o mesmo seletor, então a experiência é consistente em todos os lugares.

## Dicas

- Use as amostras de preset do seu tema para manter a consistência da marca em todas as páginas e componentes.
- Mude para o modo HSL quando precisar criar variantes mais claras ou mais escuras da mesma tonalidade — basta ajustar o valor de luminosidade.
- Copie o código hex do campo de texto para reutilizar exatamente a mesma cor em outro campo ou compartilhá-la com um designer.
- Use RGBA com opacidade reduzida para efeitos de overlay sutis em imagens e seções de destaque.
- O seletor lembra as cores recentemente usadas durante sua sessão, então as cores personalizadas usadas com frequência permanecem acessíveis.
- Se você colar um valor de cor em qualquer formato suportado no campo de entrada de hex, o seletor reconhecerá e converterá automaticamente.