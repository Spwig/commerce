---
title: Configurazione del fornitore SMS
---

Le notifiche SMS mantengono informati i clienti a ogni passo del loro ordine — dalla conferma fino alla consegna. Per inviare messaggi SMS o WhatsApp dal tuo negozio, collega un account di un fornitore SMS con le tue credenziali. Una volta collegato, Spwig utilizza quell'account per inviare tutti i messaggi di testo in uscita.

Naviga verso **Sistema SMS > Account dei fornitori SMS** per gestire i tuoi fornitori SMS.

![Elenco degli account dei fornitori SMS](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Aggiunta di un fornitore SMS

Puoi aggiungere un fornitore utilizzando il **Wizard di configurazione** (consigliato per la prima configurazione) o il modulo manuale.

### Utilizzo del wizard di configurazione

1. Naviga verso **Sistema SMS > Account dei fornitori SMS**
2. Clicca su **Wizard di configurazione** nella barra degli strumenti
3. Segui i passaggi guidati:
   - **Passo 1**: Scegli il tuo fornitore dall'elenco dei fornitori disponibili
   - **Passo 2**: Inserisci le tue credenziali del fornitore (chiavi API, SID account, ecc.)
   - **Passo 3**: Imposta il nome visualizzato e le impostazioni predefinite, quindi salva
4. Il wizard testa automaticamente la connessione prima di salvare

### Aggiunta di un fornitore manualmente

1. Naviga verso **Sistema SMS > Account dei fornitori SMS**
2. Clicca su **Esplora fornitori** per esplorare i fornitori SMS disponibili, o clicca direttamente su **+ Aggiungi account fornitore SMS**
3. Nel campo **Fornitore**, seleziona il tuo fornitore SMS dal menu a discesa
4. Dopo aver selezionato un fornitore, i campi delle credenziali appaiono automaticamente in base a ciò che richiede quel fornitore
5. Compila i campi delle credenziali richiesti (questi variano in base al fornitore — vedi le sezioni di seguito per i fornitori comuni)
6. Inserisci un **Nome visualizzato** per identificare questo account (es. `Twilio — Principale`)
7. Imposta le **Impostazioni predefinite** (vedi di seguito)
8. Clicca su **Salva**

## Credenziali del fornitore

### Twilio

| Campo | Dove trovarlo |
|-------|-----------------|
| Account SID | Console Twilio → Dashboard |
| Token di autenticazione | Console Twilio → Dashboard |
| Numero da | Il tuo numero di telefono Twilio nel formato E.164 (es. `+15551234567`) |

### Altri fornitori

Altri componenti dei fornitori SMS installati mostreranno i propri campi specifici delle credenziali quando selezionati. Riferirsi alla documentazione del fornitore per i valori esatti necessari — di solito una chiave API o un token di accesso e un identificatore mittente.

## Impostazioni predefinite

Dopo aver inserito le credenziali, configura come viene utilizzato questo account:

- **Attivo** — abilita o disabilita questo account. Gli account non attivi non vengono utilizzati per l'invio, anche se impostati come predefiniti
- **Account SMS predefinito** — quando selezionato, tutti i messaggi SMS dal tuo negozio utilizzano questo account. Solo un account può essere l'account SMS predefinito alla volta
- **Account WhatsApp predefinito** — se questo fornitore supporta WhatsApp (es. Twilio tramite WhatsApp Business API), selezionalo per utilizzarlo come predefinito per i messaggi WhatsApp

## Test della connessione

Dopo aver salvato un account del fornitore, testa che le credenziali funzionino:

1. Naviga verso **Sistema SMS > Account dei fornitori SMS**
2. Clicca sull'account del fornitore per aprirlo
3. Clicca sul pulsante **Test Connessione**
4. Spwig invia una richiesta di test al fornitore e aggiorna il campo **Stato Connessione**

| Stato | Significato |
|--------|---------|
| Connesso | Le credenziali sono valide e il fornitore è raggiungibile |
| Connessione fallita | Le credenziali sono errate o il fornitore non è raggiungibile |
| Non testato | La connessione non è stata testata ancora |

Se il test fallisce, controlla nuovamente le tue credenziali e assicurati che il tuo account abbia i permessi necessari nel dashboard del fornitore.

## Colonna stato connessione

L'elenco Account dei fornitori SMS mostra un badge **Connessione** colorato per ogni account:

- **Connesso** (verde) — account funzionante
- **Connessione fallita** (rosso) — credenziali non valide — aggiorna le credenziali
- **Non testato** (grigio) — account non testato ancora

## Suggerimenti

- Utilizza il Wizard di configurazione per il tuo primo fornitore — ti guida attraverso ogni campo e testa la connessione prima di salvare
- Solo un account può essere l'Account SMS predefinito alla volta.

Se aggiungi un secondo account e lo segni come predefinito, l'account predefinito precedente viene automaticamente disattivato
- Tieni un registro delle credenziali API del tuo fornitore in un luogo sicuro.

Se le credenziali cambiano, aggiornale immediatamente qui per evitare notifiche fallite
- Gli account inattivi rimangono nell'elenco ma non vengono utilizzati per l'invio — utile per conservare credenziali di backup senza attivarli
- La maggior parte dei fornitori addebita per ogni messaggio inviato — monitora l'utilizzo nel pannello di controllo del tuo fornitore per evitare fatture inaspettate