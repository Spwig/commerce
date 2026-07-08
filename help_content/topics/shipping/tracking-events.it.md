---
title: Eventi di Tracciamento
---

Gli eventi di tracciamento registrano checkpoint sullo stato del spedizione durante il ciclo di vita della consegna—ogni evento cattura lo stato (in transito, in consegna, consegnato), timestamp, posizione, descrizione e dati grezzi del carrier. Gli eventi vengono creati automaticamente tramite notifiche webhook del carrier o manualmente dai commercianti. I clienti vedono l'history degli eventi di tracciamento nel loro account e nelle e-mail di conferma dell'ordine, fornendo una visibilità in tempo reale sulla consegna.

Questa pagina amministrativa visualizza un history degli eventi in sola lettura per scopi di audit e supporto al cliente.

## Struttura degli Eventi di Tracciamento

Ogni evento contiene:

**Informazioni sullo Stato**:
- **Stato**: in_transit, out_for_delivery, delivered, exception, failed, returned
- **Descrizione**: stato leggibile da un umano (es. "Pacchetto arrivato alla struttura di smistamento")
- **Codice Stato Carrier**: stato originale del carrier (es. "DEP" per partenza)

**Dati sulla Posizione**:
- **Città**: città della posizione dell'evento
- **Stato**: stato/provincia della posizione dell'evento
- **Paese**: paese della posizione dell'evento
- **Codice Postale**: codice postale/ZIP della posizione dell'evento

**Timestamp**:
- **Verificato il**: quando l'evento è realmente avvenuto (orario del carrier)
- **Creato il**: quando l'evento è registrato in Spwig (orario del sistema)

**Metadati**:
- **Dati grezzi**: risposta completa in formato JSON dal carrier API
- **Spedizione**: ID spedizione collegata

---

## Tipi di Stato degli Eventi

**in_transit**: Pacchetto in movimento attraverso la rete del carrier
- Esempi: "Partenza dalla struttura", "Arrivato al centro", "In transito verso la prossima struttura"

**out_for_delivery**: Pacchetto sul veicolo di consegna
- Esempi: "In consegna", "Sul veicolo di consegna"

**delivered**: Pacchetto consegnato con successo
- Esempi: "Consegnato alla porta d'ingresso", "Lasciato alla reception", "Consegnato al destinatario"

**exception**: Problema di consegna che richiede attenzione
- Esempi: "Ritardo per condizioni meteorologiche", "Indirizzo errato", "Consegna tentata senza successo"

**failed**: Consegna fallita definitivamente
- Esempi: "Indirizzata in modo non consegnabile", "Rifiutata dal destinatario"

**returned**: Pacchetto in ritorno al mittente
- Esempi: "Ritorno al mittente iniziato", "Pacchetto in ritorno"

---

## Come Vengono Creati gli Eventi di Tracciamento

### Automatico (Webhook del Carrier)

**Flusso di lavoro**:
1. Carrier scansiona il pacchetto (partenza, arrivo, consegna)
2. Carrier invia un webhook all'endpoint webhook di Spwig
3. Webhook registrato nella tabella WebhookLog
4. Sistema analizza il payload del webhook
5. TrackingEvent creato con i dati estratti
6. Invio e-mail di notifica al cliente (se configurato)

**Vantaggi**:
- Aggiornamenti in tempo reale (nessun polling necessario)
- Timestamp accurati dal carrier
- History completa degli eventi mantenuta automaticamente

### Manuale (Inserimento del Commerciante)

**Flusso di lavoro**:
1. Naviga verso i dettagli della spedizione
2. Clicca su "Aggiungi Evento di Tracciamento"
3. Seleziona lo stato dal menu a discesa
4. Inserisci la descrizione
5. Opzionale: Inserisci i dati sulla posizione
6. Imposta il timestamp verificato
7. Salva

**Casi d'uso**:
- Carrier senza supporto webhook
- Correzioni manuali delle spedizioni
- Consegna locale (non da carrier)
- Aggiornamenti di stato interni

---

## Ordine di Visualizzazione degli Eventi

