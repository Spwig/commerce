---
title: Programma di Referenza
---

Il programma di referenza permette ai tuoi clienti esistenti di condividere un link di referenza unico con i loro amici e familiari. Quando un amico referenziato effettua il primo acquisto qualificabile, sia il referente che il nuovo cliente possono ricevere un premio — stimolando l'acquisizione di nuovi clienti attraverso il passaparola.

## Funzionamento del programma di referenza

1. Un cliente condivide il proprio link di referenza unico (o il codice) con un amico.
2. L'amico clicca sul link e viene tracciato tramite un cookie per un massimo di 30 giorni (configurabile).
3. L'amico si registra e effettua il primo ordine qualificabile.
4. Il sistema crea un record di attribuzione della referenza e esegue controlli per frodi e idoneità.
5. Se l'attribuzione è approvata, vengono assegnati premi a entrambe le parti.

Il tuo negozio ha una singola configurazione del programma di referenza. Naviga verso **Marketing > Programma di Referenza** per impostarlo.

## Configurazione del programma di referenza

### Stato del programma

Il programma ha tre stati:

- **Bozza** — Il programma è in fase di configurazione ma non è ancora attivo. I link di referenza sono inattivi.
- **Attivo** — Il programma è attivo. I clienti possono condividere i link e guadagnare premi.
- **Sospeso** — Il programma è temporaneamente sospeso. Le attribuzioni esistenti vengono comunque elaborate, ma non vengono tracciati nuovi riferimenti.

Imposta lo **Stato** su **Attivo** quando sei pronto a lanciare il programma. Puoi sospenderlo in qualsiasi momento.

### Configurazione dei premi

