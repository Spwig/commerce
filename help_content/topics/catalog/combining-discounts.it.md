---
title: Combinare Sconti
---

La piattaforma offre quattro tipi di sconti che possono funzionare insieme: sconti sui prodotti, promozioni, codici sconto e carte regalo. Comprendere come interagiscono aiuta a condurre campagne efficaci senza risultati inaspettati o sconti doppi non intenzionali.

## I Quattro Livelli di Sconto

Ogni tipo di sconto opera a un livello diverso e è visibile ai clienti in modi diversi.

| Livello | Dove è Impostato | Come Viene Applicato | Visibile al Cliente |
|--------|------------------|--------------------|---------------------|
| **Sconto sul Prodotto** | Formulario di modifica prodotto > Sezione Sconto | Modifica automaticamente il prezzo visualizzato | Sì — mostrato come prezzo originale barrato |
| **Promozione** | Marketing > Vendite e Promozioni | Applicato automaticamente ai prodotti corrispondenti | Sì — mostrato come prezzo di vendita sulle schede prodotto |
| **Codice Sconto** | Marketing > Codici Sconto | Il cliente inserisce un codice al checkout | Solo al checkout dopo aver inserito il codice |
| **Carta Regalo** | Applicato al checkout da un saldo di carta regalo | Riduce l'importo totale del pagamento | Solo al checkout |

## Come Funziona la Priorità

Le promozioni hanno un campo **Priorità** che accetta valori da 0 in su. Valori più alti significano priorità più alta.

Quando più promozioni corrispondono allo stesso prodotto, quella con **la priorità più alta vince**. Non si sovrappongono — solo una promozione si applica per prodotto.

**Esempio:** "Flash Sale 50% di sconto" (priorità 10) e "Summer Sale 20% di sconto" (priorità 5) si rivolgono a tutti i prodotti. Un cliente vede il prezzo della flash sale del 50%, non un 70% combinato.

Nello stesso livello di priorità, il sistema seleziona la promozione che offre lo sconto più grande al cliente.

## Regole di Sovrapposizione

La seguente tabella mostra quali combinazioni di sconti sono consentite e come controllarle.

| Combinazione | Consentito? | Come Controllarlo |
|--------------|------------|-------------------|
| Sconto sul Prodotto + Promozione | Solo se abilitato | Controlla **"Abilita sovrapposizione con sconti sui prodotti"** nelle Impostazioni Avanzate della promozione |
| Promozione + Promozione | No — vince la priorità più alta | Imposta i valori di priorità per controllare quale si applica |
| Promozione + Codice Sconto | Sì | Lo sconto della promozione riduce il prezzo del prodotto, il codice sconto riduce l'importo totale del carrello separatamente |
| Codice Sconto + Codice Sconto | Configurabile | La bandiera **"Non combinabile con altri codici sconto"** del codice sconto controlla questo (abilitata di default) |
| Codice Sconto + Articoli in Sconto | Configurabile | La bandiera **"Escludi articoli in sconto"** del codice sconto controlla questo |
| Carta Regalo + Qualsiasi Sconto | Sì — sempre | Le carte regalo vengono applicate per ultime, riducendo l'importo finale del pagamento dopo tutti gli altri sconti |

## Scenario Comuni

### Scenario A: Promozione su tutto il sito + codice sconto

- **Configurazione:** 20% di sconto su tutto (promozione) + il cliente ha un codice sconto di $10
- **Risultato:** Un prodotto da $100 diventa $80 (promozione), quindi il codice sconto di $10 si applica all'importo totale del carrello. Il cliente paga **$70**.

### Scenario B: Prodotto in sconto + promozione su tutto il sito

- **Configurazione:** Il prodotto ha uno sconto del 30% a livello di prodotto + esiste una promozione del 20% su tutto il sito
- **Risultato (sovrapposizione disabilitata):** Si applica solo lo sconto sul prodotto. Il cliente paga **$70**.
- **Risultato (sovrapposizione abilitata):** Entrambi si applicano. 30% di sconto iniziale = $70, quindi 20% di sconto = **$56**.

### Scenario C: Due promozioni sullo stesso prodotto

- **Configurazione:** "Flash Sale 40% di sconto" (priorità 10) + "Summer Sale 20% di sconto" (priorità 5), entrambe si rivolgono a tutti i prodotti
- **Risultato:** La Flash Sale vince perché ha una priorità più alta. Il cliente paga **$60** per un prodotto da $100.

### Scenario D: Codice sconto su un prodotto in sconto

- **Configurazione:** Il prodotto è in sconto del 25%. Il cliente inserisce un codice sconto del 10% che ha la bandiera "Escludi articoli in sconto" abilitata.
- **Risultato:** Il codice sconto non si applica a quel prodotto. Se il carrello contiene articoli non in sconto, il codice sconto si applica solo a quelli.

## Quale Tipo di Sconto Utilizzare

| Obiettivo | Approccio Consigliato | Perché |
|----------|----------------------|------|
| Smaltire l'inventario stagionale | **Promozione** (target su categoria o raccolta) | Automatico, non richiede azione del cliente, visibile sulle schede prodotto |
| Riconoscere un cliente specifico | **Codice Sconto** (uso singolo, limite per cliente) | Mirato, tracciabile, sembra personale |
| Offerta rapida per un singolo prodotto | **Sconto sul Prodotto** (sul formulario di modifica prodotto) | Più veloce da impostare, non è necessario l'aiuto per le promozioni |
| Credito o regalo | **Carta Regalo** | Basata su saldo, il cliente gestisce il proprio credito |
| Evento su tutto il sito | **Promozione** (target su tutti i prodotti) | Maggiore raggio d'azione, una configurazione copre tutto |
| Campagna per recuperare clienti | **Codice Sconto** (limiti per clienti nuovi o ritornati) | Può mirare a specifici segmenti di clienti |

## Consigli

- **Testa con un carrello reale** — dopo aver configurato le promozioni e i codici sconto, aggiungi prodotti a un carrello e procedi al checkout per verificare che gli sconti si applichino come previsto.
- **Verifica il numero di prodotti interessati** — nel passo di revisione della promozione, verifica che il numero di prodotti interessati corrisponda all'intento.
- **Usa la priorità con attenzione** — se esegui più promozioni contemporaneamente, imposta sempre valori di priorità diversi in modo da controllare quale vince.
- **Mantieni la sovrapposizione disabilitata di default** — abilita "Abilita sovrapposizione con sconti sui prodotti" solo quando desideri specificamente sconti doppi.
- **Documenta la tua strategia** — usa il campo Descrizione della promozione per annotare il motivo per cui esiste una promozione e come si relaziona ad altre promozioni attive.