---
title: Gestione della chiave di licenza
---

La gestione delle chiavi di licenza ti permette di controllare come vengono generate, archiviate e consegnate alle chiavi di licenza software ai clienti quando acquistano prodotti digitali. Spwig supporta la generazione di chiavi integrate, pool di chiavi precaricate e integrazioni con servizi esterni di gestione delle licenze.

## Panoramica

Esistono tre modi per gestire le chiavi di licenza in Spwig:

| Metodo | Migliore per |
|--------|---------|
| **Template delle licenze** | Genera automaticamente chiavi uniche in un formato personalizzato al momento dell'acquisto |
| **Pool di licenze** | Genera in anticipo un lotto di chiavi per la distribuzione di massa |
| **Fornitori esterni** | Delega la generazione e la gestione delle chiavi a un servizio di terze parti come Keygen.sh |

Questi metodi possono essere combinati - ad esempio, un pool può utilizzare un template personalizzato per definire il formato della chiave e può sincronizzare opzionalmente le chiavi generate con un fornitore esterno.

## Template delle chiavi di licenza

Un template per le chiavi di licenza definisce il *formato* delle chiavi generate. I template utilizzano un modello con segnaposti che Spwig riempie al momento della generazione.

### Creare un template

1. Vai a **Catalogo > Template delle chiavi di licenza**
2. Clicca su **+ Aggiungi template delle chiavi di licenza**
3. Inserisci un **Nome** (es. `Licenza App Standard`)
4. Configura il **Modello** utilizzando segnaposti (vedi di seguito)
5. Imposta il **Prefisso** e il **Suffisso** se necessario (es. un prefisso di `MYAPP` aggiunge `MYAPP-` a ogni chiave)
6. Scegli il **Separatore** (predefinito: `-`)
7. Imposta l'**Insieme di caratteri** - i caratteri utilizzati per i segmenti casuali. Il predefinito esclude caratteri ambigui come `0` e `O`, `1` e `I`
8. Imposta **Lunghezza minima/massima** per la validazione
9. Clicca su **Salva**

### Segnaposti del modello

| Segnaposto | Descrizione | Output di esempio |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N caratteri casuali dall'insieme di caratteri | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | Controllo di somma a N cifre per la validazione | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | Il valore del prefisso del template | `MYAPP` |
| `{SUFFIX}` | Il valore del suffisso del template | `PRO` |
| `{ORDER_ID}` | Il numero dell'ordine | `10045` |
| `{PRODUCT_SKU}` | Il SKU del prodotto | `SOFTPRO` |
| `{DATE:FORMAT}` | Data formattata | `{DATE:YYMMDD}` → `260318` |

**Esempio di modello**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Questo genera chiavi come: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Anteprima delle chiavi

Dopo aver salvato un template, è disponibile un'azione **Genera chiave di esempio** nell'elenco dei template. Utilizza questa funzione per verificare che il tuo modello generi chiavi nel formato previsto prima di assegnare il template a un prodotto.

## Pool di licenze

Un pool di licenze è un lotto di chiavi generate in anticipo per un prodotto. I pool sono utili quando:
- Hai bisogno di chiavi per l'imballaggio fisico (scatole retail, carte stampate)
- Lavori con rivenditori che necessitano di lotti di chiavi
- Vuoi generare chiavi in anticipo invece che su richiesta

### Creare un pool di licenze

1. Vai a **Catalogo > Pool di licenze**
2. Clicca su **+ Aggiungi pool di licenze**
3. Compila i dettagli del pool:

| Campo | Descrizione |
|-------|-------------|
| **Nome** | Nome descrittivo (es. `Pack Retail Q1 2026`) |
| **Prodotto** | Il prodotto per cui sono destinate queste chiavi |
| **Template di licenza** | Modello per il formato della chiave (predefinito al modello del prodotto) |
| **Totale chiavi** | Quante chiavi generare |
| **Tipo di chiave** | Perpetua, abbonamento o prova |
| **Massime attivazioni** | Quante dispositivi ogni chiave può attivare |
| **Scade dopo giorni** | Giorni dopo l'attivazione iniziale prima che la licenza scada (lascia vuoto per nessuna scadenza) |
| **Scade il pool a** | Data dopo la quale le chiavi non utilizzate da questo pool diventano non valide |
| **Sincronizza con fornitore** | Opzionalmente sincronizza le chiavi generate con un fornitore esterno di licenze |

4. Clicca su **Salva** - Spwig inizia a generare le chiavi in background

### Stato del pool


