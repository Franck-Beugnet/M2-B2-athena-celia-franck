# Note de réflexion — Stratégie d'anonymisation (perso)

> Template à remplir en phase async individuelle (jeudi/vendredi matin).
> **Max 1 page.** Personnel — chaque apprenant rédige la sienne.
> Public : Marianne (évaluation) + futur toi qui relit ce repo.

---

## Ma stratégie d'anonymisation

> Quelle stratégie ai-je choisie ? Suppression / substitution /
> généralisation / hash / mix ?

J'ai choisi une stratégie mixte, avec une règle centrale simple et robuste :

- toutes les personnes détectées sont remplacées par [PERSON] ;
- les identifiants directs (email, téléphone, IBAN partiel) sont supprimés via
  des marqueurs explicites ([REDACTED_EMAIL], [REDACTED_PHONE]) ;
- les dates sont généralisées (ou masquées) selon le contexte ;
- les lieux sont masqués en [LOCATION] lorsque présents.

Je n'utilise pas de hash comme méthode principale, car cela reste de la
pseudonymisation et non une anonymisation légale forte.

## Ce que j'ai gardé lisible et pourquoi

> Quelles informations laisse-t-on dans le texte (et pourquoi c'est OK) ?

- la structure métier du commentaire (alerte, suivi RH, demande de transfert,
  validation, etc.) ;
- les relations d'action (quelqu'un valide, quelqu'un suit un dossier), mais
  sans identité nominative ;
- les références opérationnelles non personnelles si elles ne permettent pas de
  ré-identification directe.

Objectif : conserver la valeur analytique (audit qualité RH, typologie des
cas) sans exposer de données personnelles identifiantes.

## Ce que j'ai masqué et pourquoi

> Quelles informations ai-je remplacées et avec quelle logique ?

- PERSON -> [PERSON], systématiquement.

Raison principale : l'inférence de rôle (manager vs employee) depuis du texte
libre n'est pas fiable à 100 % (phrases ambiguës, multi-personnes, FR/EN).
Je préfère une règle uniforme, stable et défendable.

- EMAIL -> [REDACTED_EMAIL] ; PHONE -> [REDACTED_PHONE] ;

Raison : ce sont des identifiants directs à fort risque de ré-identification.

- DATE -> [DATE] ou forme agrégée (mois/année).

Raison : limiter le chaînage temporel avec d'autres sources.

- GPE/location -> [LOCATION].

Raison : diminuer le risque de ré-identification géographique.

## Trade-offs assumés

> Lisibilité du texte vs protection vie privée. Où ai-je placé le curseur,
> et pour quelles raisons (RGPD, métier, robustesse) ?

J'ai placé le curseur du côté de la protection :

- perte assumée : on ne distingue plus explicitement manager et employee dans
  le texte anonymisé ;
- gain : règle homogène, moins d'erreurs de classification de rôle, réduction
  du risque de fuite d'identité ;
- robustesse : stratégie simple à maintenir et plus stable sur corpus mixte
  anglais/français.

Je privilégie donc la fiabilité de l'anonymisation sur la finesse sémantique.

## Cadre réglementaire — RGPD + AI Act

> Deux textes, deux angles : positionne tes choix face aux **deux**.

- **RGPD** (données personnelles) : minimisation, finalité, droit à l'effacement.
  Mon anonymisation y répond par : suppression des identifiants directs,
  réduction des quasi-identifiants (dates/lieux), et minimisation de la donnée
  nominative (PERSON -> [PERSON]). La finalité reste l'analyse qualitative RH,
  sans nécessité de conserver l'identité.
- **AI Act** (règlement UE 2024, risque classé par usage) : un système qui exploite
  des **commentaires RH** pour évaluer des personnes relève potentiellement du
  **« haut risque »** (emploi / gestion des travailleurs = Annexe III) → exigences
  renforcées de **qualité des données, traçabilité et supervision humaine**. En quoi
  mon audit + mon anonymisation y contribuent : meilleure qualité des données
  d'entrée (moins de bruit PII), documentation explicite des limites NER
  anglais sur commentaires français, et réduction du risque de décisions
  automatisées reposant sur des données identifiantes.

## Limites de ma stratégie

> Qu'est-ce que ma fonction `anonymize_comments` rate ? Quels faux positifs
> ou faux négatifs ai-je observés sur l'échantillon ?

- Faux négatifs (PII non détectées) : certains noms FR rares, formes abrégées,
  et variantes non couvertes par les regex peuvent passer.
- Faux positifs (texte normal anonymisé à tort) : certains groupes de mots
  capitalisés peuvent être pris pour des noms ; quelques ORG/GPE détectés par
  le modèle EN sont erronés sur texte FR.

Limite clé documentée : le modèle en_core_web_md est performant sur anglais,
moins fiable sur la partie francophone du corpus. 

## Si je devais industrialiser

> Que faudrait-il ajouter pour une vraie mise en production (M5+) ?

- pipeline bilingue : détection de langue puis NER adapté (EN/FR) ;
- jeux de tests annotés (FR/EN) + métriques de précision/rappel par type de
  PII ;
- journalisation des transformations pour auditabilité ;
- revue humaine pour les cas sensibles avant usage en aval.

---

*Note rédigée par Franck, 17/06/2026, dans le cadre du brief M2-B2 ATOS.*