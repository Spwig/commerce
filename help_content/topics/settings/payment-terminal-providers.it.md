---
title: Fornitori di terminali di pagamento
---

I fornitori di terminali di pagamento abilitano l'accettazione di carte di credito e debito nei tuoi terminali POS. Stripe Terminal è il principale fornitore supportato, offrendo lettori di carte moderni (S700, WisePOS E, P400), tariffe competitive per l'elaborazione e un'integrazione senza interruzioni. Configura gli account dei fornitori con le credenziali API, monitora lo stato della connessione in tempo reale e gestisci più fornitori se operi in diverse regioni. Il sistema dei fornitori è estensibile - possono essere integrati ulteriori processori di pagamento tramite il framework dei fornitori se Stripe Terminal non opera nel tuo mercato.

Utilizza i fornitori di pagamento per accettare i pagamenti con carta in modo sicuro, tracciare lo stato dell'elaborazione dei pagamenti e gestire l'assegnazione dei lettori tra i terminali.

![Elenco dei fornitori di pagamento](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Panoramica dei fornitori di pagamento

I fornitori di pagamento sono servizi di terze parti che elaborano i pagamenti con carta a nome del tuo business:

**Responsabilità del fornitore**:
- Autorizzare le transazioni con carta in tempo reale
- Comunicare con i lettori fisici di carta
- Gestire la sicurezza dei pagamenti (conformità PCI, crittografia)
- Trasferire i fondi sul tuo conto bancario (liquidazione)
- Fornire report sulle transazioni e la gestione delle dispute

**Ruolo di Spwig**:
- Indirizza le richieste di pagamento al fornitore configurato
- Archivia le credenziali del fornitore crittografate
- Monitora lo stato della connessione
- Associa i lettori ai terminali
- Registra i risultati dei pagamenti negli ordini

## Stripe Terminal (Fornitore principale)

Stripe Terminal è il fornitore di pagamento consigliato per la maggior parte dei commercianti:

**Funzionalità**:
- Lettori di carte a chip EMV moderni
- Supporto per pagamenti senza contatto (NFC) (Apple Pay, Google Pay, carte tap-to-pay)
- Gestione delle dispute integrata
- Autorizzazione in tempo reale
- API amichevole per gli sviluppatori
- Disponibile in 40+ paesi

**Prezzi** (a partire dal 2024, verificare le tariffe attuali):
- Tariffe per transazione: 2,7% + $0,05 per transazione in persona (USA)
- Nessuna tariffa mensile, nessuna tariffa di configurazione, nessuna tariffa di conformità PCI
- Hardware del lettore di carte: acquisto unico ($59-$299 a seconda del modello)

**Regioni supportate**:
- Stati Uniti, Canada, Regno Unito, Unione Europea, Australia, Singapore e molto altro
- Controlla la disponibilità di Stripe: https://stripe.com/terminal

**Lettori supportati**:
- BBPOS WisePOS E (terminale Android tutto-in-uno)
- Stripe Reader S700 (lettore da banco)
- Verifone P400 (lettore legacy, ancora supportato)

## Configurazione di Stripe Terminal

**Passo 1: Crea un account Stripe**
- Registrati su stripe.com
- Completa la verifica aziendale (conto bancario, ID fiscale)
- Attiva i pagamenti

**Passo 2: Abilita Stripe Terminal**
- Nel pannello di controllo di Stripe, vai a **Prodotti > Terminal**
- Clicca su **Inizia**
- Accetta i termini e le condizioni del Terminal

**Passo 3: Crea una posizione**
- Stripe Terminal richiede una "Posizione" che rappresenta il tuo sito retail fisico
- Vai a **Terminal > Posizioni**
- Clicca su **Crea posizione**
- Inserisci l'indirizzo e i dettagli del negozio
- Salva l'ID della posizione (sembra `tml_1ABC123...`)

**Passo 4: Genera una chiave API**
- Vai a **Sviluppatori > Chiavi API**
- Trova la tua **Chiave segreta** (inizia con `sk_live_...` per la produzione, `sk_test_...` per i test)
- Copia la chiave segreta (non condividerla pubblicamente)

**Passo 5: Configura in Spwig**
- Vai a **POS > Fornitori di pagamento**
- Clicca su **+ Aggiungi fornitore di pagamento**
- Seleziona **Fornitore**: "Stripe Terminal"
- Inserisci **Chiave segreta API** (dal passo 4)
- Inserisci **ID posizione** (dal passo 3)
- Salva

**Passo 6: Testa la connessione**
- Dopo aver salvato, lo stato del fornitore dovrebbe cambiare in "Connesso" (verde)
- Se lo stato mostra "Errore" (rosso), verifica la chiave API e l'ID posizione
- Controlla il messaggio di errore nella vista dettagliata del fornitore

![Form per l'aggiunta di un fornitore di pagamento](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Campi di configurazione del fornitore

**Chiave del fornitore** - Seleziona il processore di pagamento:
- **stripe_terminal** - Stripe Terminal (consigliato)
- **manual** - Inserimento manuale del pagamento (solo per test, nessuna elaborazione effettiva)
- Possono apparire ulteriori fornitori se installati tramite il sistema di componenti

**Credenziali (Crittografate)** - Struttura JSON contenente le credenziali API:
- Crittografate automaticamente prima del salvataggio
- Mai visibili in testo semplice dopo il salvataggio
- Esempio di struttura (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Impostazioni del fornitore** - Configurazione aggiuntiva (specifiche del fornitore):
- Descrittore dello stato (appare sulla fattura della carta di credito del cliente)
- Cattura automatica (cattura immediatamente le transazioni autorizzate rispetto alla cattura manuale)
- Sovrascrittura della valuta (se l'account del fornitore utilizza una valuta diversa da quella del negozio)

**Stato della connessione** - Indicatore di stato in tempo reale:
- **Connesso** (verde) - Il fornitore è raggiungibile e configurato correttamente
- **Errore** (rosso) - Connessione fallita o credenziali non valide
- **Sconosciuto** (grigio) - Non ancora testato (immediatamente dopo la creazione)

**Ultimo test** - Timestamp dell'ultimo test di connessione
- Aggiornato automaticamente quando vengono elaborate le transazioni
- Triggera manualmente il test tramite l'azione amministrativa **Test Connection**

## Monitoraggio dello stato della connessione

Il sistema monitora la connettività dei fornitori per avvisarti di eventuali problemi prima che i clienti tentino di effettuare pagamenti:

**Test automatico**:
- Ogni transazione di pagamento attiva un test di connessione (necessità)
- Un lavoro in background testa la connessione ogni 6 ore (monitoraggio preventivo)

**Significato degli stati**:

**Connesso** - L'API del fornitore è raggiungibile, le credenziali sono valide, pronte per elaborare i pagamenti

**Errore** - Cause comuni:
- Chiave API non valida (revocata, scaduta o errata)
- ID posizione non valido (posizione eliminata in Stripe, ID errato inserito)
- Problemi di connettività di rete (firewall che blocca l'API di Stripe)
- Interruzione del servizio Stripe (raro)

**Sconosciuto** - Fornitore mai testato (account appena creato in attesa della prima transazione)

**Risoluzione dello stato di errore**:
1. Controlla il messaggio di errore nella vista dettagliata del fornitore (spiega il problema specifico)
2. Verifica che la chiave API sia ancora valida nel pannello di controllo di Stripe
3. Verifica che l'ID posizione esista ancora nel pannello di controllo di Stripe
4. Esegui manualmente il test di connessione tramite l'azione amministrativa **Test Connection**
5. Aggiorna le credenziali se necessario

![Dettagli del fornitore di pagamento](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Confronto dei lettori di carte supportati

Stripe Terminal offre diverse opzioni di hardware per i lettori:

| Modello | Tipo | Metodi di pagamento | Display | Migliore per | Prezzo |
|---------|------|---------------------|---------|--------------|-------|
| **WisePOS E** | Tutto-in-uno | Chip EMV, NFC, swipe | Touchscreen a colori da 5" | POS al dettaglio completo di funzionalità | ~$299 |
| **S700** | Da banco | Chip EMV, NFC, swipe | LCD monocromatico | Checkout al dettaglio standard | ~$249 |
| **P400** | Da banco | Chip EMV, NFC, swipe | LCD monocromatico | Deployment legacy | ~$299 |

**Vantaggi di WisePOS E**:
- Basato su Android (esegue app, può visualizzare contenuti personalizzati)
- Touchscreen a colori (migliore esperienza utente per le richieste di mancia, la firma)
- Stampa ricevute integrate (opzionale)
- Velocità di transazione più rapida

**Vantaggi di S700**:
- Costo inferiore rispetto a WisePOS E
- Dimensioni compatte
- Design resistente all'acqua

**P400** (modello più vecchio):
- Ancora supportato ma non consigliato per nuove deployment
- Elaborazione delle carte a chip più lenta rispetto a S700/WisePOS E

Tutti i lettori si connettono al POS di Spwig tramite l'API di Stripe Terminal (nessuna connessione diretta USB/Bluetooth al dispositivo POS richiesta).

## Considerazioni sulla sicurezza

**Crittografia delle credenziali**:
- Tutte le credenziali dei fornitori sono crittografate in stato di riposo nel database
- La crittografia utilizza la chiave segreta dell'applicazione (definita nelle impostazioni dell'applicazione)
- Le credenziali non appaiono mai nei log o nei messaggi di errore

**Autorizzazioni della chiave API**:
- Utilizza **chiavi API ristrette** in produzione (limita le autorizzazioni al solo Terminal)
- Non utilizzare chiavi segrete non limitate (accesso più ampio del necessario = rischio di sicurezza)
- Nel pannello di controllo di Stripe, crea una chiave ristretta con solo **Terminal** autorizzazioni

**Conformità PCI**:
- Stripe Terminal gestisce la conformità PCI (i dati delle carte non toccano mai i server di Spwig)
- I numeri di carta vengono elaborati interamente sull'hardware del lettore → server Stripe → reti di carte
- Spwig archivia solo i risultati dei pagamenti (approvati/rifiutati), mai i dettagli delle carte

**Rotazione delle chiavi**:
- Ruota le chiavi API annualmente come pratica di sicurezza consigliata
- Quando si ruota, aggiorna le credenziali nella configurazione del fornitore
- Le chiavi vecchie possono essere revocate nel pannello di controllo di Stripe dopo aver confermato che la nuova chiave funziona

## Più fornitori

Alcuni commercianti necessitano di più account fornitori:

**Operazioni a più valute**:
- I negozi statunitensi utilizzano l'account Stripe USA (elabora USD)
- I negozi europei utilizzano l'account Stripe UE (elabora EUR)
- Configura un fornitore separato per ogni valuta

**Fornitori di backup**:
- Fornitore principale (Stripe Terminal)
- Fornitore di backup (inserimento manuale) quando i lettori non funzionano
- Il cassiere seleziona il fornitore quando inizia il pagamento

**Test vs produzione**:
- Fornitore di test con chiave API `sk_test_...`
- Fornitore di produzione con chiave API `sk_live_...`
- Passa ai fornitori dopo la fase di test

## Risoluzione dei problemi comuni

**Problema 1: Lo stato mostra "Errore" con il messaggio "Chiave API non valida"**
- **Causa**: Chiave API revocata o copiata in modo errato
- **Soluzione**: Genera una nuova chiave API nel pannello di controllo di Stripe, aggiorna le credenziali del fornitore, testa la connessione

**Problema 2: Lettore non rilevato durante il pagamento**
- **Causa**: Lettore non registrato alla posizione del fornitore
- **Soluzione**: Nel pannello di controllo di Stripe, verifica che il lettore sia registrato alla stessa ID posizione utilizzata nella configurazione del fornitore

**Problema 3: Pagamenti rifiutati nonostante carta valida**
- **Causa**: Account Stripe non completamente attivato (verifica in sospeso)
- **Soluzione**: Completa la verifica aziendale nel pannello di controllo di Stripe (conto bancario, ID fiscale)

**Problema 4: Lo stato della connessione mostra "Sconosciuto" e non si aggiorna mai**
- **Causa**: Fornitore mai testato (nessuna transazione tentata)
- **Soluzione**: Utilizza l'azione amministrativa **Test Connection** per attivare manualmente il test di connettività

## Consigli

- **Modalità di test prima della produzione** - Utilizza le chiavi API di test di Stripe (`sk_test_...`) per l'impostazione iniziale e i test
- **Un fornitore per valuta** - Non tentare di elaborare EUR con un account Stripe basato su USD; crea fornitori separati
- **Monitora lo stato della connessione settimanalmente** - Il monitoraggio proattivo previene i fallimenti dei pagamenti al momento del checkout
- **Limita le autorizzazioni della chiave API** - Limita le chiavi API di Stripe solo alle autorizzazioni Terminal (principio del privilegio minimo)
- **Documenta gli ID delle posizioni** - Mantieni un registro di quale posizione Stripe corrisponde a quale negozio fisico
- **Testa l'assegnazione del lettore** - Dopo la configurazione del fornitore, effettua un pagamento con un lettore di carte reale per verificare il flusso end-to-end
- **Mantieni aggiornate le informazioni di contatto di Stripe** - Assicurati che le informazioni di contatto aziendale in Stripe corrispondano alle attuali (importante per le dispute, la conformità)