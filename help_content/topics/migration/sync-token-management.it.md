---
title: Gestione del Token di Sincronizzazione
---

I token di sincronizzazione sono credenziali sicure che consentono a due installazioni di Spwig di comunicare tra loro. Prima di poter sincronizzare le impostazioni o migrare i dati tra negozi, è necessario generare un token nel negozio **destinatario** e fornirlo al negozio **mittente**.

## Come Funzionano i Token di Sincronizzazione

Un token di sincronizzazione è una chiave API visibile una sola volta che autentica le richieste tra due installazioni di Spwig. Quando si configura una connessione, il negozio remoto utilizza questo token per dimostrare di avere il permesso di leggere da o scrivere nel tuo negozio.

- I token vengono generati nel negozio che sarà **connesso a** (il destinatario)
- Ogni token può essere visualizzato solo una volta, immediatamente dopo la generazione
- I token possono essere revocati in qualsiasi momento per interrompere immediatamente l'accesso
- Un negozio può avere diversi token attivi per diverse connessioni

## Generazione di un Token

1. Vai a **Data Migration > Spwig-to-Spwig Sync** nel menu laterale di amministrazione
2. Clicca su **Manage Tokens** nel pannello di sincronizzazione
3. Inserisci un nome descrittivo per il token (es. "Server di Staging" o "Sincronizzazione di Produzione")
4. Clicca su **Generate Token**
5. **Copia immediatamente il token** -- non verrà visualizzato nuovamente

> **Importante:** Conserva il token in modo sicuro. Se lo perdi, dovrai generarne uno nuovo.

## Utilizzo di un Token

Una volta che hai ottenuto un token dal negozio destinatario:

1. Vai al pannello **Spwig-to-Spwig Sync** nel negozio che inizierà la connessione
2. Avvia una nuova **Sincronizzazione delle Impostazioni** o **Migrazione Completa**
3. Nella fase di Connessione, inserisci l'URL del negozio destinatario e incolla il token
4. Clicca su **Test Connection** per verificare che funzioni
5. La connessione verrà salvata per un uso futuro

## Revoca di un Token

Se un token è compromesso o non è più necessario:

1. Vai a **Manage Tokens** nel pannello di sincronizzazione
2. Trova il token che desideri revocare
3. Clicca sul pulsante **Revoke**
4. Conferma la revoca

La revoca di un token entra in vigore immediatamente. Tutte le connessioni attive che utilizzano quel token smetteranno di funzionare e dovranno essere riconfigurate con un nuovo token.

## Linee Guida per l'Utilizzo

- **Assegna nomi descrittivi ai token** in modo da sapere a quale connessione appartiene ogni token
- **Revoca i token non utilizzati** per ridurre al minimo l'esposizione di sicurezza
- **Genera token separati** per ogni negozio che si connette, invece di condividere un unico token tra diversi negozi
- **Rigenera i token periodicamente** come parte della tua routine di sicurezza, soprattutto dopo i cambiamenti del personale