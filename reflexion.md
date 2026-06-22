# Note de réflexion — Stratégie d'anonymisation (perso)

> Template à remplir en phase async individuelle (jeudi/vendredi matin).
> **Max 1 page.** Personnel — chaque apprenant rédige la sienne.
> Public : Marianne (évaluation) + futur toi qui relit ce repo.

---
## Typologie des données
En analysant les données avec regex et spaCY NER, on s'aperçoit qu'il y a plusieurs types à anonymiser, et que selon la langue configurée, ils ne sont pas détectés de la meme façon.


## Ma stratégie d'anonymisation

Stratégie choisie par type de données :

|Type|Stratégie anonymisation|Justification|
|--- |--- |---|
|PERSON|Substitution sans mapping|Pour une meilleure lisibilité et RGPD compliant|
|EMAIL	|Suppression|RGPD compliant, ne perd pas de sens|
|IBAN	|Suppression|RGPD compliant, ne perd pas de sens|
|PHONE	|Suppression|	RGPD compliant, ne perd pas de sens|
|ORG	|Aucune|Données peu sensible|
|GPE |Aucune|Données peu sensible|
|LOC |Aucune|Données peu sensible|

# Ce que j'ai gardé lisible et pourquoi

> Quelles informations laisse-t-on dans le texte (et pourquoi c'est OK) ?

- ORG : Organisation, non anonymisée car ce ne sont pas des PII, surtout si elles sont isolées, c'est à dire sans donnée proxy (les info PII ont été anonymisées par suppression).
- GPE / LOC : Localisation, non anonymisée car ce ne sont pas des PII, surtout si elles sont isolées, c'est à dire sans donnée proxy  (les info PII ont été anonymisées par suppression).

## Ce que j'ai masqué et pourquoi

> Quelles informations ai-je remplacées et avec quelle logique ?

- Choix 1 : PERSON : Personnes, donnée très sensible de type PII. Elles nécessitent une anonymisation forte, c'est pourquoi elles ont été anonymisées par subsitution sans mapping avec Faker.
- Choix 2 : EMAIL, PHONE, IBAN : donnée très sensible de type PII. Elles nécessitent une anonymisation forte, c'est pourquoi elles ont été anonymisées par suppression/masking.

## Trade-offs assumés

Le choix 1 permet de conserver une bonne lisibilité, tout en étant RGPD compliant, puisque sans mapping c'est irréversible et donc la donnée n'est plus soumise au RGPD.

Le choix 2 privilégie une anonymisation par suppression, plus forte, mais qui a moins d'impact sur la lecture compte tenu du type des données.

...

## Cadre réglementaire — RGPD + AI Act

> Deux textes, deux angles : positionne tes choix face aux **deux**.

- **RGPD** (données personnelles) : minimisation, finalité, droit à l'effacement.
  Mon anonymisation y répond par : la suppression et la substitution irréversible des entités fortement identifiantes (PERSON, EMAIL, IBAN, PHONE). En ne conservant aucune table de correspondance (mapping), on sort du cadre de la pseudonymisation pour atteindre une véritable anonymisation. La donnée n'est alors plus soumise au RGPD, tout en préservant son utilité analytique (minimisation des données).
- **AI Act** (règlement UE 2024, risque classé par usage) : un système qui exploite
  des **commentaires RH** pour évaluer des personnes relève potentiellement du
  **« haut risque »** (emploi / gestion des travailleurs = Annexe III) → exigences
  renforcées de **qualité des données, traçabilité et supervision humaine**. En quoi
  mon audit + mon anonymisation y contribuent : ils permettent de garantir que le système s'entraîne ou s'exécute sur des données expurgées de biais d'identification directe, réduisant ainsi le risque de discrimination ciblée. La démarche traçable que nous documentons ici assure que les obligations de gouvernance des données sont respectées.

## Limites de ma stratégie

> Qu'est-ce que ma fonction `anonymize_comments` rate ? Quels faux positifs
> ou faux négatifs ai-je observés sur l'échantillon ?

- Faux négatifs (PII non détectées) : spaCy peine parfois à détecter des noms propres plus rares, mal orthographiés ou sans majuscule. De plus, la conservation de certains champs (ORG, LOC, GPE) couplée à un intitulé de poste (ex: "Le directeur de l'agence de Paris") peut créer des données proxy permettant la ré-identification d'une personne sans les champs PII classiques. Les Regex peuvent aussi rater un éventuel format international atypique.
- Faux positifs (texte normal anonymisé à tort) : spaCy peut confondre des mots communs placés en début de phrase ou des noms de produits avec des noms de personnes (PERSON). Certaines combinaisons de chiffres inoffensives peuvent être interprétées par erreur comme des IBANs ou téléphones si les Regex ne sont pas assez ciblées.

## Si je devais industrialiser

> Que faudrait-il ajouter pour une vraie mise en production (M5+) ?

- **Outils spécialisés** : Intégrer une librairie orientée PII comme Microsoft Presidio, plus robuste et personnalisable que spaCy brut pour la détection fine des données sensibles, avec des "recognizers" par contexte.
- **Monitoring et Évaluation Systématique** : Mettre en place un benchmark (Precision / Recall) de notre pipeline sur un dataset de référence annoté manuellement, pour valider que le taux de re-identification est bien sous des seuils acceptables.
- **Human in the Loop** : Isoler les textes ayant un faible score de confiance dans le NER et les attribuer à une supervision humaine (Data Stewards) en vue de fine-tuner ponctuellement notre modèle spaCy aux spécificités de notre domaine.

---

*Note rédigée par Célia, 2026-06-22, dans le cadre du brief M2-B2 ATOS.*