Definisci i premi che vengono assegnati quando una referenza si converte. Il programma supporta **premi a doppia faccia** — il che significa che puoi premiare sia il referente (il cliente che ha condiviso il link) che il referee (il nuovo cliente che l'ha utilizzato).

Configura i premi per ciascun destinatario nel campo **Configurazione dei Premi**. I tipi di premi disponibili sono:

| Tipo di Premio | Descrizione |
|----------------|-------------|
| **Crediti per il Negozio** | Aggiunge crediti al portafoglio del cliente, utilizzabili per futuri ordini |
| **Codice Sconto** | Genera un codice unico per un voucher di sconto |
| **Sconto Percentuale** | Emette uno sconto percentuale utilizzabile al momento del checkout |
| **Beneficio Esclusivo** | Un beneficio personalizzato (es. regalo gratuito, accesso prioritario) — descritto nel campo descrizione del premio |

**Esempio di configurazione** — 10 dollari di credito per il referente e 10 dollari di sconto per il nuovo cliente:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Imposta "double_sided": false se desideri premiare solo il referente.

### Regole di idoneità

Le regole di idoneità determinano quali referenze sono idonee per i premi. Configura queste regole nel campo **Regole di Idoneità**:

| Regola | Cosa fa |
|--------|---------|
| `new_customer_only` | Se `true`, l'amico referenziato deve essere un nuovo cliente (nessun ordine precedente) |
| `min_order_value` | L'importo minimo dell'ordine (in valuta del tuo negozio) che l'amico referenziato deve spendere |
| `exclude_discounts` | Se `true`, gli ordini in cui il cliente referenziato ha utilizzato un voucher non sono idonei |
| `exclude_staff` | Se `true`, gli account dello staff non possono essere referenti o referee |

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

L'uso di `post_refund` è l'approccio più cauto — attende che il periodo di reso sia passato prima di assegnare i premi, riducendo il rischio di premiare ordini che saranno successivamente rimborsati.

### Limiti e sovrapposizioni

Impedisce a un singolo referente di guadagnare premi illimitati impostando limiti nel campo **Limiti e Sovrapposizioni**:

| Impostazione | A cosa serve |
|---------|--------------|
| `monthly_per_referrer` | Numero massimo di referenze riuscite premiate al mese, per ogni referente |
| `lifetime_per_referrer` | Numero totale massimo di referenze riuscite premiate mai, per ogni referente |
| `max_reward_per_order` | Valore massimo del premio (in valuta del tuo negozio) assegnato per una singola conversione di referenza |

**Esempio** — 20 referenze al mese, 200 nel corso della vita, premio massimo di $50 per conversione:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Configurazione del tracciamento

Configura come vengono tracciati i collegamenti di referenza nel campo **Configurazione del tracciamento**:

| Impostazione | A cosa serve |
|---------|--------------|
| `cookie_ttl_days` | Numero di giorni in cui rimane attivo il cookie di tracciamento delle referenze dopo che un amico clicca sul collegamento (predefinito: 30) |
| `attribution` | Metodo di attribuzione — attualmente `last_touch` (l'ultimo clic sul collegamento di referenza è considerato valido) |

### Politica di frode

Il sistema di rilevamento delle frodi assegna automaticamente un punteggio di rischio a ogni attribuzione di referenza prima di approvarla. Configura la politica nel campo **Politica di frode**:

| Impostazione | A cosa serve |
|---------|--------------|
| `policy` | Rigidezza complessiva: `strict`, `balanced` o `lenient` |
| `auto_reject_threshold` | Punteggio di rischio (0–100) al di sopra del quale le attribuzioni vengono automaticamente rifiutate (predefinito: 80) |
| `auto_approve_threshold` | Punteggio di rischio al di sotto del quale le attribuzioni vengono automaticamente approvate (predefinito: 30) |
| `check_ip` | Se `true`, verifica se il referente e il cliente referenziato condividono lo stesso indirizzo IP |
| `check_device` | Se `true`, verifica se il referente e il cliente referenziato condividono lo stesso fingerprint del dispositivo |
| `check_velocity` | Se `true`, monitora per tassi di referenze insolitamente elevati da una singola fonte |
| `velocity_window_hours` | Finestra temporale (in ore) per il controllo del tasso |
| `max_referrals_per_window` | Numero massimo di referenze consentite da una singola fonte all'interno della finestra del tasso |

Le attribuzioni con un punteggio di rischio compreso tra i limiti di rifiuto automatico e approvazione automatica vengono indicate come **In attesa** e richiedono una revisione manuale.

### Termini e condizioni

Inserisci eventuali termini e condizioni legali per il programma nel campo **Termini e condizioni**. Questo testo viene visualizzato ai clienti quando visualizzano il programma di referenza. È supportato il formattaggio Markdown.

## Visualizzazione delle attribuzioni di referenza

Naviga verso **Marketing > Attribuzioni di Referenza** per visualizzare tutti i casi di referenza — il collegamento tra un referente e un cliente referenziato.

![Elenco delle attribuzioni di referenza](/static/core/admin/img/help/referral-program/attribution-list.webp)

Ogni attribuzione mostra il referente, il cliente referenziato, il primo ordine che hanno effettuato, lo stato corrente e il punteggio di rischio.

### Stati delle attribuzioni

| Stato | Cosa significa |
|--------|---------------|
| **In attesa** | In attesa di revisione — il punteggio di rischio è compreso nell'intervallo di revisione manuale |
| **Approvato** | Referenza valida — i premi sono stati o saranno assegnati |
| **Rifiutato** | La referenza non ha soddisfatto i criteri o è stata segnalata come fraudolenta |
| **Scaduto** | La referenza non è stata convertita entro la finestra di tracciamento |

### Approvazione o rifiuto manuale delle attribuzioni

Per le attribuzioni nello stato **In attesa**, puoi approvare o rifiutare manualmente aprendo il record dell'attribuzione e utilizzando i pulsanti di azione. Quando rifiuti, scegli un **Motivo del rifiuto**:

- Referenza su se stesso
- Non nuovo cliente
- Valore dell'ordine inferiore al minimo
- Email temporanea
- Limite superato
- Rischio di frode
- Ordine rimborso o annullato
- Rifiuto manuale

Puoi anche aggiungere **Note sul rifiuto** per i tuoi registri.

### Filtraggio per livello di rischio

Utilizza il filtro **Livello di rischio** nel pannello laterale per concentrarti sulle attribuzioni ad alto rischio che necessitano di revisione:

- Basso rischio (punteggio 0–30) — Approvato automaticamente
- Rischio medio (punteggio 31–70) — Revisione manuale
- Alto rischio (punteggio 71–89) — Revisione manuale, trattare con cautela
- Rischio molto alto (punteggio 90+) — Rifiutato automaticamente

## Visualizzazione dei premi emessi

Passa a **Marketing > Rewards emessi** per visualizzare tutti i premi emessi come risultato di attribuzioni approvate.

Ogni voce del premio mostra il cliente, se è il riferente o il riferito, il tipo e l'importo del premio, e lo stato corrente di rimborso.

### Stati dei premi

| Stato | Cosa significa |
|--------|---------------|
| **In attesa** | Il premio è stato creato ma non è ancora stato consegnato al cliente |
| **Emesso** | Il premio è attivo e disponibile per l'uso del cliente |
| **Utilizzato** | Il cliente ha utilizzato il premio |
| **Scaduto** | Il premio è scaduto senza essere stato utilizzato |
| **Revocato** | Il premio è stato annullato manualmente (ad esempio, se l'ordine originale è stato rimborsato dopo l'emissione del premio) |

### Revoca di un premio

Se un premio deve essere annullato — ad esempio, l'ordine qualificante è stato restituito — apri il record del premio e utilizza l'azione **Revoca**. Aggiungi una nota che spiega il motivo per cui è stato revocato per i tuoi archivi.

## Consigli

- Inizia con l'impostazione di timing `post_refund`. Attendere che il periodo di restituzione scada prima di emettere i premi impedisce di premiare gli ordini che alla fine vengono restituiti.
- La politica di frode `balanced` è un buon valore predefinito per la maggior parte dei negozi. Passa a `strict` se noti un picco insolito di riferimenti da un numero limitato di account.
- Imposta limiti realistici per i premi mensili e per tutta la vita. Se il valore del premio è elevato, un limite di 10–20 al mese per riferente è ragionevole per prevenire l'abuso.
- Rivedi settimanalmente le attribuzioni **In attesa**. Lasciarle non revisionate per troppo tempo può frustrare i riferenti legittimi che aspettano il loro premio.
- Utilizza il filtro **Livello di rischio** per prioritizzare la tua coda di revisione manuale — inizia con le attribuzioni a rischio molto elevato prima di passare a quelle a rischio medio.
- Mantieni i Termini e le Condizioni brevi e in linguaggio semplice. I clienti sono più propensi a partecipare quando comprendono chiaramente le regole.