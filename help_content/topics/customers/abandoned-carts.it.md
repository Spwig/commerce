---
title: Carrelli Abbandonati
---

Un carrello abbandonato viene creato quando un cliente autenticato aggiunge articoli al carrello ma non completa il checkout entro 24 ore. Spwig traccia automaticamente questi carrelli in modo da poter comprendere la perdita di ricavi, identificare i pattern per cui i clienti abbandonano e prendere azioni per recuperare le vendite.

Naviga verso **Clienti > Carrelli Abbandonati** per visualizzare tutti gli abbandoni registrati.

## Cosa puoi vedere nell'elenco dei carrelli abbandonati

La vista elenco mostra ogni carrello abbandonato con le seguenti informazioni a colpo d'occhio:

| Colonna | Descrizione |
|---|---|
| **Cliente** | Nome e indirizzo email del cliente |
| **Abbandonato il** | Data e orario in cui il carrello è stato segnalato come abbandonato |
| **Valore Totale** | Valore monetario degli articoli nel carrello al momento dell'abbandono |
| **Totale Articoli** | Numero di articoli nel carrello |
| **Motivo Stimato** | Il miglior stimato di Spwig sul motivo per cui il carrello è stato abbandonato |
| **Stato di Recupero** | Se questo carrello è stato recuperato (trasformato in un ordine completato) |
| **Giorni da Abbandono** | Quanto tempo fa è stato abbandonato il carrello |

### Filtrare i carrelli abbandonati

Utilizza i filtri a destra per restringere l'elenco:

- **Motivo Stimato** — filtra per il motivo dell'abbandono (es. mostra solo i carrelli in cui il motivo stimato era un costo di spedizione elevato)
- **Recuperato** — filtra per mostrare solo i carrelli recuperati o non recuperati
- **Abbandonato il** — filtra per intervallo di date per concentrarti sugli abbandoni recenti o su un periodo specifico di una campagna

## Comprendere i motivi dell'abbandono

Spwig registra un motivo stimato per ogni abbandono. Questi motivi si basano su segnali catturati durante il processo di checkout e non sono garantiti per essere esatti, ma forniscono un punto di partenza utile per diagnosticare i pattern di abbandono.

| Motivo | Cosa potrebbe indicare |
|---|---|
| **Sconosciuto** | Nessun segnale specifico è stato catturato — il motivo più comune |
| **Costo di Spedizione Elevato** | Il cliente potrebbe aver rinunciato a causa del costo di spedizione visualizzato al checkout |
| **Totale Troppo Elevato** | Il totale complessivo dell'ordine potrebbe essere stato più alto del previsto |
| **Problemi al Checkout** | Il cliente ha incontrato un problema durante il processo di checkout |
| **Pagamento Fallito** | È stata fatta un'azione di pagamento ma è fallita |
| **Confronto di Prezzi** | Il cliente probabilmente ha visitato per confrontare i prezzi |
| **Salvato per un'Altra Volta** | Il cliente ha intenzionalmente salvato gli articoli per una futura visita |

Se noti una proporzione elevata di carrelli con lo stesso motivo — ad esempio, un cluster significativo di abbandoni per "Costo di Spedizione Elevato" — è un segnale degno di essere investigato nelle impostazioni di spedizione o nella presentazione del checkout.

## Visualizzare un carrello abbandonato singolo

Fai clic su qualsiasi riga nell'elenco per aprire la vista dettagliata. Verrai a conoscenza di:

- **Dettagli dell'Abbandono** — il cliente, il riferimento del carrello, quando è stato abbandonato e il motivo stimato
- **Riepilogo del Carrello** — il numero di articoli e il valore totale al momento dell'abbandono
- **Tracciamento del Recupero** — se il carrello è stato recuperato, quando è stato recuperato e a quale ordine si è convertito

Il campo **Carrello** si collega direttamente al record del carrello sottostante, quindi puoi vedere esattamente quali prodotti erano nel carrello.

## Flusso di lavoro per il recupero

Spwig traccia se ciascun carrello abbandonato si converte infine in un ordine completato. Quando un cliente ritorna e completa un acquisto da un carrello abbandonato, il record viene automaticamente contrassegnato come **Recuperato** e l'ordine risultante viene collegato.

Il contatore **Email di Recupero Inviate** mostra quante email di recupero automatizzate sono state inviate al cliente per questo carrello. Questo ti aiuta a comprendere se le tue campagne email stanno incoraggiando i clienti a tornare.

### Azioni di recupero manuale

La vista dei carrelli abbandonati è in sola lettura — è un registro di ciò che è accaduto, non uno strumento per modificare il contenuto del carrello. Per agire sui carrelli abbandonati:

1.

Nota l'indirizzo email del cliente dal record del carrello abbandonato
2.

Utilizza il tuo sistema di posta elettronica o gli strumenti di marketing per inviare un messaggio personalizzato
3.

Considera l'aggiunta di un codice sconto per dare al cliente un incentivo a completare l'acquisto
4.

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Monitora lo stato **Recovered** nei giorni successivi per verificare se l'outreach ha avuto successo

## Analisi delle tendenze dell'abbandono del carrello

Controlla regolarmente l'elenco dei carrelli abbandonati come check-up sulla salute del processo di checkout:

- Un improvviso aumento degli abbandoni potrebbe indicare un problema tecnico con il checkout o il pagamento
- I valori dei carrelli elevati e costantemente presenti nei carrelli non recuperati rappresentano il segmento con le maggiori opportunità di recupero
- Confronta il rapporto tra carrelli recuperati e non recuperati nel tempo per misurare l'efficacia delle tue email di recupero

La sezione **Customer Analytics** del profilo di ogni cliente mostra anche il tasso personale di abbandono del carrello, quindi puoi identificare i clienti che aggiungono spesso al carrello ma raramente completano un acquisto.

## Consigli

- Ordina per **Total Value** (in ordine discendente) per identificare i carrelli di maggior valore da prioritizzare per un outreach personalizzato
- Usa il filtro **Abandoned At** per data per revisionare gli abbandoni da una campagna specifica o da un periodo promozionale — un picco durante una vendita flash potrebbe significare che la tua promozione ha attratto visitatori piuttosto che acquirenti
- Combina i dati dei carrelli abbandonati con le campagne di buoni: invia un codice sconto a tempo limitato ai clienti con carrelli non recuperati di alto valore per creare un senso di urgenza
- Un carrello abbandonato da più di 7 giorni è improbabile che venga recuperato da solo — se sono abilitate le email di recupero, questi sono i carrelli che necessitano di maggiore attenzione
- I clienti ospiti non appaiono nei carrelli abbandonati — questo tracciamento si applica solo ai clienti con account registrati