---
title: Impostazione di un prodotto personalizzabile
---

Questo documento ti guida attraverso il processo completo di impostazione di un prodotto personalizzabile, dall'aggiunta del prodotto alla configurazione delle superfici, dei prezzi e delle restrizioni di upload. Vengono utilizzati due esempi pratici: un **maglione personalizzato** (abbigliamento a più superfici) e un **poster personalizzato** (stampa su una singola superficie).

## Passaggio 1: Crea il prodotto

1. Vai a **Prodotti > Tutti i prodotti** e fai clic su **+ Aggiungi prodotto**
2. Imposta **Tipo di prodotto** su **Prodotto personalizzabile**
3. Inserisci il nome del prodotto, la descrizione, le immagini e i prezzi come faresti per qualsiasi prodotto
4. Salva il prodotto

Dopo aver salvato, compare un nuovo pulsante **Apri editor di disegno** sulla form del prodotto. Questo ti porta alla pagina dedicata per l'impostazione, dove puoi configurare l'editor di disegno visivo.

## Passaggio 2: Accedi all'impostazione dell'editor di disegno

1. Apri il prodotto appena creato nell'amministrazione
2. Fai clic sul pulsante **Apri editor di disegno** (nella sezione Prodotto personalizzabile)
3. La pagina di impostazione si apre con tre schede: **Superfici**, **Impostazioni** e **Prezzi**

La pagina di impostazione è dove definisci tutto riguardo all'editor di disegno per questo prodotto.

## Passaggio 3: Aggiungi superfici di disegno

Una superficie rappresenta una singola faccia personalizzabile del tuo prodotto. Fai clic su **+ Aggiungi superficie** per creare ogni superficie.

### Esempio di maglione: 3 superfici

| Superficie | Nome | Dimensioni | Zona di disegno | Note |
|-----------|------|-----------|----------------|------|
| 1 | Fronte | 300 x 400 mm | Area centrale del petto | Area principale di disegno |
| 2 | Retro | 300 x 400 mm | Area superiore della schiena | Area secondaria di disegno |
| 3 | Manica sinistra | 100 x 100 mm | Area superiore del braccio | Solo area per logo piccolo |

### Esempio di poster: 1 superficie

| Superficie | Nome | Dimensioni | Zona di disegno | Note |
|-----------|------|-----------|----------------|------|
| 1 | Fronte | 210 x 297 mm (A4) | Area stampabile completa | Singola superficie, alta risoluzione |

### Configurazione di ogni superficie

Per ogni superficie, configura quanto segue:

**Informazioni di base:**
- **Nome** — Cosa i clienti vedranno nelle schede delle superfici (es. "Fronte", "Retro")
- **Slug** — Identificatore sicuro per URL, generato automaticamente dal nome
- **Ordine di ordinamento** — Controlla l'ordine in cui le superfici vengono visualizzate (i numeri più bassi vengono visualizzati per primi)

**Immagine del mockup:**
- Fai clic sull'area dell'immagine del mockup per aprire la Libreria Media e selezionare una foto del prodotto che mostra questa superficie
- Utilizza una foto di alta qualità del tuo prodotto dall'angolazione corretta

**Posizionamento della zona di disegno:**
- Dopo aver selezionato un'immagine del mockup, compare un sovrapposizione rettangolare sul riquadro di anteprima
- **Trascina** la sovrapposizione per posizionarla dove la zona di disegno dovrebbe essere sull'immagine del mockup
- **Ridimensiona** la sovrapposizione trascinando i bordi per definire i limiti dell'area di disegno
- La zona viene memorizzata come coordinate basate su percentuale, quindi si adatta a qualsiasi dimensione dello schermo

La zona di disegno informa l'editor esattamente dove sull'immagine del prodotto il disegno del cliente apparirà. Posizionala con attenzione per corrispondere all'area effettivamente stampabile del tuo prodotto.

**Dimensioni fisiche:**
- **Larghezza** e **Altezza** — Le dimensioni reali dell'area di disegno
- **Unità** — Millimetri, pollici o pixel
- Queste dimensioni determinano il rapporto di aspetto del canvas di disegno e vengono utilizzate per calcolare la risoluzione di stampa DPI

