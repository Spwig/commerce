---
title: Richieste di Reso & Elaborazione
---

Le richieste di reso tracciano i resi dei clienti dall'inizio al completamento del rimborso—i clienti selezionano gli articoli da restituire con motivazioni, i commercianti approvano o rifiutano le richieste, generano etichette di reso, ispezionano gli articoli restituiti e elaborano i rimborsi. Il flusso di lavoro procede attraverso 9 stadi di stato (in sospeso → approvato → etichetta_inviata → in_transito → ricevuto → ispezionato → completato/rifiutato/annullato) con motivazioni di reso a livello di articolo, note di ispezione e spese di rimborso facoltative.

Utilizza questa pagina di amministrazione per rivedere, approvare ed elaborare le richieste di reso dei clienti in modo efficiente.

## Flusso di lavoro per le Richieste di Reso

**Processo a 9 Fasi**:

### 1. In sospeso (Cliente inizia)

Il cliente invia la richiesta di reso:
- Seleziona gli articoli dall'ordine
- Fornisce la motivazione del reso per ogni articolo
- Note del cliente facoltative
- Stato: `in sospeso`

### 2. Approvato/Rifiutato (Commerciante valuta)

Il commerciante valuta la richiesta:
- **Approva**: Reso consentito, procedi alla generazione dell'etichetta
- **Rifiuta**: Reso negato con motivo di rifiuto
- Stato: `approvato` o `rifiutato`

### 3. Etichetta Inviata (Spedizione di reso)

Etichetta di reso generata:
- Il commerciante crea un' spedizione di reso (facoltativo)
- L'etichetta di reso è inviata per email al cliente
- Il cliente spedisce gli articoli
- Stato: `etichetta_inviata`

### 4. In transito (Cliente spedisce)

Cliente spedisce gli articoli:
- Il tracciamento mostra il movimento
- Aggiornamento automatico dello stato tramite webhook del carrier
- Stato: `in_transito`

### 5. Ricevuto (Arrivo in magazzino)

Gli articoli arrivano:
- Il magazzino scansiona la spedizione
- Gli articoli vengono controllati
- Stato: `ricevuto`

### 6. Ispezionato (Controllo qualità)

Il commerciante ispeziona gli articoli:
- Registra lo stato dell'articolo (eccellente/buono/accettabile/danneggiato/defettoso)
- Aggiungi note di ispezione
- Applica le spese di rimborso se applicabile
- Stato: `ispezionato`

### 7. Completato (Rimborso elaborato)

Rimborso emesso:
- Crea rimborso associato
- Pagamento elaborato
- Reso chiuso
- Stato: `completato`

**Risultati alternativi**:
- **Annullato**: Cliente annulla prima della spedizione
- **Rifiutato**: Commerciante rifiuta dopo la valutazione

---

## Elaborazione delle Richieste di Reso

**Passo a passo**:

**Passo 1: Rivedi le Richieste in sospeso**
- Naviga a Ordini > Richieste di Reso
- Filtra per stato = "In sospeso"
- Clicca sulla richiesta per visualizzare i dettagli

**Passo 2: Valuta la Richiesta**
- Rivedi i dettagli dell'ordine
- Controlla le motivazioni del reso
- Verifica la conformità alla politica di reso (entro la finestra di reso, articoli idonei)

**Passo 3: Approva o Rifiuta**
- Clicca su "Approva" per accettare il reso
- O clicca su "Rifiuta" e inserisci il motivo del rifiuto
- Salva la decisione

**Passo 4: Genera l'Etichetta di Reso** (se approvato)
- Clicca su "Crea spedizione di reso"
- Seleziona il carrier/servizio
- Il sistema genera l'etichetta di reso
- L'etichetta viene automaticamente inviata per email al cliente
- Stato → `etichetta_inviata`

**Passo 5: Monitora la Trasmissione**
- Gli aggiornamenti del tracciamento vengono sincronizzati automaticamente tramite webhook del carrier
- Lo stato passa automaticamente a `in_transito` quando il carrier scansiona il pacco

**Passo 6: Ricevi gli Articoli**
- Quando gli articoli arrivano, clicca su "Segna come Ricevuti"
- Stato → `ricevuto`

**Passo 7: Ispeziona gli Articoli**
- Apri la richiesta di reso
- Seleziona lo stato dell'articolo dal menu a discesa:
  - Eccellente (nuovo come originale, riconoscibile)
  - Buono (uso minimo, riconoscibile)
  - Accettabile (usura visibile, riconoscibile con sconto)
  - Danneggiato (non riconoscibile)
  - Defettoso (difetto di produzione)
- Aggiungi note di ispezione
- Facoltativo: applica le spese di rimborso (percentuale o fissa)
- Stato → `ispezionato`

