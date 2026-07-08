---
title: Gestione delle traduzioni dell'interfaccia utente
---

La pagina delle traduzioni dell'interfaccia utente ti permette di personalizzare l'aspetto delle stringhe dell'interfaccia frontend—pulsanti, etichette, messaggi di errore e altri testi dell'interfaccia—per ogni lingua. A differenza delle traduzioni del contenuto dei prodotti o delle pagine, queste sono gli elementi fissi dell'interfaccia che i clienti vedono in tutto il tuo negozio. Personalizzale per adattarle alla tua voce di marca o per migliorare la chiarezza per il tuo pubblico specifico.

Questa pagina mostra tutte le stringhe dell'interfaccia traducibili e ti permette di sovrascrivere le traduzioni predefinite fornite da Spwig.

## Comprendere le traduzioni dell'interfaccia utente

Le traduzioni dell'interfaccia utente sono le stringhe di testo che compongono l'interfaccia del tuo negozio:

**Esempi di stringhe dell'interfaccia utente**:
- Pulsanti: "Aggiungi al carrello", "Checkout", "Cerca"
- Etichette: "Prezzo", "Quantità", "Indirizzo di spedizione"
- Messaggi: "Prodotto aggiunto al carrello", "Ordine confermato", "Indirizzo email non valido"
- Navigazione: "Home", "Negozio", "Contattaci"
- Campi del modulo: "Email", "Password", "Nome"

Spwig include traduzioni predefinite per circa 300 stringhe dell'interfaccia utente in tutte le lingue supportate. La pagina delle traduzioni dell'interfaccia utente ti permette di sovrascrivere qualsiasi una di queste predefinite con le tue traduzioni personalizzate.

## Perché personalizzare le traduzioni dell'interfaccia utente?

**Voce di marca**: Cambia "Aggiungi al carrello" in "Compra ora" o "Ottieni il tuo" per adattarti alla personalità della tua marca

**Variazioni regionali**: Modifica le traduzioni per mercati specifici (inglese britannico vs. inglese americano, spagnolo europeo vs. spagnolo latinoamericano)

**Chiarezza**: Se la traduzione predefinita non ha senso per i tuoi prodotti o pubblico, sostituiscila con un testo più chiaro

**Terminologia specifica del settore**: Usa il linguaggio che i tuoi clienti aspettano (ad esempio, "Prenota un appuntamento" invece di "Aggiungi al carrello" per negozi basati su servizi)

## Ricerca delle stringhe

Utilizza la casella di ricerca per trovare stringhe specifiche dell'interfaccia utente:

**Cerca per testo in inglese**: Digita "add to cart" per trovare le traduzioni di quel pulsante

**Cerca per traduzione**: Digita un testo in qualsiasi lingua per trovare traduzioni corrispondenti

**Cerca per chiave**: Se conosci la chiave di traduzione (ad esempio, `cart.add_item`), cerca direttamente per essa

La pagina si aggiorna immediatamente mentre digiti, mostrando solo le stringhe corrispondenti.

## Visualizzazione dei dettagli delle traduzioni

Ogni stringa dell'interfaccia utente mostra:

**Testo sorgente in inglese** - La versione predefinita in inglese (il tuo punto di riferimento)

**Chiave di traduzione** - L'identificatore interno utilizzato nel codice (ad esempio, `cart.add_to_cart`)

**Colonne delle lingue** - Traduzione corrente per ciascuna lingua attiva

**Stato di sovrascrittura** - Se hai personalizzato la traduzione (evidenziata se sovrascritta)

## Creare sovrascritture delle traduzioni

Per personalizzare la traduzione di una stringa dell'interfaccia utente:

1. **Trova la stringa** utilizzando la ricerca (ad esempio, cerca "add to cart")
2. **Fai clic sulla cella della lingua** che desideri personalizzare
3. **Inserisci la tua traduzione personalizzata** nell'editor a comparsa
4. **Salva** - La tua sovrascrittura entra immediatamente in vigore

La traduzione predefinita originale viene conservata - stai creando una sovrascrittura che ha la precedenza.

## Ripristinare le traduzioni predefinite