**Impostazioni di stampa:**
- **DPI minimo** — Il valore minimo accettabile di punti per pollice. I clienti vedranno un avviso se le immagini caricate sono al di sotto di questo valore. Predefinito: 150
- **DPI consigliato** — La risoluzione ideale per la migliore qualità di stampa. Predefinito: 300
- **Bleed (mm)** — Margine aggiuntivo fuori dall'area di disegno per la stampa bleed. Imposta a 0 se non è necessario (comune per l'abbigliamento), o 3 mm per prodotti di stampa professionale
- **Massimo numero di colori** — Per la stampa serigrafica, puoi limitare il numero di colori. Lascia vuoto per un numero illimitato (stampa digitale)
- **Colore di sfondo** — Colore predefinito dello sfondo del canvas

### Impostazioni di stampa per maglione vs poster

| Impostazione | Maglione | Poster |
|-------------|--------|-------|
| DPI minimo | 150 | 200 |
| DPI consigliato | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Massimo numero di colori | 6 (serigrafia) | Vuoto (illimitato) |
| Colore di sfondo | Corrispondente al colore dell'abbigliamento | `#ffffff` (bianco) |

## Passo 4: Vincoli per superficie

Ogni superficie puo' sovrascrivere le impostazioni globali. Questo permette di abilitare strumenti diversi su superfici diverse.

Le opzioni di vincolo sono:

| Impostazione | Opzioni | Descrizione |
|---------|---------|-------------|
| **Consenti Testo** | Eredita / Si / No | Se i clienti possono aggiungere testo su questa superficie |
| **Consenti Caricamento Immagine** | Eredita / Si / No | Se i clienti possono caricare immagini su questa superficie |
| **Consenti Clipart** | Eredita / Si / No | Se i clienti possono usare clipart su questa superficie |
| **Max Elementi** | Numero o vuoto | Numero massimo di elementi di design consentiti su questa superficie |

Quando impostato su **Eredita**, la superficie utilizza le configurazioni definite nelle impostazioni globali (Passo 6). Quando impostato su **Si** o **No**, sovrascrive l'impostazione globale per questa superficie specifica.

### Esempio: Vincolo per manica di maglietta

Per la superficie della manica di una maglietta, potresti voler limitare la personalizzazione solo a un piccolo logo:

| Impostazione | Valore | Motivo |
|---------|-------|--------|
| Consenti Testo | No | Troppo piccolo per testo leggibile |
| Consenti Caricamento Immagine | Si | Consente il caricamento di un piccolo logo |
| Consenti Clipart | No | Mantieni semplice |
| Max Elementi | 1 | Solo un logo |

Le superfici davanti e dietro rimarranno impostate su **Eredita**, permettendo tutti gli strumenti come definito nelle impostazioni globali.

### Esempio: Vincolo per poster

Per un poster, di solito tutte le superfici ereditano dalle impostazioni globali poiché c'e' una sola superficie e tutti gli strumenti dovrebbero essere disponibili. Non sono necessarie sovrascritture per superficie.

## Passo 5: Configura restrizioni di caricamento

Nella scheda **Impostazioni**, configura come i clienti possono caricare file:

| Impostazione | Descrizione | Esempio maglietta | Esempio poster |
|---------|-------------|-----------------|----------------|
| **Dimensione Massima Caricamento** | Dimensione massima del file per caricamento | 10 MB | 20 MB |
| **Max Caricamenti per Superficie** | Quanti immagini per superficie | 5 | 3 |
| **Tipi di Caricamento Consentiti** | Formati di file accettati | JPG, PNG, WebP | JPG, PNG, WebP |

E' consigliabile impostare limiti di dimensioni dei file piu' grandi per prodotti da stampare dove i clienti devono caricare immagini ad alta risoluzione.

## Passo 6: Impostazioni dell'editor

Nella scheda **Impostazioni**, configura il comportamento globale dell'editor:

**Modalità Editor:**
- **Editor Canvas** — Editor visivo completo con anteprima in tempo reale del canvas. Consigliato per la maggior parte dei prodotti.
- **Form Semplificato** — Campi tradizionali del form per personalizzazioni di base (es. testo inciso solo)

**Interruttori di funzionalità (impostazioni globali predefinite):**
- **Consenti Testo** — Permetti ai clienti di aggiungere elementi di testo
- **Consenti Caricamento Immagine** — Permetti ai clienti di caricare le proprie immagini
- **Consenti Clipart** — Permetti ai clienti di navigare e usare la tua libreria di clipart

Queste impostazioni globali si applicano a tutte le superfici a meno che non siano sovrascritte dai vincoli per superficie (Passo 4).

## Passo 7: Configura i prezzi

Nella scheda **Pricing**, imposta le tariffe di design che vengono aggiunte al prezzo base del prodotto:

