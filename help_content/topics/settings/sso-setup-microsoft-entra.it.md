---
title: 'Configurazione SSO: Microsoft Entra ID'
---

Questo documento ti guida attraverso il collegamento di Spwig a Microsoft Entra ID (precedentemente Azure Active Directory) per il singolo accesso (SSO) degli amministratori. Una volta configurato, il tuo personale può accedere al pannello di amministrazione di Spwig utilizzando il proprio account Microsoft per il lavoro.

**Nota:** Microsoft potrebbe aggiornare l'interfaccia del centro amministratore Entra nel tempo. Queste istruzioni sono state scritte in base all'interfaccia disponibile all'inizio del 2026. Se alcuni passaggi differiscono da quanto visualizzi, consulta la documentazione ufficiale di Microsoft su [registrazione di un'applicazione con la piattaforma di identità Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Requisiti preliminari

- Una sottoscrizione Azure con accesso a Microsoft Entra ID
- Ruolo **Application Administrator** o **Global Administrator** nel tuo tenant Entra ID
- Il URL della tua store Spwig (es. `https://your-store.com`)
- I membri dello staff devono avere indirizzi email in Spwig che corrispondano ai loro account Microsoft

## Passaggio 1: Registra un'applicazione

1. Accedi al [Microsoft Entra admin center](https://entra.microsoft.com)
2. Naviga verso **Identity > Applications > App registrations**
3. Clicca su **New registration**
4. Configura la registrazione:

| Campo | Valore |
|-------|-------|
| **Nome** | `Spwig Admin SSO` (o qualsiasi nome tu preferisca) |
| **Tipi di account supportati** | **Accounts in this organizational directory only** (Single tenant) |
| **Redirect URI** | Piattaforma: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Clicca su **Register**

**Importante:** L'URI di reindirizzamento deve corrispondere esattamente a `https://your-store.com/oidc/callback/` — incluso lo slash finale. Sostituisci `your-store.com` con il dominio effettivo del tuo store.

## Passaggio 2: Nota gli ID dell'applicazione

Dopo la registrazione, vedrai la pagina **Overview** dell'applicazione. Nota questi due valori — li userai più tardi:

| Valore | Dove trovarlo | A cosa serve |
|-------|-----------------|---------------|
| **Application (client) ID** | Pagina Overview, sezione superiore | Inserisci come **Client ID** in Spwig |
| **Directory (tenant) ID** | Pagina Overview, sezione superiore | Utilizzato per costruire l'URL di Discovery |

## Passaggio 3: Crea un segreto client

1. Nella registrazione dell'app, naviga verso **Certificates & secrets**
2. Clicca su **New client secret**
3. Inserisci una descrizione (es. `Spwig SSO`) e scegli un periodo di scadenza
4. Clicca su **Add**
5. **Copia immediatamente il Valore** — viene visualizzato solo una volta. Questo è il segreto client che inserirai in Spwig.

**Non copiare l'ID del segreto** — hai bisogno della colonna **Valore**, non della colonna ID.

**Imposta un promemoria** per ruotare il segreto prima che scada. Quando un segreto scade, l'SSO smetterà di funzionare fino a quando non ne creerai uno nuovo e lo aggiornerai in Spwig.

## Passaggio 4: Configura le autorizzazioni API

1. Naviga verso **API permissions**
2. Verifica che **Microsoft Graph > User.Read** (delegated) sia elencato. Questo viene aggiunto di default.
3. Se le autorizzazioni `openid`, `email` e `profile` non sono elencate, clicca su **Add a permission > Microsoft Graph > Delegated permissions** e aggiungile.
4. Clicca su **Grant admin consent for [your organization]** se richiesto.

## Passaggio 5: Costruisci l'URL di Discovery

L'URL di Discovery OIDC segue questo formato:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Sostituisci `{tenant-id}` con l'**ID Directory (tenant)** ottenuto nel passaggio 2.

Esempio: se il tuo ID tenant è `a1b2c3d4-e5f6-7890-abcd-ef1234567890`, l'URL di Discovery è:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Passaggio 6: Configura le richieste di gruppo (opzionale)

Se desideri che Spwig assegni automaticamente lo stato di staff o superuser in base all'appartenenza a gruppi Entra ID:

1. Nella registrazione dell'app, naviga verso **Token configuration**
2. Clicca su **Add groups claim**
3. Seleziona i tipi di gruppo da includere (di solito **Security groups**)
4. Nella sezione **Customize token properties by type**, per il token **ID**, seleziona **Group ID**
5. Clicca su **Add**

**Importante:** Entra ID invia **Object IDs** (UUID come `a1b2c3d4-...`), non i nomi visuali dei gruppi.

Quando si configura la mappatura dei ruoli in Spwig, è necessario utilizzare questi Object IDs.

Per trovare l'Object ID di un gruppo:
1. Nel centro amministrativo Entra, vai a **Identity > Groups > All groups**
2. Fai clic sul gruppo
3. Copia l'**Object ID** dalla pagina di panoramica del gruppo

### Limite dei gruppi

Microsoft Entra ID include un massimo di **200 gruppi** nel token. Se un utente appartiene a più di 200 gruppi, l'asserzione dei gruppi viene sostituita con un collegamento all'API Microsoft Graph. Per le organizzazioni con molti gruppi, considera la creazione di un gruppo di sicurezza dedicato per l'accesso a Spwig e l'utilizzo della [filtratura dei gruppi](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) per limitare i gruppi inclusi.

## Passaggio 7: Configura in Spwig

1. Nel pannello di amministrazione di Spwig, vai a **Enterprise SSO > SSO Provider Configuration**
2. Imposta **Provider Name** su `Microsoft Entra ID`
3. Incolla l'URL di scoperta da Step 5 in **OIDC Discovery URL**
4. Fai clic su **Auto-Discover** — questo popola automaticamente tutti i campi degli endpoint
5. Inserisci l'**Client ID** da Step 2
6. Inserisci il **Client Secret** (il Valore) da Step 3
7. Se hai configurato le asserzioni dei gruppi in Step 6:
   - Imposta **Groups Claim** su `groups`
   - In **Staff Groups**, inserisci gli Object ID dei gruppi i cui membri dovrebbero essere dello staff (separati da virgole)
   - In **Superuser Groups**, inserisci gli Object ID dei gruppi i cui membri dovrebbero essere superutenti (separati da virgole)
8. Fai clic su **Save**

## Passaggio 8: Abilita e testa

1. Vai a **Site Settings > Security**
2. Seleziona **Enable SSO for admin login**
3. Fai clic su **Save**
4. Apri la pagina di accesso amministrativo in una **finestra privata/incognito**
5. Dovresti vedere un pulsante **Sign in with Microsoft Entra ID**
6. Fai clic su di esso — dovresti essere reindirizzato alla pagina di accesso di Microsoft
7. Accedi con un account Microsoft il cui indirizzo email corrisponde a un utente dello staff in Spwig
8. Dovresti essere reindirizzato nuovamente al pannello di amministrazione di Spwig

## Problemi comuni

| Problema | Causa | Soluzione |
|---------|-------|----------|
| **AADSTS50011: L'URI di reindirizzamento non corrisponde** | L'URI di reindirizzamento in Entra non corrisponde esattamente | Verifica che l'URI di reindirizzamento sia `https://your-store.com/oidc/callback/` con la barra finale. Controlla la corrispondenza tra HTTP e HTTPS. |
| **AADSTS700016: Applicazione non trovata** | Client ID errato o tenant | Verifica nuovamente il Client ID e che l'URL di scoperta utilizzi l'ID tenant corretto |
| **L'accesso ha successo su Microsoft ma fallisce su Spwig** | Nessun utente corrispondente in Spwig | Assicurati che esista un account dello staff in Spwig con lo stesso indirizzo email dell'account Microsoft. Controlla che l'utente abbia lo status dello staff se è abilitata l'opzione Restrict to Staff. |
| **L'asserzione dei gruppi è vuota** | Le asserzioni dei gruppi non sono configurate | Segui Step 6 per aggiungere un'asserzione dei gruppi alla configurazione del token |
| **L'asserzione dei gruppi restituisce un URL invece che ID** | L'utente appartiene a più di 200 gruppi | Utilizza la filtratura dei gruppi per limitare i gruppi nel token, o assegna gruppi specifici |
| **SSO smette di funzionare dopo alcuni mesi** | Il segreto client è scaduto | Crea un nuovo segreto client in Entra e aggiornalo nella configurazione del provider SSO di Spwig |

## Consigli

- **Utilizza i gruppi di sicurezza** per la mappatura dei ruoli, non i gruppi Microsoft 365 o le liste di distribuzione.

I gruppi di sicurezza sono progettati per il controllo degli accessi e funzionano in modo più affidabile con le asserzioni OIDC.
- **È consigliabile utilizzare un singolo tenant** — selezionando "Accounts in this organizational directory only" si limita l'SSO agli utenti dell'organizzazione.

Le configurazioni multi-tenant richiedono una validazione aggiuntiva.
- **Imposta una scadenza lunga del segreto** — quando si crea il segreto client, scegli 24 mesi e crea un promemoria nel calendario a 22 mesi per aggiornarlo.
- **Accesso condizionale** — puoi creare politiche di accesso condizionale in Entra ID che si applicano specificamente all'iscrizione dell'app Spwig.


Per esempio, richiedi l'MFA, blocca l'accesso da ubicazioni non attendibili o richiedi dispositivi conformi.
- **Testa con un account non amministratore** — crea un account staff di test in Spwig per verificare che l'SSO funzioni prima di attivarlo per l'intero team.