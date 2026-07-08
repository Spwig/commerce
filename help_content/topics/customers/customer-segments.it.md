---
title: Segmenti dei clienti
---

I segmenti dei clienti ti permettono di classificare automaticamente i tuoi clienti in gruppi significativi in base al loro comportamento d'acquisto. Una volta che i clienti sono segmentati, puoi utilizzare questi gruppi per concentrare gli sforzi del marketing — ad esempio, offrire premi di fedeltà ai clienti VIP o inviare campagne per recuperare clienti che non hanno acquistato da un po'.

Spwig valuta i criteri dei segmenti rispetto ai dati di ciascun cliente e li assegna al segmento con la priorità più alta a cui si qualificano. Questo avviene automaticamente man mano che i dati dei clienti vengono aggiornati.

## Tipi di segmento disponibili

Spwig include un insieme di tipi di segmento predefiniti. Ogni tipo di segmento ha un identificatore interno fisso, ma puoi personalizzare il nome visualizzato, la descrizione, i criteri e il colore in base a come pensi riguardo ai tuoi clienti.

| Tipo di Segmento | Utilizzo Tipico |
|---|---|
| **Cliente ospite** | Clienti che hanno effettuato l'acquisto senza creare un account |
| **Nuovo cliente** | Clienti che hanno effettuato di recente il loro primo acquisto |
| **Cliente abituale** | Clienti con un'esperienza d'acquisto costante |
| **Acquirente frequente** | Clienti che acquistano spesso (intervallo breve tra gli ordini) |
| **Alto valore** | Clienti con un totale di spesa elevato |
| **Cliente VIP** | I tuoi clienti più preziosi e fedeli |
| **Cacciatore di sconti** | Clienti che tendono ad acquistare durante le promozioni |
| **A rischio** | Clienti che non hanno acquistato da un po' |
| **Inattivo** | Clienti che sono assenti da un periodo prolungato |

## Comprendere i criteri dei segmenti

Ogni segmento è definito da una combinazione di criteri. Spwig verifica questi criteri rispetto ai dati memorizzati per ciascun cliente. Tutti i criteri all'interno di un segmento vengono combinati — un cliente deve soddisfare ogni condizione impostata per qualificarsi.

### Criteri di spesa

- **Minimo Totale Speso** — il cliente deve aver speso almeno questa somma su tutti gli ordini completati
- **Massimo Totale Speso** — il cliente non deve aver speso più di questa somma

Utilizza una gamma di spesa per identificare un livello specifico. Ad esempio, impostando Min a $500 e Max a $2.000 si mira ai clienti di livello medio.

### Criteri del numero di ordini

- **Minimo Ordini** — il cliente deve aver effettuato almeno questo numero di ordini completati
- **Massimo Ordini** — il cliente non deve aver effettuato più di questo numero di ordini completati

Combinare il Minimo Ordini con un minimo di spesa è un modo affidabile per definire i clienti VIP: acquistano spesso *e* spendono generosamente.

### Criteri di recentezza

- **Minimo Giorni da Ultimo Acquisto** — l'ultimo ordine del cliente deve risalire almeno a questo numero di giorni fa
- **Massimo Giorni da Ultimo Acquisto** — l'ultimo ordine del cliente deve essere entro questo numero di giorni

I criteri di recentezza sono essenziali per i segmenti a rischio e inattivi. Ad esempio, impostando Min Days a 90 e Max Days a 365 si identificano clienti che si sono fatti silenziosi ma non completamente persi.

## Priorità dei segmenti

Quando un cliente si qualifica per più di un segmento, il segmento con il **valore di priorità più alto** vince. Puoi impostare la priorità per ciascun segmento nella sezione **Impostazioni di visualizzazione** del modulo del segmento.

Il segmento **Cliente ospite** viene sempre valutato per primo, indipendentemente dall'ordine di priorità, perché lo stato ospite è determinato dal tipo di account e non dai criteri di acquisto.

## Visualizzazione e gestione dei segmenti

Naviga verso **Clienti > Segmenti dei clienti** per visualizzare tutti i segmenti configurati. L'elenco mostra il nome visualizzato di ciascun segmento, il tipo interno, il colore assegnato, la priorità, il numero corrente di clienti che corrispondono e se il segmento è attivo.

