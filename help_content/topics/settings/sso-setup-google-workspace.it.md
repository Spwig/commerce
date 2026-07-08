---
title: 'SSO Setup: Google Workspace'
---

Configurazione SSO: Google Workspace

Questo documento ti guida attraverso il collegamento di Spwig a Google Workspace per il singolo accesso (SSO) degli amministratori. Una volta configurato, il tuo personale può accedere al pannello di amministrazione di Spwig utilizzando il proprio account Google Workspace.

**Nota:** Google potrebbe aggiornare l'interfaccia del Cloud Console nel tempo. Queste istruzioni sono state scritte in base all'interfaccia disponibile all'inizio del 2026. Se alcuni passaggi differiscono da quanto visualizzi, consulta la documentazione ufficiale di Google su [configurazione OAuth 2.0](https://support.google.com/cloud/answer/6158849).

## Prerequisiti

- Una sottoscrizione Google Workspace (Google Workspace Business, Enterprise o Education)
- Accesso amministrativo al [Google Cloud Console](https://console.cloud.google.com)
- L'URL del tuo negozio Spwig (es. `https://your-store.com`)
- I membri dello staff devono avere indirizzi email in Spwig che corrispondano ai loro account Google Workspace

## Passaggio 1: Crea o seleziona un progetto Google Cloud

1. Vai al [Google Cloud Console](https://console.cloud.google.com)
2. Fai clic sul selettore dei progetti nella barra superiore
3. Fai clic su **Nuovo progetto** (o seleziona un progetto esistente se preferisci)
4. Inserisci un nome per il progetto (es. `Spwig SSO`)
5. Seleziona la tua organizzazione
6. Fai clic su **Crea**

## Passaggio 2: Configura lo schermo di consenso OAuth

1. Nel Cloud Console, vai a **APIs & Services > OAuth consent screen**
2. Seleziona **Internal** come tipo utente — questo limita l'accesso agli utenti all'interno della tua organizzazione Google Workspace
3. Fai clic su **Crea**
4. Compila i campi richiesti:

| Campo | Valore |
|-------|-------|
| **Nome dell'app** | `Spwig Admin` (o il nome del tuo negozio) |
| **Email del supporto utente** | Il tuo indirizzo email amministrativo |
| **Domini autorizzati** | `your-store.com` (il dominio del tuo negozio, senza `https://`) |
| **Email del contatto sviluppatore** | Il tuo indirizzo email amministrativo |

5. Fai clic su **Salva e continua**
6. Nella pagina **Scopes**, fai clic su **Aggiungi o rimuovi scopes** e aggiungi:
   - `openid`
   - `email`
   - `profile`
7. Fai clic su **Salva e continua**
8. Rivedi il riepilogo e fai clic su **Back to Dashboard**

## Passaggio 3: Crea le credenziali OAuth

1. Vai a **APIs & Services > Credentials**
2. Fai clic su **Crea credenziali > OAuth client ID**
3. Configura il client:

| Campo | Valore |
|-------|-------|
| **Tipo di applicazione** | Web application |
| **Nome** | `Spwig SSO` |
| **URL di reindirizzamento autorizzati** | `https://your-store.com/oidc/callback/` |

4. Fai clic su **Crea**
5. Una finestra di dialogo mostra il tuo **Client ID** e **Client Secret** — copia entrambi i valori. Puoi anche scaricarli come JSON per un archiviazione sicura.

**Importante:** L'URL di reindirizzamento deve corrispondere esattamente a `https://your-store.com/oidc/callback/` — incluso lo slash finale e lo schema `https://`. Sostituisci `your-store.com` con il dominio effettivo del tuo negozio.

## Passaggio 4: Ottenere l'URL di Discovery

Google utilizza un singolo URL di Discovery standard per tutti i tenant Workspace:

```
https://accounts.google.com/.well-known/openid-configuration
```

Questo URL è lo stesso per ogni organizzazione Google Workspace — non è necessario personalizzarlo con un tenant o un dominio.

## Passaggio 5: Configurare in Spwig

1. Nel pannello di amministrazione di Spwig, vai a **Enterprise SSO > SSO Provider Configuration**
2. Imposta **Provider Name** su `Google Workspace`
3. Inserisci l'URL di Discovery: `https://accounts.google.com/.well-known/openid-configuration`
4. Fai clic su **Auto-Discover** — questo popola automaticamente tutti i campi degli endpoint
5. Inserisci il **Client ID** ottenuto nel passaggio 3
6. Inserisci il **Client Secret** ottenuto nel passaggio 3
7. Fai clic su **Salva**

### Mappatura delle richieste

Google utilizza i nomi standard delle richieste OIDC, quindi la configurazione predefinita di Spwig funziona immediatamente:

| Impostazione Spwig | Richiesta Google | Valore predefinito |
|---------------|-------------|---------------|
| Richiesta Email | `email` | `email` |
| Richiesta Nome | `given_name` | `given_name` |
| Richiesta Cognome | `family_name` | `family_name` |

Non sono necessari cambiamenti alla mappatura delle richieste.

## Passaggio 6: Abilita e testa

1.

Naviga su **Site Settings > Security** tab
2.

Seleziona **Enable SSO for admin login**
3.

Fai clic su **Save**
4.

Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Apri la pagina di accesso amministratore in una **finestra privata/incognito**
5.

Dovresti vedere un pulsante **Accedi con Google Workspace**
6.

Cliccalo — dovresti essere reindirizzato alla pagina di accesso di Google
7.

Accedi con un account Google Workspace il cui indirizzo email corrisponde a un utente dello staff in Spwig
8.

Dovresti essere reindirizzato nuovamente al dashboard amministratore di Spwig

## Mappatura dei Ruoli basata sui Gruppi

A differenza di Microsoft Entra ID o Okta, Google non include l'appartenenza ai gruppi nei token OIDC standard di default. L'implementazione delle dichiarazioni dei gruppi con Google richiede l'API Directory Google Workspace e una configurazione aggiuntiva al di là del OIDC di base.

Per la maggior parte delle implementazioni Google Workspace, raccomandiamo di gestire lo stato di staff e superuser direttamente in Spwig invece di utilizzare una mappatura automatica dei ruoli:

1. Crea account staff in Spwig con i permessi appropriati
2. Utilizza il sistema Ruoli Staff di Spwig per controllare i livelli di accesso
3. Lo staff si accede tramite SSO, e Spwig utilizza i loro permessi esistenti

Se hai bisogno di una mappatura automatica dei ruoli basata sui gruppi, consulta la [documentazione dell'API Directory Admin SDK di Google Workspace](https://developers.google.com/admin-sdk/directory) per configurare dichiarazioni personalizzate.

## Problemi Comuni

| Problema | Causa | Soluzione |
|---------|-------|----------|
| **Errore 400: redirect_uri_mismatch** | L'URI di reindirizzamento in Google Cloud non corrisponde esattamente | Verifica che l'URI di reindirizzamento sia `https://your-store.com/oidc/callback/` con la barra finale. Controlla HTTP vs HTTPS. |
| **Errore 403: access_denied** | L'utente non appartiene all'organizzazione Google Workspace | Con il tipo utente "Internal", solo gli utenti della tua organizzazione possono accedere. Verifica che l'account utente faccia parte del tuo dominio Workspace. |
| **La schermata di consenso OAuth mostra "Questo app non è verificato"** | Normale per gli app Interni | Questo avviso è previsto per gli app Interni e non influisce sulla funzionalità. Gli utenti della tua organizzazione possono comunque accedere. |
| **L'accesso ha successo su Google ma fallisce su Spwig** | Nessun utente corrispondente in Spwig | Assicurati che esista un account staff in Spwig con la stessa email dell'account Google Workspace. Verifica che "Ristretto a Staff" sia configurato correttamente. |
| **"Accesso bloccato: questa richiesta dell'app è invalida"** | Scopes non configurati correttamente | Verifica che gli scopes `openid`, `email` e `profile` siano aggiunti alla schermata di consenso OAuth. |

## Consigli

- **Utilizza il tipo utente "Internal"** — questo limita l'accesso all'organizzazione Google Workspace e non richiede il processo di verifica delle app di Google.
- **I segreti client Google non scadono** — a differenza di Microsoft Entra ID, i segreti client OAuth di Google non hanno una data di scadenza. Tuttavia, puoi ruotarli in qualsiasi momento dalla pagina Credenziali.
- **Un progetto per più app** — puoi creare più ID client OAuth all'interno dello stesso progetto Google Cloud se hai più installazioni di Spwig.
- **Testa con un account non amministratore** — crea un account staff di test in Spwig e utilizza un utente normale di Google Workspace (non un amministratore) per verificare che SSO funzioni come previsto.