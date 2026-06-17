#!/usr/bin/env python
"""Démonstration de l'anonymisation avec Faker substitution."""

import sys
sys.path.insert(0, r"c:\git\repository\formation\M2-B2-athena-celia-franck")

from src.anonymize import anonymize_comments

# Test 1: Exemple réaliste du notebook
sample1 = (
    "Allison Hill is a strong promotion candidate this year. "
    "Discussed with HR (Rhonda Smith, 651.216.1559). "
    "Budget pre-approved on account ****3503."
)
print("Test 1: Exemple réaliste (avec seed pour reproductibilité)")
print(f"Avant: {sample1}")
print(f"Après: {anonymize_comments(sample1, random_seed=42)}\n")

# Test 2: Email et phone
sample2 = (
    "John Smith and Jane Doe performed well. "
    "Contact: john.doe@company.com or call 555-123-4567."
)
print("Test 2: Email et phone (avec seed pour reproductibilité)")
print(f"Avant: {sample2}")
print(f"Après: {anonymize_comments(sample2, random_seed=123)}\n")

# Test 3: Organisations et lieux (ne doivent pas être anonymisés)
sample3 = "Apple and Microsoft met in Paris for the meeting."
print("Test 3: ORG et GPE (non anonymisés)")
print(f"Avant: {sample3}")
print(f"Après: {anonymize_comments(sample3)}\n")

# Test 4: Noms sans seed (noms fictifs aléatoires à chaque exécution)
sample4 = "Peter Parker and Mary Jane worked on the project."
print("Test 4: Noms aléatoires différents à chaque exécution (pas de seed)")
print(f"Avant: {sample4}")
for i in range(3):
    print(f"Exécution {i+1}: {anonymize_comments(sample4)}")

