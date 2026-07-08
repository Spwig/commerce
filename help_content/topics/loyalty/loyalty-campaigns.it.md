---
title: Campagne di fedeltà
---

Le campagne di fedeltà ti permettono di lanciare promozioni a tempo limitato e premi automatizzati che vanno oltre le tue regole di guadagno quotidiane. Utilizzale per offrire weekend con doppio punteggio, premiare i clienti per il loro compleanno, recuperare acquirenti inattivi e consegnare bonus mirati a specifiche categorie di membri.

Ogni campagna definisce un trigger o un orario, i membri a cui si applica e le azioni da eseguire. Una volta attiva, una campagna si attiva automaticamente — la configuri una volta e Spwig gestisce il resto.

## Tipi di campagne

| Tipo | Quando si attiva |
|------|------------------|
| **Basata su trigger** | Quando si verifica un evento specifico (es. un ordine è effettuato, un compleanno è rilevato) |
| **Pianificata** | Su un orario ripetitivo (giornaliero, settimanale, mensile) |
| **Manuale** | Solo quando la esegui esplicitamente dall'amministrazione |
| **Comportamentale** | Quando un cliente corrisponde a un modello comportamentale (es. naviga senza acquistare) |

## Creare una campagna

Naviga verso **Promozioni > Campagne di fedeltà** e fai clic su **+ Aggiungi Campagna di Fedeltà**.

### Passo 1: informazioni di base

- **Nome** — un nome chiaro e descrittivo visibile solo nell'amministrazione (es. `Bonus Compleanno — 200 Punti`)
- **Slug** — generato automaticamente dal nome; utilizzato internamente
- **Descrizione** — note opzionali sulla finalità della campagna
- **Tipo di Campagna** — seleziona il tipo dalla tabella sopra

### Passo 2: trigger o orario

**Per le campagne basate su trigger**, imposta l'**Evento di Trigger** che attiva la campagna. I trigger disponibili includono:

| Trigger | Descrizione |
|---------|-------------|
| Ordine Effettuato | Si attiva quando un membro completa un ordine |
| Primo Acquisto | Si attiva sul primo ordine di un membro |
| Compleanno del Cliente | Si attiva nel compleanno del membro |
| Anniversario della Membri | Si attiva ogni anno nell'anniversario dell'iscrizione del membro |
| Carrello Abbandonato | Si attiva quando un carrello è abbandonato senza checkout |
| Promozione del Livello | Si attiva quando un membro passa a un livello superiore |
| Punti Prossimi a Scadere | Si attiva quando un membro ha punti prossimi a scadere |
| Inattivo da 90 Giorni | Si attiva quando un membro non ha effettuato un acquisto in 90 giorni |
| Recensione Inviata | Si attiva quando un membro invia una recensione di prodotto |
| Riferimento Convertito | Si attiva quando un cliente riferito effettua un acquisto |

Puoi aggiungere **Condizioni di Trigger** come un oggetto JSON per filtrare ulteriormente quando la campagna si attiva. Ad esempio, per attivare solo gli ordini superiori a $100:

```json
{
  "min_order_amount": 100
}
```

**Per le campagne pianificate**, imposta il **Tipo di Pianificazione** (Giornaliera, Settimanale, Mensile o Cron Personalizzato) e configura l'orario nel campo **Configurazione Pianificazione**:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Passo 3: azioni

Il campo **Azioni** definisce cosa accade quando la campagna si attiva. Inserisci un array JSON di oggetti azione. L'azione più comune è l'assegnazione di punti bonus:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Bonus compleanno — grazie per essere un membro!"
  }
]
```

Altre azioni disponibili includono l'invio di una notifica email o l'assegnazione di un badge. Consulta la documentazione del componente del tuo fornitore per l'elenco completo.

### Passo 4: targeting

Controlla a quali membri si applica la campagna utilizzando i campi di targeting:

- **Targeta Tutti i Membri** — selezionato per default; la campagna si applica a ogni membro attivo della fedeltà
- **Targeta Segmento** — limita la campagna ai membri di un segmento specifico (vedi [Segmenti](#managing-member-segments) di seguito)
- **Targeta Livelli** — limita la campagna ai membri di specifici livelli di fedeltà

### Passo 5: limiti e cooldown

- **Massimo Trigger per Membro** — quante volte lo stesso membro può beneficiare di questa campagna. Imposta su `1` per bonus unici come un premio per compleanno. Lascia vuoto per un numero illimitato.
- **Giorni di Cooldown** — giorni minimi tra i trigger della campagna per lo stesso membro. Ad esempio, imposta su `365` per impedire che una campagna per compleanno si attivi più di una volta all'anno.

### Passo 6: date della campagna

Imposta la **Data di Inizio** e la **Data di Fine** per rendere la campagna limitata nel tempo. Lascia entrambe vuote per una campagna in corso.

Le campagne possono essere in uno di questi stati:

| Stato | Descrizione |
|--------|-------------|
| **Bozza** | Creata ma non ancora attiva; sicuro per configurarla e testarla |
| **Attiva** | In esecuzione e verrà attivata quando vengono soddisfatti i criteri |
| **Pausa** | Fermata temporaneamente senza perdere la configurazione |
| **Terminata** | Superata la data di fine; non attiva più |
| **Archiviata** | Nascosta dall'elenco attivo ma conservata per i record |

Dopo aver compilato tutti i campi, fai clic su **Salva**. Poi cambia lo stato in **Attiva** per avviare la campagna.

## Esempi pratici

### Esempio: doppio punti nel fine settimana

**Scenario:** Assegna 2x punti su tutti gli acquisti effettuati durante un fine settimana specifico.

| Campo | Valore |
|-------|-------|
| Nome | `Double Points Weekend — March` |
| Tipo di Campagna | Trigger-Based |
| Evento Trigger | Ordine Piaciuto |
| Azioni | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Data di Inizio | Venerdì sera |
| Data di Fine | Domenica mezzanotte |
| Target Tutti i Membri | Spuntato |

### Esempio: bonus compleanno

**Scenario:** Dà a ogni membro del programma fedeltà 200 punti bonus nel giorno del suo compleanno.

| Campo | Valore |
|-------|-------|
| Nome | `Birthday Bonus` |
| Tipo di Campagna | Trigger-Based |
| Evento Trigger | Compleanno del Cliente |
| Azioni | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Happy birthday from us!\"}"]` |
| Massimo Trigger per Membro | 1 |
| Giorni di Raffreddamento | 365 |
| Target Tutti i Membri | Spuntato |

