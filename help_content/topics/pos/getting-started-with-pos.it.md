---
title: Getting Started with POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

Spwig POS trasforma qualsiasi tablet o browser in un registratore di cassa completo — collegato al tuo catalogo prodotti, all'inventario e alla cronologia degli ordini. Questa checklist ti guiderà da un'installazione nuova al primo acquisto. Ogni passaggio include un collegamento a un argomento dedicato se desideri i dettagli completi.

![POS Dashboard](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Passaggio 1: Abilita POS per un'ubicazione del negozio

I terminali POS sono associati a un'ubicazione fisica del negozio. In Spwig, le ubicazioni del negozio sono magazzini contrassegnati come ubicazioni retail.

1. Naviga verso **Catalogo > Magazzini** nel tuo menu laterale di amministrazione.
2. Apri il magazzino che desideri utilizzare come negozio, oppure crea uno nuovo.
3. Attiva l'interruttore **Ubicazione retail** e inserisci un **nome visualizzato per POS** (es. "High Street Store"). Questo nome appare sui ricevuti e nel selettore dei terminali.
4. Salva il magazzino.

Se hai più negozi o desideri raggrupparli per report regionali, crea prima un **Gruppo di negozi** in **POS > Gruppi di negozi**, quindi assegna ciascun magazzino a quel gruppo. I gruppi di negozi ti permettono di impostare una valuta, un fuso orario e un modello di ricevuta condivisi che tutte le ubicazioni nel gruppo erediteranno.

## Passaggio 2: Crea o verifica almeno un account dello staff con accesso POS

Lo staff si autentica al POS utilizzando le stesse credenziali utilizzate per l'amministrazione Spwig. Qualsiasi account dello staff con stato **Attivo** e almeno il permesso `pos_admin` può accedere al POS.

Per controllare o concedere l'accesso, vai a **Impostazioni > Gestione dello staff**, apri l'account dello staff e conferma che abbia il ruolo POS appropriato assegnato. Non è necessario un account POS separato.

## Passaggio 3: Registra il tuo primo terminale POS

Un terminale rappresenta un singolo registratore o dispositivo. Lo registrerai nell'amministrazione, quindi lo abbinerai a un dispositivo fisico utilizzando un codice di abbinamento a uso unico.

1. Naviga verso **POS > Terminali POS** e fai clic su **+ Aggiungi terminale POS**.
2. Assegna al terminale un nome (es. "Cassa frontale") e assegnalo all'ubicazione del negozio abilitata nel passaggio 1.
3. Salva il terminale. Spwig genera un **codice di abbinamento di 8 caratteri** — lo vedrai sulla pagina dei dettagli del terminale.
4. Sul dispositivo che desideri utilizzare come registratore, apri un browser e vai a `/pos/`.
5. Inserisci il codice di abbinamento quando richiesto. Il dispositivo è ora collegato a questo terminale.

Il codice di abbinamento è a uso unico. Se devi riassegnare un dispositivo, apri il terminale nell'amministrazione e fai clic su **Rigenera codice di abbinamento**.

Per le opzioni di configurazione hardware (stampa ricevute, scanner a codice a barre, cassetto per contanti), vedi [Configurazione del terminale POS](pos-terminal-setup).

## Passaggio 4: Configura un fornitore di pagamento

Il fornitore di pagamento collega i tuoi lettori di carte a una rete di pagamento come Stripe Terminal o Square. Utilizza l'assistente di configurazione a 5 passaggi per inserire le tue credenziali.

1. Naviga verso **POS > Fornitori di pagamento** e fai clic su **Configura fornitore**.
2. L'assistente si apre a `/admin/pos/terminal-provider/wizard/step1/`.

![Wizard del fornitore di pagamento](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Seleziona il tuo fornitore (es. **Stripe Terminal**) e segui le istruzioni visualizzate attraverso tutti e cinque i passaggi: seleziona fornitore → istruzioni di configurazione → inserisci credenziali → testa la connessione → configura ubicazione.
4. Un badge verde **Connesso** conferma che l'integrazione è attiva.

Se hai bisogno solo di contanti e di inserimento manuale delle carte, seleziona **Manuale** come fornitore — non sono richieste credenziali.

Per ulteriori informazioni sui campi delle credenziali per ogni fornitore supportato, consulta [POS Payment Provider Setup](pos-payment-provider-setup).

## Passaggio 5: Accoppia un lettore di carte

Con un fornitore di pagamento connesso, puoi accoppiare un lettore di carte fisico a uno dei tuoi terminali utilizzando il wizard a 3 passaggi per il lettore.

1. Vai a **POS > Lettori di carte** e fai clic su **Aggiungi lettore**.
2. Il wizard inizia a `/admin/pos/reader/wizard/step1/`.
3. Seleziona il tuo fornitore, quindi scegli **Registra nuovo dispositivo** (inserisci il codice visualizzato sullo schermo del lettore) o **Scopri esistente** (Spwig recupera i lettori già registrati con il fornitore).
4. Nell'ultimo passaggio, assegna il lettore al terminale creato nel Passaggio 3.

Ogni terminale supporta un lettore di carte assegnato. Puoi riassegnare i lettori in qualsiasi momento dall'elenco Lettori di carte.

## Passaggio 6: Progetta il tuo ricevuta (opzionale per il primo giorno)

Spwig crea automaticamente un modello di ricevuta predefinito. Puoi iniziare a vendere immediatamente senza toccarlo — la ricevuta predefinita stampa il nome del tuo negozio, l'indirizzo, l'elenco delle vendite, il metodo di pagamento e un piè di pagina "Grazie per l'acquisto!".

Quando sei pronto a personalizzarlo, vai a **POS > Modelli di ricevuta**. Le opzioni includono il tuo logo, il numero di identificativo fiscale, la promozione tramite codice QR, la politica di reso e la larghezza della carta (58mm o 80mm per le stampanti termiche). Puoi creare modelli separati per ogni negozio o per ogni gruppo di negozi.

## Passaggio 7: Apri il tuo primo turno

I turni tracciano chi ha processato le vendite e quanto denaro contante dovrebbe essere presente nel cassetto. I cassieri aprono e chiudono i turni direttamente sul POS.

1. Sul dispositivo accoppiato, vai a `/pos/` e accedi con le tue credenziali dello staff.
2. Seleziona il terminale e la posizione del negozio.
3. Spwig ti chiede di **contare il fondo iniziale** — inserisci l'importo in contanti già presente nel cassetto (inserisci `0` se il cassetto è vuoto).
4. Tocca **Apri turno**. Il registratore di cassa è ora pronto per le vendite.

Per una spiegazione completa sui turni, sui movimenti in contanti e sui report di conciliazione, consulta [Managing POS Shifts](pos-shifts).

## Passaggio 8: Esegui la tua prima vendita

Una volta aperto il turno, vendere è semplice:

1. Cerca i prodotti per nome, scansiona un codice a barre o naviga per categorie per aggiungere articoli al carrello.
2. Applica uno sconto o un codice voucher se necessario.
3. Tocca **Carica** per iniziare il pagamento. Scegli il metodo di pagamento (contanti, carta tramite lettore o pagamento fratto).
4. Per i pagamenti con carta, il lettore chiede al cliente di toccare o inserire la carta.
5. La ricevuta viene stampata automaticamente (o viene visualizzata un'opzione per la ricevuta digitale). L'ordine viene salvato nella tua cronologia degli ordini in tempo reale.

## Passaggio 9: Chiudi il turno alla fine della giornata

Chiudere un turno blocca il registratore e genera un riepilogo di conciliazione.

1. Dal menu POS, tocca **Chiudi turno**.
2. Conta il denaro nel cassetto e inserisci l'importo totale quando richiesto.
3. Spwig calcola l'importo previsto in contanti in base al fondo iniziale, alle vendite in contanti e a eventuali movimenti in contanti durante il turno, e ti mostra la differenza.
4. Conferma per chiudere. Il rapporto del turno viene salvato e visualizzato in **POS > Turni** nel tuo amministratore.

Registra eventuali somme prelevate o aggiunte al cassetto durante la giornata come **movimenti in contanti** (tramite il menu del turno) invece di modificare il conteggio finale — questo mantiene la tua conciliazione precisa.

## Suggerimenti

- Completa i passaggi 1 a 5 prima del tuo primo giorno di commercio.

I passaggi 6 a 9 possono essere eseguiti il giorno stesso.
- Utilizza una password per lo staff forte ma memorabile — lo staff POS digita le credenziali al registratore, quindi password troppo complesse rallentano i dipendenti.
- Se il lettore di carte non appare online, fai clic su **Sincronizza lettori** sulla pagina Lettori di carte per recuperare lo stato più recente dal tuo fornitore.
- Testa l'intero flusso (apri turno → vendita → ricevuta → chiudi turno) con una transazione di test da $0.01 prima del periodo di attività intensa.
- Il POS funziona offline per le vendite in contanti di base.

I pagamenti con terminali di carta richiedono una connessione internet per l'autorizzazione.
- È possibile avere più terminali in una singola ubicazione del negozio — aggiungi un nuovo record del terminale nell'amministrazione e associa un dispositivo diverso.