Per rimuovere una sovrascrittura personalizzata e ripristinare la traduzione predefinita:

1. **Fai clic sulla traduzione sovrascritta** (queste sono evidenziate)
2. **Fai clic su "Ripristina alla predefinita"** nell'editor
3. **Conferma** - La traduzione predefinita viene ripristinata immediatamente

Puoi ripristinare le sovrascritture per singole lingue senza influenzare le tue sovrascritture in altre lingue.

## Filtrare per stato di sovrascrittura

Utilizza il menu a discesa del filtro per visualizzare:

**Tutte le stringhe** - Ogni stringa dell'interfaccia utente nel sistema (~300 totali)

**Solo le sovrascritte** - Stringhe per cui hai creato traduzioni personalizzate

**Solo le predefinite** - Stringhe che utilizzano ancora le traduzioni predefinite di Spwig

Questo ti aiuta a rivedere le stringhe che hai personalizzato e a identificare le lacune.

## Esempi comuni di personalizzazione

| Traduzione predefinita in inglese | Sovrascrittura personalizzata | Caso d'uso |
|----------------|----------------|----------|
| Add to Cart | Buy Now | Chiamata all'azione più diretta |
| Checkout | Secure Checkout | Sottolineare la sicurezza |
| Search | Find Products | Più specifico per l'e-commerce |
| Contact Us | Get in Touch | Tonatura più amichevole |
| Subscribe | Join Our Newsletter | Proposta di valore più chiara |

## Validazione delle traduzioni

Quando inserisci traduzioni personalizzate, verifica che:

**La lunghezza si adatti allo spazio dell'interfaccia** - Le traduzioni possono essere più lunghe o più corte rispetto all'inglese (le parole tedesche sono spesso più lunghe, ad esempio)

**Mantenga il significato** - Non cambiare la funzionalità nella traduzione (un pulsante "Annulla" non dovrebbe dire "Cancella")

**Terminologia coerente** - Usa la stessa traduzione per termini ripetuti in tutto l'interfaccia

**Formalità appropriata** - Adatta il tono al tuo mercato di destinazione (formale vs. informale)

## Coerenza multilingue

Quando personalizzi una stringa per più lingue:

1. **Inizia con la tua lingua predefinita** - Imposta la base
2. **Personalizza altre lingue** per adattarle allo stesso intento
3. **Testa in ciascuna lingua** per verificare il layout e il significato
4. **Utilizza parlanti nativi** quando possibile per revisionare le personalizzazioni non in inglese

Le personalizzazioni incoerenti tra le lingue creano un'esperienza confusa per i clienti.

## Esportazione/Importazione in blocco

Per personalizzazioni estese, considera di utilizzare il flusso di lavoro di esportazione/importazione:

1. **Esporta** le traduzioni correnti come JSON o CSV
2. **Modifica in un foglio di calcolo** o un editor di testo (più facile per modifiche in blocco)
3. **Importa** le traduzioni aggiornate nel sistema

Questo flusso di lavoro è disponibile tramite la pagina dei lavori di traduzione per gestire progetti di traduzione su larga scala.

## Consigli

- **Cerca prima di personalizzare** - Assicurati di modificare la stringa giusta; alcune stringhe simili servono a scopi diversi
- **Testa sull'interfaccia frontend dopo aver salvato** - Verifica che la tua traduzione personalizzata appaia correttamente nell'interfaccia effettiva
- **Mantieni le traduzioni concise** - Più breve è, meglio è per pulsanti ed etichette
- **Documenta le tue sovrascritture** - Tieni note su perché hai personalizzato stringhe specifiche per riferimenti futuri
- **Utilizza una terminologia coerente** - Se personalizzi "Carrello" in "Cesto", fallo in modo coerente in tutte le stringhe correlate
- **Considera i layout mobili** - Le traduzioni lunghe potrebbero avvolgersi o troncarsi su schermi piccoli
- **Rivedi dopo gli aggiornamenti delle lingue** - Quando Spwig aggiunge nuove traduzioni predefinite, rivedi e personalizza quelle per mantenere la coerenza

Ricorda: Conserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.