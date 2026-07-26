---
title: Programma Fedeltà
---

Il Programma Fedeltà ti permette di premiare i clienti per gli acquisti e l'engagement con un sistema basato su punti. I clienti guadagnano punti, avanzano nei livelli e riscattano premi. Naviga verso **Marketing > Programma Fedeltà** nel menu laterale dell'amministratore.

![Dashboard fedeltà](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Dashboard Fedeltà

La dashboard fornisce un'overview completa del tuo programma fedeltà:

### Metriche Principali

- **Totale Membri** — Totale dei clienti iscritti
- **Membri Attivi (30d)** — Membri che hanno guadagnato o riscattato punti negli ultimi 30 giorni
- **Punti Pendenti** — Totale dei punti non riscattati da tutti i membri
- **Tasso di Riscatto** — Percentuale dei punti guadagnati che sono stati riscattati
- **Punti Guadagnati (30d)** — Punti guadagnati negli ultimi 30 giorni
- **Punti Riscattati (30d)** — Punti riscattati negli ultimi 30 giorni
- **Punti Medio/Membro** — Media dei punti per membro
- **Regole Attive** — Numero di regole di guadagno attive

### Azioni Veloci

La dashboard ha schede di accesso rapido per gestire tutti gli aspetti del programma:
- **Membri** — Visualizza e gestisci i membri fedeltà
- **Livelli** — Configura i livelli di appartenenza
- **Premi** — Crea il catalogo dei premi
- **Riscatti** — Visualizza la cronologia dei riscatti
- **Regole** — Configura come vengono guadagnati i punti
- **Badge** — Gestisci i badge di conquista
- **Campagne** — Esegui campagne fedeltà speciali
- **Segmenti** — Crea segmenti di membri per targeting

### Grafici e Analisi

- **Trend di Iscrizione dei Membri** — Nuovi iscritti nel tempo
- **Punti Guadagnati vs Riscattati** — Monitora l'equilibrio del flusso dei punti
- **Distribuzione dei Livelli** — Vedi come i membri sono distribuiti nei livelli

## Configurazione del Programma

### Passo 1: Crea Livelli

I livelli definiscono i livelli di appartenenza con benefici crescenti:

1. Naviga verso **Fedeltà > Livelli**
2. Crea livelli come Rame, Argento, Oro, Platino
3. Per ogni livello, imposta:
   - **Nome** — Nome visualizzato del livello
   - **Rango** — Ordine di ordinamento (rango più basso = livello più basso, ad esempio, Rame = 1, Argento = 2)
   - **Colore** — Colore di accento visivo visualizzato sui badge dei membri
   - **Punti Minimi Guadagnati** — Punti totali guadagnati per qualificarsi a questo livello
   - **Spesa Minima** — Importo totale per qualificarsi a questo livello
   - **Ordini Minimi** — Numero di ordini per qualificarsi a questo livello
   - **Moltiplicatore di Punti** — Tasso di guadagno bonus per i membri in questo livello (ad esempio, 2.0 = 2x punti)

Un membro si qualifica per un livello se **qualsiasi** dei tre limiti è soddisfatto. Puoi utilizzare solo un limite o combinare tutti e tre.

### Passo 2: Configura le Regole di Guadagno

Le regole definiscono come i clienti guadagnano punti:

1. Naviga verso **Fedeltà > Regole**
2. Crea regole utilizzando uno dei quattro tipi di regola:

| Tipo di Regola | Descrizione | Esempio |
|----------------|-------------|---------|
| **Spesa** | Punti per importo speso | 1 punto per $1 |
| **Articolo** | Punti per articolo acquistato | 50 punti per prodotto in una categoria specifica |
| **Azione** | Punti per un'azione specifica | 200 punti per l'iscrizione |
| **Evento** | Punti per un evento nel calendario | Punti bonus per compleanno |

3. Configura le impostazioni aggiuntive della regola:
   - **Ambito / Filtri di Ambito** — Limita la regola a prodotti, categorie o livelli di appartenenza specifici
   - **Importo Minimo dell'Ordine** — Valore minimo del carrello per applicare la regola
   - **Livelli Consentiti** — Limita la regola a specifici livelli di appartenenza
   - **È Esclusiva** — Quando abilitata, questa regola non può essere cumulativa con altre regole
   - **Giorni di Punti Pendenti** — Numero di giorni prima che i punti guadagnati siano disponibili (utile per considerare i periodi di reso)
   - **Giorni di Scadenza dei Punti** — Numero di giorni dopo il guadagno prima che i punti scadano (lascia vuoto per nessuna scadenza)
   - **Inizio / Fine** — Limita la regola a un intervallo di date

### Passo 3: Configura i Premi

I premi sono ciò che i clienti possono riscattare con i loro punti:

1. Naviga verso **Fedeltà > Premi**
2. Crea premi come:
   - **Buono Sconto di $5** — 500 punti
   - **Spedizione Gratuita** — 300 punti
   - **Sconto del 10%** — 1000 punti

> **Non è possibile riscattare al momento i codici sconto.** Una ricompensa con **Tipo di Ricompensa** impostato su **Codice Sconto** — come il coupon di $5 di sconto o il 10% di sconto menzionati sopra — attualmente non può essere riscattata.

L'utente vede un errore chiaro e i punti vengono automaticamente restituiti al loro saldo, quindi non si perde nulla, ma la ricompensa non è ancora utilizzabile.

Questo è un fix intenzionale: il riscatto aveva il successo segnalato mentre silenziosamente sottraeva i punti e non emetteva nulla.

Se gli utenti menzionano un riscatto "che non funziona", si tratta di questo — non è un nuovo problema.

Le ricompense in punti riprenderanno a funzionare nuovamente in un prossimo rilascio.

Questo non influisce sulle ricompense di Spedizione Gratuita, Prodotto Gratuito o Esperienza/Privilegio.

### Passaggio 4: Crea Badge (Opzionale)

I badge riconoscono i traguardi dei clienti:

1. Vai a **Loyalty > Badges**
2. Crea badge per traguardi:
   - **Primo Acquisto** — Assegnato dopo il primo ordine
   - **Grande Spenditore** — Assegnato dopo un consumo di $500+
   - **Cliente Fedele** — Assegnato dopo 10 ordini

I badge possono includere l'assegnazione di punti bonus al momento del riconoscimento.

## Gestione dei Membri

### Elenco dei Membri

Visualizza tutti i membri del programma fedeltà con:
- Tier e stato correnti
- Saldo dei punti
- Data di iscrizione
- Attività recenti

### Top Guadagnatori di Punti

Il dashboard evidenzia i membri più attivi con una classifica che mostra il rango, il nome, il tier e i punti guadagnati nel periodo.

### Transazioni Recenti

Un registro delle transazioni mostra tutta l'attività recente dei punti. I tipi di transazione includono:

| Tipo | Significato |
|------|---------|
| **Guadagna** | Punti accreditati da un acquisto qualificato o una regola |
| **Riscatta** | Punti spesi per una ricompensa |
| **Bonus** | Punti extra da un badge, campagna o assegnazione manuale |
| **Correzione** | Correzione manuale dei punti fatta da un membro dello staff |
| **Revoca** | Punti rimossi (es. dopo l'annullamento di un ordine) |
| **Scadenza** | Punti che hanno superato la data di scadenza |

### Modifiche Manuali ai Punti

Puoi aggiungere o sottrarre manualmente punti a qualsiasi membro:

1. Apri la pagina dei dettagli del membro
2. Clicca su **Modifica Punti**
3. Inserisci l'importo in punti (positivo per aggiungere, negativo per sottrarre)
4. Inserisci la motivazione per la modifica
5. Clicca su **Salva**

La modifica viene registrata come una transazione e è visibile nella cronologia delle transazioni del membro.

## Campagne

Le campagne di fedeltà ti permettono di lanciare promozioni speciali:
- **Weekend con Doppio Punti** — Aumenta temporaneamente il tasso di guadagno dei punti
- **Eventi con Punti Bonus** — Assegna punti extra per azioni specifiche
- **Promozioni per l'Avanzamento del Tier** — Riduci il limite per l'avanzamento del tier

## Consigli

- Inizia con regole semplici per il guadagno di punti (1 punto per ogni $1 speso) e espandi nel tempo.
- Imposta soglie di ricompensa raggiungibili per mantenere i membri impegnati — se le ricompense sembrano irraggiungibili, i membri perderanno interesse.
- Usa i badge per rendere il gioco più coinvolgente e incoraggiare comportamenti specifici.
- Monitora il Tasso di Riscatto — un programma sano ha un tasso di riscatto compreso tra il 10% e il 30%.
- Esegui campagne durante i periodi di bassa attività per aumentare l'engagement.
- Usa il grafico Punti Guadagnati vs. Punti Riscattati per assicurarti che il tuo programma sia sostenibile.