---
title: Vendita di prodotti come abbonamenti
---

Ogni prodotto semplice, variabile o digitale può ora essere venduto con un pagamento ricorrente, accanto o al posto di un acquisto unico. Questa guida illustra come attivare gli abbonamenti per un prodotto, scegliere quali piani i clienti possono scegliere e cosa vedono veramente i vostri clienti quando acquistano.

## Quali tipi di prodotto possono essere venduti come abbonamenti

Gli abbonamenti sono disponibili solo per questi tipi di prodotto:

| Eligibile | Non eleggibile |
|----------|---------------|
| Prodotto semplice | Pacco prodotti |
| Prodotto variabile | Buono regalo |
| Prodotto digitale | Prodotto personalizzabile |
| | Prodotto configurabile |
| | Prodotto per prenotazioni |

Il motivo non è il prezzo, ma la consegna: un abbonamento riscuote i pagamenti del cliente ad ogni ciclo e riconsegna il prodotto tramite un nuovo ordine ogni volta. Spwig sa come rimandare un prodotto semplice o variabile e riconcedere nuovamente il download o la licenza di un prodotto digitale ad ogni rinnovo - ma non può eseguire nuovamente in modo sicuro l'emissione di un buono regalo, un insieme multi-componente, una personalizzazione salvata del cliente, un'architettura costruita o uno slot di prenotazione in modo ricorrente. Consentire che questi tipi vengano venduti come abbonamenti comporterebbe il rischio di prendere i soldi del cliente al secondo ciclo senza poter consegnare nulla.

La casella **Abilita abbonamento** non è nascosta o disattivata per i tipi non eleggibili - puoi tecnicamente selezionarla su qualsiasi prodotto. Se provi a salvare un prodotto Buono regalo, Pacco, Personalizzabile, Configurabile o Prenotazione con gli abbonamenti attivi, Spwig rifiuterà il salvataggio con un errore di convalida che spiega che questo tipo di prodotto non può essere venduto come abbonamento. Cambia prima il **Tipo di prodotto** (scheda Informazioni base), oppure lascia disattivati gli abbonamenti per quel prodotto.

## Abilitare gli abbonamenti su un prodotto

1. Vai su **Prodotti > Tutti i prodotti** e apri il prodotto che desideri vendere come abbonamento (o crea un nuovo prodotto).
2. Conferma che il **Tipo di prodotto** sulla scheda Informazioni base sia Semplice, Variabile o Digitale.
3. Clicca sulla scheda **Abbonamenti**.
4. Seleziona **Abilita abbonamento**.
5. Nel campo **Piani di abbonamento**, seleziona uno o più piani che questo prodotto dovrebbe offrire. Puoi scegliere solo piani che esistono già - se non ne hai ancora creati, consulta prima [Piani di abbonamento](/help/subscription-plans).
6. Configura le due caselle di controllo per il modo di acquisto (sotto).
7. Clicca su **Salva**.

