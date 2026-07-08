---
title: Attributi del prodotto
---

Gli attributi del prodotto definiscono le dimensioni lungo le quali un prodotto può variare — ad esempio, Taglia, Colore o Materiale. Una volta che hai creato un attributo e i suoi possibili valori, puoi assegnarlo a qualsiasi prodotto variabile e Spwig genererà il selettore di variazione che i clienti utilizzano al momento del checkout.

Naviga verso **Catalogo > Attributi del prodotto** per gestire gli attributi e i loro valori.

## Funzionamento degli attributi

Gli attributi sono riutilizzabili in tutto il tuo catalogo. Li crei una volta e li assegni a quanti prodotti necessiti. Ogni attributo ha:

- Un **nome** che lo identifica (es. "Taglia")
- Un **tipo di visualizzazione** che controlla come il selettore appare sulla pagina del prodotto
- Uno o più **valori** che rappresentano le opzioni disponibili (es. "Piccolo", "Medio", "Grande")

Quando assegni un attributo a un prodotto, specifichi anche quali dei suoi valori sono disponibili per quel prodotto specifico. Questo significa che un attributo "Taglia" potrebbe avere valori da S a 3XL, ma una specifica maglietta potrebbe offrire solo S, M e L.

## Tipi di visualizzazione degli attributi

Il campo **Tipo** su un attributo controlla come il widget di selezione appare sulla pagina del prodotto del tuo negozio online:

| Tipo | Aspetto | Migliore per |
|---|---|---|
| **Selettore a discesa** | Un menu a discesa che il cliente apre per scegliere un valore | Gli attributi con molti valori (es. una gamma di taglie con 10+ taglie) |
| **Anteprima colore** | Cerchi o quadrati colorati che il cliente clicca | Gli attributi di colore dove l'identificazione visiva è utile |
| **Gruppo di pulsanti** | Pulsanti a forma di pillola visualizzati in linea | Gli attributi con un piccolo numero di valori (es. S, M, L, XL) |
| **Pulsanti di selezione** | Elenco tradizionale di pulsanti di selezione | Qualsiasi attributo dove desideri un layout elenco chiaro e accessibile |

Scegli il tipo di visualizzazione che corrisponde a come i tuoi clienti pensano all'attributo. Per i colori, le anteprime sono quasi sempre preferibili rispetto a un menu a discesa. Per le taglie, i gruppi di pulsanti funzionano bene quando ci sono meno di 8 opzioni.

## Creare un attributo

1. Naviga verso **Catalogo > Attributi del prodotto**
2. Clicca su **+ Aggiungi attributo del prodotto**
3. Inserisci il **Nome** (es. `Taglia`, `Colore`, `Materiale`)
4. Il **Slug** viene riempito automaticamente — puoi lasciarlo così com'è
5. Seleziona il **Tipo** (Selettore a discesa, Anteprima colore, Gruppo di pulsanti o Pulsanti di selezione)
6. Seleziona **Obbligatorio** se i clienti devono selezionare questo attributo prima di poter aggiungere il prodotto al carrello — è appropriato per la maggior parte degli attributi di taglia e colore
7. Imposta l'**Ordine di ordinamento** — gli attributi con numeri più bassi appaiono per primi nel selettore di variazione sulla pagina del prodotto
8. Aggiungi i valori dell'attributo direttamente nella sezione **Valori** (vedi di seguito)
9. Clicca su **Salva**

## Aggiungere valori degli attributi

I valori degli attributi sono le opzioni individuali all'interno di un attributo. Puoi aggiungerli direttamente mentre crei o modifichi un attributo, utilizzando il modulo dei valori inline in fondo alla pagina dei dettagli dell'attributo.

Per ogni valore:

- **Valore** — l'etichetta di visualizzazione (es. `Piccolo`, `Rosso`, `Cotone`)
- **Slug** — riempito automaticamente dal valore; utilizzato negli URL e negli identificatori delle varianti
- **Codice esadecimale del colore** — rilevante solo per gli attributi di tipo **Anteprima colore**. Inserisci un codice colore esadecimale (es. `#FF0000` per il rosso) in modo che l'anteprima mostri il colore corretto.
- **Ordine di ordinamento** — controlla l'ordine in cui i valori appaiono nel selettore. Assegna numeri più bassi ai valori che desideri che appaiano per primi.

### Ordinare i valori in modo logico

Per gli attributi di taglia, imposta l'ordine di ordinamento in modo che le taglie vanno da piccole a grandi:

| Valore | Ordine di ordinamento |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Per gli attributi di colore, potresti ordinarli in ordine alfabetico o raggruppare i colori simili — qualunque cosa abbia più senso per i tuoi clienti.

## Gestione dei valori degli attributi separatamente

Puoi anche gestire i valori degli attributi in modo indipendente in **Catalogo > Valori degli attributi**. Questa lista è utile quando devi trovare o aggiornare un valore specifico nel tuo catalogo senza aprire ogni attributo singolarmente. La lista è filtrabile per nome dell'attributo.

## Assegnare gli attributi ai prodotti

Gli attributi vengono assegnati a livello di prodotto, non a livello globale.

Per aggiungere un attributo a un prodotto:

1. Vai a **Catalogo > Prodotti** e apri un prodotto variabile
2. Nella scheda **Variazioni**, trova la sezione **Attributi**
3. Seleziona l'attributo che desideri aggiungere
4. Scegli quali valori dell'attributo sono disponibili per questo prodotto
5. Salva il prodotto — Spwig genererà le combinazioni di varianti corrispondenti

Per una guida dettagliata sulla configurazione delle varianti dei prodotti, consulta l'argomento di aiuto **Product Variants**.

## Esempi pratici

### Esempio: Attributo di taglia per abbigliamento

| Campo | Valore |
|---|---|
| Nome | Size |
| Tipo | Button Group |
| Obbligatorio | Sì |
| Ordine di ordinamento | 1 |
| Valori | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Esempio: Attributo di anteprima colore

| Campo | Valore |
|---|---|
| Nome | Colour |
| Tipo | Color Swatch |
| Obbligatorio | Sì |
| Ordine di ordinamento | 2 |
| Valori | Black (#000000), White (#FFFFFF), Navy (#001F5B), Red (#CC0000) |

### Esempio: Attributo di materiale

| Campo | Valore |
|---|---|
| Nome | Material |
| Tipo | Dropdown Select |
| Obbligatorio | No |
| Ordine di ordinamento | 3 |
| Valori | 100% Cotton, Cotton/Polyester Blend, Merino Wool, Linen |

## Consigli

- Crea attributi che rappresentino decisioni reali di acquisto fatte dai clienti — se i clienti non devono sceglierlo, potrebbe non essere necessario che sia un attributo
- Usa nomi coerenti in tutto il catalogo: se alcuni prodotti utilizzano "Colour" e altri "Color", i clienti e il tuo team potrebbero trovare l'incoerenza confusa
- L'ordine di ordinamento per gli attributi e i valori è importante — metti l'attributo più importante per primo (di solito Size o Colour) e ordina i valori in una sequenza logica
- Il tipo Color Swatch richiede codici esadecimali accurati; testa i colori in un browser color picker prima di salvare per assicurarti che l'anteprima corrisponda al colore reale del prodotto
- Se devi rinominare un attributo (ad esempio, da "Color" a "Colour"), aggiorna il campo **Nome** invece di creare un nuovo attributo — il cambio del nome non influisce sulle assegnazioni esistenti dei prodotti