Gli eventi sono visualizzati in **ordine cronologico inverso** (più recenti prima):

**Esempio di Visualizzazione**:
```
13 feb 2026 10:30 AM - Consegnato (Brooklyn, NY)
13 feb 2026 08:15 AM - In consegna (Brooklyn, NY)
12 feb 2026 11:45 PM - Arrivato alla struttura locale (Brooklyn, NY)
12 feb 2026 06:30 PM - In transito (Newark, NJ)
12 feb 2026 02:15 PM - Partenza dall'origine (Philadelphia, PA)
12 feb 2026 09:00 AM - Prelevato (Philadelphia, PA)
```

---

## Visibilità per i Clienti

Gli eventi di tracciamento vengono mostrati ai clienti in:

**Email di Conferma Ordine**:
- Ultimo stato dell'evento
- Data stimata di consegna
- Link di tracciamento

**Account Cliente > Dettagli Ordine**:
- Timeline completa degli eventi
- Descrizioni degli eventi
- Storia delle posizioni
- Timestamp

**Pagina di Tracciamento** (se abilitata):
- URL dedicato per la tracciamento
- Timeline visiva
- Logo del carrier
- Mappa di consegna (se disponibili i dati di posizione)

---

## Filtraggio degli Eventi di Tracciamento

**Filtraggi Utili**:
- **Spedizione**: Visualizza eventi per spedizione specifica
- **Stato**: Filtra per tipo di evento (consegnato, in_transit, ecc.)
- **Intervallo di Date**: Eventi all'interno di un periodo
- **Luogo**: Eventi in città/stato specifici

**Casi d'uso**:
- "Mostra tutte le spedizioni consegnate oggi"
- "Trova tutte le eccezioni della settimana scorsa"
- "Monitora spedizioni attualmente in transito"

---

## Dati Grezzi (Debugging)

**Campo Dati Grezzi**:
- Memorizza la risposta completa dell'API del carrier in formato JSON
- Utile per il debug dei problemi dei webhook
- Contiene metadati specifici del carrier

**Esempio di Dati Grezzi** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Out for delivery",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Quando Controllare i Dati Grezzi**:
- Descrizione dell'evento non chiara
- Dati di posizione mancanti
- Errori di elaborazione del webhook
- Escalation del supporto del carrier

---

## Temporizzazione degli Eventi

**Verificato il** vs **Creato il**:

**Verificato il**: Quando l'evento del carrier è realmente avvenuto
- Esempio: Pacchetto scansionato alle 10:30 AM

**Creato il**: Quando Spwig ha ricevuto il webhook
- Esempio: Webhook ricevuto alle 10:32 AM (ritardo di 2 minuti)

**Perché Sono Diversi?**:
- Latenza di rete
- Elaborazione batch del carrier
- Ritardi di riprovare webhook

**Usa Verificato il per la visualizzazione del cliente** - riflette più accuratamente il progresso effettivo della consegna.

---

## Consigli

- **Gli eventi sono in sola lettura** - Non possono essere modificati dopo la creazione (integrità degli audit)
- **Controlla i dati grezzi per i dettagli** - Contiene più informazioni rispetto ai campi visualizzati
- **Monitora il ritardo del webhook** - Un grande ritardo tra verificato il e creato il indica problemi con i webhook
- **Usa per il supporto al cliente** - La timeline degli eventi aiuta a diagnosticare problemi di consegna
- **Traccia i pattern di consegna** - Analizza la temporizzazione degli eventi per valutare le prestazioni del carrier
- **Configura notifiche** - Invia automaticamente e-mail ai clienti su eventi chiave (in_consegna, consegnato)
- **Non cancellare gli eventi** - Mantieni l'intera traccia degli audit
- **Controlla WebhookLog per i fallimenti** - Gli eventi mancanti potrebbero indicare errori nell'elaborazione dei webhook
- **I dati di posizione variano per carrier** - Alcuni carrier forniscono dati di posizione dettagliati, altri minimi
- **Gli eventi eccezione richiedono attenzione** - Monitora e segui le eccezioni di consegna