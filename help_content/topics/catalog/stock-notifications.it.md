---
title: Notifiche di scorte
---

Le notifiche di scorte consentono ai clienti di registrarsi per ricevere un'email quando un prodotto esaurito torna disponibile. Le impostazioni di visualizzazione delle scorte controllano ciò che i clienti vedono nelle pagine prodotto — come etichette di stato delle scorte, avvisi di scorte basse e cosa accade quando un prodotto si esaurisce.

## Impostazioni di visualizzazione delle scorte

Le impostazioni di visualizzazione delle scorte sono valori predefiniti a livello di negozio che si applicano a tutti i prodotti, a meno che non vengano sovrascritti a livello di categoria o prodotto.

Accedi a **Catalogo > Impostazioni di visualizzazione delle scorte** per configurare queste opzioni. C'è un record di impostazioni per il tuo negozio — cliccalo per modificarlo.

### Visualizzazione dello stato delle scorte

| Impostazione | Descrizione |
|---------|-------------|
| **Mostra stato delle scorte** | Visualizza le etichette "Disponibile" o "Esaurito" nelle pagine prodotto |
| **Mostra avviso scorte basse** | Mostra un messaggio "Solo X rimasti" quando le scorte stanno per esaurirsi |
| **Soglia scorte basse** | La quantità a o sotto la quale appare l'avviso di scorte basse (predefinito: 5) |
| **Mostra quantità esatta** | Mostra il numero esatto rimanente (es. "Solo 3 rimasti!") invece di un avviso generico |

### Comportamento per prodotti esauriti

L'impostazione **Azione per prodotto esaurito** determina cosa vedono i clienti quando un prodotto non ha scorte disponibili:

| Azione | Cosa vedono i clienti |
|--------|-------------------|
| **Nascondi dalle liste** | Il prodotto viene rimosso dalle pagine di categoria e dai risultati di ricerca |
| **Mostra come non disponibile** | Il prodotto è visibile ma non può essere aggiunto al carrello |
| **Mostra pulsante "Avvisami"** | I clienti possono registrare la loro email per essere avvisati quando le scorte tornano |
| **Consenti ordini anticipati** | I clienti possono acquistare il prodotto anche quando le scorte sono a zero |

Imposta **Messaggio per prodotto esaurito** per personalizzare il testo mostrato quando un prodotto non è disponibile (predefinito: `Esaurito`).

Imposta **Messaggio per ordini anticipati** per personalizzare il testo mostrato per i prodotti acquistabili in anticipo (predefinito: `Disponibile in ordine anticipato`).

### Visualizzazione di spedizione e consegna

| Impostazione | Descrizione |
|---------|-------------|
| **Mostra posizione "Spedito da"** | Visualizza il nome del magazzino nella pagina prodotto |
| **Mostra consegna stimata** | Visualizza le date di consegna stimate calcolate dalla posizione del magazzino |

### Consenti ordini anticipati (a livello di sito)

Seleziona **Consenti ordini anticipati** per consentire ai clienti di acquistare qualsiasi prodotto esaurito in modo predefinito. I singoli prodotti e le categorie possono sovrascrivere questa impostazione.

## Notifiche di riapprovvigionamento

Quando imposti l'azione per prodotto esaurito su **Mostra pulsante "Avvisami"**, i clienti possono inserire il loro indirizzo email nella pagina prodotto per ricevere un'email quando il prodotto viene riapprovvigionato.

### Visualizzazione delle richieste di notifica

Accedi a **Catalogo > Notifiche di scorte** per vedere tutte le richieste di notifica dei clienti. Ogni record mostra:
- Indirizzo email del cliente
- Prodotto e variante (se applicabile)
- Magazzino preferito (se il cliente ha selezionato una preferenza regionale)
- Quando la richiesta è stata creata
- Quando la notifica è stata inviata (vuoto se non ancora inviata)

### Quando vengono inviate le notifiche

Spwig invia automaticamente le email di riapprovvigionamento quando il livello di scorte di un prodotto supera lo zero. Il campo **Notificato il** registra quando l'email è stata inviata.

I clienti ricevono una sola email di notifica. Una volta avvisati, devono registrarsi di nuovo se il prodotto si esaurisce una seconda volta.

Se preferisci inviare più di un semplice avviso — ad esempio, mostrando il prodotto riapprovvigionato con un blocco di contenuto **Prodotto in evidenza**, o facendo un follow-up un giorno dopo — crea un percorso **Prodotto di nuovo disponibile** in **Campaign Studio > Percorsi** e impostalo su **Attivo**. Una volta che quel percorso esiste, i clienti in attesa vengono iscritti ad esso invece di ricevere l'email una tantum semplice; senza un percorso attivo, questa email una tantum continua a essere inviata esattamente come descritto sopra. Vedi [Percorsi attivati](/help/triggered-journeys) per come funziona il trigger.

### Filtraggio delle richieste di notifica

Usa i filtri di amministrazione per trovare:
- Richieste per un prodotto specifico
- Richieste che sono già state notificate (per vedere chi è stato contattato)
- Richieste che sono ancora in attesa (clienti in attesa di un riapprovvigionamento)

## Override a livello prodotto

Le impostazioni per la visualizzazione del magazzino a livello del sito possono essere sovrascritte per prodotto o categoria. Nel modulo di modifica del prodotto, cerca la sezione **Stock** dove puoi impostare un'**azione di sottoscrizione** specifica del prodotto che differisce dal default globale.

Questo è utile quando si desidera che la maggior parte dei prodotti consenta gli ordini di riapprovvigionamento, ma si tengono alcuni prodotti impostati su "Notifica quando disponibile" - oppure quando un prodotto specifico deve essere nascosto quando non è disponibile.

## Suggerimenti

- Imposta **Soglia di scorta bassa** al punto di riapprovvigionamento che di solito utilizzi, in modo che i clienti vengano avvisati sulla disponibilità limitata prima che tu esaurisca completamente.
- Usa l'opzione **Mostra pulsante "Notifica quando disponibile"** invece di nascondere i prodotti non disponibili - i clienti che si iscrivono rappresentano un reale bisogno che può giustificare un ordine di riapprovvigionamento.
- Attiva **Mostra quantità esatta** con parsimonia. Per la maggior parte dei negozi, mostrare "Solo 3 a disposizione!" funziona meglio rispetto a mostrare il numero esatto, in quanto crea urgenza senza rivelare l'intero quadro del tuo inventario.
- Controlla l'elenco delle notifiche sullo stock prima di effettuare un nuovo ordine - il numero di richieste di notifica in sospeso ti dice quanto sia la domanda esistente per quel prodotto.
- Se utilizzi gli ordini di riapprovvigionamento, aggiorna il tuo **Messaggio sugli ordini di riapprovvigionamento** per stabilire aspettative accurate (es. "Spedizione in 2-3 settimane - ordina ora per riservare il tuo posto").
- Unisci le notifiche sugli stock esauriti con la marketing via email: quando rifornisci un prodotto popolare, invia una campagna a tutti coloro che si sono iscritti, non solo alla email di notifica automatica.