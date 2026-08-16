---
title: Notifiche sullo stock
---

Le notifiche sull'approvvigionamento consentono ai clienti di iscriversi per ricevere un'email quando un prodotto esaurito diventa nuovamente disponibile. Le impostazioni per la visualizzazione dello stock controllano cosa vedono i clienti sulle pagine dei prodotti - ad esempio, etichette sullo stato dello stock, avvisi per stock basso e cosa accade quando un prodotto si esaurisce.

## Impostazioni per la visualizzazione dello stock

Le impostazioni per la visualizzazione dello stock sono le impostazioni predefinite per l'intero negozio che si applicano a tutti i prodotti, a meno che non vengano sovrascritte a livello di categoria o prodotto.

Vai a **Catalogo > Impostazioni per la visualizzazione dello stock** per configurare queste opzioni. Esiste un record di impostazioni per il tuo negozio - cliccalo per modificare.

### Visualizzazione dello stato dello stock

| Impostazione | Descrizione |
|---------|-------------|
| **Mostra stato dello stock** | Visualizza etichette "In magazzino" o "Esaurito" sulle pagine dei prodotti |
| **Mostra avviso per stock basso** | Visualizza un messaggio "Ne rimangono solo X" quando lo stock sta per esaurirsi |
| **Soglia per stock basso** | La quantità a cui o al di sotto della quale appare l'avviso per stock basso (predefinito: 5) |
| **Mostra quantità esatta** | Visualizza il numero esatto rimanente (ad esempio, "Ne rimangono solo 3!") invece di un avviso generico |

### Comportamento per prodotti esauriti

L'impostazione **Azione per prodotti esauriti** determina cosa vedono i clienti quando un prodotto non ha più scorte:

| Azione | Cosa vedono i clienti |
|--------|-------------------|
| **Nascondi dagli elenchi** | Il prodotto viene rimosso dalle pagine della categoria e dai risultati della ricerca |
| **Mostra come non disponibile** | Il prodotto è visibile ma non può essere aggiunto al carrello |
| **Mostra pulsante "Notificami"** | I clienti possono registrare la loro email per ricevere una notifica quando lo stock torna disponibile |
| **Consenti ordinazioni in backorder** | I clienti possono acquistare il prodotto anche quando lo stock è zero |

Imposta **Messaggio per prodotti esauriti** per personalizzare il testo visualizzato quando un prodotto non è disponibile (predefinito: `Esaurito`).

Imposta **Messaggio per backorder** per personalizzare il testo visualizzato per i prodotti che accettano backorder (predefinito: `Disponibile in backorder`).

### Visualizzazione della spedizione e consegna

| Impostazione | Descrizione |
|---------|-------------|
| **Mostra luogo "Spedito da"** | Visualizza il nome del magazzino sulla pagina del prodotto |
| **Mostra consegna stimata** | Visualizza le date di consegna stimata calcolate dal luogo del magazzino |

### Consentire gli ordini in backorder (a livello di sito)

Seleziona **Consenti backorder** per consentire ai clienti di acquistare qualsiasi prodotto esaurito di default. I prodotti e le categorie singoli possono sovrascrivere questo settaggio.

## Notifiche per rientro a magazzino

Quando imposti l'azione per prodotti esauriti su **Mostra pulsante "Notificami"**, i clienti possono inserire l'indirizzo email sulla pagina del prodotto per ricevere un'email quando il prodotto torna disponibile.

### Visualizzazione delle richieste di notifica

Vai a **Catalogo > Notifiche sull'approvvigionamento** per vedere tutte le richieste di notifica dei clienti. Ogni record mostra:
- Indirizzo email del cliente
- Prodotto e variante (se applicabile)
- Deposito preferito (se il cliente ha selezionato una preferenza regionale)
- Quando la richiesta è stata creata
- Quando la notifica è stata inviata (vuoto se non ancora inviata)

### Quando vengono inviate le notifiche

Spwig invia automaticamente le email per rientro a magazzino quando il livello di scorte del prodotto supera lo zero. Il campo **Notificato il** registra quando è stata inviata l'email.

I clienti ricevono una notifica via email. Dopo aver ricevuto la notifica, devono iscriversi nuovamente se il prodotto esaurisce nuovamente le scorte.

### Filtraggio delle richieste di notifica

Utilizza i filtri dell'amministratore per trovare:
- Richieste per un prodotto specifico
- Richieste che sono state già notificate (per vedere chi è stato contattato)
- Richieste che sono ancora in sospeso (clienti in attesa di rifornimento)

## Override a livello di prodotto

Le impostazioni per la visualizzazione dello stock a livello di sito possono essere sovrascritte a livello di prodotto o categoria. Nel modulo di modifica del prodotto, cerca la sezione **Stock** dove puoi impostare un'**Azione per prodotti esauriti** specifica del prodotto che differisce dal default globale.

Questo è utile quando si desidera che la maggior parte dei prodotti consenta backorder ma si mantengano alcuni prodotti impostati su "Notificami" - oppure quando un prodotto specifico deve essere nascosto quando esaurito.

## Suggerimenti

Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Imposta **Soglia Scorte Minime** al punto di rifornimento che utilizzi di solito, in modo che i clienti vengano avvisati della disponibilità limitata prima che finiscano completamente.
- Usa l'opzione **Mostra pulsante "Avvisami"** invece di nascondere i prodotti non in magazzino: i clienti che si iscrivono rappresentano una domanda reale che può giustificare un ordine di rifornimento.
- Attiva **Mostra Quantità Esatta** con parsimonia.

Per la maggior parte dei negozi, mostrare "Non ne rimangono che 3!" funziona meglio rispetto a mostrare il numero esatto, in quanto crea urgenza senza rivelare l'intero quadro delle tue scorte.
- Controlla l'elenco delle notifiche sulle scorte prima di effettuare un nuovo ordine: il numero di richieste di notifica in sospeso ti dice quanto sia la domanda esistente per quel prodotto.
- Se utilizzi gli ordini di riserva, aggiorna il tuo **Messaggio sugli Ordini di Riserva** per stabilire aspettative accurate (ad esempio: "Spedizione in 2-3 settimane - ordina ora per riservare il tuo posto").
- Unisci le notifiche sui prodotti non in magazzino con la marketing via email: quando rifornisci un prodotto popolare, invia una campagna a tutti coloro che si sono iscritti, non solo alla email di notifica automatica.