![La scheda Abbonamenti del modulo di modifica prodotto: Abilita abbonamento selezionato, un piano selezionato nella lista Piani di abbonamento, e le caselle di controllo Consentire acquisto unico e Default ad abbonamento](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Collegare i piani di abbonamento

Un **Piano di abbonamento** è un modello riutilizzabile - opzioni per la frequenza di fatturazione, prova, tariffa di iscrizione, regole di annullamento - che costruisci una volta e puoi collegare a qualsiasi numero di prodotti idonei. Il campo **Piani di abbonamento** sulla scheda Abbonamenti del prodotto è dove colleghi il prodotto ai piani a cui deve essere venduto.

Puoi collegare più piani allo stesso prodotto. Questo è utile quando, ad esempio, desideri offrire un livello ricorrente "Standard" e "Premium" per lo stesso articolo - ciascun piano può avere le proprie fasce di prezzo, prova e politica di annullamento. Quando un prodotto ha più di un piano collegato, i clienti vedranno un selettore di piano nella pagina del prodotto prima di scegliere la frequenza di fatturazione.

## Controllare gli acquisti unici vs. abbonamenti

Due caselle di controllo sulla scheda Abbonamenti controllano come i clienti possono acquistare il prodotto:

- **Consenti acquisto unico** - Abilitato per impostazione predefinita.

Se selezionato, i clienti scelgono tra un normale acquisto unico e un abbonamento.

Deselezionarlo per rendere il prodotto esclusivo per abbonamenti - ogni acquisto diventa un ordine ricorrente, e non viene mostrata alcuna opzione di acquisto unico.
- **Predefinisci abbonamento** - seleziona l'opzione abbonamento (e il piano/tariffa predefiniti) quando viene caricata la pagina del prodotto, invece di richiedere attivamente ai clienti di sceglierlo.

Questo ha effetto solo quando **Consenti acquisto una tantum** è inoltre selezionato — se l'acquisto una tantum è disattivato, il prodotto è esclusivo per sottoscrizione, indipendentemente da questo settaggio.

Usa **Impostazione predefinita per la sottoscrizione** per i prodotti in cui la consegna ricorrente è la scelta naturale (caffè, integratori, prodotti di consumo) — elimina un clic e spinge i clienti verso l'opzione che li fa tornare, senza togliere loro la possibilità di acquistare una tantum.

## Cosa vedono i clienti

### Sulla pagina del prodotto

Quando un prodotto ha le sottoscrizioni attive e almeno un piano attivo, pubblico collegato, appare un selettore della modalità di acquisto sulla pagina del prodotto:

![Il selettore di acquisto del negozio con "Subscribe & Save" selezionato: un'alternativa per acquisto una tantum vs Subscribe & Save sopra un elenco della frequenza di consegna che mostra i piani annuali (risparmio 20%), mensili e trimestrali (risparmio 10%) con prezzi, oltre a note sul periodo di prova, annullamento e pagamento](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Se è consentito l'acquisto una tantum, i clienti vedono la scelta **"Acquisto una tantum"** vs **"Iscriviti e risparmia"**, predefinita alla modalità configurata.
- Se il prodotto ha più di un piano collegato, appare un selettore dei piani una volta selezionato "Iscriviti e risparmia".
- Per il piano scelto, i clienti vedono un elenco della **frequenza di consegna** costruito dai livelli di prezzo di quel piano (es. Mensile, Trimestrale, Annuale), ciascuno che mostra il suo prezzo e un **badge "Risparmia X%"** quando il livello ha uno sconto.
- La durata del periodo di prova, la tariffa di attivazione e la politica di annullamento del piano (es. "Annulla in qualsiasi momento") vengono visualizzati insieme all'elenco dei livelli, insieme a un avviso che indica che un metodo di pagamento verrà aggiunto al checkout.

### Nel carrello e al checkout

Gli articoli di sottoscrizione nel carrello portano con sé un **badge Sottoscrizione**, la frequenza di fatturazione (es. "Ogni mese") e una nota sul periodo di prova se applicabile, in modo che il cliente capisca quali righe sono ricorrenti. Al checkout, il cliente seleziona un fornitore di pagamento come al solito — questo è il metodo di pagamento che verrà addebitato per i rinnovi futuri.

> **Limitazione nota:** il salvataggio automatico della carta del cliente per i rinnovi delle sottoscrizioni al checkout è ancora in fase di connessione per alcuni fornitori di pagamento. Fino a quando un fornitore specifico non supporta questa funzione, le sottoscrizioni effettuate tramite di esso potrebbero richiedere un follow-up aggiuntivo (ad esempio, contattare il cliente per ottenere dettagli di pagamento aggiornati prima di un rinnovo) invece di essere completamente automatiche fin dal primo giorno. Controlla la configurazione del tuo fornitore di pagamento se noti che i rinnovi non vengono addebitati automaticamente per una sottoscrizione.

## Suggerimenti

- Crea e testa prima il piano di sottoscrizione (livelli di prezzo, periodo di prova, politica di annullamento), quindi collegalo ai prodotti - è più facile ottenere il piano giusto una volta che correggere il piano su diversi prodotti in seguito.
- Lascia **Consenti acquisto una tantum** selezionato per la maggior parte dei prodotti. Riserva i prodotti esclusivi per le sottoscrizioni per casi in cui l'acquisto una tantum non abbia senso per il tuo business.
- Se stai convertendo un prodotto best-seller esistente in un'opzione di sottoscrizione, mantieni **Impostazione predefinita per la sottoscrizione** disattivata all'inizio in modo da non disturbare i clienti abituati a comprarlo una tantum - attivala in seguito una volta visto come rispondono i sottoscrittori.
- I prodotti digitali sono una buona scelta per le sottoscrizioni (licenze software, iscrizioni a contenuti) poiché il rinnovo riconsegna automaticamente l'accesso senza coinvolgere la spedizione.
- Se hai bisogno di un tipo di prodotto non idoneo (ad esempio un bundle o un articolo personalizzabile) per essere venduto in modo ricorrente, considera se un equivalente semplificato o digitale potrebbe gestire la sottoscrizione al posto suo.