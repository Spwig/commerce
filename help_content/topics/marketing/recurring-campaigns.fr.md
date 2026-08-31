---
title: Campagnes récurrentes
---

Les **Campagnes récurrentes** de Campaign Studio vous permettent de configurer une newsletter une seule fois — un résumé hebdomadaire de produits, un digest mensuel de blog — et de laisser Spwig l'envoyer automatiquement selon un calendrier récurrent, au lieu de créer et d'envoyer manuellement une nouvelle campagne à chaque fois.

## Différence entre diffusion et récurrent

Chaque campagne dans Campaign Studio possède un **Type de campagne** :

| Type | Comportement |
|------|-----------|
| **Diffusion** | Envoyée une seule fois — immédiatement ou à une date et une heure planifiées uniques. Utilisez ce type pour une annonce ponctuelle, une vente ou un e-mail de lancement de produit. |
| **Récurrent** | Agit comme un modèle qui s'envoie selon un calendrier récurrent. Chaque envoi est une copie fraîche et datée appelée une **occurrence** — le modèle lui-même ne s'envoie jamais directement. |

Pour transformer une campagne en campagne récurrente, ouvrez-la dans **Campaign Studio > Campagnes** et définissez le **Type de campagne** sur **Récurrent**, puis enregistrez. Une section **Planification** apparaît sur la campagne une fois que vous la rouvrez — elle n'apparaît que pour les campagnes récurrentes.

