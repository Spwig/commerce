---
title: Prodotti Configurabili
---

I prodotti configurabili permettono ai clienti di costruire il loro prodotto selezionando opzioni da diversi slot di configurazione. Questo è ideale per gli articoli da costruire su ordinazione come PC personalizzati, scatole regalo personalizzate o mobili su ordinazione, dove ogni componente è un prodotto reale nel vostro catalogo.

![Amministratore del configuratore di prodotti](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Come Funziona

Un prodotto configurabile è composto da **slot** (categorie di scelta) e **opzioni** (i prodotti effettivi che i clienti possono selezionare). Ad esempio, un PC personalizzato potrebbe avere slot per Processore, scheda grafica, RAM e Archiviazione — ogni slot contiene diverse opzioni di prodotto da scegliere.

## Strategie di Prezzo

Scegliete come viene calcolato il prezzo finale:

| Strategia | Descrizione |
|----------|-------------|
| **Somma dei Componenti** | Prezzo finale = totale dei prezzi di tutte le opzioni selezionate. Non è necessario un prezzo base. |
| **Prezzo Base + Regolazioni** | Iniziate con il prezzo base del prodotto, quindi aggiungete/sottraete regolazioni di prezzo per ogni opzione. |
| **Prezzo Fisso** | Un prezzo unico, indipendentemente dalle opzioni selezionate dal cliente. |

## Configurazione di un Prodotto Configurabile

### Passo 1: Crea il Prodotto

1. Naviga a **Prodotti > Tutti i Prodotti** e clicca **+ Aggiungi Prodotto**
2. Imposta **Tipo Prodotto** a **Prodotto Configurabile**
3. Scegli la tua **Strategia di Prezzo** (la più comune è Somma dei Componenti)
4. Inserisci il nome del prodotto, la descrizione e altre informazioni di base
5. Salva il prodotto

### Passo 2: Aggiungi Slot di Configurazione

Dopo aver salvato, passa alla scheda **Configurazione** per impostare i tuoi slot.

1. Clicca **+ Aggiungi Slot** per creare una nuova categoria di configurazione
2. Per ogni slot, configura:
   - **Nome** — Cosa vede il cliente (es. "Processore", "Colore")
   - **Icona** — Classe di icona Font Awesome per l'identificazione visiva
   - **Obbligatorio** — Se il cliente deve effettuare una selezione
   - **Min/Max Selezione** — Quante opzioni il cliente può selezionare (predefinito: esattamente 1)
   - **Ordine di Sorteggio** — Controlla l'ordine in cui vengono visualizzati gli slot nel wizard del configuratore

### Passo 3: Aggiungi Opzioni a Ogni Slot

Ogni slot necessita di opzioni di prodotto per le scelte dei clienti:

1. Clicca **Gestisci Opzioni** su uno slot
2. Cerca e aggiungi prodotti esistenti dal tuo catalogo
3. Per ogni opzione, configura:
   - **Regolazione del Prezzo** — Importo da aggiungere o sottrarre (usato con la strategia Prezzo Base + Regolazioni)
   - **Predefinito** — Seleziona automaticamente questa opzione quando il configuratore viene caricato
   - **Popolare** — Mostra un badge "Popolare" per aiutare i clienti a decidere
   - **Quantità** — Quante unità di questo componente sono incluse
   - **Etichette di Compatibilità** — Etichette utilizzate per la generazione automatica delle regole di compatibilità

**Consiglio:** I prodotti componenti possono essere nascosti nel negozio online selezionando **Nascondi nel Negozio Online** sulla scheda Informazioni di Base del prodotto componente. Questo li mantiene disponibili come opzioni del configuratore senza ingombrare il catalogo dei prodotti.

### Passo 4: Definisci le Regole di Compatibilità

Le regole di compatibilità impediscono ai clienti di selezionare combinazioni incompatibili:

| Tipo di Regola | Descrizione |
|-----------|-------------|
| **Richiede** | Quando l'opzione A è selezionata, solo le opzioni elencate sono disponibili nello slot target |
| **Esclude** | Quando l'opzione A è selezionata, le opzioni elencate sono nascoste nello slot target |

Per aggiungere regole:

1. Scorri fino alla sezione **Regole di Compatibilità** sulla scheda Configurazione
2. Clicca **+ Aggiungi Regola**
3. Seleziona l'**opzione sorgente** (il trigger)
4. Scegli il **tipo di regola** (Richiede o Esclude)
5. Seleziona lo **slot target** e le **opzioni interessate**

Puoi anche generare automaticamente le regole dalle etichette di compatibilità assegnate alle opzioni, che è più veloce quando si gestiscono molte combinazioni.

### Passo 5: Crea Preset (Opzionale)

I preset sono configurazioni predefinite che danno ai clienti un punto di partenza rapido:

1. Scorri fino alla sezione **Preset di Configurazione**
2. Clicca **+ Aggiungi Preset**
3. Dà un nome e una descrizione al preset (es. "Costruzione per Gaming", "Inizio Economico")
4. Seleziona le opzioni per ogni slot
5. Carica opzionalmente un'immagine anteprima e segna come **Prestigioso**

I clienti possono iniziare da un preset e poi personalizzare gli slot individuali secondo le loro preferenze.

## Esperienza del Cliente

Quando un cliente visualizza un prodotto configurabile sul vostro negozio online:

1. **Interfaccia del Wizard** — Gli slot vengono presentati come passaggi, guidando il cliente attraverso ogni scelta
2. **Filtraggio** — Le opzioni incompatibili vengono nascoste automaticamente in base alle regole di compatibilità
3. **Badge Popolari** — Le opzioni contrassegnate come popolari mostrano un badge per aiutare nella decisione
4. **Preset** — I preset selezionati appaiono come opzioni di inizio rapido
5. **Aggiornamento del Prezzo** — Il prezzo totale si aggiorna in tempo reale al momento della selezione delle opzioni
6. **Riepilogo** — Un passo di revisione mostra tutte le opzioni selezionate prima di aggiungere al carrello

## Consigli

- Iniziate con la strategia di prezzo "Somma dei Componenti" — è la più intuitiva per i clienti e più facile da mantenere.
- Utilizzate le regole di compatibilità per impedire configurazioni non valide invece di contare sulla conoscenza del cliente.
- Create 2-3 preset per le vostre configurazioni più popolari per ridurre la fatica decisionale.
- Nascondete i prodotti componenti dal negozio online se devono essere disponibili solo attraverso il configuratore.
- Testate il flusso completo di configurazione sul lato frontend dopo l'impostazione per assicurarvi che tutte le regole funzionino come previsto.