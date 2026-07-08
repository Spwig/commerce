---
title: Condivisione sociale
---

I pulsanti di condivisione sociale permettono ai clienti di condividere i tuoi prodotti, articoli del blog e pagine su reti sociali direttamente dal tuo negozio online. Controlli tu quali piattaforme vengono visualizzate, come appaiono i pulsanti, dove vengono posizionati e se l'attività di condivisione viene tracciata e contata.

## Configurazione delle impostazioni di condivisione sociale

Tutto il comportamento di condivisione sociale è controllato da una singola pagina delle impostazioni. Vai a **Marketing > Impostazioni di Condivisione Sociale** (la pagina si reindirizza automaticamente al modulo delle impostazioni — esiste un solo record di impostazioni).

### Posizione: dove appaiono i pulsanti

La sezione **Posizione** controlla quali tipi di contenuti mostrano automaticamente i pulsanti di condivisione.

| Impostazione | Descrizione |
|---------|-------------|
| **Abilita sui Prodotti** | Mostra i pulsanti di condivisione sulle pagine dei dettagli del prodotto |
| **Abilita sulle Categorie** | Mostra i pulsanti di condivisione sulle pagine dell'elenco delle categorie |
| **Abilita sugli Articoli del Blog** | Mostra i pulsanti di condivisione sulle pagine degli articoli del blog |
| **Abilita sulle Pagine Personalizzate** | Mostra i pulsanti di condivisione sulle pagine personalizzate del negozio |

Seleziona i tipi di contenuti in cui desideri che i pulsanti appaiano. Puoi abilitare qualsiasi combinazione — ad esempio, solo prodotti e articoli del blog.

**Posizione dei Pulsanti** controlla dove sui pulsanti vengono visualizzati:

| Opzione | Descrizione |
|--------|-------------|
| **Sotto il Contenuto** (predefinito) | Visualizzato dopo il contenuto principale |
| **Sopra il Contenuto** | Visualizzato prima del contenuto principale |
| **Barra laterale** | Visualizzato nella barra laterale della pagina |
| **Fluttuante (fissa)** | Rimane attaccata al lato dello schermo mentre l'utente scorre |

### Aspetto: come appaiono i pulsanti

La sezione **Aspetto** controlla quali piattaforme vengono mostrate e come vengono stileggiati i pulsanti.

**Piattaforme Abilitate** — lascia vuoto per mostrare tutte le piattaforme supportate, o inserisci un array JSON per limitare le piattaforme che vengono visualizzate:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Chiavi delle piattaforme supportate: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Stile del Pulsante** opzioni:

| Stile | Descrizione |
|-------|-------------|
| **Solo Icona** (predefinito) | Mostra solo l'icona della piattaforma |
| **Icona + Etichetta** | Mostra l'icona e il nome della piattaforma |
| **Solo Etichetta** | Mostra solo il nome della piattaforma come testo |

**Dimensione del Pulsante** — scegli **Piccola**, **Media** (predefinita) o **Grande** per adattarti al design del tuo negozio online.

