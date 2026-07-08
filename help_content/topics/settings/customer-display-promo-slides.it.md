---
title: Promo Slide per Schermo del Cliente
---

Le slide promozionali vengono visualizzate sullo schermo rivolto ai clienti quando il terminale POS è inattivo (nessuna transazione attiva). Crea un carosello di immagini che mostrino promozioni stagionali, lanci di nuovi prodotti, politiche del negozio, eventi imminenti e vantaggi del programma fedeltà. Le slide possono essere mirate a specifici negozi o gruppi utilizzando l'assegnazione dello scope - attiva le promozioni per le festività solo nei negozi statunitensi, o mostra informazioni sugli eventi locali solo nei luoghi rilevanti. Le slide attive si alternano automaticamente ogni 5-10 secondi, creando un'interessante segnaletica digitale che mantiene informati i clienti mentre aspettano.

Utilizza le slide promozionali per aumentare la consapevolezza sulle promozioni attuali, istruire i clienti sulle politiche e stimolare l'interazione con i programmi fedeltà ed eventi.

![Elenco Slide Promozionali](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Comportamento dello Schermo del Cliente

Quando un terminale POS è inattivo (nessun cliente al registratore, nessuna transazione in corso), lo schermo rivolto ai clienti mostra:

**Modalità Carosello**:
- Si passa automaticamente a tutte le slide attive
- Ogni slide viene visualizzata per 5-10 secondi (configurabile per terminale)
- Transizioni fluide tra le slide
- Il carosello si ripete continuamente fino all'avvio di una transazione

**Durante la Transazione**:
- Il carosello si ferma immediatamente
- Lo schermo passa alla vista della transazione (elementi, totale in corso, promemoria di pagamento)
- Il carosello riprende quando la transazione è completata e il terminale torna inattivo

**Nessuna Slide Configurata**:
- Lo schermo mostra un messaggio "Welcome" con la grafica del negozio
- Schermo statico (nessun carosello)

**Requisiti Tecnici**:
- Lo schermo per i clienti può essere un monitor separato o lo stesso schermo del cassiere (l'app POS supporta la modalità picture-in-picture)
- Lo schermo si sincronizza tramite l'API BroadcastChannel (comunicazione tra dispositivi nello stesso dispositivo) o WebSocket (dispositivi separati)

## Assegnazione dello Scope

Come per i modelli di ricevuta, le slide promozionali supportano l'assegnazione basata su scope (priorità più alta a priorità più bassa):

| Priorità | Scope | Esempio | Caso d'uso |
|----------|-------|---------|----------|
| **1** | Specifico del negozio | Slide del negozio di Parigi | Slide per l'evento del festival estivo a Parigi |
| **2** | Specifico del gruppo | Slide dei negozi europei | Slide per la politica sulla privacy GDPR solo per l'UE |
| **3** | Tutti i negozi | Slide globali | "Spedizione gratuita per ordini >$50" (promozione aziendale) |

**Come Funziona lo Scope**:
- Il terminale visualizza le slide che corrispondono allo scope del negozio (slide specifiche del negozio)
- Più le slide che corrispondono allo scope del gruppo (se il negozio è in un gruppo)
- Più le slide senza assegnazione dello scope (slide globali)
- Risultato: Un negozio può visualizzare 3-5 slide (misto di slide specifiche e globali)

**Esempio**:
- Slide globale: "Nuovo Programma Fedeltà - Unisciti Oggi!" (nessuno scope)
- Slide del gruppo: "Promozione Memorial Day - 30% di Sconto" (solo gruppo negozi USA)
- Slide del negozio: "Grand Opening - Flagship di NYC" (solo negozio NYC)

**Il terminale del negozio NYC** visualizza tutte e 3 le slide (negozio + gruppo + globale)
**Il terminale del negozio di Londra** visualizza solo la slide globale (non fa parte del gruppo negozi USA, non è un negozio NYC)

## Requisiti per le Immagini

Le slide promozionali sono immagini a schermo intero ottimizzate per i monitor dello schermo del cliente:

**Rapporto di Aspetto**: 16:9 (widescreen)

**Risoluzione Consigliata**: 1920×1080 pixel (Full HD)
- Si adatta facilmente alla maggior parte degli schermi moderni
- Bilanciamento della dimensione del file (qualità vs velocità di caricamento)

**Risoluzioni Accettate**:
- Minima: 1280×720 (HD)
- Ottimale: 1920×1080 (Full HD)
- Massima: 3840×2160 (4K) - non consigliato (file di grandi dimensioni, caricamento più lento)

**Formato del File**: JPG, PNG o WebP
- JPG per le fotografie
- PNG per grafiche con trasparenza (sebbene si raccomandi lo sfondo)
- WebP per il formato con dimensione del file più piccola

**Dimensione del File**: <500KB per slide
- File più grandi rallentano il caricamento del carosello
- Comprimi le immagini prima di caricarle (usa l'ottimizzazione della Libreria Media)

**Consigli per la Progettazione**:
- Alto contrasto per la leggibilità a distanza (clienti a 2-6 piedi di distanza dallo schermo)
- Testo grande (minimo 48pt per il testo principale, 72pt+ per gli headline)
- Font in grassetto (font sottili si perdono su alcuni schermi)
- Evita dettagli piccoli (non saranno visibili dalla prospettiva del cliente)
- Includi un call-to-action (cosa deve fare il cliente: "Chiedi al cassiere i dettagli", "Iscriviti oggi")

## Creare una Slide Promozionale

Naviga verso **POS > Slide Promozionali** e fai clic su **+ Aggiungi Slide Promozionale**:

![Form per Aggiungere Slide Promozionale](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Immagine** - Carica o seleziona dalla Libreria Media:
- Fai clic su **Esplora Libreria Media** per selezionare un'immagine esistente
- Oppure carica una nuova immagine che soddisfi i requisiti sopra
- L'anteprima mostra come l'immagine apparirà sullo schermo

**Titolo** (Opzionale) - Testo sovrapposto in alto sulla slide:
- Massimo 60 caratteri (testo più lungo viene troncato)
- Appare in una barra semitrasparente scura in alto nell'immagine
- Usa per il titolo della slide ("Vendita Estiva", "Nuovi Arrivi")
- Lascia vuoto se l'immagine include già il titolo

**Sottotitolo** (Opzionale) - Testo sovrapposto sotto il titolo:
- Massimo 120 caratteri
- Appare sotto il titolo nella stessa barra semitrasparente
- Usa per i dettagli di supporto ("Fino al 50% di sconto", "Regalo gratuito con l'acquisto")
- Lascia vuoto se l'immagine è autonoma

**È Attiva** - Interruttore per abilitare/disabilitare la slide:
- Solo le slide attive appaiono nel carosello
- Usa per l'attivazione stagionale (disattiva dopo la fine della promozione)
- Disattivare mantiene la slide per futuri riattivazioni

**Ordine di Sort** - Controlla la posizione della slide nel carosello:
- I numeri più bassi appaiono prima nella rotazione
- Usa multipli di 10: 10, 20, 30 (consente di inserire slide tra quelle esistenti)
- Esempio: Vendita di Natale (ordine di sort 10) appare prima del programma fedeltà generale (ordine di sort 20)

**Assegnazione dello Scope** (Opzionale):
- **Magazzino** - Seleziona per mostrare solo in un negozio specifico
- **Gruppo di Negozio** - Seleziona per mostrare solo nei negozi del gruppo
- **Lascia entrambi vuoti** - Mostra in tutti i negozi (slide globale)

## Ordine di Sort e Flusso del Carosello

**Esempio di Carosello** (terminale del negozio NYC):
- Slide 1 (ordine di sort 10): "Grand Opening - Flagship di NYC" (specifico del negozio)
- Slide 2 (ordine di sort 15): "Promozione Memorial Day - 30% di Sconto" (gruppo negozi USA)
- Slide 3 (ordine di sort 20): "Nuovo Programma Fedeltà - Unisciti Oggi!" (globale)
- Slide 4 (ordine di sort 30): "Seguici su @yourstore" (globale)

Il carosello si ripete: 1 → 2 → 3 → 4 → 1 → 2 → ...

**Terminale del negozio di Londra** (non fa parte del gruppo negozi USA, negozio diverso):
- Slide 1 (ordine di sort 20): "Nuovo Programma Fedeltà - Unisciti Oggi!" (globale)
- Slide 2 (ordine di sort 30): "Seguici su @yourstore" (globale)

Il carosello si ripete: 1 → 2 → 1 → 2 → ...

Utilizza l'ordine di sort per priorizzare il contenuto più importante per prima nella rotazione.

## Strategia di Attivazione Stagionale

**Problema**: Creare/eliminare slide per ogni promozione stagionale è noioso.

**Soluzione**: Crea le slide una volta, attivali/disattivali stagionalmente:

1. **Crea Slide per Eventi Principali**:
   - "Vendita Estiva" (È Attiva: No, creata in anticipo)
   - "Rientro a Scuola" (È Attiva: No, creata in anticipo)
   - "Black Friday" (È Attiva: No, creata in anticipo)
   - "Vendita di Natale" (È Attiva: No, creata in anticipo)

2. **Attiva Quando Rilevante**:
   - 1 giugno: Imposta "Vendita Estiva" → È Attiva: Sì
   - 15 agosto: Imposta "Vendita Estiva" → È Attiva: No, imposta "Rientro a Scuola" → È Attiva: Sì
   - 20 novembre: Imposta "Black Friday" → È Attiva: Sì
   - 1 dicembre: Imposta "Black Friday" → È Attiva: No, imposta "Vendita di Natale" → È Attiva: Sì

3. **Disattiva Dopo l'Evento**:
   - Mantiene la libreria delle slide organizzata
   - Riutilizza le slide anno su anno (aggiorna l'immagine se necessario, mantiene la configurazione)

## Esempi di Caso d'Uso

**Caso d'Uso 1: Promozione Stagionale**
- Immagine: Fondo rosso con testo bianco "VENDITA ESTIVA - FINO AL 60% DI SCONTO"
- Titolo: "Vendita Estiva"
- Sottotitolo: "Fino al 50-60% di sconto su selezionati articoli. Chiedi al cassiere i dettagli."
- Scope: Tutti i negozi (globale)
- Ordine di Sort: 10 (priorità più alta durante l'estate)
- Attiva: Solo giugno-agosto

**Caso d'Uso 2: Politica del Negozio**
- Immagine: Infografica che mostra i passaggi per la politica di reso
- Titolo: "Resi Facili"
- Sottotitolo: "30 giorni con ricevuta. Senza domande."
- Scope: Tutti i negozi (globale)
- Ordine di Sort: 40 (priorità inferiore rispetto alle promozioni)
- Attiva: Tutto l'anno

**Caso d'Uso 3: Lancio di Nuovi Prodotti**
- Immagine: Foto principale del nuovo prodotto
- Titolo: "NUOVO: Auricolari Wireless Pro"
- Sottotitolo: "Ora disponibile in negozio e online. $199,99"
- Scope: Tutti i negozi (globale)
- Ordine di Sort: 5 (priorità più alta durante la settimana del lancio)
- Attiva: Solo durante la settimana del lancio, quindi disattiva

**Caso d'Uso 4: Evento Locale**
- Immagine: Poster per una corsa benefica locale
- Titolo: "Supporta il Locale"
- Sottotitolo: "Unisciti a noi alla Community 5K il 15 giugno!"
- Scope: Negozio specifico (solo negozio NYC)
- Ordine di Sort: 8 (priorità per questo negozio)
- Attiva: 2 settimane prima dell'evento

**Caso d'Uso 5: Programma Fedeltà**
- Immagine: Visualizzazione della carta fedeltà con esempi di punti
- Titolo: "Guadagna Premi"
- Sottotitolo: "Unisciti al nostro programma fedeltà e guadagna 1 punto per ogni $1 speso"
- Scope: Tutti i negozi (globale)
- Ordine di Sort: 30 (contenuto evergreen)
- Attiva: Tutto l'anno

## Gestione delle Slide

**Visualizzazione dell'Elenco delle Slide**:
- Mostra tutte le slide con anteprima dell'immagine, titolo, scope, stato
- Filtra per attive/inattive
- Filtra per scope (visualizza tutte le slide globali, tutte le slide di gruppo, ecc.)

**Attivazione/Disattivazione in Blocco**:
- Seleziona più slide nell'elenco
- Usa l'azione amministrativa per attivare o disattivare tutte insieme
- Utile per le transizioni stagionali (disattiva tutte le slide estive, attiva tutte le slide autunnali)

**Test delle Slide**:
- Dopo aver creato o aggiornato una slide, naviga verso il terminale POS
- Lascia che il terminale vada inattivo (nessuna transazione)
- Verifica che la slide appaia nel carosello
- Controlla la qualità dell'immagine, la leggibilità del testo sovrapposto, il timing

**Aggiornamento delle Slide Attive**:
- I cambiamenti entrano in vigore al prossimo aggiornamento del carosello (di solito <30 secondi)
- Non è necessario riavviare i terminali

## Consigli

- **Progetta per la distanza** - I clienti visualizzano lo schermo da 2-6 piedi di distanza; utilizza testo grande e alto contrasto
- **Mantieni il messaggio semplice** - Le slide vengono visualizzate per <10 secondi; un messaggio chiaro per slide
- **Utilizza la disattivazione stagionale** - Crea una volta, attiva/spenga annualmente invece di ricrearle
- **Priorizza con l'ordine di sort** - Le promozioni più importanti dovrebbero avere l'ordine di sort più basso (apparire prima)
- **Testa su hardware reale** - La calibrazione del colore dello schermo varia; verifica che le slide appaiano bene sui tuoi monitor specifici
- **Limita il numero di slide attive** - 3-5 slide attive per negozio è ottimale; 10+ slide significa che ciascuna appare raramente
- **Includi CTAs** - Dillo ai clienti cosa fare ("Chiedi al cassiere", "Visita il sito web", "Scansiona il codice QR sulla ricevuta")
- **Aggiorna regolarmente** - Le promozioni obsolete (vendite scadute, eventi passati) riducono la fiducia dei clienti
- **Utilizza lo scope in modo strategico** - Le promozioni regionali (scope del gruppo) e gli eventi locali (scope del negozio) sembrano più rilevanti rispetto al contenuto globale costante

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.