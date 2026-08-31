---
title: Audiences
---

Un **Segmento** è un'audience salvata a cui puoi indirizzare una campagna, un percorso o un test A/B — l'elenco dei Segmenti di Campaign Studio li chiama "Audiences mirate" e questa guida utilizza entrambe le parole per indicare la stessa cosa. Ogni segmento è **dinamico**, definito da regole che Spwig ricalcola ogni volta che viene utilizzato, oppure **statico**, un elenco esplicito di iscritti che selezioni manualmente.

Questa guida illustra come creare le regole di un segmento dinamico — inclusi i nuovi campi che mirano ai bucket di valore dei clienti del tuo store, al programma di fedeltà e agli affiliati — e il pulsante **Aggiungi audiences di partenza** che crea un set di segmenti pronti all'uso a partire dai dati già presenti nel tuo store.

## Segmenti dinamici vs. statici

| Tipo | Come funziona | Ideale per |
|---|---|---|
| **Dinamico (regole)** | Definisce condizioni — ad esempio "Spesa totale di almeno $500." Spwig ricalcola chi corrisponde ogni volta che il segmento viene utilizzato, quindi l'appartenenza cambia automaticamente insieme ai tuoi iscritti. | Audiences continue che devono essere sempre aggiornate, come "Clienti VIP" o "Non ha ordinato da 90 giorni." |
| **Statico (elenco fisso)** | Un elenco esplicito di iscritti che aggiungi o rimuovi manualmente. L'appartenenza non cambia mai a meno che tu non la modifichi. | Un elenco una tantum — tutti i partecipanti a un evento specifico, o un gruppo selezionato a mano per un invio unico. |

Scegli il tipo con il campo **Tipo** quando crei un segmento. Il resto di questa guida riguarda i segmenti dinamici — quelli statici sono semplicemente un elenco di membri senza regole da configurare.

## Creare un segmento dinamico

Apri **Campaign Studio > Segmenti**, quindi fai clic su **+ Nuovo segmento** (o apri un segmento dinamico esistente) per accedere al costruttore **Regole audience**. Fai clic su **+ Aggiungi condizione** per aggiungere una regola, scegli cosa verificare e come, e imposta se un iscritto deve corrispondere a **tutte** o a **una qualsiasi** delle tue condizioni. Un conteggio in tempo reale nell'angolo in alto a destra — ad esempio "8 iscritti corrispondenti" — si aggiorna un istante dopo ogni modifica, così puoi vedere esattamente chi soddisfa i criteri prima di salvare.

