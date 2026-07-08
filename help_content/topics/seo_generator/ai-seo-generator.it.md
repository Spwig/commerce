---
title: Generatore di SEO AI
---

Il Generatore di SEO AI scrive automaticamente titoli meta, descrizioni meta e altri contenuti SEO per i tuoi prodotti utilizzando un fornitore di AI. Invece di scrivere manualmente il contenuto SEO per ogni prodotto, puoi generare in modo accurato e ottimizzato contenuti in bulk con un'unica azione.

Il tuo negozio è dotato di un generatore di SEO integrato che funziona immediatamente. Puoi anche installare componenti aggiuntivi di fornitori di AI dal mercato dei componenti Spwig per accedere a modelli linguistici più potenti.

## Come funziona il generatore di SEO

Il generatore di SEO legge il nome, la descrizione, la categoria e gli attributi del prodotto, quindi utilizza il fornitore di AI configurato per creare contenuti SEO personalizzati per quel prodotto. Il contenuto generato viene salvato direttamente nei campi SEO del prodotto.

Puoi generare contenuti SEO per prodotti singoli dalla pagina di modifica del prodotto, o eseguire una generazione in bulk su più prodotti dalla lista dei prodotti.

## Configurazione di un fornitore di SEO

### Utilizzo del fornitore integrato

Il tuo negozio include un fornitore di SEO integrato che genera contenuti SEO in modo deterministico dai dati del prodotto — non sono necessarie chiavi API esterne. È automaticamente impostato come fornitore principale nelle nuove installazioni.

Per verificare che sia attivo:

1. Naviga su **Marketing > Fornitori di SEO**
2. Verifica che il fornitore integrato appaia con un badge **PRIMARIO** e uno stato **ATTIVO**
3. Se non sono elencati fornitori, fai clic su **+ Aggiungi account fornitore di SEO** e imposta **Chiave fornitore** su `deterministic`

### Connessione di un componente di fornitore di AI

Per contenuti SEO più ricchi e contestuali, puoi installare un componente di fornitore di AI (ad esempio, un fornitore basato su OpenAI o Claude) dal mercato dei componenti Spwig.

1. Installa il componente del fornitore tramite il sistema di aggiornamento dei componenti (chiedi all'amministratore del negozio)
2. Naviga su **Marketing > Fornitori di SEO**
3. Fai clic su **+ Aggiungi account fornitore di SEO**
4. Compila il modulo:

**Sezione Informazioni fornitore:**
- **Sito** — seleziona il tuo negozio
- **Componente fornitore** — scegli il componente del fornitore di AI installato
- **Chiave fornitore** — lascia vuoto quando si utilizza un componente basato su fornitore
- **Nome account** — un nome descrittivo come `Fornitore di SEO OpenAI`

**Sezione Configurazione:**
- **Attivo** — spunta per abilitare questo fornitore
- **Principale** — spunta per utilizzarlo come fornitore predefinito per tutta la generazione SEO
- **Priorità** — i numeri più bassi vengono provati per primi nella catena di fallback
- **Impostazioni** — impostazioni specifiche del fornitore come oggetto JSON (es. nome del modello, tono, lingua)

5. Fai clic su **Salva**

Solo un fornitore può essere impostato come principale. Se segni un nuovo fornitore come principale, il precedente principale viene automaticamente declassato.

### Catena di fallback dei fornitori

Se il tuo fornitore principale fallisce (ad esempio, a causa di un'interruzione dell'API), il tuo negozio passa automaticamente al prossimo fornitore attivo in ordine di priorità. Questo garantisce che la generazione SEO continui a funzionare anche se un fornitore è temporaneamente non disponibile.

## Generazione di contenuti SEO per un prodotto

### Prodotto singolo

1. Naviga su **Prodotti > Prodotti** e apri qualsiasi prodotto
2. Scorri fino alla sezione **SEO** del modulo del prodotto
3. Fai clic sul pulsante **Genera SEO**
4. Il fornitore di AI genera un titolo meta e una descrizione meta in base ai dettagli del prodotto
5. Rivedi il contenuto generato e modificalo se necessario
6. Fai clic su **Salva** per applicare le modifiche

### Generazione in bulk

Per generare o aggiornare il contenuto SEO per più prodotti contemporaneamente:

1. Naviga su **Prodotti > Prodotti**
2. Seleziona i prodotti che desideri aggiornare utilizzando le caselle di selezione, o seleziona tutti
3. Apri il menu a discesa **Azione**
4. Scegli **Genera contenuti SEO** (o nome dell'azione simile — controlla il menu a discesa per l'etichetta esatta)
5. Fai clic su **Vai**

Spwig inserisce le attività di generazione in coda e le elabora in background. Ricarica l'elenco dei prodotti dopo un minuto o due per visualizzare i campi SEO aggiornati.

## Rivedere la copertura SEO

Il generatore di SEO traccia quali prodotti hanno già contenuti SEO. Per identificare i prodotti che necessitano ancora di SEO:

1.

Naviga su **Prodotti > Prodotti**
2.


Utilizza il filtro **Stato SEO** (se disponibile) per visualizzare i prodotti con titoli meta mancanti o descrizioni
3.

Seleziona quei prodotti e esegui l'azione di generazione in blocco

## Impostazioni del provider

Il campo **Impostazioni** su un account di un provider SEO accetta un oggetto JSON con configurazioni specifiche del provider. Opzioni comuni includono:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Queste impostazioni variano in base al componente del provider. Consulta la documentazione del provider per l'elenco completo delle opzioni disponibili.

## Gestione di più provider

Se hai configurato più account di provider SEO, l'elenco dei provider mostra lo stato di ciascuno a colpo d'occhio:

- **Etichetta PRIMARIO** — questo provider viene utilizzato per tutta la generazione SEO di default
- **Etichetta ATTIVO** — il provider è abilitato
- **Etichetta INATTIVO** — il provider è disabilitato e non verrà utilizzato

Per modificare quale provider è primario, apri l'account del provider che desideri promuovere, seleziona la casella **È Primario** e salva. Il sistema assicura automaticamente che solo un provider possieda la bandiera primaria in qualsiasi momento.

## Consigli

- Genera il contenuto SEO per i nuovi prodotti immediatamente dopo averli creati — richiede solo alcuni secondi e fornisce ai motori di ricerca qualcosa di utile da indicizzare subito
- Controlla le descrizioni meta generate dall'AI prima di pubblicare se i tuoi prodotti hanno nomi insoliti o tecnici; il generatore funziona meglio con nomi di prodotti chiari e descrittivi
- Imposta "max_title_length": 60 e "max_description_length": 160 nelle impostazioni del provider per mantenere il contenuto generato all'interno dei limiti di caratteri consigliati da Google
- Esegui la generazione SEO in blocco dopo l'importazione di un catalogo di prodotti di grandi dimensioni per popolare rapidamente tutti i campi SEO
- Se aggiorni significativamente la descrizione di un prodotto, rigenera il suo contenuto SEO per mantenere le meta tag allineate con il nuovo testo
- Il provider deterministico predefinito è un buon punto di partenza; passa a un componente alimentato da AI una volta che il catalogo è configurato e desideri testi SEO più ricchi e naturali