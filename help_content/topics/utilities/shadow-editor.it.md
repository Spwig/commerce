---
title: Editor delle ombre
---

L'editor delle ombre ti permette di aggiungere profondità e dimensione agli elementi utilizzando ombre di box e ombre di testo configurabili. Le ombre creano una gerarchia visiva, attirano l'attenzione sugli elementi importanti e danno al tuo negozio online un aspetto raffinato e moderno. Apri il **tab Stile** di qualsiasi elemento e cerca il gruppo **Effetti** per accedere all'editor delle ombre.

![Editor delle ombre](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Tipi di ombra

L'editor presenta due schede in alto:

- **Ombra di box** — Aggiunge un'ombra intorno all'intero bounding box dell'elemento. Utilizzala per carte, pulsanti, contenitori, immagini e sezioni.
- **Ombra di testo** — Aggiunge un'ombra solo dietro i caratteri del testo. Utilizzala per titoli o testo sovrapposto a immagini per migliorare la leggibilità.

Ogni scheda ha una configurazione indipendente. Puoi applicare sia un'ombra di box che un'ombra di testo allo stesso elemento se necessario.

## Proprietà delle ombre

Ogni livello di ombra è definito dalle seguenti proprietà:

| Proprietà | Descrizione | Intervallo |
|----------|-------------|-------|
| **Offset X** | Distanza orizzontale dell'ombra dall'elemento | -50px a 50px |
| **Offset Y** | Distanza verticale dell'ombra dall'elemento | -50px a 50px |
| **Raggio di sfocatura** | Indica quanto morbida o diffusa appare l'edge dell'ombra. Valori più elevati producono ombre più morbide. | 0px a 100px |
| **Raggio di espansione** | Espande o contrae la dimensione dell'ombra rispetto all'elemento (solo ombra di box) | -50px a 50px |
| **Colore** | Il colore dell'ombra, configurabile con il supporto completo dell'opacità tramite il selettore di colori | Qualsiasi colore con alpha |
| **Inserito** | Toggle per rendere l'ombra all'interno dell'elemento invece che all'esterno (solo ombra di box) | Su / Giù |

Modifica i valori utilizzando i cursori o digita direttamente i numeri precisi nei campi di input.

## Ombre multiple

Puoi sovrapporre più livelli di ombra su un singolo elemento per creare effetti di profondità complessi e realistici:

- Clicca sul pulsante **+** per aggiungere un nuovo livello di ombra
- Ogni livello appare come una riga nell'elenco delle ombre con i propri controlli
- Trascina i livelli per riordinarli — le ombre vengono visualizzate nell'ordine dell'elenco, con il primo livello in cima
- Attiva l'icona **occhio** su qualsiasi livello per nasconderlo temporaneamente senza eliminare la configurazione
- Clicca sull'icona **cestino** per rimuovere un livello

Combinare un'ombra stretta e scura con un'ombra ampia e morbida crea un effetto naturale di "sollevamento" che imita la profondità fisica.

## Preset delle ombre

I preset applicabili rapidamente ti permettono di aggiungere stili di ombre comuni con un singolo clic:

| Preset | Descrizione |
|--------|-------------|
| **Piccolo** | Ombra sottile e vicina per un leggero sollevamento (carte, input) |
| **Medio** | Profondità moderata per elementi interattivi (pulsanti, menu a discesa) |
| **Grande** | Ombra prominente per elementi galleggianti (modali, popovers) |
| **Morbid** | Ampia sfocatura con bassa opacità per un effetto di luce morbida e diffusa |
| **Netto** | Minima sfocatura con alta opacità per un bordo netto e definito |
| **Interno** | Ombra interna per un aspetto premuto o rientrato |

Dopo aver applicato un preset, puoi modificare singolarmente le proprietà per raffinare il risultato.

## Previsione corrente vs nuova

In fondo all'editor, due caselle di confronto mostrano l'**ombra corrente** (salvata) e l'**ombra nuova** (le tue modifiche in sospeso). Questa visione a confronto ti permette di valutare facilmente la differenza prima di confermare. Clicca su **Applica** per accettare, o clicca altrove per annullare le tue modifiche.

## Dove appare

L'editor delle ombre è disponibile nei seguenti luoghi:

- **Costruttore di pagine** — Tab Stile, gruppo Effetti su sezioni, contenitori, colonne e elementi singoli
- **Costruttore di header/footer** — Impostazioni delle ombre a livello di widget per elementi come loghi, barre di ricerca e elementi di navigazione

Qualsiasi elemento che supporta il gruppo di stile Effetti mostrerà i controlli dell'editor delle ombre.

## Consigli

- Utilizza ombre sottili (preset Piccolo o Morbid) per la maggior parte degli elementi — ombre pesanti possono rendere un design caotico.
- Combina un'ombra vicina e scura con un'ombra lontana e chiara per ottenere l'elevazione più naturale.
- Le ombre interne funzionano bene sui campi di input e sui contenitori per creare un effetto di pannello "profondo".
- Le ombre del testo dovrebbero essere minimali — un offset di 1px con una leggera sfocatura migliora la leggibilità sui background delle immagini senza sembrare datato.
- Testa le tue ombre su sfondi chiari e scuri se il tuo tema supporta un toggle per la modalità scura.
