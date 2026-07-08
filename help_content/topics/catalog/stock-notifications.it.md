---
title: Notifiche di disponibilità
---

Le notifiche di disponibilità permettono ai clienti di iscriversi per ricevere un'email quando un prodotto esaurito torna disponibile. Le impostazioni di visualizzazione della disponibilità controllano ciò che i clienti vedono sulle pagine dei prodotti — ad esempio, etichette di stato della disponibilità, avvisi per disponibilità limitata e ciò che accade quando un prodotto è esaurito.

## Impostazioni di visualizzazione della disponibilità

Le impostazioni di visualizzazione della disponibilità sono impostazioni predefinite a livello di negozio che si applicano a tutti i prodotti, a meno che non siano sovrascritte a livello di categoria o prodotto.

Passa a **Catalogo > Impostazioni di visualizzazione della disponibilità** per configurare queste opzioni. Esiste un'unica voce di impostazione per il tuo negozio — clicca per modificarla.

### Visualizzazione dello stato della disponibilità

| Impostazione | Descrizione |
|---------|-------------|
| **Mostra stato della disponibilità** | Mostra le etichette "In stock" o "Out of stock" sulle pagine dei prodotti |
| **Mostra avviso per disponibilità limitata** | Mostra un messaggio "Solo X rimasti" quando la disponibilità è bassa |
| **Limite di disponibilità limitata** | La quantità a cui o al di sotto della quale compare l'avviso per disponibilità limitata (predefinito: 5) |
| **Mostra quantità esatta** | Mostra il numero esatto rimanente (es. "Solo 3 rimasti!") invece di un avviso generico |

### Comportamento per prodotti esauriti

L'impostazione **Azione per prodotti esauriti** determina ciò che i clienti vedono quando un prodotto non è disponibile:

| Azione | Cosa vedono i clienti |
|--------|-------------------|
| **Nascondi dalla lista** | Il prodotto viene rimosso dalle pagine delle categorie e dai risultati di ricerca |
| **Mostra come non disponibile** | Il prodotto è visibile ma non può essere aggiunto al carrello |
| **Mostra pulsante "Notificalo"** | I clienti possono registrare il loro indirizzo email per essere notificati quando la disponibilità torna |
| **Permetti ordini in attesa** | I clienti possono acquistare il prodotto anche quando la disponibilità è zero |

Imposta **Messaggio per prodotti esauriti** per personalizzare il testo visualizzato quando un prodotto non è disponibile (predefinito: `Out of Stock`).

Imposta **Messaggio per ordini in attesa** per personalizzare il testo visualizzato per i prodotti ordinabili in attesa (predefinito: `Available on backorder`).

### Visualizzazione di spedizione e consegna

| Impostazione | Descrizione |
|---------|-------------|
| **Mostra "Spedizione da"** | Mostra il nome del magazzino sulla pagina del prodotto |
| **Mostra data stimata di consegna** | Mostra le date stimata di consegna calcolate in base alla posizione del magazzino |

### Permetti ordini in attesa (a livello di sito)

Seleziona **Permetti ordini in attesa** per permettere ai clienti di acquistare qualsiasi prodotto esaurito di default. I singoli prodotti e le categorie possono sovrascrivere questa impostazione.

## Notifiche di ritorno in stock

Quando imposti l'azione per prodotti esauriti su **Mostra pulsante "Notificalo"**, i clienti possono inserire il loro indirizzo email sulla pagina del prodotto per ricevere un'email quando il prodotto torna in stock.

### Visualizzazione delle richieste di notifica

Passa a **Catalogo > Notifiche di disponibilità** per visualizzare tutte le richieste di notifica dei clienti. Ogni voce mostra:
- Indirizzo email del cliente
- Prodotto e variante (se applicabile)
- Magazzino preferito (se il cliente ha selezionato una preferenza regionale)
- Quando è stata creata la richiesta
- Quando è stata inviata la notifica (vuoto se non è ancora stata inviata)

### Quando vengono inviate le notifiche

Spwig invia automaticamente le email di ritorno in stock quando il livello di stock di un prodotto supera zero. Il campo **Notificato il** registra quando è stata inviata l'email.

I clienti ricevono una sola email di notifica. Una volta notificati, devono iscriversi nuovamente se il prodotto torna esaurito una seconda volta.

### Filtrare le richieste di notifica

Utilizza i filtri dell'amministratore per trovare:
- Richieste per un prodotto specifico
- Richieste già notificate (per vedere chi è stato contattato)
- Richieste ancora in attesa (clienti in attesa di un ritorno in stock)

## Sovrascritture a livello di prodotto

Le impostazioni di visualizzazione della disponibilità a livello di sito possono essere sovrascritte per prodotto o categoria. Nel modulo di modifica del prodotto, cerca la sezione **Disponibilità** dove puoi impostare un'azione specifica per prodotti esauriti diversa da quella predefinita a livello globale.

Questo è utile quando si desidera che la maggior parte dei prodotti permetta ordini in attesa, ma mantenere alcuni prodotti impostati su "Notificalo" — o quando un prodotto specifico dovrebbe essere nascosto quando è esaurito.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Imposta **Low Stock Threshold** sul punto di riordino che utilizzi di solito, in modo che i clienti vengano avvisati della limitata disponibilità prima che tu esaurisca completamente il prodotto.
- Utilizza l'opzione **Show "Notify Me" button** invece di nascondere i prodotti esauriti — i clienti che si iscrivono rappresentano una domanda reale che può giustificare un ordine di rifornimento.
- Abilita **Show Exact Quantity** con moderazione.

Per la maggior parte dei negozi, mostrare "Solo 3 rimasti!" funziona meglio rispetto alla visualizzazione del numero esatto, poiché crea urgenza senza rivelare l'intero quadro delle scorte.
- Controlla l'elenco delle notifiche di scorte prima di effettuare un nuovo ordine — il numero di richieste di notifica pendenti ti dice quanto sia la domanda per quel prodotto.
- Se utilizzi gli ordini su richiesta, aggiorna il tuo **Backorder Message** per impostare aspettative accurate (es. "Spedizione in 2-3 settimane — ordina ora per riservare il tuo posto").
- Combina le notifiche per prodotti esauriti con il marketing via email: quando rifornisci un prodotto popolare, invia una campagna a tutti coloro che si sono iscritti, non solo all'email di notifica automatica.