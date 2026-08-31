---
title: Azioni di massa per i prodotti
---

La lista **Prodotti** ti permette di eseguire azioni su molti prodotti contemporaneamente, invece di aprire ciascuno singolarmente. Dal menu a tendina **Azioni di massa** nella barra degli strumenti sopra la griglia prodotti, puoi pubblicare o non pubblicare i prodotti, segnare o non segnare i prodotti, esportare i dati in CSV, verificare quali prodotti sono pronti per la spedizione internazionale o eliminarli - tutto in un unico passaggio.

Vai a **Prodotti > Tutti i prodotti** per utilizzare queste azioni.

![La barra degli strumenti della lista prodotti con tre schede prodotto selezionate e il menu a tendina Azioni di massa che mostra ogni opzione, inclusa l'esportazione dati doganali (CSV) e la verifica della prontezza per la spedizione internazionale](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Esecuzione di un'azione di massa

1. Usa il pannello filtri o la casella **Cerca** per restringere i prodotti che desideri, se necessario
2. Seleziona la casella nell'angolo in alto a sinra di ciascuna scheda prodotto che desideri includere - la barra **Azioni di massa** mostra un conteggio in tempo reale di quanti prodotti sono selezionati
3. Scegli un'azione dal menu a tendina **Azioni di massa**
4. Clicca su **Applica**

Le azioni che modificano o esportano i dati vengono eseguite immediatamente; **Elimina selezionati** richiede una conferma prima, poiché è l'unica azione qui che non è facilmente annullabile direttamente dalla lista stessa.

## Azioni disponibili

| Azione | Cosa fa |
|--------|---------------|
| **Segna come Pubblicato** | Imposta lo stato dei prodotti selezionati su Pubblicato, in modo che siano visibili sul negozio. |
| **Segna come Bozza** | Imposta lo stato dei prodotti selezionati su Bozza, nascondendoli dal negozio mentre li stai modificando. |
| **Segna come Promozionato** | Abilita **È Promozionato** sui prodotti selezionati. |
| **Rimuovi Promozione** | Disabilita **È Promozionato** sui prodotti selezionati. |
| **Esporta in CSV** | Scarica un CSV dei seguenti dati dei prodotti selezionati: ID, nome, SKU, stato, flag promozionato e prezzo. |
| **Esporta dati doganali (CSV)** | Scarica un CSV delle informazioni doganali per i prodotti selezionati. Vedi di seguito. |
| **Verifica la prontezza per la spedizione internazionale** | Mostra un riepilogo di quali prodotti selezionati dispongono dei dati doganali necessari per le spedizioni internazionali. Vedi di seguito. |
| **Elimina selezionati** | Sposta i prodotti selezionati nel cestino, dopo una richiesta di conferma. |

## Esporta dati doganali (CSV)

Usalo quando hai bisogno di un foglio di dichiarazione doganale da consegnare a un corriere, a un vettore o a un intermediario doganale - ad esempio, prima di una grande spedizione internazionale, oppure quando si configura un nuovo corriere che richiede codici HS e dati sull'origine in anticipo.

Seleziona i prodotti, scegli **Esporta dati doganali (CSV)** dal menu a tendina e fai clic su **Applica**. Spwig scarica un file chiamato `product_customs_data.csv` con un record per prodotto e queste colonne:

| Colonna | Origine |
|--------|--------|
| **SKU** | Il SKU del prodotto |
| **Nome** | Il nome del prodotto |
| **Codice HS** | Il codice di classificazione del sistema armonizzato |
| **Paese di origine** | Dove è prodotto il prodotto |
| **Prezzo unitario doganale** | Il valore dichiarato per unità per le dogane |
| **Licenza di esportazione** | Il numero della licenza di esportazione, se il prodotto ne ha bisogno |
| **Data di scadenza della licenza** | La data di scadenza della licenza di esportazione, se impostata |
| **Pronto per la spedizione internazionale** | `Sì` o `No` - se il prodotto ha i dati minimi richiesti per la spedizione internazionale (vedi di seguito) |

Questi campi provengono dalla sezione **Spedizione internazionale / Dogane** del modulo prodotto. Se un prodotto manca di uno, la sua colonna rimane vuota nell'esportazione - completa i dati mancanti sul prodotto prima di farci affidamento per una spedizione effettiva.

## Verifica la prontezza per la spedizione internazionale

Usalo per effettuare un controllo su un insieme di prodotti prima di iniziare a spedirli in modo internazionale, senza aprire ciascun prodotto singolarmente o aspettare un'intera esportazione in CSV.

Seleziona i prodotti, scegli **Verifica la prontezza per la spedizione internazionale** e fai clic su **Applica**. Spwig controlla ciascun prodotto selezionato rispetto a tre campi obbligatori: **Codice HS**, **Paese di origine** e **Prezzo unitario doganale**, e mostra una notifica che riassume i risultati:

- Se ogni prodotto selezionato ha tutti e tre i campi compilati, vedrai una conferma che tutti e tre sono pronti.
- Se alcuni mancano di dati, la notifica segnala quanti sono pronti e quanti non lo sono, e elenca ciascun prodotto che non è pronto insieme ai campi mancanti (ad esempio, "Bicchiere in ceramica blu (mancanti: hs_code, paese_di_origine)").

Se più di 10 prodotti mancano di dati, la notifica elenca i primi 10 e ti fa sapere quanti in più ci sono.

Quest'azione legge solo i dati - non modifica nulla sui prodotti, quindi è sicuro eseguirlo ogni volta che si vuole mentre si sta compilando l'informativa doganale sull'intero catalogo.

**Numero di autorizzazione all'esportazione** e **Scadenza dell'autorizzazione all'esportazione** non fanno parte del controllo della prontezza. Si applicano solo a prodotti controllati o soggetti a restrizioni, quindi un prodotto può essere "pronto" per la spedizione internazionale senza di essi.

## Suggerimenti

- Esegui **Controllo sulla prontezza per la spedizione internazionale** sull'intero catalogo (oppure per categoria alla volta) prima del primo ordine internazionale - è molto più veloce rispetto a scoprire un codice HS mancante quando la spedizione è già al confine.
- Tieni **Dati doganali per l'esportazione (CSV)** per consegnarli a intermediari e vettori, e **Controllo sulla prontezza per la spedizione internazionale** per il tuo elenco di controllo interno - il CSV è un documento, il controllo sulla prontezza è un elenco di cose da fare.
- Compila **Codice HS**, **Paese di origine** e **Prezzo unitario doganale** sul modulo prodotto (sotto **Spedizione internazionale / Dogane**) man mano che aggiungi nuovi prodotti, in modo da non doverlo fare in blocco in seguito.
- La griglia prodotti carica automaticamente ulteriori prodotti mentre scorri (scorrimento infinito), e le tue selezioni con le caselle di controllo vengono mantenute mentre vengono caricati nuovi prodotti - quindi puoi scorrere per costruire una selezione ampia prima di applicare un'azione. Tuttavia, modificare un filtro o ricaricare la pagina cancella la tua selezione, quindi applica l'azione prima di modificare i filtri.
- **Segna come bozza** è un modo veloce per rimuovere diversi prodotti dal negozio contemporaneamente - ad esempio, prima di un conteggio delle scorte - senza modificare altro riguardo a loro.