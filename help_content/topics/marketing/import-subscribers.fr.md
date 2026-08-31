---
title: Importer des abonnés depuis un fichier CSV
---

Si vous disposez déjà d'une liste de diffusion ailleurs — un ancien outil d'e-mailing, un tableur d'inscriptions à la newsletter, une pile de scans de badges de salon — vous n'avez pas besoin d'ajouter ces contacts à Spwig un par un. L'importation d'abonnés de Campaign Studio lit un fichier CSV ou Excel et ajoute tous les contacts valides à votre audience en une seule fois, prêts à être étiquetés, segmentés et contactés par e-mail.

## Avant l'importation : consentement

Chaque importation vous oblige à cocher une case confirmant : **« Ces contacts ont accepté de recevoir des e-mails marketing de ma part. »** Ce n'est pas une formalité — n'importez que des contacts qui ont réellement souscrit à vos e-mails marketing. Cela compte pour deux raisons :

- **C'est une obligation légale dans la plupart des pays.** Envoyer des e-mails marketing à des personnes qui n'ont jamais accepté de les recevoir viole les lois sur le consentement dans de nombreuses juridictions.
- **Cela protège votre délivrabilité.** Envoyer des e-mails à des personnes qui n'ont jamais souscrit génère des signalements de spam et des rebonds, ce que les fournisseurs de messagerie utilisent pour décider si *aucun* de vos e-mails — y compris ceux envoyés à des personnes qui ont souscrit — atteint la boîte de réception.

Si une liste ne provient clairement pas d'inscriptions consenties, ne l'importez pas.

## Préparer votre fichier

L'importateur accepte un fichier `.csv` ou `.xlsx` avec une ligne d'en-tête. Une seule colonne est obligatoire :

| Colonne | Obligatoire ? | Remarques |
|--------|-----------|-------|
| **E-mail** | Oui | Doit être une adresse e-mail valide. |
| **Prénom** | Non | Utilisé pour personnaliser les e-mails. |
| **Nom** | Non | Utilisé pour personnaliser les e-mails. |
| **Langue** | Non | Le code de langue préféré de l'abonné (par ex. `en`, `es`). |

Les colonnes sont associées automatiquement à ces champs par le nom de l'en-tête, vous n'avez donc pas besoin de renommer quoi que ce soit d'abord — les variations courantes comme `E-mail`, `Email Address`, `First Name`, `Given Name`, `Surname` ou `Locale` sont toutes reconnues.

Chaque importation est limitée à **5 Mo** et **5 000 lignes**. Si votre liste est plus grande, divisez-la en fichiers plus petits et importez-les les uns après les autres.

## Importer vos contacts

1. Ouvrez **Campaign Studio > Abonnés** et cliquez sur **Importer CSV**.
2. Choisissez votre fichier `.csv` ou `.xlsx`.
3. Choisissez ce qui se passe **pour les contacts déjà présents dans votre liste** — voir [Gestion des doublons](#handling-duplicates) ci-dessous.
4. Choisissez éventuellement une étiquette sous **Étiqueter les contacts importés comme** pour étiqueter tout le monde dans cette importation (par ex. `Événement 2026`) — voir [Étiquettes d'abonnés](/help/subscriber-tags) pour en savoir plus sur les étiquettes.
5. Cochez **Ces contacts ont accepté de recevoir des e-mails marketing de ma part**.
6. Cliquez sur **Continuer**.

![Le formulaire d'importation avec un fichier choisi, une étiquette sélectionnée et le consentement confirmé](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig vous montre ensuite un aperçu avant que quoi que ce soit soit réellement importé :

![L'aperçu de l'importation montrant les compteurs de nouveaux, existants et ignorés-invalides avec les raisons](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **Nouveaux contacts** — lignes qui créeront un nouvel abonné.
- **Déjà dans votre liste** — lignes dont l'adresse e-mail correspond à un abonné existant.
- **Ignorées (invalides)** — lignes qui n'ont pas pu être lues, chacune listée avec son numéro de ligne et la raison (un format d'e-mail invalide, une cellule e-mail vide, ou un doublon d'une ligne précédente du même fichier).

Vérifiez ces chiffres, puis cliquez sur **Importer maintenant** pour valider l'importation, ou **Annuler** pour revenir en arrière sans rien changer.

## Gestion des doublons

Une ligne est considérée comme un doublon si son adresse e-mail correspond à un abonné que vous avez déjà. Vous choisissez comment Spwig traite ces lignes sur le formulaire d'importation :

| Option | Ce qui se passe |
|--------|--------------|
| **Les laisser inchangés** *(par défaut)* | Le nom et la langue de l'abonné existant sont conservés tels quels. |
| **Mettre à jour leur nom / langue** | Le prénom, le nom et la langue de l'abonné existant sont mis à jour à partir du fichier (uniquement pour les champs que le fichier fournit réellement). |

L'étiquette que vous choisissez pour l'importation est appliquée à **tous les contacts du fichier** — nouveaux et existants — quelle que soit l'option de doublon choisie.

L'importation de votre « liste VIP » avec l'étiquette **VIP** étiquette également les personnes que vous avez déjà.

L'option de doublon ne contrôle que si le *nom et la langue* d'un contact existant sont remplacés.

## Après l'importation

Chaque contact créé par une importation est enregistré avec la source **Importation** et marqué comme ayant consenti au moment où vous avez effectué l'importation (et non à une date antérieure où ils auraient pu s'inscrire ailleurs). Leur prénom et nom — si le fichier les a fournis — sont stockés dans leur enregistrement d'abonné, ce qui signifie que les champs de fusion `[[first_name]]` et `[[last_name]]` dans vos campagnes sont désormais correctement personnalisés pour eux aussi, même s'ils n'ont jamais créé de compte Spwig.

## Conseils

- Exportez votre liste source vers un CSV ou un `.xlsx` à feuille unique avec une ligne d'en-tête propre avant de téléverser — les feuilles supplémentaires, les cellules fusionnées ou les lignes de résumé peuvent perturber l'association des colonnes.
- Utilisez **Étiqueter les contacts importés comme** pour créer immédiatement l'audience exacte que vous voudrez cibler par la suite — voir [Étiquettes d'abonnés](/help/subscriber-tags) pour construire un segment à partir de celle-ci.
- Lisez toujours les raisons des **Ignorés (invalides)** avant de supposer qu'une importation a échoué — quelques lignes ignorées avec des raisons claires sont normales pour la plupart des listes réelles.
- Réexécuter le même fichier est sans risque : les contacts que vous avez déjà importés sont traités comme des doublons la deuxième fois, et non recréés.
- Si vous consolidez plusieurs petites listes, étiquetez chaque importation différemment (par exemple `Importation : Événement de janvier`, `Importation : Salon professionnel`) afin de pouvoir les distinguer plus tard, même après qu'elles ont toutes été mélangées à votre audience principale.
- Pour les listes de plus de 5 000 lignes, divisez par une limite évidente (alphabétique, par source ou par date de collecte) plutôt que par une coupure arbitraire, afin que chaque lot reste facile à identifier par la suite.