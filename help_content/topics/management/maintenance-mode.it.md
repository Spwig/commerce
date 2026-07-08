---
title: Modalità manutenzione
---

La modalità manutenzione sospende temporaneamente il tuo negozio online e mostra ai clienti un messaggio del tipo "torneremo presto". Il backend amministrativo rimane pienamente accessibile durante la manutenzione — puoi continuare a lavorare mentre i clienti vengono reindirizzati alla pagina di manutenzione.

Utilizza la modalità manutenzione prima di apportare modifiche che potrebbero causare uno stato inconsistente, ad esempio l'esecuzione di un importo di prodotti di grandi dimensioni, l'applicazione di un importante ridisegno del tema o l'attesa che un'operazione di ripristino venga completata.

![Interruttore della modalità manutenzione nel dashboard del sistema](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Abilitare la modalità manutenzione

1. Naviga su **Gestione > Metriche del sistema**
2. Fai clic su **Dashboard del sistema** dalla barra degli strumenti
3. Nel pannello **Stato del negozio**, fai clic su **Abilita modalità manutenzione**
4. Opzionalmente, inserisci una **Motivazione** — questo è per il tuo riferimento personale e non viene mostrato ai clienti (es. `Aggiornamento del catalogo prodotti in corso`)
5. Conferma cliccando su **Abilita**

Il tuo negozio online inizia immediatamente a mostrare la pagina di manutenzione a tutti i visitatori. Il backend amministrativo non è influenzato e puoi continuare a lavorare normalmente.

## Cosa vedono i clienti

Quando la modalità manutenzione è attiva, ogni pagina del tuo negozio online (il negozio, le pagine dei prodotti, il checkout e le pagine dell'account) mostra un avviso di manutenzione marchiato. Il messaggio informa i clienti che il negozio è temporaneamente non disponibile e li incoraggia a tornare presto.

I clienti che sono in una sessione o in fase di checkout al momento in cui la modalità manutenzione viene attivata vedranno anche la pagina di manutenzione alla loro prossima richiesta. Nessun ordine in corso viene perso — i dati rimangono disponibili quando disattivi la modalità manutenzione.

## Disabilitare la modalità manutenzione

1. Naviga su **Gestione > Metriche del sistema**
2. Fai clic su **Dashboard del sistema**
3. Nel pannello **Stato del negozio**, vedrai un banner che conferma che la modalità manutenzione è attiva
4. Fai clic su **Disabilita modalità manutenzione**
5. Conferma quando richiesto

Il negozio online torna online immediatamente. I clienti possono navigare e acquistare come al solito.

## Quando Spwig attiva automaticamente la modalità manutenzione

Certi operazioni del sistema attivano automaticamente la modalità manutenzione e riattivano il negozio quando terminano:

- **Aggiornamenti del sistema** — il processo di aggiornamento attiva la modalità manutenzione prima di applicare le modifiche e la disattiva quando l'aggiornamento è completato
- **Operazioni di ripristino** — il ripristino da un backup mette il negozio in modalità manutenzione per la durata del ripristino

Se un'operazione automatizzata termina in modo inaspettato, la modalità manutenzione potrebbe rimanere attiva. In tal caso, segui i passaggi sopra per disattivarla manualmente.

## Consigli

- Informa sempre il tuo team prima di abilitare la modalità manutenzione — influisce su ogni visitatore del tuo negozio online
- Mantieni i periodi di manutenzione il più brevi possibile; anche alcuni minuti di offline possono influenzare la fiducia dei clienti
- Utilizza il campo motivazione come promemoria per te stesso su motivo per cui è stata attivata la modalità manutenzione — compare nei log del sistema
- Se noti che la modalità manutenzione è attiva ma non l'hai abilitata tu stesso, controlla i log del sistema per operazioni automatizzate che potrebbero averla attivata
- Pianifica i periodi di manutenzione durante i momenti di basso traffico (sera o mattina presto) per minimizzare l'impatto sulle vendite