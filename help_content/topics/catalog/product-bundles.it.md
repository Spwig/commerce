---
title: Bundle di prodotti
---

I bundle di prodotti ti permettono di vendere pacchetti pre-assemblati di prodotti a un prezzo combinato. Questo è perfetto per set regalo, kit iniziali o qualsiasi combinazione di prodotti che desideri offrire insieme con uno sconto.

![Componenti del bundle amministratore](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Strategie di prezzo

Scegli come viene calcolato il prezzo del bundle:

| Strategia | Descrizione |
|----------|-------------|
| **Prezzo fisso** | Imposta un prezzo unico per l'intero bundle, indipendentemente dai prezzi dei componenti. |
| **Sconto percentuale** | Calcola automaticamente il prezzo come percentuale rispetto ai prezzi combinati dei componenti. |
| **Somma dei componenti** | Il prezzo del bundle equivale al totale dei prezzi di tutti i componenti (utile per la visualizzazione raggruppata senza sconto). |

## Creare un bundle

### Passo 1: Creare il prodotto

1. Vai a **Prodotti > Tutti i prodotti** e fai clic su **+ Aggiungi prodotto**
2. Imposta **Tipo di prodotto** su **Bundle di prodotti**
3. Inserisci il nome del bundle, la descrizione e le immagini
4. Salva il prodotto

### Passo 2: Aggiungere componenti

Passa alla scheda **Elementi del bundle** per aggiungere prodotti al tuo bundle:

1. Fai clic su **+ Aggiungi componente**
2. Cerca e seleziona un prodotto dal menu a discesa
3. Imposta la **Quantità** per ogni componente (es. 2x maschere per il viso in un set per la cura della pelle)
4. Imposta l'**Ordine di visualizzazione** per controllare l'ordine di visualizzazione
5. Marca opzionalmente un componente come **Opzionale** (i clienti possono escluderlo)
6. Se il componente è un prodotto variabile, scegli tra:
   - Una **variante fissa** — tutti i clienti ricevono la stessa variante
   - **Consenti la selezione della variante** — i clienti scelgono la variante preferita al momento del checkout

La sommatoria in basso mostra il **Totale componenti** e il **Valore del bundle** (somma dei prezzi dei componenti).

### Passo 3: Configurare il prezzo

Passa alla scheda **Prezzo**:

1. Seleziona la **Strategia di prezzo del bundle**
2. Per **Prezzo fisso** — inserisci direttamente il prezzo del bundle
3. Per **Sconto percentuale** — imposta la percentuale di sconto (es. 15% di sconto)
4. Per **Somma dei componenti** — il prezzo viene calcolato automaticamente

## Cosa può essere incluso in un bundle

| Tipo di prodotto | Può essere un componente? |
|-------------|-------------------|
| Prodotto semplice | Sì |
| Prodotto variabile | Sì (variante fissa o scelta del cliente) |
| Prodotto digitale | Sì |
| Prodotto personalizzabile | No |
| Prodotto configurabile | No |
| Bundle di prodotti | No (i bundle non possono essere annidati) |
| Carta regalo | No |

## Gestione delle scorte

Le scorte del bundle vengono gestite attraverso i suoi componenti:

- **Tutti i componenti devono essere in stock** affinché il bundle sia acquistabile
- Quando un bundle viene ordinato, le scorte vengono dedotte da ciascun prodotto componente individualmente
- Se qualsiasi componente esaurisce le scorte, il bundle diventa non disponibile
- I livelli di scorta dei componenti vengono verificati in tempo reale durante il checkout

## Componenti opzionali

Marca un componente come **Opzionale** per permettere ai clienti di personalizzare il loro bundle:

- I componenti opzionali vengono inclusi di default ma possono essere rimossi dal cliente
- Il prezzo del bundle si aggiusta di conseguenza quando i componenti opzionali vengono esclusi
- Almeno un componente deve essere non opzionale (obbligatorio)

## Esperienza del cliente

Quando un cliente visualizza un bundle nel tuo negozio online:

1. **Elenco dei componenti** — Tutti i prodotti inclusi vengono visualizzati con immagini e quantità
2. **Risparmio del bundle** — Viene mostrato l'importo dello sconto rispetto all'acquisto individuale degli articoli
3. **Selezione delle varianti** — Per i componenti con selezione delle varianti abilitata, i clienti scelgono l'opzione preferita
4. **Elementi opzionali** — I clienti possono attivare o disattivare gli elementi opzionali
5. **Aggiungi al carrello singolo** — L'intero bundle viene aggiunto come un singolo elemento

## Consigli

- Utilizza la strategia di sconto percentuale per il prezzo più flessibile — si aggiusta automaticamente quando i prezzi dei componenti cambiano.
- Mostra in modo prominente l'importo del risparmio nella descrizione del prodotto per incoraggiare gli acquisti di bundle.
- Mantieni i bundle da 3 a 5 componenti per la migliore esperienza del cliente. Troppi elementi possono risultare sopraffacenti.
- Utilizza componenti opzionali per offrire una versione "base" e "premium" dello stesso bundle.
- Verifica regolarmente che tutti i prodotti componente siano ancora attivi e in stock.
