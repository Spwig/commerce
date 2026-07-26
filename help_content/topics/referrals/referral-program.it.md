---
title: Programma di referenza
---

Il programma di referenza permette ai tuoi clienti esistenti di condividere un link di referenza unico con i loro amici e familiari. Quando un amico referenziato effettua il primo acquisto qualificabile, sia il referente che il nuovo cliente possono ricevere un premio — stimolando l'acquisizione di nuovi clienti attraverso il passaparola.

## Come funziona il programma di referenza

1. Un cliente condivide il proprio link di referenza unico (o il codice) con un amico.
2. L'amico clicca sul link e viene tracciato tramite un cookie per un massimo di 30 giorni (configurabile).
3. L'amico si registra e effettua il primo ordine qualificabile.
4. Il sistema crea un record di attribuzione della referenza e esegue controlli per frodi e idoneità.
5. Se l'attribuzione è approvata, vengono assegnati i premi a entrambe le parti.

Il tuo negozio ha una singola configurazione del programma di referenza. Naviga verso **Marketing > Programma di Referenza** per impostarlo.

## Impostazione del programma di referenza

### Stato del programma

Il programma ha tre stati:

- **Bozza** — Il programma è in fase di configurazione ma non è ancora attivo. I link di referenza sono inattivi.
- **Attivo** — Il programma è attivo. I clienti possono condividere i link e guadagnare premi.
- **Pausa** — Il programma è temporaneamente sospeso. Le attribuzioni esistenti vengono comunque elaborate, ma non vengono tracciati nuovi riferimenti.

Imposta lo **Stato** su **Attivo** quando sei pronto a lanciare il programma. Puoi sospendere il programma in qualsiasi momento.

### Configurazione dei premi