![Elenco dei segmenti dei clienti](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Creare o modificare un segmento

1.

Naviga verso **Clienti > Segmenti dei clienti**
2.

Fai clic su un segmento esistente per modificarlo, o fai clic su **+ Aggiungi segmento dei clienti** per crearne uno nuovo
3.

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Compila la scheda **Informazioni sul segmento**:
   - **Nome** — seleziona il tipo di segmento interno dal menu a discesa
   - **Nome visualizzato** — il nome leggibile per l'utente visualizzato nell'amministrazione (es. "VIP Customers")
   - **Descrizione** — una breve nota interna che spiega cosa rappresenta questo segmento
4.

Imposta i criteri attraverso le schede pertinenti:
   - **Criteri - Spesa** — importo minimo e massimo totale speso
   - **Criteri - Ordini** — numero minimo e massimo di ordini
   - **Criteri - Recenza** — numero minimo e massimo di giorni da ultima acquisto
5.

Configura **Impostazioni di visualizzazione**:
   - **Colore** — un colore in formato esadecimale utilizzato per identificare visivamente questo segmento nelle liste
   - **Priorità** — un numero più alto significa che questo segmento viene valutato per primo
   - **Attivo** — deseleziona per disattivare il segmento senza eliminarlo
6.

Fai clic su **Salva** per applicare le modifiche

### Esempio: Configurazione di un segmento VIP

Ecco un esempio realistico per un segmento VIP ad alto valore:

| Campo | Valore |
|---|---|
| Nome | `vip` |
| Nome visualizzato | VIP Customers |
| Spesa minima totale | $1.000 |
| Ordini minimi | 5 |
| Giorni massimi da ultima acquisto | 180 |
| Priorità | 90 |
| Colore | `#FFD700` |

Questo significa: un cliente è considerato VIP se ha speso almeno $1.000, ha effettuato almeno 5 ordini e ha effettuato un acquisto negli ultimi 6 mesi.

### Esempio: Configurazione di un segmento a rischio

| Campo | Valore |
|---|---|
| Nome | `at_risk` |
| Nome visualizzato | A rischio |
| Giorni minimi da ultima acquisto | 60 |
| Giorni massimi da ultima acquisto | 180 |
| Priorità | 30 |
| Colore | `#FF6B35` |

## Utilizzo dei segmenti per il marketing mirato

I segmenti vengono visualizzati nei profili dei clienti in tutto l'amministratore, quindi il tuo team sa immediatamente a quale livello appartiene ogni cliente. Utilizza questa informazione per:

- **Eseguire campagne con buoni sconto mirati** — crea buoni sconto limitati ai clienti di un segmento specifico, quindi utilizza il tuo sistema di posta elettronica per inviarli solo a quel gruppo
- **Priorizzare il supporto** — segnala i clienti VIP o ad alto valore in modo che il tuo team possa fornire un servizio prioritario
- **Pianificare il riacquisimento** — esamina regolarmente i segmenti A rischio e Inattivi per identificare i clienti che necessitano di un'email di riacquisimento o di un'offerta speciale
- **Regolare la spesa di marketing** — concentra il budget di acquisizione sui canali che portano clienti ad alto valore analizzando i segmenti in cui convertono i gruppi di clienti

## Consigli

- Inizia con i tipi di segmento predefiniti prima di creare criteri personalizzati — coprono le esigenze di segmentazione più comuni di default
- Controlla periodicamente il numero di clienti in ogni segmento; un segmento VIP con zero clienti o un segmento A rischio in crescita rapida sono entrambi deggni di indagine
- Utilizza il campo **Priorità** con attenzione — se i criteri si sovrappongono tra i segmenti (es. un cliente è idoneo sia per Frequent Buyer che per High Value), il segmento con priorità più alta vince
- Disattiva i segmenti che non stai utilizzando al momento invece di eliminarli — puoi riattivarli in seguito senza dover riconfigurare i criteri
- I criteri dei segmenti vengono verificati contro le metriche dei clienti archiviate, che vengono ricalcolate automaticamente. Se le contati dei segmenti sembrano obsolete, è possibile ricalcolarle dalla sezione Metriche dei clienti dell'amministratore