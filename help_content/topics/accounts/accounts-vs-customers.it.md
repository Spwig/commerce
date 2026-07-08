---
title: Accounts vs Customers
---

I commercianti spesso si chiedono: "Qual è la differenza tra un account e un cliente?" Questo malinteso è comune perché ogni cliente è un account, ma non ogni account è un cliente. Questa guida chiarisce la distinzione e spiega quando utilizzare ciascun'interfaccia amministrativa.

![User List](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## Cosa è un Account?

Un **account** è l'oggetto principale di autenticazione in Spwig. Chiunque possa accedere al tuo piattaforma — un membro dello staff o un cliente — ha un account. Gli account vengono gestiti nel sistema di autenticazione Spwig e sono archiviati nel modello `User`.

Tutti gli account hanno:
- **Indirizzo email** — L'identificatore principale e le credenziali di accesso
- **Nome utente** — Un nome utente unico (generato automaticamente dall'email per default)
- **Password** — Hashata e archiviata in modo sicuro
- **Flag is_staff** — Determina se l'account può accedere al backend amministrativo

Gli account possono anche autenticarsi tramite provider OAuth (Google, Facebook, ecc.) configurati a **Impostazioni > Autenticazione**.

## Cosa è un Cliente?

Un **cliente** è un tipo speciale di account con `is_staff=False`. I clienti fanno acquisti sul tuo negozio online, effettuano ordini e gestiscono i propri profili. Ogni account cliente è automaticamente esteso con:

- **CustomerProfile** — Archivia le preferenze, lo stato di iscrizione alla newsletter e i valori dei campi personalizzati
- **CustomerMetrics** — Traccia il valore vitale (LTV), i punteggi RFM, l'history degli ordini e i dati di segmentazione
- **OrderHistory** — Collegamenti a tutti gli ordini effettuati da questo cliente

I clienti possono essere:
- **Clienti registrati** — Creati tramite la registrazione sul negozio online o tramite l'amministrazione
- **Utenti ospiti** — Account temporanei creati durante il checkout come ospite (il nome utente inizia con `guest_`)
- **Clienti importati** — Migrati da altre piattaforme tramite l'importazione CSV

## La Differenza Principale

| Attributo | Account | Cliente |
|-----------|---------|----------|
| **Scopo** | Autenticazione e autorizzazione | Acquisti, ordini e analisi |
| **Ambito** | Membri dello staff E clienti | Solo clienti |
| **Flag is_staff** | True O False | Sempre False |
| **Dati estesi** | Nessuno (solo campi principali) | CustomerProfile + CustomerMetrics |
| **Posizione nell'amministrazione** | Impostazioni > Utenti | Clienti > Profili dei clienti |
| **Può accedere** | Sì | Sì |
| **Può effettuare ordini** | Solo se ha CustomerProfile | Sì |
| **Può accedere all'amministrazione** | Solo se is_staff=True | No |

In breve:
- Un **account** è chiunque possa accedere
- Un **cliente** è un account che effettua acquisti e ordini

## I Membri dello Staff Sono Anche Account

I membri dello staff sono account con `is_staff=True`. Possono accedere al backend amministrativo e eseguire azioni in base ai permessi assegnati **StaffRole**.

I membri dello staff possono avere opzionalmente un **CustomerProfile** se effettuano acquisti anche sul negozio online. Per esempio, se tu (il commerciante) effetti un ordine di test sul tuo stesso negozio, viene creato un CustomerProfile per il tuo account dello staff. Questo NON influisce sull'accesso amministrativo.

I permessi dello staff vengono controllati da:
- **StaffRole** — Definisce quali sezioni e azioni amministrative lo staff può accedere
- **Flag is_superuser** — Conferisce l'accesso completo e non limitato (usare con moderazione)

Gestisci i membri dello staff a **Impostazioni > Gestione dello Staff**.

## Utenti Ospiti

Il checkout come ospite crea account temporanei con nomi utente automaticamente generati che iniziano con `guest_`. Questi account:
- Hanno `is_staff=False` (sono clienti)
- Hanno un CustomerProfile (per l'associazione degli ordini)
- Hanno una password casuale (l'ospite non può accedere a meno che non si converte in un cliente registrato)
- Vengono esclusi per default dalle analisi dei clienti

Gli ospiti possono convertirsi in clienti registrati in:
1. Creare un account sul negozio online con la stessa email
2. Verificare l'indirizzo email
3. Il sistema unisce l'history degli ordini dell'ospite all'account registrato nuovo

Gestisci le impostazioni di conversione degli ospiti a **Impostazioni > Checkout > Checkout come ospite**.

## Dove Trovare Ogni Elemento

| Posizione nell'amministrazione | Cosa Gestisci | Caso d'uso Principale |
|----------------|-----------------|---------------|
| **Impostazioni > Utenti** | Tutti gli account (staff + clienti) | Reimposta password, attiva/disattiva account, assegna permessi staff |
| **Impostazioni > Gestione dello Staff** | Solo account staff (is_staff=True) | Assegna ruoli, gestisci l'accesso dei membri del team, configura i permessi |
| **Clienti > Profili dei clienti** | Solo account clienti (is_staff=False) | Visualizza le preferenze dei clienti, l'history degli ordini, LTV, punteggi RFM, segmenti |
| **Clienti > Analisi** | Metriche e segmenti dei clienti | Analizza il comportamento dei clienti, crea segmenti di marketing, traccia la ritenzione |

![Customer Profile List](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## Quando Utilizzare Ogni Interfaccia

Utilizza **Impostazioni > Utenti** quando hai bisogno di:
- Reimpostare la password di un cliente
- Disattivare un account compromesso
- Creare manualmente un account cliente
- Visualizzare le connessioni di accesso OAuth
- Vedere tutti gli account (staff + clienti) in una lista

Utilizza **Impostazioni > Gestione dello Staff** quando hai bisogno di:
- Aggiungere un nuovo membro del team
- Assegnare o modificare il ruolo di un membro dello staff
- Configurare i permessi dettagliati
- Controllare i log dell'attività dello staff

Utilizza **Clienti > Profili dei clienti** quando hai bisogno di:
- Visualizzare l'history degli ordini di un cliente
- Vedere le preferenze del cliente e i valori dei campi personalizzati
- Controllare lo stato di iscrizione alla newsletter
- Rivedere il valore vitale (LTV) e i punteggi RFM dei clienti
- Gestire i segmenti dei clienti

Utilizza **Clienti > Analisi** quando hai bisogno di:
- Identificare i clienti ad alto valore
- Creare segmenti di marketing (es. "clienti che non hanno ordinato in 90 giorni")
- Analizzare le tendenze del valore vitale (LTV) dei clienti
- Esportare le liste dei clienti per le campagne

## Consigli

- **I profili dei clienti vengono creati automaticamente** — Quando un cliente effettua il primo ordine (ospite o registrato), Spwig crea un record CustomerProfile e CustomerMetrics per l'analisi.
- **Lo staff può anche essere clienti** — Se un membro dello staff effettua un ordine sul negozio online, riceve un CustomerProfile. Questo è normale e non influisce sull'accesso amministrativo.
- **Gli account ospite possono ingombrare l'elenco utenti** — Utilizza l'interfaccia dei profili dei clienti per concentrarti sui clienti reali e coinvolti. L'elenco utenti include tutti gli account ospite.
- **Segmenta per is_staff=False** — Quando esporti le liste dei clienti per le campagne email, filtra sempre per `is_staff=False` per escludere i membri del team.
- **Gli account OAuth sono anche account** — Quando un cliente si autentica tramite Google o Facebook, Spwig crea un account e lo collega al profilo OAuth. Il campo email viene popolato dal fornitore OAuth.