---
title: Tag degli iscritti
---

I tag sono etichette che scegli tu per organizzare il tuo pubblico di Studio delle Campagne: indicatori brevi come `VIP`, `all'ingrosso`, o `evento-2026` che definisci e applichi a qualsiasi iscritto che vi si adatti. Una volta che un tag esiste, puoi filtrare l'elenco degli iscritti in base ad esso, applicarlo o rimuoverlo da qualsiasi numero di persone contemporaneamente e - in modo particolarmente utile - utilizzarlo come condizione quando si crea un Segmento, in modo che le tue campagne e i tuoi percorsi possano puntare esattamente alle persone che hai contrassegnato.

## Cosa sono i tag

Un tag non è altro che un nome che scegli. Spwig non ha alcun tag predefinito e non applica mai automaticamente un tag: decidi tu come si chiamano e a chi vengono assegnati. Questo li rende adatti a qualsiasi cosa specifica per la tua azienda che non corrisponde a uno stato che Spwig tiene già traccia: un livello di fedeltà, un conto all'ingrosso, tutti coloro che si sono iscritti a un convention, o un elenco per un evento unico come `evento-2026`.

Ogni tag riceve anche una **Slug** - una versione semplificata, sicura per URL del suo nome - generata automaticamente quando lo crei. I segmenti e i filtri utilizzano la slug internamente; come commerciante quasi mai avrai bisogno di guardarla.

## Creazione di un tag

I tag hanno la loro sezione amministrativa. Apri **Studio delle Campagne > Iscritti**, quindi fai clic su **Studio delle Campagne** in cima alla pagina per vedere l'elenco completo delle sezioni di Studio delle Campagne e scegli **Tag degli iscritti**.

1. Fai clic su **Aggiungi tag degli iscritti**.
2. Inserisci un **Nome** - leggi meglio se breve e specifico, ad esempio `VIP`, `All'ingrosso` o `Evento 2026`.
3. Spwig compila automaticamente un **Slug** corrispondente mentre digiti. Puoi lasciarlo come generato.
4. Un campo opzionale **Colore** è inoltre disponibile se desideri registrare un colore esadecimale (es. `#2563eb`) associato al tag per il tuo riferimento.
5. Fai clic su **Salva**.

Non devi nemmeno lasciare ciò che stai facendo per crearne uno, inoltre - un segno verde **+** accanto al campo **Tag** su qualsiasi pagina di modifica di un iscritto apre lo stesso modulo "aggiungi un tag" in un popup. Inoltre, se provi a contrassegnare più iscritti prima di aver creato alcuni tag, il selettore di tag offre un collegamento **Crea un tag** che ti porta direttamente lì.

## Assegnazione di tag agli iscritti

Il modo più comune per applicare un tag è in blocco, dall'elenco degli iscritti:

1. Apri **Studio delle Campagne > Iscritti**.
2. Seleziona la casella di controllo su ciascun iscritto che desideri contrassegnare (o **Seleziona tutti questa pagina**).
3. Dalla casella **Azioni in blocco**, scegli **Aggiungi tag selezionati...** (o **Rimuovi tag dai selezionati...** per rimuovere i tag).
4. Fai clic su **Vai**.
5. Scegli il tag dall'elenco e fai clic su **Aggiungi tag** (o **Rimuovi tag**).

![Il selettore di tag in blocco dopo aver scelto "Aggiungi tag selezionati..." per quattro iscritti](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Una volta applicato, un tag viene visualizzato come piccola scheda sull'elenco degli iscritti, accanto ai loro badge di stato e origine. Un filtro **Tag** appare anche nel pannello filtri dell'elenco degli iscritti una volta che hai almeno un tag, in modo da poter restringere l'elenco a tutti coloro che hanno un certo tag - utile per verificare chi è incluso in un pubblico prima di costruire una campagna attorno ad esso.

![L'elenco degli iscritti filtrato al tag VIP, con il pulsante Importa CSV e le chip dei tag visibili](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

Puoi inoltre aggiungere o rimuovere i tag di un singolo iscritto direttamente dalla loro pagina di modifica, utilizzando lo stesso campo **Tag** gestito dall'azione in blocco.

## Utilizzo dei tag nei segmenti

I segmenti sono gli utenti salvati basati su regole a cui punti le tue campagne e i tuoi percorsi. Una volta creato almeno un tag, una condizione **Ha tag** diventa disponibile nel costruttore di regole del segmento - non appare su un installazione pulita con nessun tag definito, quindi non vedrai un'opzione non utile prima che sia utile per te.

Per utilizzarlo, apri **Studio delle Campagne > Segmenti**, aggiungi (o modifica) un segmento dinamico e fai clic su **+ Aggiungi condizione**:

1. Imposta il campo della condizione su **Ha tag**.
2. Scegli un operatore - **è** per un singolo tag, oppure **è uno di** quando preferisci esprimere in quel modo.
3. Scegli il tag dal menu a tendina.

![Una condizione "Ha tag" impostata su VIP, che mostra un conteggio in tempo reale degli abbonati corrispondenti](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

Il conteggio in alto a destra si aggiorna mentre crei la regola, così puoi vedere esattamente quanti abbonati soddisfano attualmente i criteri prima di salvare. Ogni condizione **Ha tag** corrisponde attualmente a un tag alla volta: se desideri un pubblico che corrisponda a *uno qualsiasi* di più tag (ad esempio, `VIP` o `Wholesale`), aggiungi una condizione **Ha tag** per ogni tag e imposta **Corrispondenza** su **uno qualsiasi**.

Questo è ciò che rende i tag utili oltre l'organizzazione: un segmento basato su **Ha tag** diventa un pubblico che puoi selezionare come **Segmento** in una campagna broadcast o ricorrente, oppure come impostazione **Solo per segmento** di un percorso — in modo che "tutti i taggati VIP" possano avere la propria serie di benvenuto, la propria newsletter ricorrente, oppure semplicemente essere il pubblico selezionato la prossima volta che invii un annuncio una tantum.

## Suggerimenti

- Mantieni i nomi dei tag brevi e specifici: vengono visualizzati come chip compatti sulle schede degli abbonati, quindi `VIP` è più leggibile di `Very Important Person - Tier 1`.
- Usa il filtro **Tag** per verificare chi è effettivamente taggato prima di creare un segmento o inviare una campagna basata su di esso.
- Il tagging è additivo: la rimozione di un tag da un abbonante non influisce mai su nessun altro tag che possiede e non tocca mai il suo stato, la sua origine o il suo consenso.
- Combina i tag con altre condizioni del builder di regole (come **Abbonato al marketing** o **Spesa totale**) nello stesso segmento per un pubblico più preciso, non solo un tag da solo.
- Un abbonante può avere quanti tag vuoi: non c'è un limite, quindi è perfettamente accettabile usarli per più scopi sovrapposti (un livello di fedeltà *e* un elenco eventi *e* un'annotazione di origine).
- Se un tag smette di essere utile, la sua eliminazione da **Tag degli abbonati** lo rimuove da tutti gli abbonanti a cui era applicato e da tutte le regole dei segmenti che lo facevano riferimento — i segmenti che lo utilizzano semplicemente smetteranno di corrispondere su quella condizione.