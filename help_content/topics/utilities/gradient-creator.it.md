---
title: Creatore di Gradienti
---

Il Creatore di Gradienti ti permette di creare transizioni di colore fluide per lo sfondo degli elementi. È accessibile tramite la scheda Gradienti dello sfondo editor e si apre come un pannello galleggiante con una barra visiva dei gradienti, controlli per i punti di colore e opzioni predefinite.

![Creatore di Gradienti](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Accesso al Creatore di Gradienti

1. Seleziona un elemento nel Page Builder o nell'Header/Footer Builder
2. Apri la scheda **Stile** nel pannello delle proprietà
3. Clicca sulla sezione **Sfondo** per aprire lo sfondo editor
4. Passa alla scheda **Gradienti**
5. Il pannello del Creatore di Gradienti si apre con un'anteprima in tempo reale e controlli per l'editing

## Anteprima in tempo reale

In alto nel pannello è presente un confronto a lato a lato:

| Scatola | Scopo |
|--------|-------|
| **Corrente** | Il gradiente esistente (o trasparente se non è stato impostato) |
| **Nuovo** | Aggiornamenti in tempo reale mentre apporti modifiche |

Una freccia tra le due scatole indica la direzione del cambiamento.

## Tipi di Gradienti

Sono disponibili tre tipi di gradienti, selezionabili tramite schede in alto nell'editor:

| Tipo | Descrizione | Controlli |
|------|-------------|----------|
| **Lineare** | Transizioni di colore lungo una linea retta | Regolatore dell'angolo (0-360 gradi) con pulsanti di direzione predefinita (su, diagonale, destra, giù, ecc.) |
| **Radiale** | Transizioni di colore che si irradiano da un punto centrale | Selettore di forma (cerchio o ellisse) e selezione della posizione (centro, alto, basso, angoli) |
| **Conico** | Transizioni di colore che ruotano intorno a un punto centrale | Regolatore dell'angolo iniziale (0-360 gradi) e selezione della posizione |

### Controlli sulla Direzione Lineare

Per i gradienti lineari, puoi impostare l'angolo in tre modi:
- **Regolatore dell'angolo** — trascina da 0 a 360 gradi
- **Campo di input dell'angolo** — digita un valore preciso in gradi
- **Pulsanti predefiniti** — clicca sugli iconi delle frecce per le direzioni comuni (verso l'alto, verso l'alto a destra, verso destra, verso il basso a destra, verso il basso, verso il basso a sinistra, verso sinistra, verso l'alto a sinistra)

## Punti di Colore

La barra del gradiente mostra i tuoi punti di colore correnti come marker trascinabili. Ogni punto definisce un colore in una posizione specifica lungo il gradiente.

**Aggiungere punti** — Clicca sul pulsante **+** nella sezione Punti di Colore per aggiungere un nuovo punto. Non c'è un limite fisso al numero di punti.

**Modificare i punti** — Ogni punto nell'elenco mostra:
- Un campione di colore che apre il Color Picker quando cliccato
- Un valore di posizione (0% a 100%) che puoi digitare o regolare
- Un controllo di opacità (0 a 1)
- Un pulsante di eliminazione per rimuovere il punto

**Riordinare** — Trascina i punti lungo la barra del gradiente per riposizionarli visivamente.

## Preset di Gradienti

Sono disponibili sei preset predefiniti per un punto di partenza rapido. Clicca su qualsiasi preset per applicarlo immediatamente:

| Preset | Colori | Angolo |
|--------|--------|-------|
| **Oceano** | Blu chiaro a blu | 120 gradi |
| **Sunset** | Arancio caldo a rosa corallo (3 punti) | 45 gradi |
| **Foreste** | Indaco a verde emerale | 135 gradi |
| **Mirtilli** | Rosso a blu viola | 90 gradi |
| **Fiamma** | Rosso a giallo dorato | 45 gradi |
| **Notte** | Grigio scuro a blu oceano | 180 gradi |

I preset sono punti di partenza. Dopo averne applicato uno, puoi modificare i colori, aggiungere o rimuovere punti e cambiare l'angolo per creare la tua versione personalizzata.

## Azioni del Footer

| Pulsante | Azione |
|--------|--------|
| **Cancella** | Rimuove completamente il gradiente, reimpostandolo su trasparente |
| **Applica** | Salva il gradiente e chiude l'editor |

Chiudere l'editor senza cliccare su Applica elimina le tue modifiche.

## Dove Viene Utilizzato

Il Creatore di Gradienti viene utilizzato in:

- **Page Builder** — tramite la scheda Gradienti dello sfondo editor su qualsiasi elemento
- **Header/Footer Builder** — per gli sfondi gradienti su sezioni header, barre di navigazione e aree footer

Lavora insieme allo sfondo editor, che offre anche opzioni per sfondi solidi, immagini e video.

## Consigli

- **Inizia con un preset** — applica un preset che sia vicino a ciò che desideri, quindi modifica i colori e l'angolo invece di costruire da zero.
- **Utilizza due o tre punti** — i gradienti semplici con due punti sembrano puliti e professionali. Più punti sono utili per effetti complessi, ma possono rapidamente diventare sopraffacenti.
- **Abbinare i colori del tuo brand** — utilizza il Color Picker per inserire valori esatti in formato esadecimale dal tuo palette di colori del brand per gradienti coerenti con il brand.
- **Testa con il contenuto** — i gradienti che sembrano impressionanti da soli possono ridurre la leggibilità del testo. Controlla sempre che il testo su sfondi gradienti abbia un contrasto sufficiente.
- **Prova i radiali per effetti spotlight** — i gradienti radiali funzionano bene per attirare l'attenzione su un'area centrale, ad esempio su un punto focale di una sezione hero.