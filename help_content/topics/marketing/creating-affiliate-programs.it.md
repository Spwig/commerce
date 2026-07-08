---
title: Creazione di programmi di affiliazione
---

I programmi di affiliazione definiscono come i tuoi partner guadagnano commissioni quando riferiscono clienti al tuo negozio. Ogni programma ha la propria struttura delle commissioni, le proprie regole di tracciamento e i propri limiti di pagamento. Puoi creare diversi programmi per servire diverse segmentazioni di affiliati — ad esempio, influencer, creatori di contenuti o partner di riferimento di massa.

![Elenco dei programmi](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Componenti del programma

Ogni programma di affiliazione è composto da:

- **Nome e descrizione** — Identifica il programma e spiega agli affiliati
- **Struttura delle commissioni** — Quanto guadagnano gli affiliati per ogni vendita (percentuale o importo fisso)
- **Durata della cookie** — Quanto dura il tracciamento dei riferimenti dopo un clic (1-365 giorni)
- **Approvazione automatica** — Se i nuovi affiliati si uniscono automaticamente o richiedono una revisione manuale
- **Limite minimo di pagamento** — Quanto devono guadagnare gli affiliati prima di richiedere un pagamento
- **Stato** — Attivo, sospeso o archiviato

## Tipi di commissioni

Scegli tra due modelli di commissioni quando crei il tuo programma:

| Tipo | Funzionamento | Quando utilizzarlo | Calcolo di esempio |
|------|-------------|-------------|---------------------|
| **Percentuale** | L'affiliato guadagna una percentuale del sottototale dell'ordine | Premi scalabili che crescono con il valore dell'ordine | 10% di un ordine da 150 $ = 15 $ di commissione |
| **Importo fisso** | L'affiliato guadagna un importo fisso per ogni vendita | Costi prevedibili; ideale per prodotti ad alto volume e basso margine | 25 $ per vendita, indipendentemente dal valore dell'ordine |

**Le commissioni in percentuale** si scalano naturalmente — gli affiliati guadagnano di più quando riferiscono clienti ad alto valore. Questo allinea i loro incentivi con i tuoi e è il modello più comune (tipicamente 5–15%).

**Le commissioni fisse** funzionano bene per servizi, abbonamenti o programmi di riferimento di massa dove desideri costi prevedibili per vendita. Sono facili da comprendere e da pianificare, ma potrebbero non compensare adeguatamente gli affiliati che portano ordini di grandi dimensioni.

## Creazione di un programma

Naviga a **Marketing > Programmi di affiliazione** e fai clic su **+ Aggiungi programma**.

### Configurazione passo dopo passo

1. **Nome del programma**
   Inserisci un nome descrittivo visibile agli affiliati (es. "Programma Partner" o "Livello Influencer").

2. **Slug**
   Un identificatore amico degli URL generato automaticamente dal nome. Utilizzato negli URL e nelle referenze interne. Puoi personalizzarlo se necessario.

3. **Descrizione**
   Testo opzionale che spiega i vantaggi e i termini del programma. Gli affiliati lo vedono quando esaminano i programmi a cui possono aderire.

4. **Tipo di commissione**
   Seleziona **Percentuale** o **Importo fisso**.

5. **Valore della commissione**
   - Per percentuale: inserisci un valore compreso tra 0 e 100 (es. `10` per 10%)
   - Per importo fisso: inserisci l'importo in dollari per vendita (es. `25.00` per 25 $)

6. **Durata della cookie in giorni**
   Quanti giorni dura il cookie di tracciamento (1–365). Vedi la sezione sottostante per le linee guida.

7. **Approvazione automatica degli affiliati**
   - **Selezionato** — I nuovi affiliati si uniscono automaticamente
   - **Non selezionato** — Devi revisionare manualmente e approvare ogni candidatura

8. **Pagamento minimo**
   L'importo minimo che un affiliato deve accumulare prima di richiedere un pagamento (es. `50.00` per 50 $).

9. **Stato**
   Impostalo su **Attivo** per accettare nuovi affiliati e tracciare i riferimenti.

10. **Salva** il programma.

## Spiegazione della durata della cookie

La durata della cookie determina quanto tempo Spwig ricorda che un cliente ha cliccato su un link di riferimento di un affiliato.

### Funzionamento

1. Un cliente clicca su un link di un affiliato
2. Spwig imposta un cookie di tracciamento nel browser del cliente
3. Se il cliente completa un acquisto **entro la durata della cookie**, l'ordine è attribuito all'affiliato
4. Se il cookie scade prima dell'acquisto, l'affiliato non guadagna una commissione

### Scegliere una durata

| Durata | Caso d'uso | Scenario tipico |
|----------|----------|------------------|
| **1–7 giorni** | Acquisti impulsivi, offerte flash | Prodotti di consumo rapido, offerte a tempo limitato |
| **30 giorni** | E-commerce standard | Retail online generale, raccomandazione predefinita |
| **60–90 giorni** | Acquisti ponderati | Articoli ad alto prezzo, B2B, servizi |
| **180+ giorni** | Cicli di vendita lunghi | Software per aziende, abbonamenti, prodotti di lusso |

**Lo standard dell'industria è 30 giorni.** Questo equilibra l'attribuzione equa per gli affiliati con i limiti pratici di tracciamento. Le durate più brevi favoriscono i clienti che si convertono rapidamente; le durate più lunghe danno ai clienti tempo per cercare e tornare a completare l'acquisto.

### Nota tecnica

La durata della cookie influisce solo sull'**attribuzione**. Le commissioni approvate rimangono valide in modo permanente — la durata della cookie determina solo se un ordine è attribuito all'affiliato in primo luogo.

## Impostazioni di approvazione automatica

L'impostazione di approvazione automatica controlla se le nuove candidature degli affiliati richiedono una revisione manuale.

### Quando abilitare l'approvazione automatica

- **Programmi pubblici** — Desideri espandere rapidamente la tua base di affiliati senza colloqui
- **Prodotti a basso rischio** — Il rischio di frode o di marchio è minimo
- **Programmi ad alto volume** — Prevedi molte candidature e non puoi revisionarle manualmente una per una

### Quando richiedere una revisione manuale

- **Programmi su invito** — Accetti solo partner già verificati
- **Programmi premium** — Alte commissioni o benefici esclusivi
- **Prodotti sensibili al marchio** — Devi assicurarti che gli affiliati siano allineati ai valori del tuo marchio
- **Prevenzione della frode** — Desideri verificare gli account sospetti

### Considerazioni sulla sicurezza

La revisione manuale degli affiliati aiuta a prevenire:
- Schemi di auto-riferimento (affiliati che creano account falsi per guadagnare commissioni)
- Violazioni del marchio (affiliati che fanno offerte per i termini del tuo marchio in ricerca pagata)
- Mismatch del marchio (affiliati che promuovono i tuoi prodotti in contesti inappropriati)

Per la maggior parte dei negozi, iniziare con **approvazione manuale** è più sicuro. Puoi sempre abilitare l'approvazione automatica in seguito una volta che hai stabilito i modelli di fiducia.

## Limite minimo di pagamento

Il limite minimo di pagamento previene l'eccessivo onere amministrativo derivante dal processare molti piccoli pagamenti.

### Perché impostare un limite minimo

- **Riduce le commissioni di transazione** — I processori di pagamento addebitano per transazione, quindi il raggruppamento dei pagamenti risparmia denaro
- **Semplifica la contabilità** — Meno eventi di pagamento significano meno lavoro di riconciliazione
- **Standard dell'industria** — La maggior parte dei programmi di affiliazione ha limiti (25 $–100 $)

### Limite tipico

| Limite | Caso d'uso |
|-----------|----------|
| **25 $–50 $** | Programmi ad alto volume dove gli affiliati raggiungono rapidamente il limite minimo |
| **50 $–100 $** | Limite standard per la maggior parte dei programmi |
| **100 $–200 $** | Programmi premium o pagamenti internazionali con elevate commissioni di elaborazione |

### Equilibrio tra soddisfazione degli affiliati

Impostare il limite **troppo alto** frustra gli affiliati che potrebbero dover aspettare mesi per ricevere il loro primo pagamento. Impostare il limite **troppo basso** crea un onere amministrativo e riduce i tuoi margini con le commissioni.

**Consiglio:** Inizia a 50 $. Questo è abbastanza basso che gli affiliati attivi raggiungono il limite nei loro primi pochi acquisti, ma sufficientemente alto per raggruppare i pagamenti in modo efficiente.

### Nessun limite massimo

Non esiste un limite massimo — gli affiliati possono accumulare guadagni indefinitamente prima di richiedere un pagamento. Alcuni affiliati preferiscono raggruppare le richieste trimestralmente o annualmente per la pianificazione fiscale.

## Gestione dello stato del programma

I programmi possono essere in uno dei tre stati:

| Stato | Descrizione | Comportamento |
|--------|-------------|----------|
| **Attivo** | Il programma è in esecuzione | Accetta nuovi affiliati, traccia i riferimenti, calcola le commissioni |
| **Sospeso** | Disattivato temporaneamente | Gli affiliati esistenti rimangono ma non ci sono nuove iscrizioni; i cookie di riferimento esistenti funzionano comunque |
| **Archiviato** | Chiuso definitivamente | Nessun nuovo affiliato, nessun nuovo riferimento tracciato; i dati storici vengono conservati per i report |

### Quando sospendere un programma

- Stai rivedendo le commissioni o i termini
- Hai superato il budget per i pagamenti agli affiliati in questo trimestre
- Stai testando una nuova struttura del programma e non vuoi che nuovi affiliati si uniscano a quella vecchia

I programmi sospesi rispettano comunque i cookie di tracciamento esistenti e le commissioni in sospeso — stai solo impedendo a nuovi affiliati di unirsi.

### Quando archiviare un programma

- Hai sostituito il programma con una nuova struttura
- Il programma era limitato nel tempo (es. campagna stagionale)
- Stai consolidando diversi programmi in uno solo

I programmi archiviati rimangono nel database per i report storici ma vengono rimossi dalle visualizzazioni attive.

## Esempi di programmi

### Esempio 1: Programma per influencer (Percentuale)

| Campo | Valore |
|-------|-------|
| Nome | Programma per influencer |
| Tipo di commissione | Percentuale |
| Valore della commissione | 10 |
| Durata della cookie in giorni | 30 |
| Approvazione automatica | Non selezionato (revisione manuale) |
| Limite minimo di pagamento | 50.00 |
| Stato | Attivo |

**Caso d'uso:** Recruti influencer del social media e creatori di contenuti. La commissione del 10% si scala con il valore dell'ordine, premiando gli affiliati che attraggono clienti ad alto spendendo. L'approvazione manuale assicura che tu verifichi l'audience e l'allineamento del marchio di ogni influencer.

### Esempio 2: Programma di riferimento di massa (Fisso)

| Campo | Valore |
|-------|-------|
| Nome | Programma per partner di riferimento |
| Tipo di commissione | Importo fisso |
| Valore della commissione | 25.00 |
| Durata della cookie in giorni | 7 |
| Approvazione automatica | Selezionato |
| Limite minimo di pagamento | 100.00 |
| Stato | Attivo |

**Caso d'uso:** Collabora con siti di offerte, aggregatori di coupon e reti di riferimento che generano un alto volume. La commissione fissa di 25 $ mantiene i costi prevedibili, e la breve durata della cookie (7 giorni) si rivolge a clienti che si convertono rapidamente. L'approvazione automatica è abilitata poiché questi partner tipicamente si servono da soli.

### Esempio 3: Partner premium (Alta percentuale)

| Campo | Valore |
|-------|-------|
| Nome | Livello partner premium |
| Tipo di commissione | Percentuale |
| Valore della commissione | 15 |
| Durata della cookie in giorni | 90 |
| Approvazione automatica | Non selezionato |
| Limite minimo di pagamento | 200.00 |
| Stato | Attivo |

**Caso d'uso:** Programma esclusivo per affiliati ad alte prestazioni o partner strategici. Maggiore commissione (15%) premia il traffico di qualità, e la durata della cookie di 90 giorni si adatta a cicli di considerazione più lunghi. Approvazione manuale solo — è un livello su invito.

## Consigli

- Inizia con una **commissione in percentuale** (5–15%) per la maggior parte dei programmi — è più facile da spiegare agli affiliati e si scalano naturalmente con il valore dell'ordine.
- Utilizza una **durata della cookie di 30 giorni** come base — è lo standard dell'industria e bilancia l'attribuzione equa con i limiti pratici di tracciamento.
- Abilita inizialmente l'**approvazione manuale** per verificare gli affiliati, quindi passa all'approvazione automatica una volta che hai stabilito i modelli di fiducia e i controlli contro la frode.
- Imposta il **limite minimo di pagamento** a 50–100 $ per bilanciare la soddisfazione degli affiliati (non troppo alto da raggiungere) con l'efficienza amministrativa (non troppi piccoli pagamenti).
- Crea **programmi separati** per diverse segmentazioni di affiliati (influencer, siti di contenuti, aggregatori di offerte) in modo da poter tracciare le prestazioni e regolare le commissioni in modo indipendente.
- Monitora regolarmente il **pannello di controllo delle analisi** per individuare gli affiliati ad alte prestazioni e regolare le commissioni per mantenere i partner top.

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.