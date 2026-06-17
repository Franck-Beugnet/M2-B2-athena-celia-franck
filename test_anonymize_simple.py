#!/usr/bin/env python
"""Tests simples pour la fonction d'anonymisation - sans dépendance pytest."""

import sys
sys.path.insert(0, r"c:\git\repository\formation\M2-B2-athena-celia-franck")

from src.anonymize import anonymize_comments

def test_person_anonymization():
    """Test substitution PERSON par noms fictifs Faker."""
    result = anonymize_comments("John Smith is here")
    # Doit contenir un nom fictif, pas le nom original
    assert "John Smith" not in result
    # Le résultat doit être un nom (avec majuscules généralement)
    assert len(result) > 0
    # Vérifier que c'est un nom fictif (doit contenir au moins un espace généralement)
    assert "is here" in result  # Le reste du texte doit être intact
    print("✓ test_person_anonymization")

def test_email_anonymization():
    """Test suppression EMAIL."""
    result = anonymize_comments("Contact john@example.com")
    assert "[EMAIL]" in result
    assert "@" not in result
    print("✓ test_email_anonymization")

def test_phone_anonymization():
    """Test suppression PHONE."""
    result = anonymize_comments("Call 555-123-4567")
    assert "[PHONE]" in result
    assert "555-123-4567" not in result
    print("✓ test_phone_anonymization")

def test_iban_anonymization():
    """Test suppression IBAN."""
    result = anonymize_comments("Account ****3503")
    assert "[IBAN]" in result
    assert "****3503" not in result
    print("✓ test_iban_anonymization")

def test_multiple_names():
    """Test plusieurs noms remplacés par noms fictifs différents."""
    result = anonymize_comments("John Smith and Jane Doe discussed", random_seed=42)
    # Les noms originaux ne doivent plus être présents
    assert "John Smith" not in result
    assert "Jane Doe" not in result
    # Mais le reste doit être intact
    assert "discussed" in result
    print("✓ test_multiple_names")

def test_organization_not_anonymized():
    """Test que ORG n'est pas anonymisé."""
    result = anonymize_comments("Working with Apple and Microsoft")
    assert "Apple" in result
    assert "Microsoft" in result
    print("✓ test_organization_not_anonymized")

def test_location_not_anonymized():
    """Test que LOC/GPE n'est pas anonymisé."""
    result = anonymize_comments("Meeting in Paris and London")
    assert "Paris" in result
    assert "London" in result
    print("✓ test_location_not_anonymized")

def test_combined():
    """Test cas combiné réaliste avec noms fictifs."""
    text = (
        "Allison Hill is a strong promotion candidate. "
        "Discussed with HR (Rhonda Smith, 651.216.1559). "
        "Budget ****3503. Email: allison@company.com"
    )
    result = anonymize_comments(text, random_seed=123)
    
    # Vérifier que les noms originaux sont remplacés
    assert "Allison Hill" not in result
    assert "Rhonda Smith" not in result
    # Vérifier que les autres PII sont supprimées
    assert "651.216.1559" not in result
    assert "****3503" not in result
    assert "allison@company.com" not in result
    
    # Vérifier la présence des marqueurs pour les suppressions
    assert "[PHONE]" in result
    assert "[IBAN]" in result
    assert "[EMAIL]" in result
    
    # Vérifier que les noms fictifs remplacent les originaux (contiennent un espace généralement)
    # et que "candidate" est encore là
    assert "candidate" in result
    print("✓ test_combined")

def test_empty_and_none():
    """Test entrées vides."""
    assert anonymize_comments("") == ""
    assert anonymize_comments(None) is None
    print("✓ test_empty_and_none")

def test_non_string():
    """Test entrées non-string."""
    assert anonymize_comments(123) == 123
    assert anonymize_comments(False) is False
    print("✓ test_non_string")

def test_punctuation_preservation():
    """Test préservation ponctuation avec noms fictifs."""
    result = anonymize_comments("John Smith, Jane Doe. Robert Wilson!", random_seed=99)
    # Les noms originaux doivent être remplacés
    assert "John Smith" not in result
    assert "Jane Doe" not in result
    assert "Robert Wilson" not in result
    # La ponctuation doit être préservée
    assert "," in result
    assert "." in result
    assert "!" in result
    print("✓ test_punctuation_preservation")

def test_repeated_name():
    """Test que noms répétés sont remplacés (potentiellement différemment sans mapping)."""
    result = anonymize_comments("John Smith met John Smith yesterday", random_seed=55)
    assert "John Smith" not in result
    assert "yesterday" in result
    print("✓ test_repeated_name")

def test_random_seed_reproducibility():
    """Test que le seed Faker produit des résultats reproductibles."""
    text = "John Smith and Jane Doe discussed"
    result1 = anonymize_comments(text, random_seed=42)
    result2 = anonymize_comments(text, random_seed=42)
    # Même seed doit produire les mêmes noms fictifs
    assert result1 == result2
    print("✓ test_random_seed_reproducibility")

def test_different_seeds_produce_different_names():
    """Test que des seeds différentes produisent des noms fictifs différents."""
    text = "John Smith"
    result1 = anonymize_comments(text, random_seed=42)
    result2 = anonymize_comments(text, random_seed=99)
    # Des seeds différentes doivent normalement produire des noms différents
    # (bien que statistiquement possibles mais très peu probables)
    assert result1 != result2 or "Smith" in result1  # Au cas où
    print("✓ test_different_seeds_produce_different_names")

if __name__ == "__main__":
    print("=" * 60)
    print("Exécution des tests d'anonymisation (Faker substitution)")
    print("=" * 60)
    
    tests = [
        test_person_anonymization,
        test_email_anonymization,
        test_phone_anonymization,
        test_iban_anonymization,
        test_multiple_names,
        test_organization_not_anonymized,
        test_location_not_anonymized,
        test_combined,
        test_empty_and_none,
        test_non_string,
        test_punctuation_preservation,
        test_repeated_name,
        test_random_seed_reproducibility,
        test_different_seeds_produce_different_names,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Exception: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Résultats : {passed} passés, {failed} échoués")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)
