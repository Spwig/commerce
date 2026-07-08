---
title: Editor dei bordi
---

L'Editor dei bordi fornisce un controllo dettagliato sui bordi degli elementi, incluso lo stile, il colore, la larghezza per lato e il raggio degli angoli per ogni angolo. Si apre come un pannello galleggiante con un'anteprima in tempo reale e due schede per le impostazioni di base e avanzate.

![Editor dei bordi](/static/core/admin/img/help/border-editor/border-editor.webp)

## Anteprima in tempo reale

Una casella di anteprima in alto nell'editor mostra i tuoi cambiamenti ai bordi in tempo reale. La casella visualizza la parola "Anteprima" all'interno di un rettangolo con bordo che si aggiorna immediatamente mentre regoli lo stile, il colore, la larghezza e i valori del raggio degli angoli.

## Modalità di base vs avanzata

L'editor è organizzato in due schede:

| Scheda | Cosa contiene |
|--------|---------------|
| **Base** | Stile del bordo, colore, larghezza (con controlli per lato), e raggio del bordo (con controlli per angolo) |
| **Avanzata** | Regolazione fine del raggio degli angoli singoli e la proprietà sperimentale Shape degli angoli |

La maggior parte del lavoro sui bordi viene eseguito interamente nella scheda Base. La scheda Avanzata è utile quando hai bisogno di un controllo preciso sugli angoli singoli o quando desideri sperimentare con nuove funzionalità CSS.

## Stile del bordo

Un menu a discesa con nove opzioni che controllano l'aspetto della linea del bordo:

| Stile | Descrizione |
|-------|-------------|
| **Nessuno** | Nessun bordo (rimuove qualsiasi bordo esistente) |
| **Solido** | Una singola linea continua (predefinito) |
| **Tratteggiato** | Una serie di brevi trattini |
| **Puntini** | Una serie di punti rotondi |
| **Doppio** | Due linee solide parallele |
| **Solco** | Un bordo inciso con effetto 3D che sembra premuto sulla superficie |
| **Rilievo** | Un bordo sollevato con effetto 3D (opposto a solco) |
| **Inserito** | Fa sembrare l'elemento incassato o premuto |
| **Sporgente** | Fa sembrare l'elemento sollevato o sporgente |

Impostare lo stile su Nessuno rimuove completamente il bordo, indipendentemente dalle impostazioni di larghezza o colore.

## Colore del bordo

Un campo di input testuale abbinato a un pulsante del Selettore di colori. Inserisci un valore esadecimale direttamente (es. `#3b82f6`) o fai clic sul campione di colore per aprire il Selettore di colori completo con modi di input esadecimale, RGB e HSL più un'area visiva dei colori. Il colore predefinito è nero (`#000000`).

## Larghezza del bordo

Controlla lo spessore del bordo in pixel. La scheda Base mostra quattro input per lato individuali:

| Lato | Input |
|------|-------|
| **Superiore** | Input numerico, minimo 0 |
| **Destra** | Input numerico, minimo 0 |
| **Inferiore** | Input numerico, minimo 0 |
| **Sinistra** | Input numerico, minimo 0 |

Un **pulsante di commutazione collegato** (icona a catena) accanto all'etichetta controlla se tutti e quattro i lati sono collegati:

- **Collegati** (predefinito) — modificando qualsiasi valore aggiorna tutti e quattro i lati contemporaneamente
- **Non collegati** — ogni lato può avere una larghezza diversa, utile per effetti come un bordo solo in basso o bordi di accento a sinistra

## Raggio del bordo

Controlla la rotondità di ogni angolo. La scheda Base mostra quattro input per gli angoli:

| Angolo | Etichetta |
|--------|-------|
| **In alto a sinistra** | TL |
| **In alto a destra** | TR |
| **In basso a sinistra** | BL |
| **In basso a destra** | BR |

Un **pulsante di commutazione collegato** funziona allo stesso modo della larghezza del bordo:

- **Collegati** (predefinito) — tutti e quattro gli angoli condividono lo stesso valore di raggio
- **Non collegati** — ogni angolo può avere un raggio diverso

Valori di raggio comuni:

| Valore | Effetto |
|-------|--------|
| 0px | Angoli quadrati netti |
| 4-8px | Rounding sottile, adatto per schede e pulsanti |
| 12-16px | Rounding notevole, un aspetto moderno e morbido |
| 50% | Cerchio completo o forma a pillola (a seconda delle dimensioni dell'elemento) |

Il selettore delle unità supporta px, em, rem e % per i valori di larghezza e raggio.

## Forma degli angoli (Avanzato)

La scheda Avanzata include una proprietà sperimentale **Forma degli angoli**. Questa funzionalità CSS controlla se gli angoli arrotondati utilizzino la forma standard rotonda o una forma più angolare "scoop". Il supporto del browser è limitato, e l'editor visualizza un avviso di compatibilità quando il browser corrente non supporta questa proprietà.

## Azioni del piè di pagina

| Pulsante | Azione |
|--------|--------|
| **Annulla** | Ripristina tutti i valori allo stato in cui era l'editor quando è stato aperto |
| **Annulla** | Chiude l'editor senza applicare le modifiche |
| **Applica** | Salva le impostazioni del bordo e chiude l'editor |

## Dove appare

L'Editor dei bordi è disponibile in diversi costruttori:

- **Costruttore di pagine** — seleziona qualsiasi elemento, apri la scheda Stile e fai clic sulla sezione Bordo
- **Costruttore di intestazione/piede di pagina** — aggiungi bordi alle sezioni dell'intestazione, ai contenitori di navigazione e alle aree del piede di pagina
- **Costruttore del menu** — stila i bordi degli elementi del menu e dei contenitori a discesa

L'editor legge gli stili dei bordi correnti dall'elemento live sul canvas, quindi si apre sempre con i valori esistenti corretti.

## Consigli

- **Utilizza i bordi con moderazione** — bordi sottili di 1px in un grigio chiaro creano una separazione pulita tra le sezioni senza aggiungere peso visivo.
- **Combina raggio e ombra** — angoli arrotondati abbinati a un'ombra di box morbida (tramite l'Editor delle ombre) producono un effetto scheda raffinato.
- **Prova i bordi su un solo lato** — discollega i lati e imposta solo un bordo in basso o a sinistra per linee di accento, separatori di sezioni o indicatori di barra laterale.
- **Utilizza il raggio in percentuale per le pillole** — imposta tutti gli angoli su 50% su un pulsante o un badge per creare una forma a pillola che si adatta a qualsiasi dimensione del contenuto.
- **Controlla l'anteprima** — la casella di anteprima in tempo reale si aggiorna immediatamente, quindi sperimenta liberamente prima di applicare.
