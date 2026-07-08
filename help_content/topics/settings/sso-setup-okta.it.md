---
title: 'Configurazione SSO: Okta'
---

Questo documento ti guida attraverso il collegamento di Spwig a Okta per il singolo accesso (SSO) amministrativo. Una volta configurato, il tuo personale può accedere al pannello di amministrazione di Spwig utilizzando il loro account Okta.

**Nota:** Okta potrebbe aggiornare l'interfaccia del loro console di amministrazione nel tempo. Queste istruzioni sono state scritte in base al console di amministrazione Okta come era all'inizio del 2026. Se alcuni passaggi differiscono da quanto vedi, consulta la documentazione ufficiale di Okta su [creare un'integrazione di applicazione OIDC](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Prerequisiti

- Un'organizzazione Okta (qualsiasi livello — gli account gratuiti per sviluppatori funzionano per i test)
- Ruolo **Super Administrator** o **Application Administrator** in Okta
- Il tuo URL dello store Spwig (es. `https://your-store.com`)
- I membri dello staff devono avere indirizzi email in Spwig che corrispondano ai loro account Okta

## Passo 1: Creare un'applicazione

1. Accedi al [Okta Admin Console](https://your-org-admin.okta.com)
2. Naviga verso **Applications > Applications**
3. Clicca su **Create App Integration**
4. Seleziona:

| Campo | Valore |
|-------|-------|
| **Metodo di accesso** | OIDC - OpenID Connect |
| **Tipo di applicazione** | Web Application |

5. Clicca su **Next**

## Passo 2: Configurare l'applicazione

Compila le impostazioni dell'applicazione:

| Campo | Valore |
|-------|-------|
| **Nome dell'integrazione dell'app** | `Spwig Admin SSO` (o qualsiasi nome preferisci) |
| **Tipo di concessione** | Authorization Code (dovrebbe essere selezionato di default) |
| **URI di reindirizzamento per l'accesso** | `https://your-store.com/oidc/callback/` |
| **URI di reindirizzamento per l'uscita** | `https://your-store.com/en/admin/login/` |
| **Accesso controllato** | Scegli in base alle tue esigenze (vedi di seguito) |

Per **Accesso controllato**, scegli uno dei seguenti:

- **Consenti a tutti gli utenti dell'organizzazione di accedere** — tutti gli utenti Okta possono accedere (puoi comunque controllare l'accesso a Spwig con l'impostazione Restrict to Staff)
- **Limita l'accesso ai gruppi selezionati** — solo gli utenti in gruppi specifici di Okta possono accedere
- **Salta l'assegnazione ai gruppi per ora** — assegnerai gli utenti o i gruppi manualmente in un secondo momento

Clicca su **Save**.

**Importante:** L'URI di reindirizzamento per l'accesso deve corrispondere esattamente a `https://your-store.com/oidc/callback/` — incluso lo slash finale.

## Passo 3: Ottenere le credenziali del client

Dopo aver salvato, la scheda **General** dell'applicazione mostra le tue credenziali:

| Valore | Dove trovarlo |
|-------|-----------------|
| **Client ID** | Scheda General, sezione Client Credentials |
| **Client Secret** | Scheda General, sezione Client Credentials (clicca sull'icona occhio per visualizzarlo) |

Copia entrambi i valori — li userai per Spwig.

## Passo 4: Costruire l'URL di scoperta

L'URL di scoperta dipende dalla tua organizzazione Okta e dal server di autorizzazione:

**Server di autorizzazione predefinito (più comune):**

Fai clic su **Aggiungi richiesta**
5.

Configura la richiesta:

| Campo | Valore |
|-------|-------|
| **Nome** | `groups` |
| **Includi nel tipo di token** | ID Token, Always |
| **Tipo di valore** | Groups |
| **Filtro** | Corrisponde a regex: `.*` (per includere tutti i gruppi) |
| **Includi in** | Qualsiasi ambito (o `openid` se desideri limitarlo) |

6. Fai clic su **Crea**

**Suggerimento:** A differenza di Microsoft Entra ID che invia Object IDs, Okta invia per default **nomi di gruppo**. Questo rende la mappatura dei ruoli più intuitiva — puoi utilizzare i nomi visualizzati dei tuoi gruppi Okta direttamente nei campi Gruppi dello Staff e Gruppi Superuser di Spwig.

### Filtrare i gruppi

Se gli utenti appartengono a molti gruppi Okta e desideri includere solo alcuni specifici nel token:

- Modifica il filtro da `.*` a una regex più specifica, ad esempio `^Spwig.*` per includere solo i gruppi che iniziano con "Spwig"
- Oppure utilizza i filtri **Inizia con**, **Uguale a** o **Contiene** invece della regex

## Passaggio 7: Configurare in Spwig

1. Nel pannello di amministrazione di Spwig, vai a **Enterprise SSO > Configurazione del provider SSO**
2. Imposta **Nome del provider** su `Okta`
3. Inserisci l'URL di discovery ottenuto nel passaggio 4
4. Fai clic su **Auto-Discover** — questo popola automaticamente tutti i campi degli endpoint
5. Inserisci l'**ID client** ottenuto nel passaggio 3
6. Inserisci il **Client Secret** ottenuto nel passaggio 3
7. Se hai configurato le richieste di gruppo nel passaggio 6:
   - Imposta **Groups Claim** su `groups`
   - In **Staff Groups**, inserisci i nomi dei gruppi Okta i cui membri dovrebbero essere dello staff (separati da virgole)
   - In **Superuser Groups**, inserisci i nomi dei gruppi Okta i cui membri dovrebbero essere superutenti (separati da virgole)
8. Fai clic su **Salva**

## Passaggio 8: Abilita e testa

1. Vai a **Impostazioni del sito > scheda Sicurezza**
2. Seleziona **Abilita SSO per il login amministratore**
3. Fai clic su **Salva**
4. Apri la pagina di login amministratore in una **finestra privata/incognito**
5. Dovresti vedere un pulsante **Accedi con Okta**
6. Clicca su di esso — dovresti essere reindirizzato alla pagina di accesso di Okta
7. Accedi con un account Okta assegnato all'applicazione e la cui email corrisponde a un utente dello staff in Spwig
8. Dovresti essere reindirizzato nuovamente al pannello di amministrazione di Spwig

## Problemi comuni

| Problema | Causa | Soluzione |
|---------|-------|----------|
| **L'URI di reindirizzamento non è consentito** | L'URI di reindirizzamento non corrisponde alla configurazione dell'applicazione | Verifica che l'URI di reindirizzamento per l'accesso sia esattamente `https://your-store.com/oidc/callback/` con la barra finale |
| **L'utente non è assegnato all'applicazione client** | L'utente non è assegnato all'app Okta | Assegna l'utente o il loro gruppo all'applicazione nella scheda Assegnamenti |
| **L'accesso ha successo a Okta ma fallisce a Spwig** | Nessun utente corrispondente in Spwig | Assicurati che esista un account dello staff in Spwig con la stessa email. Controlla l'impostazione Restrict to Staff. |
| **La richiesta dei gruppi è vuota** | La richiesta dei gruppi non è configurata sul server di autorizzazione | Segui il passaggio 6 per aggiungere una richiesta dei gruppi. Assicurati di aggiungerla al server di autorizzazione corretto. |
| **Server di autorizzazione errato** | L'URL di discovery utilizza un diverso server di autorizzazione rispetto a dove è configurata la richiesta dei gruppi | Verifica che l'URL di discovery corrisponda al server di autorizzazione dove hai configurato la richiesta dei gruppi |
| **"L'ID client fornito non è valido"** | L'ID client non corrisponde o l'app è inattiva | Controlla che l'ID client sia corretto e che lo stato dell'applicazione sia Attivo in Okta |

## Suggerimenti

- **Okta invia i nomi dei gruppi, non gli ID** — questo rende la mappatura dei ruoli semplice.

Inserisci esattamente il nome visualizzato del gruppo (ad esempio, `Spwig Admins`) nei campi Gruppi dello Staff o Gruppi Superuser di Spwig.
- **Utilizza l'assegnamento dei gruppi per il controllo degli accessi** — assegna gruppi specifici di Okta all'applicazione Spwig invece di permettere a tutti gli utenti di accedere.

# Configurazione del SSO con Okta

In questo modo, solo il personale previsto può accedere.
- **I segreti del client Okta non scadono di default** — ma è possibile ruotarli in qualsiasi momento dalla scheda Generale dell'applicazione per seguire le migliori pratiche di sicurezza.
- **Testa con un account non amministratore** — utilizza un utente Okta normale (non un super amministratore) assegnato all'applicazione per verificare che il SSO funzioni come previsto.
- **MFA in Okta** — configura la politica globale di sessione di Okta o le politiche di autenticazione per richiedere l'MFA.

Questo si applicherà a tutti i login SSO su Spwig senza la necessità di configurare separatamente l'MFA in Spwig.