---
title: Disponibilità per regione
---

La disponibilità per regione controlla quali dei tuoi Reparti commerciali un prodotto può essere venduto, e come i clienti al di fuori di queste aree esperiscono il tuo catalogo. Utilizzalo quando un prodotto è autorizzato solo per alcuni paesi, quando lo stock è riservato a un mercato locale o quando stai lanciando un nuovo prodotto in modo regione per regione.

Questo si basa sui **Reparti commerciali**, che raggruppano i paesi in mercati denominati (vedi la guida sui Reparti commerciali per impostarli). Una volta che esistono le tue aree, puoi limitare i singoli prodotti a queste e decidere come appaiono i prodotti limitati ai clienti che non possono acquistarli.

## Limitare un prodotto a specifiche aree

Ogni prodotto ha un'impostazione **Disponibilità per regione** nella sua pagina di modifica. Apri **Prodotti > Tutti i prodotti**, seleziona un prodotto e trovalo nella sezione **Stato** insieme a **Stato**, **In evidenza** e **Nascondi dal negozio**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Pagina di modifica prodotto con la sezione Stato, con l'elenco a discesa Disponibilità per regione visibile e impostato su "Solo nelle aree selezionate"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Usa un prodotto con almeno 2 aree già selezionate, in modo che nella seconda immagine la tabella abbia righe visibili.
-->

| Opzione | Cosa significa |
|--------|---------------|
| **Disponibile in tutte le aree** | Nessuna restrizione. Il prodotto viene venduto ovunque. Questa è l'impostazione predefinita per ogni prodotto. |
| **Solo nelle aree selezionate** | Un elenco di autorizzazioni. Il prodotto viene venduto solo nelle aree che selezioni qui sotto - ovunque altro, viene considerato non disponibile. |
| **Tutte le aree tranne quelle selezionate** | Un elenco di divieti. Il prodotto viene venduto ovunque *tranne* le aree che selezioni qui sotto. |

### Scegliere le aree

Sotto la sezione Stato, una tabella intitolata **Disponibilità per regione (aree selezionate)** elenca le aree a cui si applica la modalità sopra.

1. Imposta **Disponibilità per regione** su **Solo nelle aree selezionate** o **Tutte le aree tranne quelle selezionate**.
2. Nella tabella **Disponibilità per regione (aree selezionate)**, fai clic su **Aggiungi un'altra area** e scegli un Reparto commerciale.
3. Ripetilo per ogni area che desideri aggiungere.
4. Fai clic su **Salva**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: La tabella "Disponibilità per regione (aree selezionate)" con due o tre righe di aree aggiunte
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Se **Disponibilità per regione** è impostato su **Disponibile in tutte le aree**, tutto ciò che c'è in questa tabella viene ignorato - cancella prima l'elenco a discesa della modalità se desideri rimuovere una restrizione senza eliminare le righe.

Per un'anteprima a livello di catalogo di ogni regola delle aree di ogni prodotto in un elenco unico (utile quando si effettua un'ispezione di molti prodotti contemporaneamente), vai su **Visibilità dei prodotti per regione** all'indirizzo `/admin/catalog/productregionvisibility/`.

## Mostrare ai clienti dove un prodotto non viene spedito

Quando la regione del cliente non corrisponde alle regole di disponibilità del prodotto, controlli cosa vedono nei **Impostazioni visualizzazione stock**, nella sezione **Disponibilità per regione**. Questa pagina non ha ancora un collegamento nella barra laterale - apri direttamente all'indirizzo `/admin/catalog/stockdisplaysettings/`.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: Modifica del modulo Impostazioni visualizzazione stock con la sezione "Disponibilità per regione", che mostra la casella di selezione per la visualizzazione limitata alla regione
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Mantieni tutta la formattazione markdown, i percorsi immagine, i blocchi di codice e i termini tecnici.

| Opzione | Cosa vedono gli acquirenti |
|--------|-------------------|
| **Mostra, contrassegnato come non disponibile** (impostazione predefinita) | Il prodotto appare ancora nelle liste, con un'etichetta "Non disponibile" e un avviso "Non viene spedito in [area]" al posto del pulsante "Aggiungi al carrello". Viene inoltre visualizzato un banner in cima alle pagine delle liste ("Alcuni prodotti non vengono spediti in [destinazione]") con un collegamento per filtrare solo i prodotti che vengono spediti lì. |
| **Nascondi dalle liste** | Il prodotto viene rimosso completamente dalle liste e dai risultati di ricerca per gli acquirenti in quella zona. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Elenco prodotti del negozio con il banner della zona in cima e almeno una scheda prodotto che mostra l'etichetta "Non disponibile" e l'avviso "Non viene spedito in [area]"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Richiede una selezione della zona di consegna attiva (o rilevamento GeoIP) che risolva in una zona da cui un prodotto dimostrativo è limitato.
-->

Un prodotto limitato mostra sempre un avviso "Questo prodotto non viene spedito in [area]" quando un acquirente vi arriva direttamente (ad esempio, da un collegamento condiviso o da un risultato del motore di ricerca) — questo si applica indipendentemente dall'opzione di elenco scelta sopra, poiché un collegamento diretto evita l'elenco.

## Consentire agli acquirenti di scegliere o scoprire la propria zona

Spwig può rilevare automaticamente la zona dell'acquirente e offrire un cambio, e puoi aggiungere un selettore in modo che gli acquirenti possano cambiarlo in qualsiasi momento.

### Prima di iniziare

Hai bisogno di due cose configurate correttamente per il rilevamento e lo scambio della zona:

