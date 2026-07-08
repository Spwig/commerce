---
title: Editor degli Spazi
---

L'editor visivo degli spazi ti permette di configurare margini e padding utilizzando un diagramma del modello a scatola intuitivo. Un controllo preciso degli spazi garantisce layout coerenti e esperienze di lettura comode in tutta la tua vetrina online. Apri il **tab Stile** di qualsiasi elemento e cerca la sezione **Spazi** per accedere all'editor.

![Editor degli Spazi](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## Il Diagramma del Modello a Scatola

L'editor visualizza un modello a scatola con tre strati annidati:

- **Margine** (anello esterno, generalmente mostrato in arancione) — Lo spazio esterno al bordo dell'elemento, che lo separa dagli elementi vicini
- **Padding** (anello interno, generalmente mostrato in verde) — Lo spazio tra il bordo dell'elemento e il suo contenuto
- **Contenuto** (area centrale) — Il contenuto effettivo dell'elemento, ad esempio testo o un'immagine

Ogni lato del diagramma (alto, destro, basso, sinistro) ha un maniglione trascinabile e un input numerico. Trascina un maniglione verso l'esterno per aumentare il valore, o verso l'interno per diminuirlo. Puoi anche cliccare direttamente sul valore di un lato per digitare un numero preciso.

## I Tab di Margine e Padding

Due tab in alto nell'editor passano tra le visualizzazioni **Margine** e **Padding**. Quando è selezionato Margine, l'anello esterno è evidenziato e modificabile. Quando è selezionato Padding, l'anello interno è evidenziato e modificabile. L'anello non attivo rimane visibile per riferimento, ma è attenuato.

Entrambi i tab condividono gli stessi controlli e opzioni di unità, quindi il flusso di lavoro è identico per la configurazione di margini e padding.

## Controlli per Lato

Ogni lato ha un input di valore indipendente e un selettore di unità:

| Lato | Descrizione |
|------|-------------|
| **Alto** | Spazio sopra l'elemento (margine) o sopra il contenuto (padding) |
| **Destro** | Spazio a destra dell'elemento o del contenuto |
| **Basso** | Spazio sotto l'elemento o il contenuto |
| **Sinistro** | Spazio a sinistra dell'elemento o del contenuto |

Clicca sul valore di qualsiasi lato nel diagramma per selezionarlo, quindi digita un numero o usa le frecce su/giù per incrementare di 1. Tieni premuto Shift mentre premi le frecce per incrementare di 10.

## Unità

Il selettore delle unità accanto a ogni input di valore ti permette di scegliere l'unità di misura:

| Unità | Descrizione |
|------|-------------|
| **px** | Pixel. Dimensione fissa, coerente su tutti i dispositivi. Ideale per valori di spazio precisi e piccoli. |
| **em** | Relativo alla dimensione del font dell'elemento. Si adatta ai cambiamenti del testo. |
| **rem** | Relativo alla dimensione del font radice. Fornisce una scalabilità coerente su tutta la pagina. |
| **%** | Percentuale della larghezza dell'elemento padre. Utile per layout fluidi e risponsivi. |
| **auto** | Consente al browser di calcolare automaticamente il valore. Comunemente usato per il centrare orizzontalmente con i margini sinistro/destro. |

Scegli un'unità che corrisponda al tuo intento — usa `px` per spazi fissi, `rem` per spazi scalabili che rispettano i token tipografici del tema, e `%` per layout che devono adattarsi alla larghezza del contenitore.

## Collega i Lati

Un **icona di collegamento** al centro del diagramma attiva/disattiva la modalità collegata:

- **Collegato** (icona della catena connessa) — Cambiare il valore di qualsiasi lato aggiorna tutti e quattro i lati allo stesso valore. Utile per spazi uniformi.
- **Non collegato** (icona della catena rotta) — Ogni lato è controllato in modo indipendente. Usa questa opzione quando hai bisogno di valori diversi per alto/basso e sinistro/destro.

Clicca sull'icona di collegamento per passare tra i modi. Quando passi da non collegato a collegato, tutti e quattro i lati vengono impostati al valore del lato modificato di recente.

## Preset Veloci

Una riga di pulsanti di preset sotto il diagramma fornisce configurazioni degli spazi con un clic:

| Preset | Valori |
|--------|--------|
| **Nessuno** | 0 su tutti i lati |
| **Piccolo** | Spazi compatti adatti a layout stretti e elementi inline |
| **Medio** | Spazi equilibrati per un uso generale su card e sezioni |
| **Grande** | Spazi generosi per aree hero e sezioni ad alto impatto |
| **XL** | Spazi extra larghi per banner a tutta larghezza e sezioni principali della pagina |

I preset si applicano al tab attivo (Margine o Padding) e impostano tutti e quattro i lati contemporaneamente. Dopo aver applicato un preset, puoi regolare i singoli lati come necessario.

## Dove Appare

L'editor degli spazi è disponibile per ogni elemento che supporta lo spazio di layout:

- **Costruttore di Pagina** — Tab Stile, sezione Spazio su sezioni, contenitori, colonne e elementi singoli
- **Costruttore di Intestazione/Piede di Pagina** — Controlli di spazio per righe e widget per spazi orizzontali e verticali
- **Costruttore del Menu** — Padding degli elementi del menu e impostazioni del margine del contenitore

L'interfaccia editor è utilizzata in tutti i luoghi, garantendo un'esperienza coerente in tutti i costruttori.

## Consigli

- Usa valori di spazio coerenti in tutte le tue pagine — scegli 2-3 dimensioni standard e mantieniti per ottenere un layout pulito e professionale.
- Imposta il margine su **auto** a sinistra e destra per centrare orizzontalmente un elemento a larghezza fissa all'interno del suo elemento padre.
- Preferisci le unità `rem` per gli spazi se il tuo tema utilizza tipografia risponsiva, in modo che gli spazi si scalino proporzionalmente alla dimensione del testo.
- Usa la modalità collegata per impostare rapidamente un padding uniforme, quindi disattivala e raffina i singoli lati se il contenuto richiede uno spazio asimmetrico.
- Evita un eccessivo padding su dispositivi mobili — testa i tuoi spazi a larghezze di viewport strette per assicurarti che il contenuto non venga schiacciato o eccessivamente riempito.