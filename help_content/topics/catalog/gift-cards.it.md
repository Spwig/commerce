---
title: Carte Regalo
---

Le carte regalo permettono ai tuoi clienti di acquistare crediti per il negozio che possono inviare a qualcuno come regalo o conservare per uso personale. I destinatari ricevono un codice unico per email che possono utilizzare per il pagamento.

![Gestione delle carte regalo](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Tipi di Denominazioni

Controlla come i clienti possono scegliere l'importo della carta regalo:

| Tipo | Descrizione |
|------|-------------|
| **Denominazioni Fisse** | I clienti scelgono da importi predefiniti (es. $25, $50, $100) |
| **Importo Personalizzato** | I clienti inseriscono qualsiasi importo all'interno di un intervallo minimo/massimo |
| **Entrambi** | Offri denominazioni predefinite più un'opzione di importo personalizzato |

## Creare un Prodotto Carta Regalo

### Passo 1: Configurare il Prodotto

1. Vai a **Prodotti > Tutti i Prodotti** e fai clic su **+ Aggiungi Prodotto**
2. Imposta **Tipo di Prodotto** su **Carta Regalo**
3. Compila il nome del prodotto e la descrizione
4. Configura le impostazioni delle denominazioni:
   - Scegli un **Tipo di Denominazione** (Fissa, Personalizzata o Entrambi)
   - Per Fissa: imposta gli importi disponibili delle denominazioni
   - Per Personalizzata: imposta l'**Importo Minimo** e l'**Importo Massimo** consentiti
5. Imposta **Giorni di Scadenza** (0 = non scade mai) — determina per quanto tempo le carte regalo sono valide dopo l'acquisto
6. Salva e pubblica il prodotto

### Passo 2: Pubblicare e Vendere

Una volta pubblicata, la carta regalo appare nel tuo negozio online come qualsiasi altro prodotto. I clienti possono navigare per trovarla, selezionare un importo e aggiungerla al carrello.

## Ciclo di Vita della Carta Regalo

Una carta regalo segue questo ciclo di vita:

1. **Acquisto** — Il cliente acquista il prodotto carta regalo e fornisce i dettagli del destinatario
2. **Consegna** — Viene inviata automaticamente un'e-mail con il codice della carta regalo al destinatario
3. **Utilizzo** — Il destinatario inserisce il codice al momento del pagamento per applicare il saldo
4. **Tracciamento del Saldo** — Ogni utilizzo sottrae dal saldo fino a quando non raggiunge lo zero

## Flusso di Acquisto del Cliente

Quando un cliente acquista una carta regalo:

1. **Seleziona l'Importo** — Scegli una denominazione o inserisci un importo personalizzato
2. **Dettagli del Destinatario** — Inserisci l'indirizzo email e il nome del destinatario
3. **Messaggio Personale** — Aggiungi un messaggio opzionale da includere nell'e-mail di consegna
4. **Nome del Mittente** — Fornisci il nome del mittente per l'e-mail
5. **Consegna Pianificata** — Pianifica opzionalmente l'e-mail per una data futura (es. un compleanno)
6. **Pagamento** — Completa l'acquisto come qualsiasi altro prodotto

## Consegna Automatica

Dopo l'acquisto, la carta regalo viene consegnata automaticamente:

- Viene inviata un'e-mail formattata al destinatario con:
  - Il codice unico della carta regalo
  - Il valore della carta regalo
  - Il messaggio personale del mittente
  - Un link per controllare il saldo rimanente
- Se è stata impostata una consegna pianificata, l'e-mail verrà inviata alla data e all'ora specificate
- Il mittente riceve una conferma dell'ordine con i dettagli della carta regalo

## Gestione delle Carte Regalo nell'Amministrazione

Vai a **Prodotti > Carte Regalo** per gestire tutte le carte regalo:

### Pannello delle Statistiche

In alto nella pagina, quattro schede mostrano metriche chiave:

- **Totale Carte Regalo** — Numero totale di carte regalo emesse
- **Attive** — Carte attive con saldo disponibile
- **Totale Saldo** — Saldo rimanente complessivo su tutte le carte
- **Utilizzate Parzialmente** — Carte che sono state utilizzate parzialmente

### Filtri

Filtra le carte regalo per:

- **Cerca** — Trova per codice, email o nome del destinatario
- **Stato** — Attive, Inattive, Scadute, Interamente Utilizzate o Utilizzate Parzialmente
- **Saldo** — Con Saldo o Senza Saldo
- **Creato** — Periodo di tempo (Oggi, Questa Settimana, Questo Mese, Questo Anno)

### Dettagli della Carta Regalo

Ogni carta regalo mostra:

- **Codice** — Il codice unico di utilizzo (es. GC-XXXX-XXXX-XXXX)
- **Destinatario** — Email e nome
- **Badge di Stato** — Stato corrente con codifica a colori
- **Saldo / Iniziale / Utilizzato** — Riepilogo finanziario con percentuale utilizzata
- **Date Importanti** — Creato, emesso, primo utilizzo
- **Mittente** — Chi ha acquistato la carta regalo

### Azioni

Per ogni carta regalo, puoi:

- **Modifica** — Visualizza e modifica i dettagli della carta regalo
- **Visualizza Transazioni** — Vedi l'intera cronologia delle transazioni
- **Rinvia Email** — Rinvia l'e-mail di consegna al destinatario
- **Disattiva** — Disabilita la carta (il saldo viene conservato ma non può essere utilizzato)

## Utilizzo della Carta Regalo al Checkout

Quando un cliente inserisce un codice carta regalo al checkout:

1. Il codice viene validato (attivo, non scaduto, con saldo)
2. Viene visualizzato il saldo disponibile
3. Il saldo viene applicato al totale dell'ordine
4. Se il saldo copre l'intero ordine, non è necessario un pagamento aggiuntivo
5. Se il saldo è inferiore al totale dell'ordine, il cliente paga l'importo rimanente
6. La transazione viene registrata e il saldo viene aggiornato

## Gestione dei Rimborsi

Quando si rimborsano ordini che hanno utilizzato una carta regalo:

- **Carte regalo non utilizzate** — Disattiva completamente la carta regalo
- **Carte utilizzate parzialmente** — Il saldo deve essere aggiustato manualmente tramite una transazione
- **Rimborso completo** — Credita l'importo sulla carta regalo tramite una transazione di rimborso

## Consigli

- Imposta periodi di scadenza ragionevoli (es. 365 giorni) per rispettare le normative locali sulle carte regalo — alcune giurisdizioni richiedono periodi minimi di validità.
- Utilizza il tipo di denominazione "Entrambi" per offrire comodità (importi predefiniti) e flessibilità (importi personalizzati).
- Monitora regolarmente la metrica Totale Saldo — rappresenta un'obbligazione pendente nei tuoi libri contabili.
- Utilizza la consegna programmata per le promozioni stagionali — i clienti possono acquistare le carte regalo in anticipo e riceverle esattamente nella data desiderata.
- Testa il flusso completo (acquisto, consegna via e-mail, utilizzo) con un ordine di test prima di lanciare.
- Se vendi a clienti in diversi paesi, puoi emettere carte regalo in valute specifiche — vedi l'argomento di aiuto **Carte Regalo a Multipla Valuta** per i dettagli.