1. **Zone di vendita** — i paesi in ciascuna zona e la valuta predefinita di ciascuna zona. Se non vedi **Zone di vendita** sotto **Inventario** nella barra laterale, attiva **Abilita più magazzini** sotto **Impostazioni > Impostazioni del negozio > E-commerce** per rivelare il collegamento del menu (non hai bisogno di utilizzare davvero più magazzini — questo settaggio sblocca solo l'elemento del menu). Puoi inoltre andare direttamente a `/admin/catalog/salesregion/`.
2. **Paesi di consegna** — i paesi a cui il tuo negozio effettivamente invia le consegne. Di solito sono già in atto: ogni paese che aggiungi a un'Area di consegna viene automaticamente aggiunto anche qui. Per verificare o modificare manualmente l'elenco, apri direttamente `/admin/shipping/shippingcountry/` (non ha ancora un collegamento nella barra laterale).

### La conferma automatica della zona

Spwig rileva la zona dell'acquirente dalla loro posizione e la applica automaticamente. Quando ciò li colloca in una zona *diversa* dal mercato predefinito (primario) del tuo negozio — e hai due o più Zone di vendita attive — Spwig mostra una conferma alla loro prima visita in modo che sappiano in quale zona si trovano e possano cambiarla:

> **Abbiamo impostato la tua zona su [Zona]**
> Abbiamo scelto questa in base alla tua posizione per mostrarti i prodotti e i prezzi giusti. Non è corretto? Scegli il tuo paese.
> Spedisce a: [selettore del paese]  **[Continua a navigare]**

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: Modale "Abbiamo impostato la tua zona su [Zona]" sulla homepage del negozio, con il selettore del paese e il pulsante Continua a navigare
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Richiede GeoIP risolvendo in una zona non predefinita e almeno 2 Zone di vendita attive per attivarlo. Localmente, imposta un cookie "geo_country" a un paese non predefinito per simulare.
-->

Scegliendo un paese diverso nel selettore, vengono spostati immediatamente. Se si annulla o si fa clic su **Continua a navigare**, viene mantenuta la zona corrente, e non verrà chiesto nuovamente su quel browser. I visitatori che si trovano già nella zona predefinita non vengono affatto mostrati con la conferma.

### Aggiunta di un selettore di consegna nel tuo header o footer

Se preferisci far sì che gli acquirenti possano modificare la zona in qualsiasi momento (anziché basarsi solo sull'avviso automatico), aggiungi il widget **Selettore di consegna** nell'header o nel footer.

1.

Vai su **Progettazione > Costruttore intestazione** (o **Costruttore piè di pagina**).
2.

Trascina il widget **Selettore Spedisci a** dalla Libreria widget in una riga.
3.

Fai clic su **Salva**.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Costruttore intestazione con la barra laterale Libreria widget aperta e il widget Selettore Spedisci a visibile/contrassegnato
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Il widget non necessita di configurazione — elenca automaticamente i Paesi di spedizione attivi e mostra la scelta corrente dello shopper (oppure il Paese rilevato tramite GeoIP, se non è stato scelto alcun Paese). Selezionando un Paese diverso, aggiorna immediatamente la regione e ricarica l'accesso ai prodotti e i prezzi della pagina.

Il Selettore Spedisci a non ha ancora un modulo delle impostazioni dedicato. Se desideri modificare lo stile del pulsante (sfasato, solido o trasparente) o nascondere l'etichetta "Spedisci a", apri le impostazioni del widget nel costruttore e modifica direttamente il campo **Configurazione personalizzata (JSON)**, utilizzando `button_style` e `show_label`.

### Valuta in base alla regione

Se il tuo negozio supporta più di una valuta (impostata sotto **Impostazioni > Multi-valuta**), passare alla regione - attraverso la richiesta o il Selettore Spedisci a - cambia anche la valuta visualizzata con quella predefinita della regione. Se il tuo negozio ha una sola valuta o non ha esplicitamente abilitato una seconda valuta, la valuta rimane invariata quando uno shopper modifica la regione.

## Suggerimenti

- Lascia **Accesso alle regioni** su **Disponibile in tutte le regioni** a meno che non tu abbia un motivo specifico per limitare un prodotto - è l'opzione più semplice e non necessita di manutenzione quando aggiungi nuove regioni in futuro.
- Usa **Solo nelle regioni selezionate** per un elenco di autorizzazioni piccolo (ad esempio, un prodotto che viene lanciato in un unico paese per primo) e **Tutte le regioni tranne quelle selezionate** per un elenco di blocchi piccolo (ad esempio, ovunque tranne un paese in cui l'oggetto non è autorizzato) - scegli l'opzione che richiede meno righe per la configurazione.
- Se gli acquirenti segnalano che un prodotto manca ma dovrebbe essere visibile, controlla sia l'impostazione **Accesso alle regioni** del prodotto che se il loro paese è incluso in un'attiva **Regione di vendita** e in un attivo **Paese di spedizione**.
- **Nascondi dagli elenchi** mantiene il catalogo pulito per gli acquirenti che non possono acquistare alcuni articoli, ma significa anche che merchandising e ricerche appariranno più vuoti in quelle regioni - **Mostra, contrassegnato come non disponibile** è generalmente meglio se desideri comunque che gli acquirenti esplorino l'intero catalogo anche dove non possono effettuare l'acquisto.
- Prova il comportamento delle regioni aggiungendo il Selettore Spedisci a nell'intestazione e passando tra i paesi da te prima di affidarti al rilevamento GeoIP durante un lancio.
- Imposta i valori di priorità delle tue regioni in modo deliberato - la regione attiva con la priorità più alta è il fallback per gli acquirenti i cui paesi non possono essere rilevati o non corrispondono a nessuna regione.