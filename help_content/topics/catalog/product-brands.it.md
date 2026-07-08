---
title: Marche dei prodotti
---

Le marche ti permettono di associare i prodotti al loro produttore o etichetta e di fornire ai clienti un modo per navigare nel tuo negozio per marca. Ogni marca ha la sua pagina sul tuo sito web, dove i clienti possono scoprire tutti i prodotti di quella marca, leggere la storia della marca e seguire un link al sito web della marca stessa.

Naviga verso **Catalogo > Marche** per gestire le tue marche.

## Perché utilizzare le marche

Le marche svolgono due funzioni in Spwig:

1. **Organizzazione** — i prodotti vengono contrassegnati con una marca, rendendo facile per i clienti fedeli a un'etichetta trovare ciò di cui hanno bisogno
2. **Merchandising** — le pagine delle marche sono uno spazio dedicato per mostrare la storia, il logo e l'intera gamma di prodotti della marca, il che può migliorare la conversione per i clienti attenti alle marche

Le marche funzionano anche con il sistema di promozioni — puoi lanciare una vendita che si applica a tutti i prodotti di una marca specifica senza dover selezionare i prodotti singolarmente.

## Creare una marca

1. Naviga verso **Catalogo > Marche**
2. Clicca su **+ Aggiungi marca**
3. Compila la sezione **Informazioni di base**:
   - **Nome** — il nome della marca come apparirà sul tuo sito web (deve essere unico)
   - **Slug** — il percorso URL per la pagina della marca (compilato automaticamente dal nome; puoi personalizzarlo)
   - **Descrizione** — una breve descrizione della marca visualizzata sulla pagina della marca
   - **Sito web** — l'URL del sito web ufficiale della marca (opzionale — visualizzato come link sulla pagina della marca)
4. Aggiungi gli asset della marca:
   - **Logo** — l'immagine del logo della marca, utilizzata nell'elenco delle marche e sulla pagina della marca
   - **Immagine banner** — un'immagine banner larga visualizzata in alto sulla pagina della marca
5. Scrivi la **Storia della marca** (opzionale) — un articolo editoriale più lungo sulla storia, sui valori o su ciò che rende speciale la marca. Questo compare sulla pagina del sito web della marca e può essere un modo efficace per raccontare la storia della marca ai clienti interessati.
6. Configura i campi **SEO**:
   - **Titolo meta** — il titolo della pagina visualizzato nei risultati dei motori di ricerca
   - **Descrizione meta** — la breve descrizione visualizzata sotto il titolo nei risultati di ricerca
7. Imposta le opzioni di visualizzazione:
   - **Mostra pagina della marca** — controlla se la marca ha una pagina accessibile al pubblico. Deseleziona per nascondere una marca dal sito web mantenendola comunque nel sistema.
   - **Attiva** — controlla se la marca è disponibile per l'assegnazione ai prodotti e visibile nel negozio
   - **In evidenza** — segna la marca per un posizionamento in evidenza nel tuo tema (es. una riga di loghi di marche sulla homepage)
8. Clicca su **Salva**

## Assegnare prodotti a una marca

Le marche vengono assegnate su singoli record di prodotto, non dalla pagina di gestione delle marche. Per assegnare una marca a un prodotto:

1. Naviga verso **Catalogo > Prodotti** e apri il prodotto
2. Nel modulo del prodotto, trova il campo **Marca**
3. Cerca e seleziona la marca appropriata
4. Salva il prodotto

Una volta che una marca è assegnata, il prodotto apparirà automaticamente sulla pagina del sito web della marca.

## Pagine delle marche sul tuo sito web

Ogni marca con **Mostra pagina della marca** abilitata ha la sua pagina a `/brand/{slug}/`. La pagina visualizza:

- Il logo e l'immagine banner della marca
- Il nome e la descrizione della marca
- La storia della marca (se fornita)
- Un link al sito web della marca (se fornito)
- Tutti i prodotti attivi assegnati a quella marca

I clienti possono raggiungere le pagine delle marche cliccando sul nome della marca su una pagina del prodotto, o attraverso i link che crei nel tuo menu o nel costruttore di pagine.

## SEO per le pagine delle marche

Compilare i campi **Titolo meta** e **Descrizione meta** per ogni marca aiuta le tue pagine delle marche a apparire bene nei risultati di ricerca. I titoli SEO efficaci per le marche combinano il nome della marca con ciò che la marca vende:

| Marca | Titolo meta efficace |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Se lasci i campi SEO vuoti, il tuo tema passerà al nome della marca.

### Generazione automatica SEO

Se **SEO Auto Generato** è abilitato per un marchio, Spwig genererà automaticamente il titolo e la descrizione meta quando il marchio viene salvato.

Questo è conveniente per i negozi con molti marchi, ma dà meno controllo sulla formulazione esatta.

Puoi sempre sovrascrivere il contenuto generato digitando direttamente nei campi e disattivando l'interruttore di generazione automatica.

## Marchi in evidenza

La bandiera **Is Featured** viene utilizzata dai temi per visualizzare una riga o una griglia curata di loghi dei marchi — spesso nella homepage. Solo un piccolo numero di marchi dovrebbe essere in evidenza alla volta; consulta la documentazione del tema per comprendere quanti marchi in evidenza vengono visualizzati in modo ottimale.

## Consigli

- Carica il logo del marchio come PNG o WebP con uno sfondo trasparente — verrà visualizzato in modo pulito su qualsiasi colore di sfondo nel tuo tema
- Scrivi una storia del marchio convincente anche per i marchi meno noti; i clienti che non conoscono un marchio apprezzano il contesto che li aiuta a decidere se i prodotti sono adatti a loro
- Se conduci promozioni mirate a specifici marchi, assicurati che il nome del marchio in Spwig corrisponda esattamente — le promozioni utilizzano il rapporto del marchio sui prodotti per determinare l'idoneità
- Disattiva un marchio invece di eliminarlo quando smetti di vendere i suoi prodotti — l'eliminazione rimuove il riferimento al marchio da tutti i prodotti associati, mentre la disattivazione conserva la storia
- Utilizza la bandiera **Is Featured** con moderazione; una homepage che mostra 20 loghi di marchi perde impatto rispetto a 6–8 scelti con cura