| Stato | Significato |
|--------|---------|
| **Generazione in corso** | Le chiavi vengono create in background |
| **Pronto** | Tutte le chiavi sono state generate e sono disponibili per la distribuzione |
| **Esaurito** | Tutte le chiavi sono state assegnate agli ordini |
| **Scaduto** | La data di scadenza del pool è passata |

### Monitoraggio di un pool

L'elenco dei pool mostra quante chiavi sono state distribuite rispetto al totale delle chiavi generate. Apri un pool per visualizzare l'elenco completo delle chiavi e i loro singoli stati.

## Fornitori di licenze esterni

I fornitori esterni sono servizi di gestione delle licenze di terze parti che gestiscono la generazione delle chiavi e il tracciamento dell'attivazione. Quando un cliente completa un acquisto, Spwig comunica con il fornitore per generare e registrare la chiave.

### Fornitori supportati

| Fornitore | Tipo |
|----------|------|
| **Spwig Server di Licenze Integrato** | Integrato — non è richiesto un account esterno |
| **Keygen.sh** | API di gestione delle licenze basata su cloud |
| **LicenseSpring** | Gestione delle licenze enterprise |
| **Cryptlex** | Gestione delle licenze con supporto offline |
| **API Personalizzata** | Qualsiasi sistema di licenze basato su REST |

### Connessione a un fornitore

1. Vai a **Catalogo > Fornitori di Licenze**
2. Clicca su **+ Aggiungi Fornitore di Licenze**
3. Compila i dettagli del fornitore:

| Campo | Descrizione |
|-------|-------------|
| **Nome** | Etichetta per questa connessione (es. `Keygen Production`) |
| **Tipo di Fornitore** | Seleziona tra i fornitori supportati |
| **Endpoint API** | URL base dell'API del fornitore |
| **Chiave API** | Chiave di autenticazione per il fornitore |
| **Segreto API** | Se richiesto dal fornitore |

4. Configura il comportamento di sincronizzazione:
   - **Sincronizza all'Ordine** — Sincronizza automaticamente quando un cliente completa un acquisto
   - **Sincronizza all'Attivazione** — Segnala le attivazioni dei dispositivi al fornitore
   - **Sincronizza alla Disattivazione** — Segnala le disattivazioni (utile per trasferimenti di licenze e rimborsi)
   - **Sincronizzazione Bidirezionale** — Consenti al fornitore di aggiornare i record di Spwig tramite webhooks

5. Clicca su **Salva**, quindi clicca su **Test Connection** per verificare che le credenziali funzionino

### Stato della connessione

Ogni fornitore mostra uno dei tre stati di connessione:

| Stato | Significato |
|--------|---------|
| **Non Testato** | La connessione non è stata verificata ancora |
| **Connesso** | L'ultimo test è stato riuscito |
| **Errore** | Il test della connessione è fallito — controlla il messaggio di errore |

### Sincronizzazione delle licenze esistenti

Per spingere manualmente le chiavi di licenza esistenti a un fornitore (per l'impostazione iniziale o dopo una sincronizzazione fallita), utilizza l'azione **Sincronizza Ora** dall'elenco dei fornitori.

## Monitoraggio dell'attività di sincronizzazione

Vai a **Catalogo > Sincronizzazioni di Licenze Esterne** per visualizzare il registro di sincronizzazione. Ogni record mostra:
- La chiave di licenza che è stata sincronizzata
- Il fornitore a cui è stata inviata
- Direzione (Spwig → Fornitore o Fornitore → Spwig)
- Stato (In attesa, Riuscito, Fallito)
- Dettagli dell'errore per le sincronizzazioni fallite

Le sincronizzazioni fallite vengono riprovate automaticamente. Puoi anche forzare una riprova modificando il record e cancellando l'errore.

## Consigli

- Utilizza l'insieme di caratteri predefinito (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) per evitare caratteri ambigui che i clienti spesso leggono male — esclude `0`, `O`, `1` e `I`.
- Aggiungi un segmento `{CHECKSUM}` al tuo modello di pattern in modo che i clienti e il tuo team di supporto possano rilevare facilmente le chiavi sbagliate.
- Per prodotti ad alto volume, utilizza un pool invece della generazione su richiesta per garantire che le chiavi vengano consegnate immediatamente al momento del checkout.
- Imposta **Pool Scade A** per batch di chiavi stagionali o a tempo limitato in modo che le chiavi vecchie e non utilizzate vengano invalidate automaticamente.
- Testa sempre la connessione al fornitore dopo l'impostazione e dopo ogni modifica delle credenziali — una connessione rotta significa che i clienti non ricevono le loro chiavi.
- Se utilizzi una sincronizzazione bidirezionale, configura l'URL del webhook del tuo fornitore in modo che punti all'endpoint del webhook per le licenze del tuo negozio.