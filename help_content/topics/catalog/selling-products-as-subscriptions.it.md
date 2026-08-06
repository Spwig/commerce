---
title: Vendita di prodotti come abbonamenti
---

Ogni prodotto semplice, variabile o digitale può ora essere venduto con pagamento ricorrente, accanto o al posto di un acquisto unico. Questa guida illustra come attivare gli abbonamenti per un prodotto, scegliere i piani tra cui i clienti possono scegliere e cosa i clienti vedono effettivamente quando acquistano.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: Il modulo di modifica del prodotto con la scheda Abbonamenti attiva, che mostra
    La casella di spunta "Abbonamento abilitato", uno o più piani selezionati nel campo "Piani di abbonamento",
    e le caselle di spunta "Acquisto unico consentito / Default ad abbonamento" visibili.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (storefront) pagina dettaglio prodotto per un prodotto abilitato per abbonamenti
  filename: subscribe-and-save-selector.webp
  description: Il selettore "Acquisto unico" vs "Iscriviti e risparmia" espanso, che mostra
    un elenco di fasce di frequenza di consegna con un badge "Risparmia X%" sulle fasce scontate.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Richiede un prodotto abilitato per abbonamenti con almeno un piano attivo
    pubblico e livelli di prezzo, visualizzato dal punto vendita (non dall'amministratore).
-->

## Quali tipi di prodotto possono essere venduti come abbonamenti

Gli abbonamenti sono disponibili solo per questi tipi di prodotto:

| Eligibile | Non eleggibile |
|----------|---------------|
| Prodotto semplice | Pacco prodotti |
| Prodotto variabile | Buono regalo |
| Prodotto digitale | Prodotto personalizzabile |
| | Prodotto configurabile |
| | Prodotto prenotabile |

Il motivo è la consegna, non il prezzo: un abbonamento riscuote il pagamento del cliente ad ogni ciclo e riconsegna il prodotto tramite un nuovo ordine ogni volta. Spwig sa come rimandare un prodotto semplice o variabile e riconcedere nuovamente il download o la licenza di un prodotto digitale ad ogni rinnovo - ma non può eseguire nuovamente l'emissione di un buono regalo, un insieme multi-componente, una personalizzazione salvata del cliente, un costruttore configurabile o un slot prenotabile in modo ricorrente. Consentire a questi tipi di essere venduti come abbonamenti comporterebbe il rischio di prendere i soldi del cliente al secondo ciclo senza poter consegnare nulla.

La casella di spunta **Abilita abbonamento** non è nascosta o disattivata per i tipi non eleggibili - puoi tecnicamente spuntarla su qualsiasi prodotto. Se provi a salvare un prodotto Buono regalo, Pacco, Personalizzabile, Configurabile o Prenotabile con gli abbonamenti attivi, Spwig rifiuterà il salvataggio con un errore di convalida che spiega che questo tipo di prodotto non può essere venduto come abbonamento. Cambia prima il **Tipo di prodotto** (scheda Informazioni base), oppure lascia disattivati gli abbonamenti per quel prodotto.

## Abilitare gli abbonamenti su un prodotto

1. Vai su **Prodotti > Tutti i prodotti** e apri il prodotto che desideri vendere come abbonamento (oppure crea un nuovo prodotto).
2. Conferma che il **Tipo di prodotto** nella scheda Informazioni base sia Simple, Variable o Digital.
3. Clicca sulla scheda **Abbonamenti**.
4. Seleziona **Abilita abbonamento**.
5. Nel campo **Piani di abbonamento**, seleziona uno o più piani che questo prodotto dovrà offrire. Puoi scegliere solo piani che esistono già - se non ne hai ancora creati, consulta prima [Piani di abbonamento](/help/subscription-plans).
6. Configura le due caselle di spunta per il modo di acquisto (sotto).
7. Clicca su **Salva**.

## Collegare i piani di abbonamento

Un **Piano di abbonamento** è un modello riutilizzabile - opzioni di frequenza di fatturazione, prova, tassa di iscrizione, regole di annullamento - che costruisci una volta e puoi collegare a qualsiasi numero di prodotti eleggibili. Il campo **Piani di abbonamento** nella scheda Abbonamenti del prodotto è il posto in cui collegare il prodotto ai piani ai quali deve essere venduto.

Puoi collegare più piani allo stesso prodotto.

Questo è utile quando, ad esempio, desideri offrire una fascia "Standard" e una "Premium" per lo stesso articolo - ogni piano può avere le proprie fasce di prezzo, prova e politica di annullamento.


Quando un prodotto ha più di un piano associato, i clienti vedono un selettore di piano nella pagina del prodotto prima di scegliere la frequenza di fatturazione.

## Controllo acquisti una tantum vs. abbonamenti

Due caselle di spunta sulla scheda Abbonamenti controllano come i clienti possono acquistare il prodotto:

- **Consenti acquisto una tantum** — Abilitato di default. Quando selezionato, i clienti scelgono tra un acquisto regolare una tantum e un abbonamento. Deselezionarlo per rendere il prodotto esclusivamente abbonamento — ogni acquisto diventa un ordine ricorrente, e non viene mostrata alcuna opzione una tantum.
- **Predefinisci abbonamento** — seleziona l'opzione abbonamento (e il relativo piano/tier predefinito) quando viene caricata la pagina del prodotto, invece di richiedere ai clienti di selezionarla attivamente. Questo ha effetto solo quando **Consenti acquisto una tantum** è inoltre selezionato — se l'acquisto una tantum è disattivato, il prodotto è esclusivamente abbonamento, indipendentemente da questo settaggio.

Utilizza **Predefinisci abbonamento** per i prodotti in cui la consegna ricorrente è la previsione naturale (caffè, integratori, prodotti di consumo) — rimuove un clic e spinge i clienti verso l'opzione che li fa tornare, senza rimuovere la loro capacità di acquistare una sola volta.

## Cosa vedono i clienti

### Nella pagina del prodotto

Quando un prodotto ha gli abbonamenti attivi e almeno un piano attivo, pubblico, associato, appare un selettore di modalità di acquisto nella pagina del prodotto:

- Se è consentito l'acquisto una tantum, i clienti vedono una scelta tra **"Acquista una tantum"** e **"Iscriviti e risparmia"**, predefinita alla modalità configurata.
- Se il prodotto ha più di un piano associato, appare un selettore di piano una volta selezionata **"Iscriviti e risparmia"**.
- Per il piano scelto, i clienti vedono un elenco di **frequenza di consegna** costruito dai piani di prezzo di quel piano (es. Mensile, Trimestrale, Annuale), ciascuno che mostra il suo prezzo e un **badge "Risparmia X%"** quando il piano ha uno sconto.
- La durata del periodo di prova, la tariffa di attivazione e la politica di annullamento del piano (es. "Annulla in qualsiasi momento") vengono visualizzati insieme all'elenco dei piani, insieme a un avviso che indica che un metodo di pagamento verrà aggiunto al checkout.

### Nel carrello e al checkout

Gli articoli di abbonamento nel carrello portano con sé un **badge Abbonamento**, la frequenza di fatturazione (es. "Ogni mese") e un avviso relativo al periodo di prova se applicabile, in modo che il cliente capisca quali righe sono ricorrenti. Al checkout, il cliente seleziona un fornitore di pagamento come al solito — questo è il metodo di pagamento che verrà addebitato nei rinnovi futuri.

> **Limitazione nota:** il salvataggio automatico della carta del cliente per i rinnovi di abbonamento al checkout è ancora in fase di connessione per alcuni fornitori di pagamento. Finché un fornitore specifico non supporta questa funzionalità, gli abbonamenti effettuati tramite di esso potrebbero richiedere un follow-up aggiuntivo (es. contattare il cliente per ottenere dettagli di pagamento aggiornati prima di un rinnovo) invece di essere completamente automatici fin dal primo giorno. Controlla la configurazione del tuo fornitore di pagamento se noti che i rinnovi non vengono addebitati automaticamente per un abbonamento.

## Suggerimenti

- Crea e testa prima il piano di abbonamento (livelli di prezzo, periodo di prova, politica di annullamento), quindi associalo ai prodotti - è più facile ottenere il piano giusto una volta che sistemare i problemi su diversi prodotti in seguito.
- Lascia **Consenti acquisto una tantum** selezionato per la maggior parte dei prodotti. Riserva i prodotti esclusivamente abbonamento per casi in cui l'acquisto una tantum non abbia senso per il tuo business.
- Se stai convertendo un prodotto best-seller esistente in un'opzione di abbonamento, mantieni **Predefinisci abbonamento** disattivato all'inizio in modo da non disturbare i clienti abituati a comprarlo una tantum - attivalo in seguito una volta che hai visto come rispondono i sottoscrittori.
- I prodotti digitali sono un'ottima scelta per gli abbonamenti (licenze software, iscrizioni a contenuti) poiché il rinnovo riconsegna automaticamente l'accesso senza coinvolgere la spedizione.
- Se hai bisogno di un tipo di prodotto non idoneo (ad esempio un bundle o un articolo personalizzabile) da vendere in modo ricorrente, considera se un equivalente semplificato o digitale potrebbe portare l'abbonamento al posto tuo.