---
title: Selettore di colori
---

Il selettore di colori avanzato ti permette di scegliere i colori utilizzando diversi metodi di input e preset a tema. Si mostra in ogni luogo in cui viene utilizzata una proprietà di colore nel sistema — nel costruttore di pagine, nel costruttore di header/footer, nel costruttore di menu e nell'amministrazione del catalogo. Clicca su qualsiasi campione di colore o campo di input del colore per aprire il selettore.

![Selettore di colori](/static/core/admin/img/help/color-picker/color-picker.webp)

## Metodi di input del colore

Il selettore supporta diversi modi per definire un colore:

| Metodo | Descrizione | Esempio |
|--------|-------------|---------|
| **Hex** | Inserisci un codice esadecimale a 6 cifre direttamente | `#FF5733` |
| **RGB** | Regola i cursori Rosso, Verde e Blu (da 0 a 255 ciascuno) | `rgb(255, 87, 51)` |
| **HSL** | Imposta Tono (0-360), Saturazione (0-100%), e Luminosità (0-100%) | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB con un canale di trasparenza (alpha) | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL con un canale di trasparenza (alpha) | `hsla(14, 100%, 60%, 0.8)` |
| **Spectro visivo** | Clicca o trascina nell'area del colore per selezionare visivamente | Selezione con puntatore |

Puoi anche digitare un valore direttamente nell'input di testo in fondo al selettore.

## Selettore di formato

Un menu a discesa in alto nel selettore ti permette di passare tra i modi di output **HEX**, **RGB**, **RGBA**, **HSL** e **HSLA**. Quando passi da un formato all'altro, il colore corrente viene automaticamente convertito — non vengono persi i valori. Scegli il formato che meglio si adatta al tuo flusso di lavoro o ai requisiti del tuo sistema di design.

## Preset di colore

Sotto l'area del colore, una fila di campioni di colore accessibili rapidamente ti permette di selezionare con un clic un colore comune. Questi campioni sono **a tema**: si adattano automaticamente ai colori primari, secondari, accessori e neutri del tema attivo. Questo rende facile mantenere la coerenza con il tuo brand senza dover memorizzare i codici esadecimali.

Per applicare un preset, clicca sul campione. Il selettore si aggiorna immediatamente per mostrare il colore selezionato nell'area del colore e nei campi di input.

## Opacità / Alpha

Quando utilizzi il formato RGBA o HSLA, un cursore orizzontale **alpha** appare sotto l'area del colore. Trascinalo per impostare la trasparenza da 0% (completamente trasparente) a 100% (completamente opaco). Il valore di opacità è anche modificabile come input numerico accanto al cursore per un controllo preciso.

I colori semitrasparenti sono utili per sovrapposizioni, effetti su hover e elementi di design sovrapposti.

## Colore corrente vs. colore nuovo

In fondo al selettore, due caselle a lato mostrano il **colore corrente** applicato e il **nuovo** colore selezionato. Questo confronto ti permette di valutare il cambiamento prima di confermarlo. Clicca su **Applica** per accettare il nuovo colore, o clicca fuori dal selettore per annullare e mantenere il valore corrente.

## Dove appare

Il selettore di colori è un'utilità condivisa utilizzata in tutto l'amministratore:

- **Costruttore di pagine** — Colore del testo, colore di sfondo, colore del bordo e stati di hover nella scheda Stile
- **Costruttore di header/footer** — Colore del testo, colore di sfondo, colore degli icon, colore dei link dei widget
- **Costruttore di menu** — Colore dei link degli elementi del menu e colori degli stati di hover/attivo
- **Amministrazione del catalogo** — Colori dei badge dei prodotti e colori accessori delle categorie

Qualsiasi campo che accetta un valore di colore apre lo stesso selettore, quindi l'esperienza è coerente ovunque.

## Consigli

- Utilizza i campioni di colore predefiniti del tuo tema per mantenere la coerenza del brand su tutte le pagine e componenti.
- Passa al formato HSL quando devi creare varianti più chiare o più scure dello stesso tono — basta regolare il valore di Luminosità.
- Copia il codice esadecimale dall'input di testo per riutilizzare esattamente lo stesso colore in un altro campo o condividerlo con un designer.
- Utilizza RGBA con opacità ridotta per effetti di sovrapposizione sottili su immagini e sezioni principali.
- Il selettore ricorda i colori utilizzati di recente durante la sessione, quindi i colori personali utilizzati frequentemente rimangono accessibili.
- Se incollare un valore di colore in qualsiasi formato supportato nell'input esadecimale, il selettore lo riconoscerà e lo convertirà automaticamente.