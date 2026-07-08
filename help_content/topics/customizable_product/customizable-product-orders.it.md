---
title: Esecuzione di ordini di prodotti personalizzabili
---

Quando un cliente progetta un prodotto e piazza un ordine, il loro design viene bloccato e archiviato insieme all'ordine. Questa guida spiega come i design personalizzati passano attraverso il ciclo di vita degli ordini e come accedere ai file pronti per la stampa di cui hai bisogno per l'esecuzione.

## Ciclo di vita del design

Il design di un cliente passa attraverso diversi stadi, dalla creazione all'esecuzione:

### 1. Creazione del design

Il cliente utilizza l'editor visivo sul sito di vendita per creare il proprio design. Mentre lavorano, i loro progressi vengono salvati automaticamente nel browser. I clienti registrati possono anche salvare i design nel loro account per un successivo editing.

### 2. Bozza del design

Quando il cliente clicca su **Aggiungi al carrello**, lo stato corrente del design viene salvato come **bozza del design**. La bozza include:

- Lo stato completo del canvas per ogni superficie (posizioni degli elementi, contenuto del testo, immagini caricate, clipart, stili)
- Una suddivisione dei prezzi che mostra tutte le spese applicabili per il design
- Anteprime a miniature di ciascuna superficie

La bozza è collegata all'elemento del carrello tramite un token unico. Questo garantisce che il design esatto creato dal cliente venga conservato anche se proseguono con lo shopping prima di procedere al checkout.

**Scadenza della bozza:** Le bozze di design scadono automaticamente dopo 7 giorni se il cliente non completa l'ordine. Questo previene l'accumulo di design abbandonati.

### 3. Snapshot del design

Quando il cliente completa il checkout e l'ordine viene piazzato, la bozza del design viene convertita in uno **snapshot del design immutabile**. Questo è il registro permanente del design:

- Lo snapshot non può essere modificato dal cliente dopo l'acquisto
- Contiene esattamente gli stessi dati del design della bozza
- È permanentemente collegato all'elemento specifico dell'ordine

Questa immutabilità è importante — garantisce che ciò che il cliente ha ordinato sia esattamente ciò che produci e spedisci, senza alcuna possibilità di modifiche dopo il pagamento.

### 4. Rendering dei file per l'esecuzione

Dopo che l'ordine è stato piazzato, il sistema genera automaticamente **file ad alta risoluzione per l'esecuzione** per ciascuna superficie del design. Questi sono immagini composte che uniscono tutti gli elementi del design (testo, immagini, clipart) in un unico file pronto per la stampa a una risoluzione in DPI configurata per ciascuna superficie.

Il rendering avviene in modo asincrono in background. Per la maggior parte dei design, il rendering viene completato in pochi secondi. Lo stato **Renderso** dello snapshot indica se i file per l'esecuzione sono pronti.

## Accesso ai dati del design negli ordini

### Pagina dettagli ordine

Quando visualizzi un ordine che contiene prodotti personalizzabili nel pannello di amministrazione:

1. Naviga su **Ordini > Tutti gli ordini**
2. Apri l'ordine che contiene il prodotto personalizzato
3. L'elemento dell'ordine per il prodotto personalizzato mostra le informazioni sul design, tra cui anteprime delle superfici e un link allo snapshot del design

### Elenco degli snapshot del design

Puoi anche navigare direttamente tutti gli snapshot del design:

1. Naviga su **Prodotti personalizzabili > Snapshot del design**
2. L'elenco mostra tutti gli snapshot collegati agli elementi degli ordini
3. Clicca su uno snapshot per visualizzare i dati completi del design, le immagini renderizzate e i file per l'esecuzione

Ogni snapshot mostra:

| Campo | Descrizione |
|-------|-------------|
| **Elemento dell'ordine** | Link all'elemento dell'ordine associato |
| **Dati del design** | Lo stato completo del canvas (JSON) |
| **Immagini renderizzate** | Anteprime a miniature per superficie |
| **File per l'esecuzione** | File ad alta risoluzione composti per la stampa |
| **Renderizzato** | Se il rendering è completato |
| **Renderizzato il** | Timestamp in cui sono stati generati i file |

## Download dei file per l'esecuzione

I file per l'esecuzione sono quelli che invii al tuo fornitore di stampa o utilizzi nel tuo processo produttivo.

**Per un ordine di maglietta personalizzata:**
- Scarica il file della superficie **Frontale** (es. immagine PNG composta a 300 DPI)
- Scarica il file della superficie **Posteriore**
- Scarica il file della superficie **Manica** (se progettato)
- Invia tutti i file al tuo stampatore o al tuo stampatore DTG (direct-to-garment)



**Per un ordine personalizzato di poster:**
- Scarica il file della singola superficie **Front** a risoluzione di stampa
- Il file include l'area di bleed se è stata configurata per la superficie
- Invia al tuo stampatore di poster/cartelle

