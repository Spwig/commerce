---
title: Configurazione della spedizione
---

# Configurazione della spedizione

Questo documento illustra come configurare la spedizione per il tuo negozio — dagli approcci di base alle integrazioni con i carrier per ottenere tariffe in tempo reale.

## Panoramica della spedizione

Spwig offre due approcci per la spedizione:

- **Metodi di spedizione manuali** — Metodi a tariffe fisse che definisci tu (es. "Spedizione standard — $5.99")
- **Integrazioni con carrier** — Tariffe in tempo reale da fornitori come FedEx, UPS e DHL

Puoi utilizzare uno o entrambi gli approcci.

## Metodi di spedizione

I metodi di spedizione sono le opzioni che i tuoi clienti vedono al momento del checkout. Naviga verso **Ordini > Spedizioni** nel menu laterale per gestirli.

![Metodi di spedizione](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Creazione di un metodo di spedizione

1. Clicca su **Aggiungi metodo di spedizione**
2. Compila i dettagli:
   - **Nome** — Nome visualizzato ai clienti (es. "Consegna espressa")
   - **Descrizione** — Breve descrizione del servizio
   - **Prezzo** — Costo fisso di spedizione
   - **Consegna stimata** — Stimativa del tempo di consegna (es. "3-5 giorni lavorativi")
3. Clicca su **Salva**

## Zone di spedizione

Le zone di spedizione definiscono le aree geografiche in cui i tuoi metodi di spedizione si applicano. Naviga verso la sezione **Zona di spedizione** per gestirle.

![Zone di spedizione](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Creazione di una zona

1. Clicca su **Aggiungi zona di spedizione**
2. Configura la zona:
   - **Nome della zona** — Nome interno (es. "US Domestic", "Europa")
   - **Paesi** — Seleziona i paesi appartenenti a questa zona
   - **Stati/Regioni** — Opzionalmente restringi a specifici stati
   - **Pattern dei codici postali** — Usa pattern come "9*" per mirare a specifiche aree
3. Assegna i metodi di spedizione a questa zona
4. Clicca su **Salva**

### Priorità della zona

Quando l'indirizzo del cliente corrisponde a più zone, la zona più specifica ha la precedenza. Una zona con targeting a livello di stato ha la precedenza su una zona a livello di paese.

## Integrazioni con carrier

Connetti i carrier per offrire tariffe calcolate in tempo reale al momento del checkout.

![Carrier di spedizione](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Provider disponibili

Esplora e installa provider di spedizione dal marketplace.

![Provider di spedizione](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

I carrier supportati includono:

- **FedEx** — Terrestre, Espressa, Internazionale
- **UPS** — Terrestre, 2 giorni, Notte, Mondiale
- **DHL** — Espressa, E-commerce
- **USPS** — Prioritaria, Prima classe, Posta per media
- E molto altro disponibile sul Marketplace

### Configurazione di un carrier

1. Vai alla pagina dei provider di spedizione e clicca su **Installa** sul carrier preferito
2. Segui la procedura guidata:
   - **Passo 1** — Rivedi i dettagli del provider
   - **Passo 2** — Configura le impostazioni generali
   - **Passo 3** — Inserisci le tue credenziali API (numero di account, chiave API, ecc.)
   - **Passo 4** — Abilita servizi specifici (Terrestre, Espressa, ecc.)
   - **Passo 5** — Testa la connessione
3. Una volta connesso, le tariffe del carrier appaiono automaticamente al momento del checkout

### Credenziali API

Ogni carrier richiede un account API:

- **FedEx** — Registrati sul portale per sviluppatori FedEx, crea un'app e copia la tua chiave API e il segreto
- **UPS** — Registrati sul Kit per sviluppatori UPS, richiedi una chiave di accesso
- **DHL** — Contatta DHL per ottenere le credenziali API tramite il loro portale aziendale

## Regole di spedizione

Crea regole avanzate per controllare quando e come vengono offerti i metodi di spedizione.

### Regole comuni

- **Spedizione gratuita per ordini superiori a $50** — Imposta un importo minimo del carrello per la spedizione gratuita
- **Tariffa fissa per ordini leggeri** — Tariffa fissa quando il peso dell'ordine è al di sotto di un limite
- **Disattiva la spedizione espressa per aree remote** — Nascondi le opzioni di spedizione espressa in base ai codici postali
- **Markup percentuale** — Aggiungi una tariffa di gestione come percentuale delle tariffe dei carrier

### Creazione di una regola

1. Naviga nella sezione regole di spedizione
2. Clicca su **Aggiungi regola**
3. Imposta le condizioni (importo totale del carrello, peso, zona, ecc.)
4. Definisci l'azione (aggiusta la tariffa, nasconde il metodo, abilita la spedizione gratuita)
5. Salva la regola

Le regole vengono valutate nell'ordine — la prima regola corrispondente si applica.

## Spedizione gratuita

### Spedizione gratuita su tutto lo store

Abilita la spedizione gratuita a livello globale in **Impostazioni > Impostazioni dello store**:

- Attiva **Spedizione gratuita**
- Imposta opzionalmente un importo minimo per l'ordine
- Scegli quali regioni sono eleggibili

### Spedizione gratuita promozionale

Crea offerte di spedizione gratuita a tempo limitato:

1. Vai a **Marketing > Vendite e promozioni**
2. Crea una nuova promozione
3. Imposta la condizione: "Importo totale del carrello superiore a X"
4. Imposta l'azione: "Spedizione gratuita"
5. Configura le date di inizio e fine

## Spedizione internazionale

Per gli ordini internazionali, assicurati che i tuoi prodotti abbiano:

- **HS Code** — Classificazione tariffaria del sistema armonizzato
- **Paese d'origine** — Paese di produzione
- **Valore doganale** — Valore dichiarato per le dogane

Questi campi si trovano nella scheda **Inventario** di ogni prodotto. I carrier utilizzano queste informazioni per generare automaticamente la documentazione doganale.

## Suggerimenti

- Inizia con i metodi di spedizione manuali per avviare rapidamente il tuo negozio, quindi aggiungi le integrazioni con i carrier in seguito.
- Crea le zone di spedizione per le destinazioni più comuni prima.
- Testa sempre la configurazione di spedizione effettuando ordini di test con diversi indirizzi.
- Utilizza la funzione di markup delle tariffe per coprire i costi di gestione e imballaggio.
- Imposta soglie per la spedizione gratuita per aumentare il valore medio degli ordini.
