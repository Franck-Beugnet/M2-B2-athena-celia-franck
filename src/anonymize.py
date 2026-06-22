"""M2-B2 — Anonymisation de commentaires manager selon la stratégie reflexion.md

Stratégie appliquée :
- PERSON : Substitution sans mapping → remplacé par noms fictifs Faker aléatoires
- EMAIL, PHONE, IBAN : Suppression
- ORG, GPE, LOC : Aucune (données peu sensibles)
"""
from __future__ import annotations

import argparse
import sys
import pandas as pd
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
    parser = argparse.ArgumentParser(description="Anonymise une colonne d'un fichier CSV.")
    parser.add_argument("input_file", help="Chemin du fichier CSV en entrée.")
    parser.add_argument("output_file", help="Chemin du fichier CSV en sortie.")
    parser.add_argument("--col", default="comment", help="Nom de la colonne à anonymiser (défaut: 'comment').")
    parser.add_argument("--seed", type=int, default=None, help="Seed optionnelle pour Faker (reproductibilité).")

    # Si aucun argument n'est fourni, afficher les exemples d'origine, sinon traiter le fichier
    if len(sys.argv) == 1:
        print("💡 ASTUCE : Vous pouvez utiliser ce script sur un fichier CSV avec :")
        print("   python src/anonymize.py data/entree.csv data/sortie.csv --col \"Commentaire\"\n")
        
        # Test rapide (fallback sans arguments)
        sample = (
            "Allison Hill is a strong promotion candidate this year. "
            "Discussed with HR (Rhonda Smith, 651.216.1559). "
            "Budget pre-approved on account ****3503."
        )
        print("--- TEST RAPIDE ---")
        print("Avant :", sample)
        print("Après :", anonymize_comments(sample))
    else:
        args = parser.parse_args()
        
        print(f"📂 Chargement de {args.input_file}...")
        try:
            df = pd.read_csv(args.input_file)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            sys.exit(1)
            
        if args.col not in df.columns:
            print(f"Erreur : La colonne '{args.col}' n'existe pas dans le fichier.")
            print(f"Colonnes disponibles : {list(df.columns)}")
            sys.exit(1)
            
        print(f"🔍 Anonymisation de la colonne '{args.col}' en cours (cela peut prendre un instant)...")
        # Appliquer la fonction, fillna("") pour éviter de crasher sur les NaN
        df[args.col] = df[args.col].fillna("").astype(str).apply(
            lambda x: anonymize_comments(x, random_seed=args.seed)
        )
        
        print(f"💾 Sauvegarde dans {args.output_file}...")
        df.to_csv(args.output_file, index=False)
        print("Terminé !")