![Type de campagne défini sur Récurrent](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Définir un calendrier

Une fois qu'une campagne est récurrente, sa section **Planification** contrôle quand elle est déclenchée :

| Champ | Description |
|-------|-------------|
| **Actif** | Active ou désactive la récurrence sans supprimer le calendrier. |
| **Fréquence** | **Quotidienne**, **Hebdomadaire** ou **Mensuelle**. |
| **Intervalle** | Envoi tous les N unités de fréquence — par exemple, un intervalle de `2` avec une fréquence **Hebdomadaire** signifie toutes les 2 semaines. |
| **Jour de la semaine** | Le jour d'envoi pour une fréquence hebdomadaire (`0` = lundi … `6` = dimanche). |
| **Jour du mois** | Le jour d'envoi pour une fréquence mensuelle (`1`–`28`, afin que chaque mois ait ce jour). |
| **Heure d'envoi** | L'heure de la journée à laquelle la campagne est envoyée. |
| **Fuseau horaire** | Un nom de fuseau horaire IANA, par exemple `Europe/London` ou `America/New_York` — l'heure d'envoi est interprétée dans cette zone, et non celle du serveur. |

![Section de planification hebdomadaire sur une campagne récurrente](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

Dès que vous enregistrez un calendrier actif, il **s'arme** — Spwig calcule le prochain moment de déclenchement et l'affiche dans **Prochaine exécution à**. Vous n'avez pas besoin de déclencher quoi que ce soit manuellement ; une tâche en arrière-plan vérifie les calendriers échus et envoie l'occurrence lorsque l'heure arrive. **Dernière exécution à** et **Occurrences envoyées** se mettent à jour automatiquement après chaque envoi afin que vous puissiez voir que le calendrier est actif.

## La politique de contenu non nouveau

Les newsletters récurrentes présentent souvent du contenu dynamique — le plus couramment un bloc **Articles de blog** (ou une **Grille de produits**) défini sur **Nouveau depuis le dernier envoi** dans le constructeur visuel, qui ne récupère que les articles publiés — ou les produits ajoutés — depuis le dernier envoi de la campagne. Cela soulève une question évidente : que se passe-t-il si une exécution planifiée arrive et qu'il n'y a rien de nouveau à mettre en avant ?

Spwig répond à cela avec la **Politique de contenu non nouveau** du calendrier :

| Politique | Ce qui se passe | Idéal pour |
|--------|---------------|----------|
| **Ignorer cet envoi** *(par défaut)* | L'occurrence est entièrement ignorée — rien n'est envoyé. L'emploi du temps passe directement à sa prochaine exécution planifiée. | Un résumé de blog ou de produits, afin que les abonnés ne reçoivent jamais un e-mail qui ne fait que répéter ce qu'ils ont déjà vu. |
| **Envoyer quand même (omettre les blocs vides)** | L'e-mail est envoyé selon l'horaire prévu, quel que soit le cas. Tout bloc qui n'a rien de nouveau — comme un bloc « Nouveaux articles de blog depuis le dernier envoi » vide — ne rend simplement rien à cet endroit. | Des lettres d'information qui ont toujours d'autres contenus à envoyer (un message de bienvenue, des sections intemporelles ou plusieurs blocs dynamiques), même si un bloc se trouve vide. |
| **Mettre en attente et envoyer en retard** | L'envoi est reporté. Spwig vérifie à nouveau chaque jour s'il y a du contenu frais, jusqu'à la **Fenêtre d'attente (jours)**. Si du nouveau contenu apparaît dans cette fenêtre, l'occurrence est envoyée en retard ; si la fenêtre expire sans rien de nouveau, cette occurrence est abandonnée et l'emploi du temps passe à son prochain créneau. | Une cadence que vous souhaitez protéger (par exemple, envoyer toujours *quelque chose* à la fin) sans déclencher un numéro vide dès qu'il n'y a rien de nouveau à publier cette semaine. |

Seules les campagnes utilisant du contenu conscient des deltas — un bloc Articles de blog ou une grille de produits réglée sur **Nouveaux depuis le dernier envoi** — déclenchent cette vérification. Une campagne récurrente sans de tels blocs est toujours considérée comme ayant du contenu frais et est envoyée normalement selon l'horaire prévu.

La **Fenêtre d'attente (jours)** ne s'applique qu'à la politique **Mettre en attente et envoyer en retard** — elle définit le nombre de jours pendant lesquels Spwig continuera à réessayer avant d'abandonner cette occurrence.

## Test A/B de chaque occurrence

Une lettre d'information récurrente est un endroit naturel pour tester en A/B vos **objets** — vous envoyez à une cadence régulière à la même audience, vous pouvez donc continuer à apprendre quels mots génèrent plus d'ouvertures. Spwig peut exécuter un test A/B d'objet frais sur **chaque occurrence** automatiquement.

Configurez-le dans la section **Emploi du temps** :

1. Dans **Objets A/B**, saisissez **deux à quatre** objets, un par ligne. Laissez vide pour envoyer les occurrences normalement avec l'objet du modèle.
2. Réglez le **% d'échantillon du test A/B** — la part de l'audience de chaque occurrence utilisée pour le test, répartie également entre les objets. Le reste est le groupe témoin qui reçoit le gagnant.
3. Choisissez la **Métrique du gagnant A/B** (taux d'ouverture ou de clic), la **Fenêtre de test A/B (heures)** pour recueillir les résultats avant de décider, et s'il faut **envoyer automatiquement le gagnant** au groupe témoin.

Désormais, chaque fois que l'emploi du temps se déclenche, cette occurrence divise son audience, envoie chaque objet à une tranche, attend la fin de la fenêtre de test, puis choisit l'objet gagnant et l'envoie à tout le monde — sans aucune action supplémentaire de votre part. Chaque occurrence est un test autonome, vous obtenez donc une lecture fraîche à chaque envoi et pouvez observer quels objets gagnent au fil des semaines. Le résultat de chaque occurrence s'affiche sous **Historique des occurrences** ci-dessous, avec un lien direct vers sa page de résultats avec les taux par variante, le gagnant et le niveau de confiance de Spwig (voir [Test A/B](ab-testing) pour savoir comment lire ces résultats).

Deux choses à savoir :

- **Le test A/B ici est limité aux objets.** Pour comparer des designs entièrement différents, utilisez un test A/B de diffusion ponctuel — l'assistant complet, qui prend en charge les variantes de contenu, est destiné aux campagnes de diffusion.
- Si l'audience d'une occurrence est **trop petite pour être divisée** entre les variantes, Spwig envoie discrètement cette occurrence comme une lettre d'information normale — une semaine chargée ne signifie jamais un envoi manqué.

## Historique des occurrences

Chaque fois qu'une campagne récurrente est réellement envoyée, Spwig crée une **occurrence** datée — un enregistrement de campagne réel et indépendant avec son propre objet, ses destinataires et ses statistiques d'envoi (envoyés, échoués, ignorés, ouvertures, clics). L'occurrence est nommée d'après le modèle avec la date d'envoi ajoutée, par exemple « Résumé hebdomadaire du blog — 2026-08-19 ».

La page d'édition de la campagne récurrente répertorie son **Historique des occurrences** — les occurrences les plus récentes, chacune menant à l'enregistrement de campagne de cette occurrence afin que vous puissiez examiner exactement ce qui a été envoyé et comment il a performé.

![Liste de l'historique des occurrences d'une campagne récurrente](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## Conseils

- Associez une campagne récurrente à un bloc **Articles de blog** réglé sur **Nouveaux depuis la dernière envoi** pour un digest « nouveaux articles cette semaine » auto-entretenu — vous écrivez les articles, Spwig gère l'envoi par e-mail.
- Commencez par **Ignorer cet envoi** pour les digests de contenu. C'est le paramètre par défaut le plus sûr : les abonnés ne reçoivent jamais une répétition du contenu de la dernière fois.
- Passez à **Envoyer quand même** uniquement si votre modèle contient d'autres éléments de contenu qui méritent d'être envoyés à eux seuls, même lorsque le bloc dynamique est vide.
- Utilisez **Mettre en attente et envoyer en retard** lorsque manquer occasionnellement un rythme est acceptable, mais que le manquer pendant des semaines consécutives ne l'est pas — réglez la fenêtre de mise en attente en fonction de la durée d'interruption que vous acceptez.
- Vérifiez **Prochaine exécution à** après avoir enregistré un planning pour confirmer qu'il a bien été fixé au jour et à l'heure attendus, en particulier lorsque vous travaillez dans plusieurs fuseaux horaires.
- Examinez régulièrement l'**Historique des occurrences** — un modèle qui continue à sauter est un signe que votre source de contenu dynamique (par exemple, le blog) est restée inactive.