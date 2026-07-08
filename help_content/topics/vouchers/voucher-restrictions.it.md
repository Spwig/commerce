---
title: Limitazioni dei Buoni
---

Le limitazioni dei buoni controllano chi può utilizzare un buono, quando e con quale frequenza. Configura queste impostazioni quando crei o modifichi un buono a **Marketing > Buoni**.

![Regole delle Limitazioni](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Limiti di Utilizzo

Imposta i limiti globali e per cliente nella sezione **Limiti di Utilizzo** del modulo del buono.

- **Max uses total** — Il numero massimo di volte in cui questo buono può essere riscosso da tutti i clienti. Lascia vuoto per un limite illimitato.
- **Max uses per customer** — Quante volte un singolo cliente può utilizzare questo buono. Imposta su 1 per la maggior parte delle campagne.

| Pattern | Max Total | Per Customer | Use Case |
|---------|-----------|--------------|----------|
| Campagna limitata | 100 | 1 | "Primi 100 clienti" scarsità |
| Codice condiviso illimitato | (vuoto) | 1 | Campagna di marketing continua |
| Utilizzo multipla illimitato | (vuoto) | (vuoto) | Sconto interno/personale |
| Codici unici a uso singolo | 1 | 1 | Codici generati in blocco per campagne |

## Valore Minimo dell'Ordine

Il campo **Min order value** protegge i tuoi margini richiedendo un totale del carrello prima che il buono venga applicato. Ad esempio, "$10 di sconto su ordini superiori a $50" assicura che non si scontino mai ordini piccoli al punto di diventare non profittevoli.

| Sconto | Valore Minimo Consigliato | Rapporto |
|----------|-------------------|-------|
| $5 di sconto | $30+ | ~6:1 |
| $10 di sconto | $50+ | ~5:1 |
| $20 di sconto | $100+ | ~5:1 |
| 15% di sconto | $40+ | Dipende dal catalogo |

## Limite di Sconto (Massimo Importo di Sconto)

Il campo **Max discount amount** in **Discount Configuration** limita quanto un buono percentuale può dedurre. Questo si applica solo ai buoni di tipo percentuale e impedisce sconti eccessivi su carrelli ad alto valore.

Esempio: "20% di sconto, massimo $50 di sconto"
- Carrello di $200 = $40 di sconto (20%)
- Carrello di $300 = $50 di sconto (limitato)
- Carrello di $1.000 = ancora $50 di sconto (limitato)

Aggiungi un limite di sconto a qualsiasi buono percentuale condiviso pubblicamente.

## Regole di Combinazione

Il fieldset **Restrictions & Rules** (clicca per espandere) contiene caselle di controllo che regolano come i buoni interagiscono con altri sconti.

| Impostazione | Cosa Fa | Quando Abilitare |
|---------|--------------|----------------|
| **Escludi articoli in promozione** | Il buono salta i prodotti già in promozione | La maggior parte delle campagne — protegge i margini delle promozioni |
| **Non combinabile con altri buoni** | Solo un buono per ordine | Predefinito per la maggior parte dei buoni |
| **Non combinabile con articoli in promozione** | Blocca il buono se il carrello contiene QUALSIASI articolo in promozione | Campagne rigorose in cui il buono sostituisce i prezzi di promozione |
| **Solo per nuovi clienti** | Solo clienti con zero ordini precedenti | Campagne di benvenuto/acquisizione |

## Limitazioni dei Clienti

Per un targeting semplice, seleziona **Solo per nuovi clienti** nel fieldset **Restrictions & Rules**.

Per un targeting avanzato, utilizza la tabella inline **Voucher Restrictions** in fondo al modulo. Clicca su **+ Aggiungi un'altra limitazione del buono** per aggiungere righe. Ogni limitazione ha tre campi:

- **Type** — La categoria della limitazione (menu a discesa)
- **Value** — Il valore corrispondente (separato da virgole o JSON)
- **Is inclusive** — Selezionato = il cliente deve corrispondere; non selezionato = il cliente non deve corrispondere

| Type | Value | Inclusive | Effect |
|------|-------|-----------|--------|
| user_email_domain | @company.com | Yes | Solo i dipendenti di company possono utilizzarlo |
| shipping_country | US,CA | Yes | Solo clienti degli Stati Uniti e del Canada |
| shipping_country | RU | No | Tutti TRanne la Russia |
| day_of_week | monday,tuesday | Yes | Solo valido lunedì e martedì |
| payment_method | stripe | Yes | Solo per pagamenti Stripe |

Combina più righe per limitazioni a strati. Tutte le limitazioni inclusive devono corrispondere, e nessuna limitazione esclusiva può corrispondere, affinché il buono venga applicato.

## Strategie di Scadenza

Controlla quando un buono scade utilizzando i campi data e validità.

- **End date** — Una scadenza fissa (es. 31 dicembre 2026).

Il buono smette di funzionare a mezzanotte.
- **Days valid** — Validità rotante a partire dalla creazione o primo utilizzo del buono.

Annulla la data di fine quando impostato.


Utili per i codici di benvenuto: "validi per 30 giorni dopo averli ricevuti".

| Strategia | Data di fine | Giorni validi | Caso d'uso |
|----------|----------|------------|----------|
| Scadenza fissa | Impostata | (vuoto) | Campagne stagionali, eventi |
| Finestra mobile | (vuoto) | 30 | Codici di benvenuto, buoni premio |
| Nessuna scadenza | (vuoto) | (vuoto) | Codici continui, sconti per il personale |

## Prevenire l'abuso

Segui questa checklist per mantenere i tuoi buoni sicuri:

- Imposta sempre **Massimo utilizzo per cliente** su 1, a meno che non esista un motivo specifico per non farlo.
- Imposta **Valore minimo dell'ordine** su tutti i buoni con importo fisso.
- Aggiungi un **Massimo importo di sconto** sui buoni percentuali pubblici.
- Utilizza codici difficili da indovinare per i buoni ad alto valore — evita codici ovvi come "DISCOUNT50".
- Monitora le analisi di utilizzo su ogni carta buono nel dashboard.
- Disattiva immediatamente un buono se noti pattern di utilizzo insoliti.
- Per campagne ad alto valore, utilizza codici unici generati in blocco invece di un singolo codice condiviso.

## Consigli

- Inizia con limiti restrittivi e allenta i limiti se l'utilizzo è troppo basso — è più facile rilassare le regole che stringerle dopo che i codici sono in circolazione.
- Testa ogni buono con un checkout reale prima di distribuirlo ai clienti.
- Controlla regolarmente il dashboard delle analisi dei buoni per individuare problemi in anticipo.
- Combina più restrizioni per una protezione a strati — ad esempio, limite per cliente + valore minimo dell'ordine + limite di sconto + escludi articoli in promozione.