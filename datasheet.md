# Datasheet — Adult Income enrichi (Athéna RH v1.0.0)

> Document accompagnant le dataset livré à Athéna RH.
> **Modèle Gebru et al. (2018), 7 sections, 2 pages max.**
> Signée binôme.

**Auteurs** : <prénom1>, <prénom2>
**Date** : <date>
**Version** : v1.0.0

## 1. Motivation

> Pourquoi ce dataset existe ? Qui l'a créé ?

- ...

## 2. Composition

> Combien d'observations, quelles colonnes, types, distribution cible,
> **variables sensibles signalées explicitement**, + le résumé du
> verdict éthique (DI les plus problématiques).

| Aspect | Valeur |
|---|---|
| Nombre de lignes | ... |
| Nombre de colonnes | 16 (14 features UCI + cible `income` + `manager_comments` synthétique) |
| Cible | `income` : `<=50K` / `>50K` |
| Distribution cible | ... |
| Variables sensibles | `sex`, `race`, `native_country`, `marital_status` |

**Schéma des colonnes** :

| Colonne | Type | Note |
|---|---|---|
| `age` | int | 17 — 90 |
| `workclass` | str | Statut de travail (9 modalités) |
| `education` | str | Diplôme (16 modalités) |
| `marital_status` | str | ⚠️ Sensible |
| `occupation` | str | Profession (15 modalités) |
| `relationship` | str | Position familiale (6 modalités) |
| `race` | str | ⚠️ Sensible (5 modalités) |
| `sex` | str | ⚠️ Sensible binaire |
| `capital_gain` / `capital_loss` | int | Très asymétriques (médiane 0) |
| `hours_per_week` | int | 1 — 99 |
| `native_country` | str | ⚠️ Sensible (40+ modalités) |
| `income` (cible) | str | `<=50K`, `>50K` |
| `manager_comments` | str | Texte libre **avec PII** — à anonymiser en async |

**Résumé verdict éthique** :
- DI le plus problématique : intersection `sex × race` — DI `Female_Other` = 0.229 (moins du quart du taux global)
- `sex` : DI Female vs overall = 0.455 (seuil critique 0.8 largement dépassé)
- `race` : `Black` DI = 0.512, `Amer-Indian-Eskimo` DI = 0.478 (sous-sélection marquée)
- `native_country` : non-USA DI = 0.820 (légèrement sous le seuil)
- Intersectionnalités notables : `Female_Black` (DI = 0.240), `Female_Other` (DI = 0.229) — effet cumulatif sexe + race
- ⚠️ RGPD art. 9 : `race`, `sex`, `native_country`, `marital_status` sont des catégories spéciales de données — traitement en principe interdit sans base légale
- ⚠️ PII : `manager_comments` contient des données personnelles identifiantes — anonymisation obligatoire

## 3. Processus de collecte

> Origine UCI Adult Census 1994 + enrichissement Athéna RH 2026.

- ...

## 4. Preprocessing appliqué

> Ce que **votre binôme** a fait dans la phase sync.

- ...

## 5. Usages prévus / à éviter

**Usages prévus** :
- ...

**Usages à éviter** :
- ...

## 6. Distribution

- Destinataire : Athéna RH (Laurence Béthencourt, DPO)
- Format : Parquet snappy
- Conditions : ...

## 7. Maintenance

- Mainteneur·euses : <prénom1>, <prénom2>
- Version : v1.0.0 — <date>
- Signaler un problème : ...

---

## 8. Verdict éthique & Risques

### Biais structurels détectés

L'audit éthique du dataset Adult Income (32 561 lignes, 16 colonnes) révèle des biais structurels significatifs sur trois variables sensibles.

**Variable `sex`**  
Le taux de sélection `>50K` est de **30,6 %** pour les hommes contre **10,9 %** pour les femmes.
Le DI vs taux global est de **0.455** pour les femmes, très en dessous du seuil critique de 0.8. Ce biais reflète des inégalités salariales et de progression de carrière documentées dans les données de recensement 1994.

**Variable `race` (sans modalité Other)**  
Les groupes `Black` (DI = 0.512) et `Amer-Indian-Eskimo` (DI = 0.478) sont nettement sous-représentés dans la tranche haute de revenus par rapport au taux global (24,2 % hors Other).
À l'inverse, `Asian-Pac-Islander` (DI = 1.097) et `White` (DI = 1.057) sont légèrement sur-représentés.
La matrice pairwise confirme des écarts forts entre les deux groupes favorisés et les deux groupes défavorisés (DI pairwise autour de 0.44–0.48).

**Variable `native_country` (USA / non-USA)**  
Le DI vs global est de **0.820** pour le groupe non-USA, légèrement sous le seuil de 0.8. Le biais est présent mais moins sévère que sur `sex` et `race`.

### Intersection la plus problématique

Le croisement `sex × race` révèle des écarts bien plus marqués :

| Groupe | DI vs overall |
|---|---|
| Male_Asian-Pac-Islander | 1.396 (sur-sélection) |
| Male_White | 1.319 (sur-sélection) |
| Female_Black | 0.240 (forte sous-sélection) |
| Female_Other | 0.229 (forte sous-sélection) |

L'effet cumulatif sexe + race pénalise massivement les femmes des groupes minoritaires. Le groupe `Female_Other` (DI = 0.229) atteint moins du quart du taux global.

### Dimension RGPD

Ce dataset soulève plusieurs problématiques au regard du Règlement Général sur la Protection des Données (RGPD, UE 2016/679) :

**Données à caractère sensible (article 9 RGPD)**  
Les colonnes `race`, `sex`, `native_country` et `marital_status` sont des **catégories spéciales de données** au sens de l'article 9 du RGPD :

| Colonne | Catégorie RGPD art. 9 |
|---|---|
| `race` | Origine raciale ou ethnique |
| `sex` | Donnée à caractère personnel (sexe) |
| `native_country` | Origine nationale |
| `marital_status` | Indirectement liée à la vie privée |

Le traitement de ces données est **en principe interdit**, sauf exception explicite (consentement, intérêt public, etc.). Les utiliser comme features dans un système de décision RH constitue un **usage prohibé** sans base légale documentée.

**Données PII dans `manager_comments`**  
La colonne `manager_comments` contient des **informations personnelles identifiantes (PII)** : noms, prénoms, éventuellement des coordonnées. Leur présence en clair dans le dataset constitue une non-conformité RGPD (droit à la minimisation des données, art. 5). Une **anonymisation obligatoire** est requise avant tout usage.

**Proxy et discrimination indirecte**  
Utiliser `fnlwgt` ou `education_num` comme features peut induire une **discrimination indirecte** au sens de l'article 22 RGPD relatif aux décisions automatisées. Même en retirant les colonnes sensibles, un modèle entraîné sur ce dataset peut reproduire les biais via ces proxies.

### Conclusion

**Le biais le plus problématique est l'intersection `sex × race`**, qui amplifie les désavantages individuels de chaque dimension. Un modèle entraîné naïvement sur ce dataset risquerait de reproduire et de consolider ces inégalités structurelles, et exposerait l'organisation à un risque juridique au titre du RGPD et des législations anti-discrimination.

**Recommandations** :
- Exclure `sex`, `race`, `native_country`, `marital_status` de tout modèle décisionnel RH.
- Anonymiser `manager_comments` avant tout traitement (cf. phase async).
- Exclure `fnlwgt` des features (proxy des variables sensibles).
- Documenter la base légale du traitement auprès du DPO (Laurence Béthencourt, Athéna RH).

---

*Datasheet produite en binôme dans le cadre du brief M2-B2 ATOS.*