---
title: Carte Regalo
---

Le carte regalo sono crediti per il negozio che i clienti possono acquistare per qualcun altro — o per se stessi — consegnati via email come codice di rimborso unico. Puoi anche emettere una carta regalo direttamente dall'amministratore senza un acquisto del cliente.

La vendita di carte regalo è attiva. Quando un cliente ne acquista una, la carta viene creata e inviata via email automaticamente una volta che il pagamento è stato processato — mai prima, quindi nessuno riceve un codice per un pagamento che successivamente fallisce.

Qualche cosa da sapere prima di abilitare un prodotto per carte regalo:

- **Una carta regalo è denaro, non uno sconto.** Viene detratta dalla somma finale dopo le tasse e le spese di spedizione, e non riduce l'importo delle tasse dovute. Questo è l'opposto di un buono, che riduce il prezzo dei prodotti.
- **Le carte sono in una sola valuta.** Una carta acquistata in euro può essere utilizzata solo per un ordine in euro. Se vendi in diverse valute, crea un prodotto per carta regalo separato per ciascuna. Questo ti protegge da variazioni di cambio su un saldo che potrebbe non essere utilizzato per un anno.
- **Le carte regalo non possono essere scontate.** Un buono non si applicherà a una riga di carta regalo, poiché vendere 100 sterline di credito per 80 sterline ti fa perdere 20 sterline ogni volta.
- **Una carta regalo non può acquistare un'altra carta regalo.** Questo chiude una via che alcune persone usano per lavare i dettagli delle carte rubate.
- **L'acquisto di una carta regalo non genera punti fedeltà.** I punti vengono guadagnati quando la carta viene utilizzata per acquistare prodotti, quindi nessuno guadagna due volte sullo stesso denaro.