**Direzione del Layout** — disponi i pulsanti **Orizzontalmente** (predefinito, uno accanto all'altro) o **Verticalmente** (sovrapposti).

**Mostra Titolo** — quando attivato, un'intestazione "Condividi" appare sopra il gruppo di pulsanti.

**Visibilità su Mobile** controlla la visualizzazione dei pulsanti su schermi piccoli:

| Opzione | Descrizione |
|--------|-------------|
| **Mostra sempre** (predefinito) | I pulsanti sono visibili su tutti i dispositivi |
| **Nascondi su Mobile** | I pulsanti sono nascosti sui dispositivi mobili |
| **Solo su Mobile** | I pulsanti vengono visualizzati solo sui dispositivi mobili |

### Impostazioni di tracciamento

**Mostra Contatori di Condivisione** — quando attivato, un badge con il conteggio appare su ogni pulsante, mostrando quante volte la piattaforma è stata condivisa. I contatori vengono aggiornati in tempo reale man mano che le condivisioni vengono registrate.

**Traccia le Condivisioni** — quando attivato, ogni clic di condivisione viene registrato nell'analisi delle condivisioni. Disattivarlo ferma la registrazione di nuovi dati ma non elimina i dati esistenti. Il tracciamento assegna anche badge di fedeltà ai clienti che condividono (se il programma di fedeltà è attivo).

Fai clic su **Salva** in fondo al modulo per applicare i tuoi cambiamenti. Le impostazioni entrano in vigore immediatamente.

## Visualizzazione dell'attività di condivisione

### Eventi di condivisione individuali

Vai a **Marketing > Condivisioni Sociali** per visualizzare un registro di ogni evento di condivisione registrato. Ogni voce mostra:

- **Piattaforma** — quale rete sociale è stata utilizzata (mostrata come un badge colorato)
- **Contenuto Condiviso** — il tipo e il nome del contenuto condiviso (es. `prodotto: Blue Widget`)
- **Utente** — il cliente che ha condiviso, o "Anonimo" per i visitatori non registrati
- **Tipo di Dispositivo** — desktop, mobile o tablet
- **Condiviso il** — data e ora della condivisione

Il registro delle condivisioni è in sola lettura — gli elementi vengono creati automaticamente quando i clienti cliccano sui pulsanti di condivisione.

Utilizza i filtri **Platform** e **Device Type** per esplorare i modelli di condivisione, e la gerarchia delle date per esaminare periodi temporali specifici.

### Condivisioni per contenuto

Vai a **Marketing > Share Counts** per visualizzare i totali aggregati delle condivisioni, raggruppati per elemento di contenuto e piattaforma. Questa vista rende facile identificare i prodotti e i post più condivisi.

Ogni voce mostra:
- **Content** — il tipo e il nome dell'elemento (es. `product: Blue Widget`)
- **Platform** — la rete sociale
- **Share Count** — totale delle condivisioni registrate su quella piattaforma
- **Last Updated** — quando il conteggio è stato ultimamente ricalcolato

L'elenco è ordinato in base al numero di condivisioni in ordine decrescente, quindi il contenuto più virale apparirà in cima. I conteggi delle condivisioni vengono aggiornati automaticamente ogni volta che viene registrato un nuovo evento di condivisione — non è necessario aggiornarli manualmente.

## Comprendere come vengono tracciate le condivisioni

Quando un cliente clicca su un pulsante di condivisione, Spwig registra:

1. Su quale piattaforma hanno condiviso
2. Qual è il contenuto condiviso (prodotto, post del blog, pagina, ecc.)
3. Se erano autenticati (se sì, la condivisione è collegata al loro account per l'integrazione con il programma fedeltà)
4. Il tipo di dispositivo
5. L'URL che è stato condiviso

Il conteggio delle condivisioni per quella piattaforma e elemento di contenuto viene incrementato automaticamente. Se **Show Share Counts** è abilitato, il conteggio aggiornato apparirà sul pulsante la prossima volta che la pagina viene caricata.

## Integrazione con il programma fedeltà

Se il programma fedeltà è attivo e **Track Shares** è abilitato, i clienti autenticati guadagnano badge fedeltà quando condividono contenuti. Il badge di condivisione sociale fa parte delle regole basate sull'azione del programma fedeltà.

Per configurare l'attribuzione di punti per le condivisioni, vai a **Customers > Loyalty Rules** e cerca le regole del tipo **Action-Based** con il tipo di azione **Social Share**.

## Consigli

- Abilita la condivisione su prodotti e post del blog prima — questi sono i tipi di contenuto più propensi a essere condivisi in modo organico
- Pinterest è particolarmente utile per categorie di prodotti visivi come moda, arredamento per la casa e cibo — prioritizza questa piattaforma nell'elenco `enabled_platforms` per quei negozi
- La condivisione tramite WhatsApp genera un forte tasso di conversione da riferimenti caldi, specialmente su dispositivi mobili; considera l'uso della modalità di visualizzazione **Mobile Only** per WhatsApp, mantenendo le altre piattaforme visibili su tutti i dispositivi
- Se noti che i conteggi delle condivisioni sono gonfiati, verifica se il traffico di test (da sessioni amministratore) è stato contato prima che la bandiera **Is Admin Traffic** fosse completamente funzionante — puoi resettare i conteggi cancellando gli elementi dall'analisi delle condivisioni
- Controlla mensilmente l'elenco Share Counts per identificare i prodotti più condivisi e mettili in evidenza maggiormente sulla homepage o nelle email di marketing