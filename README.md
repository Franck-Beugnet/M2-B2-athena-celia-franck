# M2-B2 — Squelette repo (Athéna RH — audit éthique + anonymisation)

---

## �️ Ce qui a été réalisé

Durant ce projet, les tâches suivantes ont été menées à bien :
- **Analyse des données et Audit Éthique** : Le notebook [`notebooks/M2-B2_audit_celia_franck.ipynb`](notebooks/M2-B2_audit_celia_franck.ipynb) rassemble notre travail d'exploration (EDA) ainsi que le calcul du *Disparate Impact* croisé sur les variables sensibles (intersectionnalité) pour identifier les sources de biais potentielles de l'algorithme. 
  👉 La consolidation de cette analyse et de la vie de la donnée se trouve résumée dans notre [datasheet.md](datasheet.md).
- **Anonymisation Stratégique** : Le notebook [`notebooks/M2-B2-anonymization.ipynb`](notebooks/M2-B2-anonymization.ipynb) met en pratique et expérimente la stratégie développée dans le script d'industrialisation [`src/anonymize.py`](src/anonymize.py). Cette étape combine *Name Entity Recognition* (via `spaCy`), des Regex et de la substitution artificielle (via `Faker`) pour conformer les commentaires RH aux exigences légales.
La réfléxion qui a accompagnée l'anonymisation, le choix de la stratégie et ses limites se trouve dans le fichier [reflexion.md](reflexion.md).

---

## �🚀 Démarrage

```bash
# 0. Clone ton repo perso (ou binôme)
git clone git@github.com:<owner>/<repo-name>.git
cd <repo-name>

# 1. Environnement virtuel
python -m venv .venv && source .venv/bin/activate     # Linux/macOS
# .venv\Scripts\activate                              # Windows

# 2. Dépendances
pip install -r requirements.txt

# 3. Dépose les 2 CSV reçus via Discord (fil-M2-B2) dans data/ :
#    data/adult_income_with_comments.csv  +  data/audit_sample.csv

# 4. Modèle spaCy (~50 Mo — à télécharger une fois)
python -m spacy download en_core_web_md

# 5. Vérification
jupyter notebook notebooks/M2-B2_audit_template.ipynb
```

Si ça démarre sans erreur, ton poste est prêt.

---

## 📁 Structure du repo (Actuelle)

Voici l'arborescence finale du projet avec les fichiers produits lors de nos expérimentations :

```text
M2-B2-athena-celia-franck/
├── data/                                         # Fichiers de données (gitignored)
│   ├── adult_income_with_comments.csv            # Jeu fourni via Discord
│   ├── audit_sample.csv                          # Échantillon fourni pour l'anonymisation
│   └── audit_sample_anonymized.csv               # Fichier généré après lancement du script d'anonymisation
├── notebooks/
│   ├── M2-B2_audit_celia_franck.ipynb            # Notebook d'analyse de données et d'audit du DI
│   └── M2-B2-anonymization.ipynb                 # Notebook de démonstration de la fonction d'anonymisation
├── src/
│   └── anonymize.py                              # Script CLI final d'anonymisation (spaCy + Faker + Regex)
├── datasheet.md                                  # Documentation du jeu de donnée (Gebru)
├── reflexion.md                                  # Note de réflexion justifiant nos choix techniques (RGPD / AI Act)
├── README.md                                     # Documentation du projet
├── ressources/                                   # 📚 mini-cours d'appui
│   ├── ...                                       # (Ressources fournies initialement)
├── test_anonymize_simple.py                      # Tests
├── test_demo.py                                  # Tests
├── requirements.txt                              # Dépendances (pandas, spacy, faker, etc.)
└── .gitignore
```

---

## 📚 Mini-cours d'appui

Les **6 mini-cours pédagogiques** sont fournis dans
[`./ressources/`](./ressources/). Lecture juste-à-temps :

| Tâche | Mini-cours |
|---|---|
| Audit éthique complet (DI + intersectionnalité) | [`01_Audit_ethique_complet_essentiel.md`](./ressources/01_Audit_ethique_complet_essentiel.md) |
| Datasheet Gebru — version étoffée | [`02_Datasheet_Gebru_complet_essentiel.md`](./ressources/02_Datasheet_Gebru_complet_essentiel.md) |
| spaCy NER pour la détection PII | [`03_spaCy_NER_PII_essentiel.md`](./ressources/03_spaCy_NER_PII_essentiel.md) |
| Stratégies d'anonymisation (4 options) | [`04_Strategies_anonymisation_essentiel.md`](./ressources/04_Strategies_anonymisation_essentiel.md) |
| Microsoft Presidio (bonus) | [`05_Presidio_alternative_essentiel.md`](./ressources/05_Presidio_alternative_essentiel.md) |
| Git en binôme (branches + Co-authored-by) | [`06_Git_binome_essentiel.md`](./ressources/06_Git_binome_essentiel.md) |

Cf. [`./ressources/README.md`](./ressources/README.md) pour l'ordre de mobilisation.

---

## 🧭 Démarche attendue

### Mercredi sync (2h15) — binôme

1. **Setup binôme** (15 min) — choix du binôme, repo commun, conventions
   `Co-authored-by:`, switch driver/navigator
2. **Audit éthique complet** (1h30) — DI sur ≥ 3 variables sensibles + intersection
3. **Datasheet binôme** (30 min) — 7 sections Gebru, signée duo
4. **Tour de table 11h30** — restitution duo 5 min × 4 paires

### Async jeudi/vendredi matin (6h) — individuel

5. **Fork du repo binôme** (15 min)
6. **Exploration PII** (1h)
7. **Mise en place spaCy NER** (1h) — vérification qualitative sur ~10 exemples
8. **Stratégie d'anonymisation** (2h) — tu défends ton choix dans `reflexion.md`
9. **Production livrables perso** (1h45)

→ Compétences visées : **C2 — imiter (renforcement)** + **C3 — adapter (renforcement)**.

---

## ✅ Conventions de code

- Python 3.11+
- Type hints sur toutes les signatures publiques
- Pas de `print` (utiliser `display()`)
- `pathlib.Path` pour les chemins
- En **binôme** : commits avec `Co-authored-by: <prénom> <email>` pour le
  partenaire qui n'est pas au clavier

---

## 🆘 Bloqué·e ?

1. Relis le mini-cours concerné (cf. [`./ressources/README.md`](./ressources/README.md)).
2. Si **spaCy** plante au chargement du modèle : as-tu fait
   `python -m spacy download en_core_web_md` ? (~50 Mo)
3. La **détection NER rate des noms français** (~12 % du corpus) : c'est
   attendu avec `en_core_web_md`. Complète par regex, ou charge en plus
   `fr_core_news_md` sur les commentaires détectés comme français — mais
   surtout **documente cette limite** dans ta `reflexion.md`.
4. En binôme : si vous bloquez à 2, **switchez** driver/navigator —
   souvent ça débloque.
5. Demande en direct mercredi sur Discord — `fil-M2-B2`.