![Gestione delle carte regalo](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Tipi di Denominazioni

Queste impostazioni controllano come un cliente sceglie l'importo quando acquista una carta regalo:

| Tipo | Descrizione |
|------|-------------|
| **Denominazioni Fisse** | I clienti scelgono da importi predefiniti (es. $25, $50, $100) |
| **Importo Personalizzato** | I clienti inseriscono qualsiasi importo all'interno di un intervallo minimo/massimo |
| **Entrambi** | Offri denominazioni predefinite più un'opzione di importo personalizzato |

## Creare un Prodotto per Carta Regalo

Ogni carta regalo — che verrà venduta in futuro o emessa manualmente oggi — ha bisogno di un prodotto di tipo Carta Regalo dietro di essa.

### Passo 1: Configurare il Prodotto

1. Vai a **Prodotti > Tutti i Prodotti** e fai clic su **+ Aggiungi Prodotto**
2. Imposta **Tipo di Prodotto** su **Carta Regalo**
3. Inserisci il nome e la descrizione del prodotto
4. Configura le impostazioni delle denominazioni:
   - Scegli un **Tipo di Denominazione** (Fissa, Personalizzata o Entrambi)
   - Per Fissa: imposta gli importi delle denominazioni disponibili
   - Per Personalizzata: imposta il **Minimo** e il **Massimo** degli importi consentiti
5. Imposta **Giorni di Scadenza** (0 = non scade mai) — determina per quanto tempo le carte regalo sono valide dopo l'acquisto
6. Salva e pubblica il prodotto

### Passo 2: Pubblicare

Pubblica il prodotto quando sei pronto a venderlo. I clienti possono acquistarlo direttamente dal tuo negozio online subito, e la carta viene inviata automaticamente una volta che il pagamento è stato processato.

Il prodotto è anche ciò che selezioni quando emetti una carta manualmente — quindi è utile crearne uno anche se hai intenzione di darle via solo una volta.

## Creare una Carta Regalo Manualmente

Questo è l'unico modo per creare una carta regalo finanziata al momento, e funziona completamente oggi.

1. Vai a **Prodotti > Carte Regalo** e fai clic su **+ Aggiungi Carta Regalo**
2. Scegli il **Prodotto** — deve essere un prodotto esistente di tipo Carta Regalo (vedi sopra)
3. Inserisci il **Valore Iniziale** — il saldo iniziale, in qualsiasi importo tu scelga. A differenza di un acquisto del cliente, non è limitato alle impostazioni di denominazione del prodotto
4. Imposta opzionalmente una data **Scade il** e lascia **Attivo** selezionato in modo che la carta possa essere riscattata
5. Compila la sezione **Destinatario**, più in basso sulla stessa pagina:
   - **Email del Destinatario** — obbligatorio; dove verrà inviata l'email di consegna
   - **Nome del Destinatario**, **Nome del Mittente** e **Messaggio Personale** — tutti opzionali
   - **Invia a Data e Ora Pianificata** — opzionale; lascia vuoto e invia quando sei pronto, o imposta una data/ora futura (es. un compleanno)
6. Fai clic su **Salva**

Il codice di riscatto viene generato automaticamente e il saldo iniziale viene impostato dal Valore Iniziale — non devi inserire né l'uno né l'altro tu stesso.

**Salvare la carta non la invia per email.** Per consegnarla, torna all'elenco delle carte regalo, seleziona la casella della carta, scegli **Invia email delle carte regalo** dal menu a discesa Azioni e fai clic su **Vai**.

La stessa azione riesegue l'invio dell'email se devi inviarla nuovamente in un secondo momento.

## Gestione delle carte regalo nell'amministrazione

Naviga verso **Prodotti > Carte regalo** per gestire tutte le carte regalo:

### Dashboard delle statistiche

In alto nella pagina, quattro schede mostrano metriche chiave:

- **Totale carte regalo** — Numero totale di carte regalo emesse
- **Attive** — Carte attive con saldo disponibile
- **Totale saldo** — Saldo rimanente combinato di tutte le carte
- **Parzialmente utilizzate** — Carte che sono state parzialmente riscattate

### Filtri

Filtra le carte regalo per:

- **Cerca** — Trova per codice, email o nome del destinatario
- **Stato** — Attive, Inattive, Scadute, Riscattate completamente o Parzialmente utilizzate
- **Saldo** — Con saldo o Senza saldo
- **Creato** — Periodo di tempo (Oggi, Questa settimana, Questo mese, Questo anno)

### Dettagli della carta regalo

Ogni carta regalo mostra:

- **Codice** — Il codice unico di riscatto (es. GC-XXXX-XXXX-XXXX)
- **Destinatario** — Email e nome
- **Badge di stato** — Stato corrente con codifica a colori
- **Saldo / Iniziale / Riscattato** — Riepilogo finanziario con percentuale utilizzata
- **Date importanti** — Creato, emesso, primo utilizzo
- **Mittente** — Chi ha acquistato (o chi ha emesso) la carta regalo

### Azioni

- Fai clic su una carta regalo per **modificare** i suoi dettagli e visualizzare la sua completa **storia delle transazioni**, visualizzata inline sulla stessa pagina
- Seleziona una o più carte e usa il menu a discesa **Azioni** per **Invia email delle carte regalo** (consegna o riesegue l'invio dell'email) o **Marca le carte selezionate come inattive** (disattiva — il saldo viene conservato ma la carta non può più essere riscattata)

## Riscatto Oggi

**In negozio**, al tuo terminale di cassa:

1. L'addetto alla cassa prende il codice allo step di pagamento
2. Il codice viene validato — attivo, non scaduto, con saldo e nella stessa valuta dell'acquisto
3. Il saldo viene applicato all'importo totale dovuto, incluso l'IVA e la consegna
4. Se il saldo non copre l'intero acquisto, il cliente paga il resto in un altro modo
5. Il saldo viene detratto e la transazione registrata

Nota che l'addetto alla cassa prende il codice a **pagamento**, non quando si costruisce il carrello. Una carta regalo è del denaro che il cliente ha già consegnato, quindi salda la fattura invece di scontare i prodotti.

**Online**, al checkout c'è un campo per la carta regalo allo step di pagamento. Il cliente inserisce il proprio codice, il saldo viene detratto dall'importo dovuto — dopo l'IVA e la consegna — e qualsiasi resto viene addebitato alla loro carta come di consueto. Se la carta copre l'intero ordine, non è necessario un altro pagamento. Il saldo viene effettivamente detratto solo dopo che il pagamento è confermato, quindi un checkout abbandonato non tocca mai la carta.

I destinatari possono anche controllare il loro saldo rimanente in qualsiasi momento seguendo il link nell'email di consegna.

## Gestione dei rimborsi

Quando si restituiscono ordini o vendite che hanno utilizzato una carta regalo:

- **Una carta regalo acquistata dal cliente, ancora non utilizzata** — la carta viene disattivata e il suo saldo azzerato, quindi il credito scompare insieme al rimborso.
- **Una carta regalo acquistata dal cliente e parzialmente spesa** — questo richiede la tua valutazione. Disattivarla recupererebbe il credito che il cliente ha già utilizzato, quindi il saldo rimane invariato e viene contrassegnato per la tua eventuale modifica manuale.
- **Una carta regalo utilizzata per pagare l'ordine che viene rimborsato** — il rimborso va prima sulla carta, prima di qualsiasi pagamento con carta o banca. Restituire denaro a una banca da cui il commerciante non ha mai effettivamente ricevuto è un errore peggiore, e restituire il valore dove è arrivato chiude anche una via nota di frode. Se la carta originale è scaduta o è stata disattivata, viene emessa una carta sostitutiva al medesimo destinatario senza data di scadenza.
- **Rimborso completo** — Credita l'importo sul saldo della carta regalo tramite una transazione di rimborso

## Consigli

- Utilizza l'emissione manuale per crediti di cortesia, risoluzioni del servizio clienti o qualsiasi caso in cui desideri fornire un credito al cliente senza un acquisto nel negozio online.
- Imposta periodi di scadenza ragionevoli (es. 365 giorni) per rispettare le normative locali sulle carte regalo — alcune giurisdizioni richiedono periodi minimi di validità.
- Utilizza il tipo di denominazione "Both" per offrire comodità (importi predefiniti) e flessibilità (un importo personalizzato).
- Monitora regolarmente il metrica Totale Saldo — rappresenta un obbligo pendente nei tuoi libri contabili.
- Una carta spende allo stesso modo online e in persona — durante il checkout sul web nella fase di pagamento, o al banco.

L'e-mail di consegna include un link per controllare il saldo che i destinatari possono utilizzare in qualsiasi momento.
- Se vendi a clienti in diversi paesi, puoi emettere carte regalo in valute specifiche — consulta l'argomento **Multi-Currency Gift Cards** per i dettagli.