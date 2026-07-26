---
title: Combinazione degli sconti
---

La piattaforma offre quattro tipi di sconti che possono funzionare insieme: sconti sui prodotti, promozioni, codici voucher e carte regalo. Comprendere come interagiscono aiuta a condurre campagne efficaci senza risultati inaspettati o sconti doppi non intenzionali.

> **Le carte regalo non possono essere applicate al momento del checkout online.** Il design descritto di seguito — carta regalo applicata per ultima, dopo tutti gli altri sconti — è come funzionerà una volta che questa funzionalità sarà disponibile. Al momento, una carta regalo può essere utilizzata solo in persona al **Punto di Vendita**, quindi le interazioni descritte per il negozio online non si applicano ancora specificamente alle carte regalo. Vedere l'argomento **Carte Regalo** per lo stato attuale.

## Le Quattro Strati di Sconto

Ogni tipo di sconto opera a un livello diverso e è visibile ai clienti in modi diversi.

| Strato | Dove è Impostato | Come è Applicato | Visibile al Cliente |
|-------|---------------|-----------------|-------------------|
| **Sconto sul Prodotto** | Formulario di modifica del prodotto > Sezione Sconto | Modifica automaticamente il prezzo visualizzato | Sì — mostrato come prezzo originale barrato |
| **Promozione** | Marketing > Vendite e Promozioni | Applicato automaticamente ai prodotti corrispondenti | Sì — mostrato come prezzo di vendita sulle schede dei prodotti |
| **Codice Voucher** | Marketing > Voucher | Il cliente inserisce un codice al checkout | Solo al checkout dopo aver inserito il codice |
| **Carta Regalo** | Utilizzata contro il saldo di una carta regalo | Riduce l'importo totale del pagamento | Solo al Punto di Vendita per ora (vedi nota sopra) |

## Come Funziona la Priorità

Le promozioni hanno un campo **Priorità** che accetta valori da 0 in su. Valori più alti significano priorità più alta.

Quando più promozioni corrispondono allo stesso prodotto, quella con la **priorità più alta vince**. Non si sovrappongono — solo una promozione si applica per prodotto.

**Esempio:** "Flash Sale 50% di sconto" (priorità 10) e "Summer Sale 20% di sconto" (priorità 5) si applicano a tutti i prodotti. Il cliente vede il prezzo della flash sale al 50%, non un 70% combinato.

Nello stesso livello di priorità, il sistema seleziona la promozione che offre lo sconto più grande al cliente.

## Regole di Sovrapposizione

La seguente tabella mostra quali combinazioni di sconti sono consentite e come controllarle.

| Combinazione | Consentito? | Come Controllarlo |
|-------------|----------|-------------------|
| Sconto sul Prodotto + Promozione | Solo se abilitato | Controlla **"Abilita sovrapposizione con sconti sui prodotti"** nelle Impostazioni Avanzate della promozione |
| Promozione + Promozione | No — vince la promozione con priorità più alta | Imposta i valori di priorità per controllare quale si applica |
| Promozione + Codice Voucher | Sì | La promozione riduce il prezzo del prodotto, il voucher riduce separatamente il totale del carrello |
| Voucher + Voucher | Configurabile | La bandiera **"Non combinabile con altri voucher"** del voucher controlla questo (abilitata di default) |
| Voucher + Prodotti in Sconto | Configurabile | La bandiera **"Escludi prodotti in sconto"** del voucher controlla questo |
| Carta Regalo + Qualsiasi Sconto | Sì — sempre | Le carte regalo vengono applicate per ultime, riducendo l'importo finale del pagamento dopo tutti gli altri sconti. Al momento possibile solo al Punto di Vendita — vedi nota sopra |

## Scenario Comuni

### Scenario A: Promozione su tutto il sito + codice voucher

- **Configurazione:** 20% di sconto su tutto (promozione) + il cliente ha un voucher di $10 di sconto
- **Risultato:** Un prodotto da $100 diventa $80 (promozione), quindi il voucher di $10 si applica al totale del carrello. Il cliente paga **$70**.

### Scenario B: Prodotto in sconto + promozione su tutto il sito

- **Configurazione:** Il prodotto ha uno sconto del 30% a livello di prodotto + esiste una promozione del 20% su tutto il sito
- **Risultato (sovrapposizione disabilitata):** Solo lo sconto sul prodotto si applica. Il cliente paga **$70**.
- **Risultato (sovrapposizione abilitata):** Entrambi si applicano. 30% di sconto iniziale = $70, quindi 20% di sconto = **$56**.

### Scenario C: Due promozioni sullo stesso prodotto

- **Configurazione:** "Flash Sale 40% di sconto" (priorità 10) + "Summer Sale 20% di sconto" (priorità 5), entrambe si applicano a tutti i prodotti
- **Risultato:** La Flash Sale vince perché ha una priorità più alta. Il cliente paga **$60** su un prodotto da $100.

### Scenario D: Voucher su un prodotto in sconto

- **Configurazione:** Il prodotto è in sconto del 25%.

# Risultati dei voucher con esclusione degli articoli in vendita

Il cliente inserisce un codice sconto del 10% che ha attivata l'opzione "Escludi articoli in vendita".
- **Risultato:** Il voucher non si applica a quel prodotto.

Se il carrello contiene articoli non in vendita, il voucher si applica solo a questi.

## Quale tipo di sconto utilizzare

| Obiettivo | Approccio consigliato | Perché |
|----------|---------------------|-------|
| Smaltire l'inventario stagionale | **Promozione** (target su categoria o raccolta) | Automatico, non richiede azione del cliente, visibile sulle schede prodotto |
| Riconoscere un cliente specifico | **Codice sconto** (uso singolo, limite per cliente) | Mirato, tracciabile, sembra personale |
| Offerta rapida per un singolo prodotto | **Vendita del prodotto** (nella scheda modifica prodotto) | Più veloce da impostare, non è necessario l'assistente per le promozioni |
| Crediti per il negozio o regali | **Carta regalo** | Basato su saldo; attualmente utilizzabile solo al momento del pagamento |
| Evento su tutta la sede | **Promozione** (target su tutti i prodotti) | Maggiore raggio d'azione, una configurazione copre tutto |
| Campagna per recuperare clienti | **Codice sconto** (limiti per clienti nuovi o ritornati) | Può mirare a specifici segmenti di clienti |

## Consigli

- **Testa con un carrello reale** — dopo aver configurato le promozioni e i codici sconto, aggiungi prodotti a un carrello e procedi al checkout per verificare che gli sconti si applichino come previsto.
- **Verifica il numero di prodotti interessati** — nella fase di revisione della promozione, verifica che il numero di prodotti interessati corrisponda all'intento.
- **Utilizza la priorità con attenzione** — se esegui più promozioni contemporaneamente, imposta sempre valori di priorità diversi in modo da controllare quale vince.
- **Mantieni disattivato lo stacking per default** — attiva "Stack con vendite di prodotti" solo quando desideri specificamente sconti doppi.
- **Documenta la tua strategia** — utilizza il campo Descrizione della promozione per annotare il motivo per cui esiste una promozione e come si relaziona ad altre promozioni attive.