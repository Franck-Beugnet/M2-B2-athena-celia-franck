# Tests d'anonymisation — `test_anonymize_simple.py`

## Description

Tests pour la fonction `anonymize_comments()` qui implémente la stratégie d'anonymisation définie dans `reflexion.md`.

**Stratégie appliquée :**
- `PERSON` : Remplacé par noms fictifs aléatoires générés avec **Faker** (substitution sans mapping)
- `EMAIL`, `PHONE`, `IBAN` : Supprimés (remplacés par `[EMAIL]`, `[PHONE]`, `[IBAN]`)
- `ORG`, `GPE`, `LOC` : Non modifiés (données peu sensibles selon stratégie)

## Exécution

### Option 1 : Script simple (sans pytest)
```bash
python test_anonymize_simple.py
```

Résultat :
```
============================================================
Exécution des tests d'anonymisation (Faker substitution)
============================================================
✓ test_person_anonymization
✓ test_email_anonymization
✓ test_phone_anonymization
✓ test_iban_anonymization
✓ test_multiple_names
✓ test_organization_not_anonymized
✓ test_location_not_anonymized
✓ test_combined
✓ test_empty_and_none
✓ test_non_string
✓ test_punctuation_preservation
✓ test_repeated_name
✓ test_random_seed_reproducibility
✓ test_different_seeds_produce_different_names
============================================================
Résultats : 14 passés, 0 échoués
============================================================
```

### Option 2 : Pytest (si pytest est installé)
```bash
pip install pytest
pytest tests/test_anonymize.py -v
```

## Cas couverts (14 tests)

### Cas positifs — Substitution Faker
1. **test_person_anonymization** — Noms remplacés par noms fictifs Faker
2. **test_multiple_names** — Plusieurs noms remplacés par noms fictifs différents
3. **test_faker_reproducibility_with_seed** — Même seed produit les mêmes noms fictifs
4. **test_different_seeds_produce_different_names** — Seeds différentes → noms fictifs différents

### Tests PII
5. **test_email_anonymization** — Emails supprimées
6. **test_phone_anonymization** — Téléphones supprimés
7. **test_iban_anonymization** — IBANs partiels supprimés
8. **test_organization_not_anonymized** — ORG laissés inchangés
9. **test_location_not_anonymized** — LOC/GPE laissés inchangés
10. **test_combined** — Cas réaliste avec plusieurs types de PII

### Cas limites
11. **test_empty_and_none** — Chaînes vides et None gérées gracieusement
12. **test_non_string** — Entrées non-string retournées inchangées
13. **test_punctuation_preservation** — Ponctuation préservée autour des noms fictifs
14. **test_repeated_name** — Noms répétés tous remplacés

## Exemple d'utilisation

### Avec seed (pour tests reproductibles)
```python
from src.anonymize import anonymize_comments

text = (
    "Allison Hill is a strong promotion candidate. "
    "Discussed with HR (Rhonda Smith, 651.216.1559). "
    "Budget pre-approved on account ****3503. "
    "Contact: allison@company.com"
)

result = anonymize_comments(text, random_seed=42)
# Résultat (reproductible avec seed=42):
# "Noah Rhodes is a strong promotion candidate. 
#  Discussed with HR (Allison Hill, [PHONE]). 
#  Budget pre-approved on account [IBAN]. 
#  Contact: [EMAIL]"
```

### Sans seed (aléatoire à chaque exécution)
```python
result = anonymize_comments(text)
# Chaque exécution génère des noms fictifs différents
```

## Dépendances

- `spacy>=3.7.5`
- `faker>=40.0`
- `en_core_web_sm` (téléchargé automatiquement dans `src/anonymize.py`)

Installation :
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Stratégie détaillée

### Substitution Faker (PERSON)
La stratégie est **sans mapping persistant** : chaque nom détecté par spaCy NER est remplacé par un nom fictif généré par Faker. 

**Avantages :**
- Noms réalistes et contextuellement appropriés
- Pas de mapping à maintenir
- Lisibilité préservée (le texte reste compréhensible)
- Conforme RGPD (anonymisation irréversible)

**Exemple :**
```
Avant : "John Smith discussed with Jane Doe"
Après : "Noah Rhodes discussed with Victoria Riddle"
```

### Suppression (EMAIL, PHONE, IBAN)
Ces données sensibles sont remplacées par des marqueurs génériques : `[EMAIL]`, `[PHONE]`, `[IBAN]`.

**Avantage :** Pas de risque de ré-identification.

### Non-modification (ORG, GPE, LOC)
Les organisations, pays et lieux ne sont pas anonymisés car considérés comme peu sensibles dans le contexte RH.

