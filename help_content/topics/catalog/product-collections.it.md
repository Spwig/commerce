---
title: Collezioni di prodotti
---

Le collezioni ti permettono di raggruppare i prodotti per la visualizzazione sul tuo negozio online. A differenza delle categorie, che organizzano l'intero catalogo in una gerarchia permanente, le collezioni sono gruppi flessibili e curati che crei per uno scopo specifico. Una collezione potrebbe evidenziare nuovi arrivi, mostrare articoli per una campagna stagionale o presentare una selezione curata di bestseller.

Naviga verso **Catalogo > Collezioni** per gestire le tue collezioni.

## Collezioni vs categorie

Entrambi le categorie e le collezioni raggruppano i prodotti, ma servono scopi diversi:

| | Categorie | Collezioni |
|---|---|---|
| **Scopo** | Struttura permanente del catalogo | Gruppi flessibili e curati |
| **Gerarchia** | Sì — struttura nidificata padre/figlio | No — gruppi piatti |
| **Prodotti per gruppo** | Ogni prodotto appartiene a una sola categoria | Un prodotto può apparire in molte collezioni |
| **Utilizzo tipico** | Menù di navigazione del negozio, navigazione per reparto | Pagine di destinazione, campagne, set di prodotti in evidenza |

Utilizza le categorie per "come è organizzato il tuo negozio" e le collezioni per "cosa vuoi mettere in evidenza in questo momento".

## Tipi di collezioni

Quando crei una collezione, scegli un tipo che corrisponda a come desideri gestire l'elenco dei prodotti:

| Tipo | Come vengono aggiunti i prodotti |
|---|---|
| **Selezione Manuale** | Tu scegli esattamente quali prodotti appariranno, uno alla volta |
| **Regole Automatiche** | I prodotti vengono aggiunti automaticamente in base a criteri che definisci |
| **Prodotti in Evidenza** | Una selezione editoriale curata, gestita manualmente |
| **Stagionali** | Una selezione basata sul tempo, tipicamente gestita manualmente per le campagne |

I tipi Manuali e in Evidenza ti danno un controllo preciso. Le collezioni automatiche possono crescere con il tuo catalogo senza manutenzione continua.

## Creare una collezione

1. Naviga verso **Catalogo > Collezioni**
2. Clicca su **+ Aggiungi Collezione**
3. Compila la sezione **Informazioni di Base**:
   - **Nome** — il nome della collezione come apparirà sul tuo negozio online
   - **Slug** — il percorso URL per la pagina della collezione (compilato automaticamente dal nome; puoi personalizzarlo)
   - **Descrizione** — una descrizione visualizzata sulla pagina della collezione sul negozio online
4. Seleziona un **Tipo di Collezione**
5. Aggiungi prodotti:
   - Per i tipi **Selezione Manuale** e **Prodotti in Evidenza**: utilizza il campo **Prodotti** per cercare e aggiungere prodotti
   - Per il tipo **Automatico**: definisci i criteri nel campo **Criteri Automatici**
6. Carica immagini:
   - **Immagine** — l'immagine principale della collezione utilizzata sulle pagine di elenco e sulle miniature
   - **Immagine Banner** — un'immagine banner più larga visualizzata in alto sulla pagina della collezione
7. Configura i campi **SEO** (opzionale ma consigliato):
   - **Titolo Meta** — il titolo della pagina visualizzato nei risultati di ricerca
   - **Descrizione Meta** — la descrizione visualizzata sotto il titolo nei risultati di ricerca
8. Imposta le **Opzioni di Visualizzazione**:
   - **Attiva** — controlla se la collezione è visibile sul tuo negozio online
   - **In Evidenza** — segna la collezione per una posizione in evidenza nel tuo tema
   - **Ordine di Visualizzazione** — controlla l'ordine in cui le collezioni appaiono sulle pagine di elenco (i numeri più bassi appaiono per primi)
9. Clicca su **Salva**

## Aggiungere prodotti a una collezione

Per le collezioni manuali, utilizza il campo di completamento automatico **Prodotti** per cercare nel catalogo e selezionare gli articoli. Puoi aggiungere quanti prodotti desideri — non c'è un limite.

I prodotti possono appartenere a molte collezioni contemporaneamente. Ad esempio, un prodotto potrebbe essere in entrambe le tue collezioni "Summer Sale" e "Bestsellers" senza alcun conflitto.

## Visualizzazione delle collezioni sul tuo negozio online

Ogni collezione riceve automaticamente la propria pagina a `/collection/{slug}/`. Puoi collegarti alle pagine delle collezioni dal tuo menu di navigazione, dal costruttore di pagine o da banner promozionali.

La bandiera **In Evidenza** viene utilizzata dal tuo tema per determinare quali collezioni appaiono in posizioni in evidenza — ad esempio, una griglia di collezioni in evidenza sulla homepage. Controlla la documentazione del tuo tema per comprendere esattamente come vengono visualizzate le collezioni in evidenza.

## Gestione della visibilità delle collezioni

- **Attivo** controlla se la pagina della raccolta è accessibile al pubblico.

Una raccolta non attiva è nascosta ai clienti ma rimane presente nell'amministrazione in modo da poterla riattivare in un secondo momento.
- **Ordine di ordinamento** determina l'ordine in cui le raccolte vengono visualizzate nelle pagine di elenco.

Assegna numeri più bassi alle raccolte che desideri visualizzare per prime.

## SEO per le raccolte

Ogni raccolta ha i propri campi **Titolo Meta** e **Descrizione Meta**. Questi controllano ciò che appare nei risultati dei motori di ricerca quando qualcuno trova la pagina della tua raccolta. Se lasci questi campi vuoti, il tuo tema passerà di solito al nome e alla descrizione della raccolta.

I titoli SEO delle raccolte devono essere descrittivi e specifici:
- "Summer Dresses 2026 — Floral & Lightweight Styles" ha un rendimento migliore rispetto a "Summer Collection"
- "Men's Running Shoes — Lightweight & Breathable" ha un rendimento migliore rispetto a "Running Shoes"

## Consigli

- Mantieni i nomi delle raccolte brevi e chiari — appaiono come titoli delle pagine e come testo dei collegamenti nella navigazione del tuo negozio online
- Utilizza raccolte stagionali o di campagna con un piano di inizio e fine: crea la raccolta, attivala quando inizia la campagna e disattivala (anziché eliminarla) quando termina, in modo da poterla utilizzare in futuro
- Il campo **Ordine di ordinamento** è degno di essere impostato in modo deliberato — il valore predefinito è 0 per tutte le raccolte, il che significa che vengono ordinate in ordine alfabetico. Assegna numeri specifici per controllare quali raccolte appaiano in modo più prominente
- Una raccolta senza prodotti mostrerà una pagina vuota ai clienti — aggiungi i prodotti prima di attivare la raccolta, o lasciala non attiva fino a quando non è pronta
- Controlla solo il flag **In evidenza** per le raccolte che desideri veramente mettere in risalto; la maggior parte dei temi riserva gli slot in evidenza per un piccolo numero di raccolte e l'aspetto può apparire affollato se troppi vengono contrassegnati