![Il costruttore delle regole audience con le condizioni Segmento cliente, Livello fedeltà, Valore a vita e Affiliato impostate, e un conteggio in tempo reale degli iscritti corrispondenti](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Una condizione con un controllo fisso di tipo **è vero** — **Ha ordinato**, **Consenso al marketing**, **Membro fedeltà**, **Affiliato** — non richiede nulla oltre alla selezione del campo stesso; non ci sono operatori o valori da impostare.

## Cosa puoi mirare

| Campo | Cosa verifica |
|---|---|
| **Spesa totale** | Totale degli ordini a vita. |
| **Numero di ordini** | Numero di ordini completati. |
| **Valore a vita** | Il valore a vita calcolato del cliente. |
| **Valore medio dell'ordine** | Importo medio per ordine completato. |
| **Giorni dall'ultimo ordine** | Quanto tempo è trascorso dall'ordine più recente del cliente — mira a 90+ giorni per un'audience di win-back. |
| **Ha ordinato** | Se il cliente ha almeno un ordine completato. |
| **Consenso al marketing** | Se l'iscritto ha acconsentito alle email di marketing. |
| **Lingua** | La lingua memorizzata dell'iscritto. |
| **Origine** | Come l'iscritto si è unito — Iscrizione Storefront, Importazione, Ordine, Aggiunta manualmente o API. |
| **Iscritto dopo** | Iscritti che si sono uniti in una data successiva o uguale a quella scelta. |
| **Ha tag** | Se l'iscritto ha un [tag](/help/subscriber-tags) che hai creato. |
| **Segmento cliente** | Se il cliente rientra in uno dei tuoi [segmenti cliente](/help/customer-segments) denominati — Guest Customer, New Customer, Regular Customer, Frequent Buyer, High Value, VIP Customer, Bargain Hunter, At Risk o Inactive. |
| **Membro fedeltà** | Se il cliente è un membro attivo del tuo programma di fedeltà. |
| **Punti fedeltà** | Il saldo attuale dei punti disponibili del membro. |
| **Livello fedeltà** | Il livello di fedeltà attualmente detenuto dal membro. |
| **Affiliato** | Se il cliente è uno dei tuoi partner affiliati attivi. |

**Segmento clienti**, i due campi di valore **Fidelità**, **Livello di fidelità** e **Affiliato** sono aggiunte più recenti e ciascuna viene visualizzata nel selettore di condizioni solo quando il tuo store dispone effettivamente di quel tipo di dati: i campi di fidelità appaiono una volta che il tuo programma di fidelità ha membri e almeno un livello attivo, **Affiliato** appare una volta che hai almeno un affiliato, e **Segmento clienti** appare una volta che hai almeno un segmento clienti attivo configurato.

Non vedrai un'opzione in un store nuovo che non potrebbe potenzialmente corrispondere a nessuno.

Un limite attuale da tenere a mente: per qualsiasi condizione con un menu a discesa di scelte — **Lingua**, **Origine**, **Ha tag**, **Segmento clienti**, **Livello di fidelità** — l'operatore **è uno di** consente ancora di selezionare solo un valore alla volta. Se vuoi corrispondere a più valori (ad esempio, clienti nel tuo segmento VIP o High Value), aggiungi una condizione per ogni valore e imposta **Corrispondenza** su **qualsiasi**.

## Aggiungi pubblici iniziali

Creare una regola da zero per ogni pubblico ovvio — i tuoi VIP, i tuoi membri di fidelità, tutti quelli che sono diventati inattivi — è tedioso quando Spwig può già vedere chi è idoneo. Nell'elenco dei Segmenti, fai clic su **Aggiungi pubblici iniziali** e Spwig crea un set di segmenti dinamici pronti all'uso e modificabili basati sui dati di clienti, fidelità e affiliati che il tuo store ha già.

![L'elenco dei Segmenti con i pulsanti Nuovo Segmento e Aggiungi pubblici iniziali](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Iniziale | Obiettivo | Requisiti |
|---|---|---|
| **Clienti VIP** | Il tuo segmento clienti VIP | Un segmento clienti VIP attivo |
| **Clienti ad alto valore** | I tuoi segmenti clienti VIP e High Value | Un segmento clienti VIP o High Value attivo |
| **Acquirenti ricorrenti** | I tuoi segmenti clienti Frequent Buyer e Regular | Un segmento clienti Frequent Buyer o Regular attivo |
| **Nuovi clienti** | Il tuo segmento clienti New | Un segmento clienti New attivo |
| **Clienti in fase di abbandono** | Clienti che hanno ordinato in passato ma non negli ultimi 90 giorni | Qualsiasi storico ordini dei clienti |
| **Membri di fidelità** | Tutti attivi nel tuo programma di fidelità | Un programma di fidelità attivo con membri |
| **Livello di fidelità superiore** | Membri nel tuo livello di fidelità con il punteggio più alto | Almeno un livello di fidelità attivo |
| **Affiliati** | I tuoi partner affiliati attivi | Almeno un affiliato |

Spwig crea solo gli iniziali per i quali ha effettivamente dati — uno store che non ha ancora un programma di fidelità semplicemente non riceverà un iniziale **Membri di fidelità**, anziché uno vuoto che non potrebbe mai corrispondere a nessuno. Spwig conferma esattamente cosa ha aggiunto, ad esempio: "Aggiunti 7 pubblici iniziali: Clienti ad alto valore, Acquirenti ricorrenti, Nuovi clienti, Clienti in fase di abbandono, Membri di fidelità, Livello di fidelità superiore, Affiliati."

![Messaggio di successo che conferma quali pubblici iniziali sono stati appena aggiunti](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

È sicuro fare clic su **Aggiungi pubblici iniziali** più di una volta. Spwig non crea mai un duplicato di un iniziale che esiste già, quindi fare clic di nuovo dopo aver configurato (ad esempio) il tuo programma di fidelità per la prima volta aggiunge solo ciò che è appena diventato disponibile — se tutto è già configurato, lo comunica semplicemente.

![Messaggio informativo mostrato quando tutti i pubblici iniziali esistono già](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

Se elimini un iniziale che non vuoi, fare clic di nuovo su **Aggiungi pubblici iniziali** non lo ripristinerà — Spwig lo tratta come un segmento che hai rimosso intenzionalmente, non come uno da ricreare.

Una volta creati, un iniziale è un normale segmento dinamico: aprilo dall'elenco per rivedere o regolare le sue regole, rinominarlo o eliminarlo, esattamente come faresti con qualsiasi segmento che hai creato tu stesso.

## A chi raggiungono effettivamente questi pubblici

I requisiti per i clienti, i membri fedeli e gli affiliati sopra indicati corrispondono solo ai sottoscrittori i cui indirizzi email sono collegati a un account cliente: una registrazione alla newsletter anonima non corrisponderà mai a una condizione **Membro fedele** o **VIP**, anche se corretta, poiché Spwig non ha alcun record di ordini o di fedeltà da confrontarla.

Se molti dei tuoi clienti hanno account ma non si sono ancora iscritti, chiedi a colui che gestisce l'installazione di Spwig di eseguire un'azione di sincronizzazione dei sottoscrittori: crea un record Subscriber per ogni account cliente esistente in un unico passaggio, in modo che questi gruppi abbiano persone reali da confrontare.

Indipendentemente dal numero di sottoscrittori che un segmento include, quel numero descrive chi *potrebbe* ricevere una campagna, non chi lo farà. Ogni invio controlla comunque l'autorizzazione al marketing di ciascun sottoscrittore, quindi un segmento non è mai un modo per evitarla.

## Consigli

- Inizia da un gruppo iniziale e apri le regole invece di costruire la stessa regola a mano: una volta creato, un gruppo iniziale non è diverso da qualsiasi segmento che hai costruito tu.
- Le condizioni booleane come **Membro fedele**, **Affiliato** e **Ha effettuato un ordine** non necessitano di un operatore o di un valore: basta aggiungere la condizione e si è pronti.
- Unisci i nuovi campi con i vecchi per un targeting più preciso, ad esempio **Membro fedele** più **Ha optato per il marketing**, invece di basarti solo su una singola condizione.
- Se le regole di un segmento fanno riferimento a qualcosa che è stato rimosso successivamente - un segmento clienti eliminato, un'etichetta svuotata, ecc. - Spwig li considera come non corrispondenti a nessuno, invece di tornare alla tua intera lista di sottoscrittori. Un targeting rotto invia meno persone; non invierà mai a tutti per errore.
- Se il conteggio dei membri di un segmento sembra obsoleto, aprilo e salvalo di nuovo, oppure usa l'azione collettiva **Ricrea il conteggio dei membri** dalla lista Segmenti, per calcolarlo immediatamente.
- Controlla il conteggio in tempo reale dei "sottoscrittori che corrispondono" mentre costruisci una regola: è il modo più veloce per individuare una condizione che è più ristretta (o più ampia) di quanto intendevi prima di salvare.