| Tariffa | Descrizione |
|-----|-------------|
| **Tariffa Base di Design** | Tariffa fissa aggiunta quando viene applicata qualsiasi personalizzazione |
| **Tariffa per Superficie** | Tariffa aggiuntiva per ogni superficie utilizzata oltre la prima |
| **Tariffa per Caricamento** | Tariffa per ogni immagine caricata dal cliente |
| **Tariffa per Testo** | Tariffa per ogni elemento di testo aggiunto |

### Esempio: Tariffa per maglietta

| Tariffa | Importo | Motivo |
|-----|--------|-----------|
| Tariffa Base di Design | $5.00 | Copre i costi di configurazione per qualsiasi ordine personalizzato |
| Tariffa per Superficie | $2.00 | Ogni superficie aggiuntiva aggiunge costi di stampa |
| Tariffa per Caricamento | $1.00 | Le immagini personalizzate richiedono elaborazione |
| Tariffa per Testo | $0.50 | Il testo è piu' semplice da produrre rispetto alle immagini |

**Esempio di calcolo:** Un cliente progetta una maglietta con testo davanti e un logo dietro:
- Tariffa base di design: $5.00
- 1 superficie aggiuntiva (dietro): $2.00
- 1 logo caricato: $1.00
- 1 elemento di testo: $0.50
- **Totale tariffa di design: $8.50** (aggiunto al prezzo base del prodotto)

### Esempio: Tariffa per poster


| Tariffa | Importo | Motivazione |
|-----|--------|-----------|
| Tariffa di base per la progettazione | $0.00 | Nessuna tariffa base — il prezzo del prodotto la copre |
| Tariffa per superficie | $0.00 | Singola superficie, non applicabile |
| Tariffa per caricamento | $2.00 | Elaborazione ad alta risoluzione |
| Tariffa per testo | $0.00 | Il testo è incluso nell'esperienza base |

**Esempio di calcolo:** Un cliente crea un poster con 2 foto caricate e 3 elementi di testo:
- Tariffa di base per la progettazione: $0.00
- 2 foto caricate: $4.00
- 3 elementi di testo: $0.00
- **Totale tariffa di progettazione: $4.00**

La tariffa di progettazione viene visualizzata in tempo reale ai clienti mentre aggiungono elementi, in modo che possano vedere l'impatto dei costi di ogni aggiunta prima di aggiungere al carrello.

## Confronto rapido delle impostazioni

| Aspetto | T-shirt personalizzata | Poster personalizzato |
|--------|---------------|---------------|
| Superfici | 3 (fronte, retro, manica) | 1 (fronte) |
| Immagini di anteprima | 3 foto del prodotto | 1 foto del prodotto |
| Posizionamento delle zone | Aree petto/dietro/braccio | Area stampabile completa |
| Dimensioni | 300x400mm, 100x100mm | 210x297mm (A4) |
| DPI minimo | 150 | 200 |
| Bleed | 0 mm | 3 mm |
| Massimo colori | 6 | Illimitati |
| Vincoli per superficie | Manica limitata | Nessun vincolo necessario |
| Modello di prezzo | Base + superficie + caricamento + testo | Solo tariffe per caricamento |

## Consigli

- Sempre testare l'editor di progettazione dal punto di vista del cliente dopo aver completato l'impostazione. Visitare la pagina del prodotto nel negozio online e provare ad aggiungere del testo, caricare un'immagine e passare alle superfici.
- Caricare immagini di anteprima che si avvicinano molto all'aspetto reale del prodotto. Per le t-shirt, fotografare ogni angolo separatamente. Per i poster, utilizzare una foto pulita a piatto o un'immagine di anteprima con un telaio.
- Posizionare la zona di progettazione in modo conservativo — è meglio definire una zona leggermente più piccola che permettere alle stampe di sporgere nei bordi o nelle cuciture.
- Impostare il DPI minimo in base al metodo di stampa: 150 per la stampa serigrafica, 200 per la stampa digitale standard, 300 per la stampa offset di alta qualità.
- Utilizzare un bleed di 3 mm per qualsiasi prodotto che verrà tagliato dopo la stampa (poster, biglietti da visita, volantini). Impostare il bleed su 0 per i prodotti in cui il design viene applicato su una superficie esistente (t-shirt, tazze, cover per smartphone).
- Iniziare con un prezzo semplice e adattarlo in base al feedback dei clienti. Molti commercianti iniziano con una sola tariffa base per la progettazione e aggiungono tariffe per elemento in seguito.