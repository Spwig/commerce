---
title: Disponibilità per regione
---

La disponibilità per regione controlla quali dei vostri Reparti commerciali un prodotto può essere venduto, e come gli acquirenti al di fuori di tali aree esperiscono il vostro catalogo. Utilizzatelo quando un prodotto è autorizzato solo per alcuni paesi, quando lo stock è riservato a un mercato locale o quando state lanciando un nuovo prodotto in modo regione per regione.

Questo si basa sui **Reparti commerciali**, che raggruppano i paesi in mercati denominati (vedere la guida sui Reparti commerciali per la configurazione). Una volta che i vostri reparti esistono, potete limitare i singoli prodotti a essi e decidere come appaiono i prodotti limitati agli acquirenti che non possono acquistarli.

## Limitare un prodotto a specifiche aree

Ogni prodotto ha un'impostazione di **Disponibilità per regione** nella sua pagina di modifica. Aprire **Prodotti > Tutti i prodotti**, selezionare un prodotto e trovarlo nella sezione **Stato** insieme a **Stato**, **In evidenza** e **Nascondi dal negozio**.

![La sezione Stato del modulo di modifica del prodotto, con l'elenco a discesa Disponibilità per regione impostato su "Solo nelle regioni selezionate" insieme a In evidenza e Nascondi dal negozio](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Opzione | Cosa significa |
|--------|----------------|
| **Disponibile in tutte le aree** | Nessuna restrizione. Il prodotto viene venduto ovunque. Questa è l'impostazione predefinita per ogni prodotto. |
| **Solo nelle aree selezionate** | Un elenco di autorizzazioni. Il prodotto viene venduto solo nelle aree che selezionate qui sotto - ovunque altro, viene considerato non disponibile. |
| **Tutte le aree tranne quelle selezionate** | Un elenco di divieti. Il prodotto viene venduto ovunque *tranne* le aree che selezionate qui sotto. |

### Scegliere le aree

Sotto la sezione Stato, una tabella intitolata **Disponibilità per regione (aree selezionate)** elenca le aree a cui si applica la modalità sopra.

1. Impostare **Disponibilità per regione** su **Solo nelle aree selezionate** o **Tutte le aree tranne quelle selezionate**.
2. Nella tabella **Disponibilità per regione (aree selezionate)**, fare clic su **Aggiungi un'altra area** e scegliere un Reparto commerciale.
3. Ripetere per ogni area che si desidera aggiungere.
4. Fare clic su **Salva**.

![La tabella inline "Disponibilità per regione (aree selezionate)" con le righe Nord America e Europa aggiunte](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

Se **Disponibilità per regione** è impostata su **Disponibile in tutte le aree**, tutto ciò che è in questa tabella viene ignorato - cancellare prima l'opzione di modalità se si desidera rimuovere una restrizione senza eliminare le righe.

Per un'anteprima a livello di catalogo di ogni regola di regione di ogni prodotto in un unico elenco (utile quando si effettua un'ispezione di molti prodotti contemporaneamente), andare su **Visibilità del prodotto per regione** all'indirizzo `/admin/catalog/productregionvisibility/`.

## Mostrare agli acquirenti dove un prodotto non viene spedito

Quando la regione di un acquirente non corrisponde alle regole di disponibilità del prodotto, potete controllare cosa vedono negli **Impostazioni per la visualizzazione del magazzino**, nella sezione **Disponibilità per regione**. Questa pagina non ha ancora un collegamento diretto nella barra laterale - apritela direttamente all'indirizzo `/admin/catalog/stockdisplaysettings/`.

![Impostazioni per la visualizzazione del magazzino, sezione Disponibilità per regione - l'elenco a discesa per la visualizzazione delle aree limitate, impostato su "Mostra, contrassegnato come non disponibile"](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Opzione | Cosa vedono gli acquirenti |
|--------|---------------------------|
| **Mostra, contrassegnato come non disponibile** (predefinito) | Il prodotto appare comunque negli elenchi, con un badge "Non disponibile" e un avviso "Non viene spedito in [regione]" al posto del pulsante Aggiungi al carrello. Un banner apparirà anche in cima alle pagine degli elenchi ("Alcuni prodotti non vengono spediti in [destinazione]") con un collegamento per filtrare solo gli articoli che vi vengono spediti. |
| **Nascondi dagli elenchi** | Il prodotto viene rimosso dagli elenchi e dai risultati di ricerca per gli acquirenti di questa area. |

![Elenco prodotti del negozio che spedisce in Europa - il banner "Alcuni prodotti non vengono spediti in Europa" sopra la griglia, e una scheda prodotto contrassegnata "Non disponibile" con un avviso "Non viene spedito in Europa"](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

La pagina di un prodotto ristretto mostra sempre un avviso "Questo prodotto non viene spedito in [area]" quando uno shopper vi arriva direttamente (ad esempio, da un collegamento condiviso o da un risultato del motore di ricerca) — questo vale indipendentemente dall'opzione di elenco scelta, poiché un collegamento diretto evita l'elenco completamente.

## Consentire agli acquirenti di scegliere o scoprire la propria area

Spwig può rilevare automaticamente l'area dello shopper e offrire un cambio, e puoi aggiungere un selettore in modo che gli acquirenti possano cambiarlo da soli in qualsiasi momento.

### Prima di iniziare

Hai bisogno di due cose configurate per il rilevamento e lo scambio dell'area funzionino correttamente:

1. **Aree di vendita** — i paesi in ogni area e la valuta predefinita di ogni area. Se non vedi **Aree di vendita** sotto **Inventario** nella barra laterale, attiva **Abilita Multi-warehouse** sotto **Impostazioni > Impostazioni del negozio > E-commerce** per rivelare il collegamento del menu (non hai bisogno di utilizzare davvero più warehouse — questo settaggio sblocca solo l'elemento del menu). Puoi inoltre andare direttamente a `/admin/catalog/salesregion/`.
2. **Paesi di spedizione** — i paesi a cui il tuo negozio effettivamente invia. Di solito sono già in atto: ogni paese che aggiungi a un'Area di spedizione viene automaticamente aggiunto anche qui. Per esaminare o modificare manualmente l'elenco, apri direttamente `/admin/shipping/shippingcountry/` (non ha ancora un collegamento nella barra laterale).

### La conferma automatica dell'area

Spwig rileva l'area dello shopper dalla loro posizione e la applica automaticamente. Quando ciò li colloca in un'area *diversa* dal mercato predefinito (principale) del tuo negozio — e hai due o più Aree di vendita attive — Spwig mostra una conferma alla loro prima visita in modo che sappiano in quale area si trovano e possano cambiarla:

> **Abbiamo impostato la tua area su [Area]**
> Abbiamo scelto questa in base alla tua posizione in modo che vedrai i prodotti e i prezzi giusti. Non è corretto? Scegli il tuo paese.
> Spedisce a: [selettore del paese]  **[Continua a navigare]**

![Il modulo di conferma "Abbiamo impostato la tua area su Nord America" sul negozio, con un selettore del paese "Spedisce a" e un pulsante "Continua a navigare"](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Scegliendo un paese diverso nel selettore, li sposta immediatamente. Se lo si ignora o si clicca su **Continua a navigare**, mantiene la loro area attuale, e non verrà chiesto nuovamente su quel browser. I visitatori che si trovano già nell'area predefinita del tuo negozio non vedranno affatto la conferma.

### Aggiunta di un selettore per la consegna nella testata o nel piè di pagina

Se preferisci far sì che gli acquirenti possano modificare l'area da soli in qualsiasi momento (anziché basarsi solo sull'avviso automatico), aggiungi il widget **Selettore per la consegna** nella testata o nel piè di pagina.

1. Vai a **Progettazione > Costruttore della testata** (o **Costruttore del piè di pagina**).
2. Trascina il widget **Selettore per la consegna** dalla Libreria widget in una riga.
3. Clicca su **Salva**.

![La libreria widget del Costruttore della testata con il gruppo Shop evidenziato, che mostra il widget Selettore per la consegna insieme a Shopping Cart, Account Menu e Language Selector](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

Il widget non ha bisogno di configurazione — elenca automaticamente i Paesi di spedizione attivi, e mostra la scelta attuale dello shopper (o il paese rilevato da GeoIP, se non ha ancora scelto un paese). Scegliendo un paese diverso, aggiorna immediatamente l'area e ricarica l'accessibilità e i prezzi dei prodotti della pagina.

Il Selettore per la consegna non ha ancora un modulo di impostazioni dedicato. Se desideri modificare lo stile del pulsante (outline, solido o trasparente) o nascondere l'etichetta "Spedisce a", apri le impostazioni del widget nel costruttore e modifica direttamente il campo **Configurazione personalizzata (JSON)**, utilizzando `button_style` e `show_label`.

### La valuta segue l'area

Se il tuo negozio supporta più di una valuta (impostata sotto **Impostazioni > Multi-Currency**), lo scambio dell'area — sia attraverso l'avviso che il Selettore per la consegna — cambia anche la valuta visualizzata con la valuta predefinita di quell'area.

Se il tuo negozio ha solo una valuta, o non ha abilitato esplicitamente una seconda, la valuta rimane invariata quando uno shopper cambia area.

## Suggerimenti

- Lascia **Disponibilità per area** su **Disponibile in tutte le aree** a meno che tu non abbia un motivo specifico per limitare un prodotto: è l'opzione più semplice e non richiede manutenzione quando aggiungi nuove aree.
- Usa **Solo in aree selezionate** per un elenco di autorizzazioni piccolo (ad esempio, un prodotto che viene lanciato in un singolo paese per primo) e **Tutte le aree tranne quelle selezionate** per un elenco di blocchi piccolo (ad esempio, ovunque tranne un paese in cui l'oggetto non è autorizzato) - scegli quello che ha bisogno di meno righe per la configurazione.
- Se gli acquirenti segnalano che un prodotto manca ma dovrebbe essere visibile, controlla sia la configurazione **Disponibilità per area** del prodotto, che se il loro paese è incluso in un **Area di vendita** attivo e in un **Paese di spedizione** attivo.
- **Nascondi dagli elenchi** mantiene il tuo catalogo pulito per gli acquirenti che non possono acquistare certi articoli, ma significa anche che merchandising e ricerche appariranno più vuoti in quelle aree: **Mostra, contrassegnato come non disponibile** è solitamente meglio se vuoi comunque che gli acquirenti esplorino l'intero catalogo, anche dove non possono effettuare l'acquisto.
- Prova il comportamento delle aree aggiungendo il Selettore di spedizione nella testata e passando tra i paesi da te stesso prima di affidarti alla rilevazione GeoIP durante un lancio.
- Imposta i valori di priorità delle tue aree in modo deliberato - l'area attiva con la priorità più alta è il fallback per gli acquirenti il cui paese non può essere rilevato o non corrisponde a nessuna area.