### Esempio: campagna per il ritorno dei clienti

**Scenario:** Invia 100 punti bonus ai membri che non hanno effettuato un acquisto negli ultimi 90 giorni.

| Campo | Valore |
|-------|-------|
| Nome | `90-Day Win-Back Bonus` |
| Tipo di Campagna | Trigger-Based |
| Evento Trigger | Inattivo per 90 Giorni |
| Azioni | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"We miss you — here are some bonus points\"}"]` |
| Massimo Trigger per Membro | 1 |
| Giorni di Raffreddamento | 180 |
| Target Tutti i Membri | Spuntato |

## Gestione dei segmenti dei membri

I segmenti ti permettono di mirare le campagne a gruppi specifici di membri del programma fedeltà. Naviga verso **Promotions > Loyalty Segments** per gestirli.

### Tipi di segmenti

| Tipo | Descrizione |
|------|-------------|
| **Rule-Based** | Appartenenza determinata da regole (es. membri con più di 1.000 punti) |
| **Dynamic Calculation** | Appartenenza calcolata su richiesta da criteri in tempo reale |
| **Manual Assignment** | I membri vengono aggiunti al segmento manualmente |

### Creare un segmento

1. Naviga verso **Promotions > Loyalty Segments** e fai clic su **+ Add Loyalty Segment**
2. Compila:
   - **Nome** — nome descrittivo (es. `High-Value Customers`, `Silver Tier Members`)
   - **Slug** — generato automaticamente
   - **Tipo di Criteri** — come viene determinata l'appartenenza
   - **Configurazione dei Criteri** — oggetto JSON che definisce le regole di appartenenza
3. Fai clic su **Salva**

#### Esempio: segmento per membri con almeno 500 punti

```json
{
  "min_available_points": 500
}
```

#### Esempio: segmento solo per membri Gold

```json
{
  "tier_slugs": ["gold"]
}
```

La colonna **Member Count** nell'elenco dei segmenti mostra quanti membri corrispondono attualmente. Fai clic su un segmento e usa l'azione **Refresh Member Count** per ricalcularla se i tuoi dati sono cambiati.

## Tracciamento delle prestazioni delle campagne

### Storico esecuzione delle campagne

Naviga verso **Promotions > Campaign Executions** per visualizzare un registro di ogni volta in cui una campagna è stata attivata per qualsiasi membro. Ogni record di esecuzione mostra quale campagna è stata eseguita, per quale membro e il risultato.

### Rivedere l'efficacia di una campagna

Apri il record di qualsiasi campagna per visualizzare il conteggio **Times Triggered** e quando l'ultima volta che la campagna è stata attivata. Questo ti dà una visione rapida di quanti membri hanno beneficiato della campagna.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Crea campagne nello stato **Bozza** in modo da poter controllare tutte le impostazioni prima che vengano attivate
- Utilizza **Max Triggers Per Member** in tutte le campagne per bonus unici (compleanno, primo acquisto, iscrizione) per evitare che i clienti ricevano il bonus più di una volta
- Combina un **Target Segment** con una campagna basata su trigger per eseguire promozioni esclusive per livelli — ad esempio, doppio punti sugli acquisti solo per i membri Gold e Platinum
- Imposta un valore **Cooldown Days** nelle campagne per il recupero dei clienti in modo che i membri non vengano sovraccaricati se effettuano un piccolo acquisto e poi tornano inattivi poco dopo
- L'elenco delle campagne è lo strumento migliore per tenere traccia di quali promozioni sono attive al momento — controllalo prima di lanciare nuove offerte per assicurarti che le campagne non si sovrappongano in modo non intenzionale
- Archivia le campagne terminate invece di eliminarle in modo da avere un registro storico di quali promozioni hai eseguito e quando