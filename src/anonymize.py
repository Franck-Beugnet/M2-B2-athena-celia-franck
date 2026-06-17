"""M2-B2 — Anonymisation de commentaires manager selon la stratégie reflexion.md

Stratégie appliquée :
- PERSON : Substitution sans mapping → remplacé par noms fictifs Faker aléatoires
- EMAIL, PHONE, IBAN : Suppression
- ORG, GPE, LOC : Aucune (données peu sensibles)
"""
from __future__ import annotations

import re
import spacy
from faker import Faker

# Initialiser Faker (seed pour reproduisibilité en tests)
fake = Faker()

# Charger le modèle spaCy une seule fois au niveau module
NLP = spacy.load("en_core_web_sm")

# Regex de complément (spaCy ne couvre pas tout — email, IBAN partiel, téléphone US)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
PHONE_RE = re.compile(r"\b\d{3}[.-]?\d{3}[.-]?\d{4}\b")
IBAN_PARTIAL_RE = re.compile(r"\*{2,}\d{4}")


def anonymize_comments(text: str, random_seed: int | None = None) -> str:
    """Anonymise un commentaire manager selon stratégie reflexion.md.

    Stratégie :
    - PERSON : remplacé par noms fictifs Faker aléatoires (substitution sans mapping)
    - EMAIL, PHONE, IBAN : supprimé (remplacé par [EMAIL], [PHONE], [IBAN])
    - ORG, GPE, LOC : non modifiés (données peu sensibles)

    Args:
        text: Texte libre potentiellement contenant des PII.
        random_seed: Seed optionnel pour Faker (pour tests reproductibles).

    Returns:
        Texte anonymisé.
    """
    if not text or not isinstance(text, str):
        return text

    # Optionnellement définir la seed pour la reproductibilité
    if random_seed is not None:
        fake_local = Faker()
        fake_local.seed_instance(random_seed)
    else:
        fake_local = fake

    # Étape 1 — Détection et remplacement PERSON avec spaCy + Faker
    doc = NLP(text)
    
    # Collecter les entités PERSON triées par position décroissante
    # (pour remplacer de droite à gauche et ne pas bousiller les indices)
    person_entities = [ent for ent in doc.ents if ent.label_ == "PERSON"]
    
    # Remplacer de droite à gauche par des noms fictifs
    for ent in sorted(person_entities, key=lambda e: e.start_char, reverse=True):
        fake_name = fake_local.name()
        text = text[:ent.start_char] + fake_name + text[ent.end_char:]

    # Étape 2 — Suppression des PII par regex (email, téléphone, IBAN)
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = IBAN_PARTIAL_RE.sub("[IBAN]", text)

    return text


if __name__ == "__main__":
    # Test rapide
    sample = (
        "Allison Hill is a strong promotion candidate this year. "
        "Discussed with HR (Rhonda Smith, 651.216.1559). "
        "Budget pre-approved on account ****3503."
    )
    print("Avant :", sample)
    result = anonymize_comments(sample)
    print("Après :", result)
    print()
    
    # Test avec plusieurs noms
    sample2 = (
        "John Doe and Jane Smith performed well. "
        "Contact: john.doe@company.com or jane.smith@mail.fr. "
        "Phone: 555-123-4567."
    )
    print("Avant :", sample2)
    print("Après :", anonymize_comments(sample2))