---
title: Dominio di invio marketing
---

# Dominio di invio marketing

Il tuo negozio invia due tipi molto diversi di e-mail:

- **Transazionali** — conferme d'ordine, aggiornamenti di spedizione, reimpostazioni della password. Queste devono sempre arrivare nella casella di posta in arrivo.
- **Marketing** — newsletter, promozioni, recupero del carrello, avvisi di disponibilità.

Per impostazione predefinita, entrambi vengono inviati con la stessa identità di invio, il che significa che **condividono una singola reputazione del mittente**. Se una campagna di marketing genera reclami per spam o raggiunge indirizzi obsoleti, quella reputazione cala — e le tue conferme d'ordine e le reimpostazioni della password potrebbero iniziare a finire anche nella cartella spam.

Un **dominio di invio marketing** risolve questo problema. Configuri una seconda identità di invio — su un proprio sottodominio come `news.yourstore.com` — e la marchi per il marketing. Spwig invia quindi ogni campagna da quell'identità e mantiene le e-mail transazionali sul tuo dominio principale. Una campagna problematica non può più compromettere le e-mail che i tuoi clienti *devono* ricevere.

> Questo si applica ai negozi self-hosted. Nei piani ospitati da Spwig, la reputazione di invio viene gestita per te.

## Come Spwig decide quale identità utilizzare

Una volta che esiste un account di invio marketing, il routing è automatico — non devi etichettare nulla:

- **E-mail di marketing** (campagne, percorsi, newsletter, recupero del carrello, disponibilità) →
  il dominio di invio marketing.
- **E-mail transazionali** (ordini, spedizioni, reimpostazioni della password, verifica) → il tuo
  dominio principale.

Se non configuri mai un dominio marketing, nulla cambia: tutto continua a essere inviato
dal tuo account predefinito esattamente come prima.

## Configurazione

Puoi iniziare da uno di questi due punti di accesso:

- Il pulsante **"Configura dominio marketing"** nella banner della dashboard di Campaign Studio, oppure
- **Account e-mail → "Dominio di invio marketing"**.

![La dashboard di Campaign Studio con la banner "Proteggi le tue e-mail transazionali" e il suo pulsante Configura dominio marketing](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![Il pulsante Dominio di invio marketing nell'elenco degli Account e-mail, accanto a Sfoglia Provider](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Entrambi aprono la procedura guidata di configurazione e-mail pre-impostata per un account marketing. Quindi:

1. **Scegli un sottodominio.** Usa qualcosa come `news.yourstore.com` o
   `mail.yourstore.com`. Questo è il passaggio più importante: l'identità di marketing deve essere un
   **(sotto)dominio diverso** da quello utilizzato dalle tue e-mail transazionali — quella separazione
   è esattamente ciò che protegge la tua reputazione transazionale. Inviare marketing dal tuo
   dominio principale non ti offre alcuna isolamento.
2. **Inserisci l'indirizzo del mittente** su quel sottodominio, ad es. `news@news.yourstore.com`.
3. **Aggiungi i record DNS.** La procedura guidata genera record SPF, DKIM e DMARC per il
   sottodominio — incluso una chiave DKIM unica per questa identità di marketing. Aggiungili presso
   il tuo provider DNS (la procedura guidata ha pulsanti di copia e schede per provider), quindi esegui il
   controllo finché tutti i record non superano la verifica.
4. **Completa.** L'account viene creato e marcato **Solo marketing**. Da ora in poi le tue
   campagne verranno inviate da esso.

Puoi verificare che abbia funzionato nell'elenco **Account e-mail**: vedrai un secondo account con
lo scopo **Solo marketing** e la banner di Campaign Studio scomparirà.

## Buono a sapersi

- **Non puoi accidentalmente rompere le e-mail transazionali.** Spwig non ti consentirà di impostare il tuo unico
  account su "Solo marketing", né di disabilitare/eliminare il tuo ultimo account transazionale — c'è
  sempre un posto per le conferme d'ordine e le reimpostazioni della password.
- **Riscaldalo gradualmente.** Un dominio di invio completamente nuovo non ha ancora reputazione.

Aumenta il
  volume nel corso di un paio di settimane invece di inviare a tutta la tua lista fin dal primo giorno.
- **Mantieni sani i DNS del sottodominio.** SPF, DKIM e DMARC sul sottodominio di marketing
  devono rimanere validi, proprio come il tuo dominio principale.

Vedi il
  [Runbook per la consegnabilità delle email](deliverability) per una panoramica completa.
- **Il consenso continua ad applicarsi.** Le email di marketing vengono inviate solo agli iscritti che hanno scelto di riceverle,
  e ogni campagna include un link per l'annullamento dell'iscrizione — la separazione del dominio non modifica
  nessuno di questi aspetti.