**Passo 8: Elabora il Rimborso**
- Clicca su "Crea Rimborso"
- Il sistema calcola l'importo del rimborso:
  - Prezzo originale dell'articolo
  - Meno spese di rimborso (se applicate)
  - Meno costi di spedizione (se non rimborsabili)
- Crea il rimborso (collegato alla richiesta di reso)
- Stato → `completato`

---

## Motivi di Reso a Livello di Articolo

I clienti selezionano il motivo per ogni articolo:

**Motivi Comuni**:
- Articolo ricevuto errato
- Articolo danneggiato/defettoso
- Cambiato idea/non più necessario
- Articolo non corrisponde alla descrizione
- Trovato un prezzo migliore
- Ordinato per errore
- Qualità non come previsto

**Utilizzare i Motivi Per**:
- Analisi (tracciare le cause comuni dei resi)
- Controllo qualità (identificare articoli difettosi)
- Miglioramento del processo (ridurre i resi prevenibili)

---

## Spese di Rimborso

Applica spese per compensare i costi di elaborazione del reso:

**Configurazione**:
- **Tipo**: Percentuale (es. 15%) o Fissa (es. $5)
- **Quando applicare**: Resi non difettosi, articoli aperti, ordini speciali

**Esempio**:
```
Acquisto originale: $100
Spese di rimborso: 15%
Importo del rimborso: $85
```

**Linee guida**:
- Comunica chiaramente la politica delle spese di rimborso
- Non applicare a articoli difettosi
- Considera l'esonero per clienti VIP

---

## Linee Guida per l'Ispezione dei Resi

Stabilisci criteri di ispezione coerenti:

**Eccezionale**:
- Imballaggio originale non aperto
- Nessuna usura visibile
- Tutti gli accessori inclusi
- Riconoscibile al prezzo completo

**Buono**:
- Aperto ma uso minimo
- Usura minima dell'imballaggio
- Tutti i componenti presenti
- Riconoscibile al prezzo completo

**Accettabile**:
- Usura/uso visibile
- Imballaggio danneggiato
- Accessori non essenziali mancanti
- Riconoscibile con sconto

**Danneggiato**:
- Danneggiato fisicamente
- Parti mancanti
- Non riconoscibile
- Richiede smaltimento o riparazione

**Defettoso**:
- Difetto di produzione
- Malfunzionamento
- Richiesta di garanzia
- Reso al produttore

---

## Opzioni di Spedizione per i Resi

**Opzione 1: Cliente paga la spedizione del reso**
- Nessuna etichetta di reso fornita
- Cliente seleziona il proprio carrier
- Inserimento manuale del numero di tracciamento

**Opzione 2: Commerciante fornisce etichetta prepagata**
- Genera l'etichetta di reso tramite l'account del provider
- Costo dedotto dal rimborso O commerciante assorbe
- Sincronizzazione automatica del tracciamento

**Opzione 3: Spedizione di reso gratuita**
- Commerciante assorbe il costo della spedizione del reso
- Migliora la soddisfazione del cliente
- Aumenta il tasso di reso (considera il trade-off)

---

## Filtraggio & Reporting

**Filtri utili**:
- Stato: In sospeso (azione richiesta)
- Intervallo di date: Ultimi 30 giorni
- Ordine: Ricerca ordine specifico
- Motivo: Tracciare le cause dei resi

**Analisi dei Resi**:
- Tasso di reso per prodotto
- Motivi di reso più comuni
- Tempo medio di elaborazione (in sospeso → completato)
- Entrate da spese di rimborso

---

## Suggerimenti

- **Stabilisci una politica di reso chiara** - Comunica la finestra (30 giorni), condizioni, spese
- **Elabora le richieste in modo tempestivo** - Rispondi alle richieste in sospeso entro 24 ore
- **Ispeziona accuratamente** - Documenta lo stato per prevenire dispute
- **Traccia i motivi dei resi** - Utilizza i dati per migliorare prodotti/descrizioni
- **Automatizza dove possibile** - Webhook del carrier aggiornano automaticamente lo stato di transito
- **Comunica con i clienti** - Invia aggiornamenti per email a ogni cambiamento di stato
- **Sia giusto con le spese di rimborso** - Applicale in modo coerente, esonerale per difetti
- **Monitora i resi fraudolenti** - Segnala i clienti con troppi resi
- **Migliora l'imballaggio** - Riduci i resi legati al danno
- **Aggiorna l'inventario prontamente** - Ripristina lo stock dopo l'ispezione
- **Impara dai pattern** - Alti tassi di reso per prodotti specifici potrebbero indicare un problema di qualità