Definisci i premi che vengono assegnati quando una referenza si converte. Il programma supporta **premi a doppia faccia** — il che significa che puoi premiare sia il referente (il cliente che ha condiviso il link) che il referente (il nuovo cliente che l'ha utilizzato).

Configura i premi per ciascun destinatario nel campo **Configurazione dei Premi**. I tipi di premi disponibili sono:

| Tipo di Premio | Descrizione |
|----------------|-------------|
| **Crediti del Negozio** | Aggiunge crediti al portafoglio del cliente, utilizzabili per gli ordini futuri |
| **Codice Sconto** | Genera un codice unico per uno sconto |
| **Sconto Percentuale** | Emette uno sconto percentuale utilizzabile al momento del checkout |
| **Beneficio Esclusivo** | Un beneficio personalizzato (es. regalo gratuito, accesso prioritario) — descritto nel campo descrizione del premio |

I premi di Codice Sconto e Sconto Percentuale sono bloccati al cliente che li ha guadagnati — il codice voucher funziona solo quando quel cliente è connesso. Se un referente condivide il proprio codice premio con qualcun altro invece del link di referenza, l'amico non sarà in grado di utilizzarlo; solo il link di referenza stesso è destinato a essere condiviso.

**Esempio di configurazione** — 10 dollari di credito per il referente e 10 dollari di sconto per il nuovo cliente:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Imposta `"double_sided": false` se desideri premiare solo il referente.

### Regole di idoneità

Le regole di idoneità determinano quali referenze sono qualificate per i premi. Configura queste regole nel campo **Regole di Idoneità**:

| Regola | Cosa fa |
|--------|---------|
| `new_customer_only` | Se `true`, l'amico referenziato deve essere un nuovo cliente (nessun ordine precedente) |
| `min_order_value` | L'importo minimo dell'ordine (in valuta del tuo negozio) che l'amico referenziato deve spendere |
| `exclude_discounts` | Se `true`, gli ordini in cui il cliente referenziato ha utilizzato un voucher non sono idonei |
| `exclude_staff` | Se `true`, gli account dello staff non possono essere referenti o referenti |

**Esempio** — solo nuovi clienti, importo minimo di 40 dollari, staff escluso:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Configurazione del timing

Il campo **Configurazione del Timing** controlla quando vengono assegnati i premi dopo un ordine qualificabile:

| Impostazione | Cosa fa |
|-------------|---------|
| `issue_on` | Quando assegnare il premio: `signup` (immediatamente alla registrazione), `first_purchase` (immediatamente dopo l'ordine) o `post_refund` (dopo che è scaduto il periodo di rimborso) |
| `refund_window_days` | Quanti giorni attendere prima di assegnare i premi quando si utilizza `post_refund` (predefinito: 14 giorni) |


L'uso di `post_refund` è l'approccio più prudente — attende che il periodo di restituzione sia trascorso prima di emettere i premi, riducendo il rischio di premiare ordini che successivamente vengono restituiti.

### Limiti e sovrapposizioni

Impedisce a un singolo riferente di guadagnare premi illimitati stabilendo limiti nel campo **Limiti e sovrapposizioni**:

| Impostazione | Cosa fa |
|---------|--------------|
| `monthly_per_referrer` | Numero massimo di riferimenti riusciti premiati al mese, per riferente |
| `lifetime_per_referrer` | Totale massimo di riferimenti riusciti premiati mai, per riferente |
| `max_reward_per_order` | Valore massimo del premio (in valuta del tuo negozio) emesso per un singolo conversione di riferimento |

**Esempio** — 20 riferimenti al mese, 200 nel corso della vita, $50 massimo di premio per conversione:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Configurazione del tracciamento

Configura come vengono tracciati i collegamenti di riferimento nel campo **Configurazione del tracciamento**:

| Impostazione | Cosa fa |
|---------|--------------|
| `cookie_ttl_days` | Numero di giorni in cui il cookie di tracciamento del riferimento rimane attivo dopo che un amico clicca il collegamento (predefinito: 30) |
| `attribution` | Metodo di attribuzione — attualmente `last_touch` (l'ultimo clic sul collegamento del riferimento è creditato) |

### Politica di frode

Il sistema di rilevamento delle frodi assegna automaticamente un punteggio di rischio a ogni attribuzione di riferimento prima di approvarla. Configura la politica nel campo **Politica di frode**:

| Impostazione | Cosa fa |
|---------|--------------|
| `policy` | Rigidezza complessiva: `strict`, `balanced` o `lenient` |
| `auto_reject_threshold` | Punteggio di rischio (0–100) al di sopra del quale le attribuzioni vengono automaticamente rifiutate (predefinito: 80) |
| `auto_approve_threshold` | Punteggio di rischio al di sotto del quale le attribuzioni vengono automaticamente approvate (predefinito: 30) |
| `check_ip` | Se `true`, verifica se il riferente e il cliente riferito condividono lo stesso indirizzo IP |
| `check_device` | Se `true`, verifica se esiste un'impronta di dispositivo condivisa tra riferente e cliente riferito |
| `check_velocity` | Se `true`, monitora per tassi di riferimento insolitamente elevati da una singola fonte |
| `velocity_window_hours` | La finestra temporale (in ore) per il controllo della velocità |
| `max_referrals_per_window` | Numero massimo di riferimenti consentiti da una singola fonte all'interno della finestra di velocità |

Le attribuzioni con un punteggio di rischio compreso tra i limiti di rifiuto automatico e approvazione automatica vengono inserite in uno stato **In attesa** e richiedono una revisione manuale.

### Termini e condizioni

Inserisci eventuali termini e condizioni legali per il programma nel campo **Termini e condizioni**. Questo testo viene visualizzato ai clienti quando visualizzano il programma di riferimento. È supportato il formattaggio Markdown.

## Visualizzazione delle attribuzioni di riferimento

Naviga verso **Marketing > Attribuzioni di riferimento** per visualizzare tutti i casi di riferimento — il collegamento tra un riferente e un cliente riferito.

![Elenco delle attribuzioni di riferimento](/static/core/admin/img/help/referral-program/attribution-list.webp)

Ogni attribuzione mostra il riferente, il cliente riferito, il primo ordine che hanno effettuato, lo stato corrente e il punteggio di rischio.

### Stati delle attribuzioni

| Stato | Cosa significa |
|--------|---------------|
| **In attesa** | In attesa di revisione — il punteggio di rischio è nella gamma di revisione manuale |
| **Approvato** | Riferimento valido — i premi sono stati o saranno emessi |
| **Rifiutato** | Il riferimento non ha soddisfatto i requisiti o è stato segnalato come frodenza |
| **Scaduto** | Il riferimento non è stato convertito entro la finestra di tracciamento |

### Approvazione o rifiuto manuale delle attribuzioni

Per le attribuzioni nello stato **In attesa**, puoi approvare o rifiutare manualmente aprendo il record dell'attribuzione e utilizzando i pulsanti di azione. Quando rifiuti, scegli un **Motivo del rifiuto**:

- Riferimento a se stesso
- Non nuovo cliente
- Valore dell'ordine inferiore al minimo
- Email temporanea
- Limite superato
- Rischio di frode
- Ordine restituito o annullato
- Rifiuto manuale

Puoi anche aggiungere **Note sul rifiuto** per i tuoi registri.

### Filtraggio per livello di rischio

Utilizza il filtro **Livello di rischio** nel riquadro laterale per concentrarti sulle attribuzioni ad alto rischio che necessitano di revisione:

- Rischio basso (punteggio 0–30) — Approvato automaticamente
- Rischio medio (punteggio 31–70) — Revisione manuale
- Rischio alto (punteggio 71–89) — Revisione manuale, trattare con cautela
- Rischio molto alto (punteggio 90+) — Rifiutato automaticamente

## Visualizzazione dei premi emessi

Passa a **Marketing > Premi emessi** per visualizzare tutti i premi emessi come risultato di attribuzioni approvate.

Ogni voce del premio mostra il cliente, se è il referente o il referee, il tipo e l'importo del premio e lo stato corrente di rimborso.

### Stati dei premi

| Stato | Cosa significa |
|--------|---------------|
| **In sospeso** | Il premio è stato creato ma non è ancora stato consegnato al cliente |
| **Emesso** | Il premio è attivo e disponibile per l'uso del cliente |
| **Utilizzato** | Il cliente ha utilizzato il premio |
| **Scaduto** | Il premio è scaduto senza essere stato utilizzato |
| **Revocato** | Il premio è stato annullato manualmente (ad esempio, se l'ordine originale è stato rimborsato dopo l'emissione del premio) |

### Revoca di un premio

Se un premio deve essere annullato — ad esempio, l'ordine qualificante è stato restituito — apri il record del premio e utilizza l'azione **Revoca**. Aggiungi una nota che spiega il motivo della revoca per i tuoi registri.

## Consigli

- Inizia con l'impostazione di timing `post_refund`. Attendere che il periodo di resi scada prima di emettere i premi impedisce di premiare gli ordini che alla fine vengono restituiti.
- La politica di frode `balanced` è un buon valore predefinito per la maggior parte dei negozi. Passa a `strict` se noti un picco insolito di referimenti da un piccolo numero di account.
- Imposta limiti mensili e totali realistici. Se il valore del premio è elevato, un limite di 10–20 al mese per referente è ragionevole per prevenire l'abuso.
- Rivedi settimanalmente le attribuzioni **In sospeso**. Lasciarle non revisionate per troppo tempo può frustrare i referenti legittimi che aspettano il loro premio.
- Utilizza il filtro **Livello di rischio** per prioritizzare la tua coda di revisione manuale — inizia con le attribuzioni a rischio molto alto prima di passare a quelle a rischio medio.
- Mantieni i Tuoi Termini e Condizioni brevi e in linguaggio semplice. I clienti sono più propensi a partecipare quando comprendono chiaramente le regole.