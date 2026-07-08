---
title: Servizio di traduzione
---

Il servizio di traduzione fornisce traduzioni basate sull'intelligenza artificiale per le descrizioni dei prodotti, il contenuto delle pagine, gli articoli del blog, i campi SEO e altri contenuti del commerciante. Le traduzioni vengono eseguite localmente sul tuo server o tramite fornitori esterni, quindi il tuo contenuto rimane privato e le traduzioni avvengono in secondi.

![Gestione delle lingue](/static/core/admin/img/help/translation-service/language-management.webp)

## Come Funziona

1. Attiva le **lingue** per il tuo negozio (es. inglese, tedesco, giapponese)
2. Quando crei o modifichi contenuti (prodotti, pagine, articoli del blog), scrivi nella tua lingua predefinita
3. Fai clic su **Traduci** in qualsiasi campo traducibile per generare traduzioni basate sull'intelligenza artificiale nelle tue lingue attive
4. Le traduzioni vengono salvate insieme al contenuto originale e vengono servite automaticamente in base alla lingua del visitatore

## Gestione delle Lingue

Naviga verso **Impostazioni > Lingue** per gestire le lingue del tuo negozio.

### Dashboard delle Lingue

La dashboard mostra:
- **Totale Lingue** — Tutte le lingue disponibili nel sistema (100+)
- **Lingue Attive** — Lingue attualmente abilitate per il tuo negozio
- **Copertura del Modello** — Quante lingue il modello di traduzione installato supporta

### Attivazione delle Lingue

1. Trova la lingua nella colonna **Lingue Disponibili**
2. Fai clic sulla lingua per spostarla nella colonna **Lingue Attive**
3. La lingua è immediatamente disponibile per le traduzioni e apparirà nel selettore di lingue del tuo negozio

### Lingua Predefinita

Una lingua è contraddistinta come **predefinita**. Questa è:
- La lingua in cui scrivi i contenuti
- La lingua di fallback quando non esiste una traduzione
- La lingua visualizzata quando i visitatori non hanno selezionato una preferenza

## Modelli di Traduzione

Spwig include un motore di traduzione locale basato sull'intelligenza artificiale che funziona interamente sul tuo server — nessun dato viene inviato a servizi esterni.

### Modelli Disponibili

| Modello | Lingue | Velocità | Qualità |
|---------|--------|---------|--------|
| **M2M100-418M** | 100 | Veloce | Buona per le coppie di lingue comuni |
| **M2M100-1.2B** | 100 | Moderata | Qualità migliore, utilizzo delle risorse più elevato |
| **NLLB-200** | 200+ | Moderata | Migliore copertura, incluso le lingue rare |

### Selezione del Modello

La pagina di gestione delle lingue mostra quale modello è installato e la sua copertura linguistica. Il modello funziona come un servizio locale utilizzando CTranslate2 per un'inferenza efficiente.

## Fornitori Esterni

Per i negozi che preferiscono la traduzione basata sul cloud o necessitano di una qualità specifica per una lingua, Spwig supporta i fornitori esterni di traduzione.

| Fornitore | Descrizione |
|-----------|------------|
| **DeepL** | Qualità premium per le lingue europee e asiatiche |
| **Google Translate** | Ampia copertura linguistica con traduzione basata su macchina neurale |
| **Azure Translator** | Servizio di traduzione neurale di Microsoft |
| **AWS Translate** | Traduzione automatica di Amazon con supporto per terminologia personalizzata |

### Connessione a un Fornitore

1. Naviga verso **Impostazioni > Fornitori di Traduzione**
2. Seleziona il fornitore e inserisci la tua chiave API
3. Imposta il fornitore come motore di traduzione preferito
4. Le traduzioni utilizzeranno il fornitore esterno invece del modello locale

Puoi utilizzare fornitori esterni insieme al modello locale — ad esempio, usa DeepL per le lingue europee e il modello locale per tutto il resto.

## Traduzione del Contenuto

### Traduzione a Livello di Campo

I campi traducibili (nomi dei prodotti, descrizioni, titoli SEO, ecc.) mostrano un **pulsante di traduzione** accanto al campo. Fai clic per:

1. **Traduci in tutte le lingue attive** — Genera traduzioni per ogni lingua attiva contemporaneamente
2. **Traduci in una lingua specifica** — Seleziona singole lingue per la traduzione

Le traduzioni appaiono nelle schede delle lingue nell'editor. Puoi rivedere e modificare manualmente qualsiasi traduzione automatica.

### Lavori di Traduzione di Massa

Per grandi quantità di contenuti, utilizza **lavori di traduzione di massa**:

1. Naviga verso **Impostazioni > Lavori di Traduzione**
2. Crea un nuovo lavoro selezionando:
   - **Tipo di contenuto** — Prodotti, pagine, articoli del blog, categorie, ecc.
   - **Lingua di origine** — La lingua da cui tradurre
   - **Lingue di destinazione** — Una o più lingue in cui tradurre
   - **Ambito** — Tutti i contenuti, o solo i campi non tradotti
3. Invia il lavoro — viene eseguito in background tramite una coda di task
4. Monitora i progressi nell'elenco dei lavori (in coda → in elaborazione → completato)

I lavori di massa sono utili quando attivi una nuova lingua e desideri tradurre l'intero catalogo in una sola volta.

## Gestione delle Traduzioni

### Revisione delle Traduzioni

Ogni campo tradotto traccia:
- **Stato della traduzione** — Se il campo è stato tradotto automaticamente, modificato manualmente o mancante
- **Stato del blocco** — Le traduzioni bloccate non verranno sovrascritte da future traduzioni automatiche
- **Ultima traduzione** — Quando la traduzione è stata ultimamente generata o modificata

### Blocco delle Traduzioni

Se hai manualmente modificato una traduzione automatica per migliorarla, **blocca** il campo per impedire che venga sovrascritto la prossima volta che viene eseguita una traduzione di massa. I campi bloccati vengono saltati durante la traduzione automatica.

### Copertura delle Traduzioni

Il tracker della copertura mostra la percentuale di contenuti tradotti per ogni lingua. Naviga verso **Impostazioni > Lingue** per vedere:
- Percentuali di completamento per lingua
- Quali tipi di contenuti hanno lacune
- Campi che necessitano ancora di traduzione

## Sovrascritture delle Traduzioni dell'Interfaccia Utente

Oltre al contenuto dei prodotti e delle pagine, puoi personalizzare le traduzioni delle **stringhe dell'interfaccia frontend** — pulsanti, etichette, messaggi e altro testo dell'interfaccia utente mostrato ai visitatori.

Naviga verso **Impostazioni > Sovrascritture dell'Interfaccia Utente** per:
1. Cercare una stringa specifica (es. "Aggiungi al carrello")
2. Inserire la tua traduzione preferita per ogni lingua
3. Salva — la sovrascrittura entra in vigore immediatamente

Ci sono circa 300 stringhe frontend disponibili per la personalizzazione. Le sovrascritture hanno la precedenza rispetto alle traduzioni predefinite.

## Consigli

- Inizia attivando solo le lingue che i tuoi clienti utilizzano effettivamente — puoi sempre aggiungere di più in seguito.
- Utilizza il **modello AI locale** per le traduzioni quotidiane — è veloce, privato e non ha costi per traduzione.
- Considera **DeepL** se hai bisogno della massima qualità per le lingue europee principali — produce in modo costante traduzioni più naturali rispetto ai modelli generici.
- Controlla sempre le **traduzioni automatiche** per i nomi dei prodotti, i termini del brand e i testi promozionali — l'AI gestisce bene i contenuti tecnici ma potrebbe non cogliere le sfumature nei testi creativi.
- **Blocca** eventuali traduzioni che hai manualmente raffinate per proteggerle da essere sovrascritte durante i lavori di traduzione di massa.
- Utilizza **lavori di traduzione di massa** quando attivi una nuova lingua per tradurre l'intero catalogo in un'unica passata invece di tradurre i prodotti uno alla volta.
- Personalizza le **sovrascritture dell'interfaccia utente** per adattarle alla voce del tuo brand — ad esempio, cambia "Aggiungi al carrello" in "Acquista Ora" se questo si adatta meglio al tuo negozio.