Ogni file è un'immagine composta unica che contiene tutti gli elementi del design uniti, renderizzati a DPI configurati per quella superficie.

## Design salvati

I clienti registrati possono salvare i loro design nell'account per un successivo editing. Come commerciante, puoi visualizzare questi design salvati in una lista in sola lettura:

1. Vai a **Customizable Products > Saved Designs**
2. L'elenco mostra tutti i design salvati dai clienti con il nome del cliente, il prodotto, il nome del design e la data

I design salvati sono:
- **Proprietà del cliente** — Appartengono all'account del cliente
- **In sola lettura per i commercianti** — Puoi visualizzarli ma non puoi modificarli
- **Separati dagli ordini** — Un design salvato diventa un ordine solo quando il cliente lo aggiunge al carrello e effettua il checkout
- **Riutilizzabili** — I clienti possono caricare un design salvato, modificarlo e ordinare più volte

## Flusso di esecuzione

### Flusso standard

1. **Ricevi l'ordine** — L'ordine appare nella tua lista degli ordini con gli articoli personalizzati
2. **Verifica la renderizzazione** — Controlla che lo snapshot del design mostri **Rendered: Yes**. Se la renderizzazione non è ancora completata, attendi alcuni minuti e aggiorna
3. **Scarica i file** — Scarica il file per l'esecuzione per ogni superficie progettata
4. **Controlla la qualità** — Apri i file e verifica che il design soddisfi gli standard di qualità di stampa (controlla DPI, posizionamento degli elementi e leggibilità del testo)
5. **Invia alla produzione** — Inoltra i file al tuo fornitore di stampa o al team di produzione
6. **Spedisci e completa** — Dopo la produzione, spedisci il prodotto e marca l'ordine come completato

### Esempio di esecuzione per magliette

1. Ordine ricevuto: "Custom Team T-shirt" con design sul fronte e sul retro
2. Apri l'ordine → visualizza lo snapshot del design
3. Scarica `front.png` (300 DPI, 300x400mm) e `back.png` (300 DPI, 300x400mm)
4. Invia entrambi i file al tuo stampatore DTG con il colore e la taglia dell'articolo selezionati nell'ordine
5. Dopo la stampa e il controllo di qualità, spedisci al cliente

### Esempio di esecuzione per poster

1. Ordine ricevuto: "Custom A4 Poster" con una singola superficie progettata
2. Apri l'ordine → visualizza lo snapshot del design
3. Scarica `front.png` (300 DPI, 210x297mm con 3mm di bleed)
4. Invia al tuo servizio di stampa per poster
5. Dopo la stampa e la tagliatura, spedisci al cliente

## Risoluzione dei problemi

**Problema:** Lo snapshot del design mostra "Rendered: No" e la renderizzazione non è completata

- **Causa:** Il compito di rendering in background potrebbe essere fallito o è ancora in elaborazione
- **Soluzione:** Aspetta alcuni minuti. Se la renderizzazione non si completa, controlla i log dei compiti in background. Puoi anche visualizzare i dati del design direttamente nello snapshot per confermare che il design del cliente sia preservato

**Problema:** Il file per l'esecuzione sembra di qualità inferiore rispetto all'atteso

- **Causa:** Il cliente potrebbe aver caricato immagini a risoluzione bassa
- **Soluzione:** Controlla le impostazioni DPI della superficie. Se sono state configurate avvisi per DPI minimo, il cliente sarebbe stato avvisato durante il processo di progettazione. Per futuri prodotti, considera di aumentare il requisito minimo di DPI

**Problema:** Il cliente richiede un cambiamento al design dopo l'ordine

- **Soluzione:** Gli snapshot del design sono immutabili per design. Se il cliente ha bisogno di modifiche, dovrebbe effettuare un nuovo ordine con il design aggiornato. Se accetti di fare un'eccezione, il cliente può utilizzare il design salvato (se ne ha uno) come punto di partenza per un nuovo ordine

## Consigli

- Verifica sempre che la renderizzazione sia completata prima di iniziare la produzione.

Controlla il campo **Rendered** nello snapshot del design.
- Mantieni le impostazioni DPI appropriate per il tuo metodo di stampa.

Un DPI più alto produce una qualità migliore ma con file più grandi. 300 DPI è lo standard per la maggior parte dei prodotti di stampa professionale.
- Incoraggia i clienti a salvare i loro design prima di ordinare.

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.


# Se si verifica un problema di produzione e l'ordine deve essere riconfezionato, il design salvato rende il riacquisto semplice.
- Inserisci un buffer nel tuo calendario di produzione per i prodotti personalizzabili.

A differenza dei prodotti standard, ogni articolo richiede un trattamento file individuale.
- Se gestisci elevate quantità di ordini personalizzabili, considera l'automazione del passaggio di download dei file integrando con l'API del tuo fornitore di stampa.