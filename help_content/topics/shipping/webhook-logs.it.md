---
title: Log dei Webhook
---

I log dei webhook forniscono un registro permanente di tutte le richieste di webhook in entrata provenienti dai carrier—registrando il metodo della richiesta, l'URL dell'estremità, gli header, il payload, lo stato di elaborazione (in attesa/elaborato/fallito) e la risposta. Ogni webhook viene registrato prima dell'elaborazione per garantire che nessun evento venga perso in caso di fallimento dell'elaborazione. I log permettono di debuggare problemi di integrazione dei webhook, monitorare l'affidabilità dell'API del carrier e ricostruire i cronogrammi di consegna per il supporto clienti.

Questa pagina amministrativa di sola lettura aiuta a risolvere i problemi di fallimento dei webhook e a verificare lo stato di salute dell'integrazione del carrier.

## Struttura del Log dei Webhook

Ogni voce del log registra:

**Dettagli della Richiesta**:
- **Chiave Fornitore**: Quale carrier ha inviato il webhook (fedex, ups, dhl)
- **Estremità**: Percorso dell'URL del webhook (es. `/webhooks/shipping/fedex/`)
- **Metodo**: Metodo HTTP (di solito POST)
- **Header**: Header della richiesta (JSON)
- **Payload**: Corpo della richiesta (JSON)

**Elaborazione**:
- **Stato di Elaborazione**: in attesa, elaborato, fallito
- **Messaggio di Errore**: Motivo del fallimento (se stato=fallito)
- **Risposta**: Risposta HTTP inviata al carrier
- **Codice Stato della Risposta**: 200, 400, 500, ecc.

**Timestamp**:
- **Ricevuto Il**: Quando è arrivato il webhook
- **Elaborato Il**: Quando è stata completata l'elaborazione

---

## Valori dello Stato di Elaborazione

**in attesa**: Webhook ricevuto, in attesa di elaborazione
- Normale per un breve momento dopo la ricezione
- Se rimane in attesa, indica un ritardo nella coda di elaborazione

**elaborato**: Webhook elaborato con successo
- Creato il TrackingEvent
- Notifica al cliente inviata (se applicabile)
- Risposta 200 inviata al carrier

**fallito**: Elaborazione del webhook fallita
- Controllare il campo error_message per il motivo
- Causa comune: JSON non valido, spedizione sconosciuta, evento duplicato

---

## Flusso del Webhook

**Workflow Normale**:
```
1. Carrier scansiona il pacchetto
   ↓
2. Carrier invia POST all'estremità del webhook di Spwig
   ↓
3. Spwig crea WebhookLog (stato=in attesa)
   ↓
4. Lavoratore in background elabora il webhook
   ↓
5. Analizza il payload JSON
   ↓
6. Trova spedizione corrispondente (per numero di tracciamento)
   ↓
7. Crea TrackingEvent
   ↓
8. Aggiorna WebhookLog (stato=elaborato)
   ↓
9. Invia risposta HTTP 200 al carrier
```

**Situazioni di Fallimento**:
- **JSON non valido**: Carrier ha inviato dati malformatati → stato=fallito, errore="errore di analisi JSON"
- **Spedizione Sconosciuta**: Il numero di tracciamento non corrisponde a nessuna spedizione → stato=fallito, errore="Spedizione non trovata"
- **Duplicato**: Evento già esistente → stato=fallito, errore="Evento duplicato"

---

## Debugging dei Fallimenti dei Webhook

**Passo a Passo**:

**1. Filtra per Stato=Fallito**
- Naviga su Spedizioni > Log dei Webhook
- Filtra: Stato di Elaborazione = "fallito"
- Rivedi i fallimenti recenti

**2. Controlla il Messaggio di Errore**
- Clicca sulla voce del log
- Leggi il campo error_message
- Errori comuni:
  - "Spedizione non trovata" → Discrepanza nel numero di tracciamento
  - "Errore di decodifica JSON" → Carrier ha inviato JSON non valido
  - "Campo richiesto mancante" → Payload manca dati previsti

**3. Analizza il Payload**
- Visualizza il payload JSON grezzo
- Verifica che la struttura corrisponda al formato previsto
- Controlla la presenza di campi mancanti (tracking_id, event_type, ecc.)

**4. Verifica che la Spedizione Esista**
- Estrai il numero di tracciamento dal payload
- Cerca Spedizioni per numero di tracciamento
- Assicurati che la spedizione esista e utilizzi il carrier corretto

**5. Controlla la Configurazione del Fornitore**
- Verifica che l'account del fornitore sia attivo
- Conferma che l'URL dell'estremità del webhook sia corretto
- Testa le credenziali API del fornitore

**6. Riprova l'Elaborazione** (se applicabile)
- Alcuni elaboratori di webhook supportano il riprova manuale
- Risolvi prima il problema sottostante
- Riprova il webhook fallito

---

