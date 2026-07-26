---
title: Parcheggio e ripresa delle transazioni POS
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Vista della lista dei carrelli parcheggiati (potrebbe essere vuota su un nuovo installato — cattura comunque)
  save-to: core/static/core/admin/img/help/pos/
-->

I carrelli parcheggiati permettono ai cassieri di sospendere una transazione e di iniziare immediatamente a servire il prossimo cliente — senza perdere nemmeno un singolo articolo o sconto. Quando sei pronto, il carrello originale viene ripristinato esattamente come era e la vendita continua da dove era stata interrotta.

## Cosa fa il parcheggio di un carrello

Quando un cassiere tocca **Parcheggia** sul registratore di cassa, Spwig salva uno snapshot completo del carrello corrente sul server. Il registratore viene pulito in modo da poter iniziare immediatamente una nuova transazione. Il carrello parcheggiato viene salvato e associato al terminale su cui è stato creato.

Niente viene perso nello snapshot. Il carrello parcheggiato mantiene:

- Ogni articolo e la sua quantità
- Qualsiasi cliente che era stato associato alla vendita
- Sconti manuali applicati al carrello o a singoli articoli

Il carrello parcheggiato rimane disponibile sullo stesso terminale per un massimo di **24 ore**. Dopo tale periodo, Spwig lo rimuove automaticamente. I carrelli che sono già stati ripristinati vengono rimossi immediatamente dopo il ripristino e non contano verso la finestra di 24 ore.

## Come parcheggiare una transazione

Devi avere almeno un articolo nel carrello prima di poter parcheggiare. Un carrello vuoto non può essere parcheggiato.

1. Mentre una vendita è in corso, tocca il pulsante **Parcheggia** sul registratore di cassa.
2. Spwig salva il carrello e pulisce il registratore. Verrà visualizzata una conferma e il conteggio dei carrelli parcheggiati nell'area dei carrelli parcheggiati verrà aggiornato.
3. Inizia la transazione del prossimo cliente sul registratore ora vuoto.

Se il cliente era stato associato alla vendita prima del parcheggio, il suo nome apparirà nell'elenco dei carrelli parcheggiati per un facile riconoscimento.

## Come riprendere una transazione parcheggiata

1. Tocca l'area o l'icona **Carrelli parcheggiati** sul registratore di cassa. Verrà visualizzata un elenco di tutti i carrelli attualmente parcheggiati su questo terminale, mostrando il nome del cliente (se uno è stato associato), il numero di articoli, l'importo totale, il cassiere che ha parcheggiato il carrello e l'orario in cui è stato parcheggiato.
2. Tocca il carrello che desideri riprendere.
3. Se il tuo registratore attuale contiene degli articoli, il POS li pulirà prima di ripristinare il carrello parcheggiato. Assicurati di aver completato o parcheggiato la transazione corrente prima di riprendere un'altra.
4. Gli articoli del carrello parcheggiato, l'associazione al cliente e gli sconti manuali vengono tutti ripristinati. La vendita continua come normale.

## Visibilità dei carrelli parcheggiati

I carrelli parcheggiati sono **associati al terminale** su cui sono stati creati. Qualsiasi cassiere che si è loggato sullo stesso terminale può vedere e riprendere qualsiasi carrello parcheggiato su quel terminale — non esiste alcuna restrizione per cassiere su chi può riprendere un carrello parcheggiato.

I carrelli parcheggiati su un terminale diverso, anche nello stesso punto vendita, non sono visibili sul tuo terminale corrente.

## Annullamento di un carrello parcheggiato dal POS

Un cassiere può eliminare un carrello parcheggiato direttamente dall'elenco dei carrelli parcheggiati sul terminale — tocca il carrello e usa l'opzione di eliminazione o scarto. I carrelli parcheggiati eliminati vengono rimossi in modo permanente e non possono essere recuperati.

## Scadenza automatica e pulizia

Ogni carrello parcheggiato scade **24 ore dopo che è stato parcheggiato**. Spwig esegue un compito in background che rimuove i carrelli scaduti che non sono mai stati ripristinati. Non c'è niente che devi fare — la pulizia avviene automaticamente.

Se devi eliminare i carrelli parcheggiati prima della finestra di 24 ore, un cassiere può eliminarli uno alla volta dall'elenco dei carrelli parcheggiati sul terminale.

## Turni e carrelli parcheggiati

Non esiste un collegamento rigido tra un carrello parcheggiato e il turno aperto quando è stato parcheggiato. Chiudere un turno **non** elimina o annulla automaticamente qualsiasi carrello parcheggiato su quel terminale. I carrelli parcheggiati sopravvivono ai cambi di turno e rimangono disponibili per l'intero periodo di 24 ore.

Questo significa:

- Un carrello parcheggiato alla fine di un turno mattutino può essere ripristinato da un cassiere in un turno successivo.
- Se non desideri che i carrelli parcheggiati siano disponibili tra i turni, fai in modo che i cassieri puliscano l'elenco dei carrelli parcheggiati prima di chiudere il loro turno.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Parcheggia un carrello non appena un cliente dice "Ho bisogno solo di prendere un altro oggetto" — è più veloce che chiedergli di aspettare in coda nuovamente o di aggiungere manualmente gli articoli.
- Se l'elenco dei carrelli parcheggiati sta diventando lungo, controlla se un cassiere precedente ha lasciato transazioni non risolte alla fine del loro turno e cancella eventuali carrelli obsoleti.
- Collega un cliente alla vendita prima di parcheggiare quando puoi — il loro nome appare nell'elenco, rendendo molto più facile trovare il carrello giusto quando tornano.
- I carrelli parcheggiati scadono dopo 24 ore, quindi non sono adatti per mantenere le transazioni per tutta la notte attraverso diversi giorni feriali.
- Ricorda che riprendere un carrello parcheggiato cancellerà ciò che è attualmente nel registratore di cassa.

Completa o parcheggia la transazione attiva prima di prendere un diverso carrello parcheggiato.