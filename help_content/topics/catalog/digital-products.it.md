---
title: Prodotti digitali
---

I prodotti digitali ti permettono di vendere file scaricabili, licenze software e altri beni non fisici. Spwig supporta prodotti digitali autonomi, nonché prodotti ibridi che combinano consegna fisica e digitale.

![Fornitori di licenze](/static/core/admin/img/help/digital-products/license-providers.webp)

## Tipi di prodotti digitali

### Prodotto digitale autonomo

Imposta il **Tipo di prodotto** su **Prodotto digitale** per gli elementi che sono puramente digitali:
- Applicazioni software
- E-book e PDF
- File musicali e audio
- Opere d'arte digitali e modelli

### Prodotti ibridi

Qualsiasi tipo di prodotto può includere la consegna digitale verificando **È un prodotto digitale** sulla scheda Informazioni di base. Questo è utile per:
- **Prodotti digitali variabili** — Software con edizioni Basic/Pro/Enterprise
- **Prodotti digitali personalizzabili** — Asset digitali progettati su misura
- **Bundle fisico + digitale** — Un libro che include un download digitale

## Configurazione di un prodotto digitale

### Passaggio 1: Crea il prodotto

1. Vai a **Prodotti > Tutti i prodotti** e clicca su **+ Aggiungi prodotto**
2. Imposta **Tipo di prodotto** su **Prodotto digitale** (o verifica **È un prodotto digitale** su un altro tipo di prodotto)
3. Compila i dettagli del prodotto (nome, descrizione, prezzo)
4. Salva il prodotto

### Passaggio 2: Aggiungi file scaricabili

1. Vai alla scheda **Inventario** del prodotto
2. Nella sezione **File digitali**, carica i file che i clienti riceveranno dopo l'acquisto
3. Per ogni file, puoi impostare:
   - **Nome del file** — Nome visualizzato ai clienti
   - **Limite di download** — Numero massimo di volte in cui il file può essere scaricato (0 = illimitato)
   - **Giorni di scadenza** — Numero di giorni in cui il collegamento per il download rimane attivo

### Passaggio 3: Configura la consegna delle licenze (opzionale)

Se il tuo prodotto digitale richiede chiavi di licenza:

1. Vai a **Impostazioni > Gestione licenze**
2. Connetti un fornitore di licenze (vedi di seguito)
3. Nel modulo di modifica del prodotto, assegna il fornitore di licenze

## Fornitori di licenze

I fornitori di licenze sono servizi esterni che generano e gestiscono automaticamente le chiavi di licenza software quando un cliente acquista il tuo prodotto.

### Tipi di fornitori disponibili

| Fornitore | Descrizione |
|----------|-------------|
| **Spwig Server di licenze integrato** | Generazione semplice di chiavi di licenza integrata nella piattaforma |
| **Keygen.sh** | API di gestione completa delle licenze |
| **LicenseSpring** | Gestione delle licenze enterprise |
| **Cryptlex** | Licenze software con supporto offline |
| **API personalizzata** | Connetti qualsiasi sistema di licenze tramite API REST |

### Connessione a un fornitore di licenze

1. Vai a **Impostazioni > Gestione licenze**
2. Clicca su **Connetti fornitore**
3. Segui il wizard di configurazione:
   - **Passaggio 1** — Seleziona il tipo di fornitore
   - **Passaggio 2** — Configura le impostazioni generali
   - **Passaggio 3** — Inserisci le credenziali API
4. Testa la connessione per verificare che funzioni
5. Salva la configurazione

### Carta del fornitore

Ogni fornitore connesso mostra:
- **Etichette di stato** — Attivo/Inattivo e stato della connessione
- **Endpoint API** — L'URL del server configurato
- **Capacità di sincronizzazione** — Supporto per sincronizzazione Ordine, Attivazione e Disattivazione
- **Pulsanti d'azione** — Configura, Testa e Sincronizza ora

### Capacità di sincronizzazione

I fornitori di licenze possono sincronizzare su tre eventi:

- **Ordine** — Genera automaticamente una chiave di licenza quando un cliente completa l'acquisto
- **Attivazione** — Traccia quando un cliente attiva la sua licenza
- **Disattivazione** — Gestisci la disattivazione delle licenze per rimborsi o trasferimenti

## Esperienza del cliente

### Dopo l'acquisto

Quando un cliente acquista un prodotto digitale:

1. **Conferma dell'ordine** — Mostra che la consegna digitale è inclusa
2. **Consegna via email** — I collegamenti per il download e/o le chiavi di licenza vengono inviati automaticamente
3. **Pagina del profilo** — I clienti possono accedere ai loro download dal dashboard del loro account
4. **Pagina di download** — Collegamenti di download sicuri con scadenza temporale

### Sicurezza del download

I download dei file digitali sono protetti da:
- Token di download unici e temporanei
- Limiti di conteggio dei download facoltativi
- Date di scadenza dopo le quali i collegamenti diventano inattivi
- Requisito di accesso (per clienti registrati)

## Consigli

- Imposta limiti di download ragionevoli (3-5 download) per prevenire abusi ma permettere i ridownload.
- Utilizza giorni di scadenza che corrispondono al periodo di supporto (es. 365 giorni per un anno di accesso).
- Testa il flusso completo di acquisto con un ordine di test per assicurarti che i collegamenti per il download e le chiavi di licenza vengano consegnati correttamente.
- Per prodotti software, connetti un fornitore di licenze per automatizzare la generazione delle chiavi invece di gestirle manualmente.
- Utilizza la funzione prodotti ibridi quando vendi beni fisici che includono extra digitali (es. libro stampato + PDF).