## Problemi Comuni dei Webhook

**Problema 1: "Spedizione non trovata"**

**Causa**: Il numero di tracciamento nel webhook non corrisponde a nessuna spedizione
- Battitura quando si crea la spedizione
- Webhook per un account diverso
- Spedizione eliminata prima che il webhook fosse ricevuto

**Soluzione**:
- Verifica l'ortografia del numero di tracciamento
- Controlla che il carrier della spedizione corrisponda al fornitore del webhook
- Ricrea la spedizione se necessario

---

**Problema 2: "Errore di decodifica JSON"**

**Causa**: Carrier ha inviato JSON malformatato
- Raro, di solito un bug nell'API del carrier
- Problemi di codifica dei caratteri

**Soluzione**:
- Contatta il supporto del carrier con il payload grezzo
- Controlla gli header per la codifica del carattere
- Verifica l'URL dell'estremità nel pannello di controllo del carrier

---

**Problema 3: Webhook duplicati**

**Causa**: Carrier invia lo stesso evento più volte
- Logica di riprova (carrier non ha ricevuto la risposta 200)
- Bug del carrier

**Soluzione**:
- Il sistema rifiuta automaticamente i duplicati (comportamento normale)
- Verifica che response_status_code sia 200
- Se persistente, contatta il supporto del carrier

---

**Problema 4: Webhook mancanti**

**Causa**: Webhook previsto mai ricevuto
- Carrier non ha inviato (scansione mancata)
- Estremità del webhook configurata male nel pannello di controllo del carrier
- Firewall che blocca le richieste

**Soluzione**:
- Controlla la configurazione del webhook nel pannello di controllo del carrier
- Verifica che l'URL dell'estremità sia pubblico e accessibile
- Testa l'estremità con curl/Postman
- Controlla le regole del firewall del server

---

## Configurazione dell'Estremità del Webhook

**URL dei Webhook Tipici**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Configurazione nel Pannello del Carrier**:
1. Accedi al portale per sviluppatori del carrier
2. Naviga verso le impostazioni del webhook
3. Inserisci l'URL del webhook di Spwig
4. Seleziona gli eventi a cui sottoscrivere (aggiornamenti di tracciamento, consegna, eccezioni)
5. Salva la configurazione
6. Testa il webhook con lo strumento di test del carrier

**Sicurezza**:
- I webhook richiedono HTTPS (non HTTP)
- Alcuni carrier firmano le richieste (verifica la firma)
- Elenco di indirizzi IP (se il carrier fornisce indirizzi IP fissi)

---

## Monitoraggio della Salute dei Webhook

**Metriche Chiave**:

**Tasso di Successo**:
```
Tasso di Successo = (Elaborato / Totale) × 100%

Obiettivo: >98%
```

**Tempo di Elaborazione**:
```
Tempo Medio = Elaborato Il - Ricevuto Il

Obiettivo: <2 secondi
```

**Pattern di Fallimento**:
- Picco improvviso di fallimenti → Cambiamento o interruzione dell'API del carrier
- Fallimenti costanti "spedizione non trovata" → Problema di sincronizzazione del numero di tracciamento
- Tutti i webhook falliti → Problema di configurazione dell'estremità

**Strategia di Monitoraggio**:
- Controlla il tasso di fallimento quotidianamente
- Allerta se il tasso di fallimento >5%
- Rivedi i messaggi di errore settimanalmente
- Confronta con lo stato del carrier

---

## Conservazione dei Webhook

**I log sono permanenti** - mai eliminati automaticamente

**Perché Permanent**:
- Conformità all'audit
- Supporto clienti (ricostruzione del cronogramma di consegna)
- Risoluzione di dispute
- Debug dei webhook

**Archiviazione**: I log sono archiviati in modo efficiente (JSON compresso)

---

## Consigli

- **I webhook sono un registro permanente di audit** - Mai eliminare, anche se elaborati con successo
- **Controlla quotidianamente i webhook falliti** - Cattura problemi di integrazione precocemente
- **Monitora il ritardo di elaborazione** - Ritardi lunghi indicano problemi di prestazioni
- **Salva i payload grezzi** - Essenziale per debuggare cambiamenti nell'API del carrier
- **Testa la configurazione dell'estremità** - Usa gli strumenti di test del carrier per verificare la configurazione
- **Abilita la firma dei webhook** - Verifica che le richieste provengano effettivamente dal carrier
- **Elenco di indirizzi IP del carrier** - Se il carrier fornisce range di IP fissi
- **Configura allerte** - Notifica quando il tasso di fallimento supera un limite
- **Confronta con lo stato del carrier** - Le lacune nei webhook potrebbero indicare un'interruzione del carrier
- **Documenta i formati dei payload del carrier** - Aiuta quando il carrier aggiorna l'API
- **Mantieni le URL dei webhook stabili** - Cambiare le URL richiede un aggiornamento nel pannello di controllo del carrier
