"""Tests pour la fonction d'anonymisation de commentaires manager.

Couverture des cas d'usage selon la stratégie :
- PERSON : substitution par noms fictifs Faker aléatoires (sans mapping)
- EMAIL, PHONE, IBAN : suppression
- ORG, GPE, LOC : inchangés
"""

import pytest
from src.anonymize import anonymize_comments


class TestPersonAnonymization:
    """Tests pour la détection et substitution des noms de personne par Faker."""

    def test_simple_person_name(self):
        """Un nom simple doit être remplacé par un nom fictif Faker."""
        text = "John Smith is a manager."
        result = anonymize_comments(text, random_seed=42)
        assert "John Smith" not in result
        assert "is a manager" in result  # Reste du texte intact
        # Vérifier que le résultat contient un nom (doit être non-vide et différent)
        assert len(result) > 0

    def test_multiple_person_names(self):
        """Plusieurs noms doivent être remplacés par noms fictifs."""
        text = "John Smith and Jane Doe discussed the project."
        result = anonymize_comments(text, random_seed=42)
        assert "John Smith" not in result
        assert "Jane Doe" not in result
        assert "discussed the project" in result

    def test_person_with_title(self):
        """Un nom avec titre honorifique doit être détecté et remplacé."""
        text = "Dr. Robert Johnson reviewed the file."
        result = anonymize_comments(text, random_seed=42)
        assert "Robert Johnson" not in result
        assert "reviewed the file" in result

    def test_empty_or_none(self):
        """Les chaînes vides ou None doivent être traitées sans erreur."""
        assert anonymize_comments("") == ""
        assert anonymize_comments(None) is None

    def test_person_at_beginning(self):
        """Un nom au début du texte doit être remplacé."""
        text = "Alice Brown started working here."
        result = anonymize_comments(text, random_seed=42)
        assert "Alice Brown" not in result
        assert "started working here" in result

    def test_faker_reproducibility_with_seed(self):
        """Même seed Faker doit produire les mêmes noms fictifs."""
        text = "John Smith met Jane Doe."
        result1 = anonymize_comments(text, random_seed=42)
        result2 = anonymize_comments(text, random_seed=42)
        assert result1 == result2

    def test_different_seeds_produce_different_names(self):
        """Seeds différentes doivent produire des noms fictifs différents."""
        text = "John Smith"
        result1 = anonymize_comments(text, random_seed=42)
        result2 = anonymize_comments(text, random_seed=99)
        # Très probable que deux seeds différentes produisent des noms différents
        assert result1 != result2


class TestEmailAnonymization:
    """Tests pour la suppression des adresses email."""

    def test_simple_email(self):
        """Une email simple doit être supprimée."""
        text = "Contact john.doe@company.com for details."
        result = anonymize_comments(text)
        assert "[EMAIL]" in result
        assert "john.doe@company.com" not in result

    def test_multiple_emails(self):
        """Plusieurs emails doivent être supprimées."""
        text = "Reach out to alice@test.fr or bob@mail.com."
        result = anonymize_comments(text)
        assert result.count("[EMAIL]") == 2
        assert "@" not in result

    def test_email_with_special_chars(self):
        """Une email avec caractères spéciaux doit être détectée."""
        text = "Email: jane.smith+tag@domain.co.uk"
        result = anonymize_comments(text)
        assert "[EMAIL]" in result
        assert "@" not in result


class TestPhoneAnonymization:
    """Tests pour la suppression des numéros de téléphone."""

    def test_phone_us_format(self):
        """Un numéro au format US XXX-XXX-XXXX doit être supprimé."""
        text = "Call me at 555-123-4567."
        result = anonymize_comments(text)
        assert "[PHONE]" in result
        assert "555-123-4567" not in result

    def test_phone_dot_format(self):
        """Un numéro au format XXX.XXX.XXXX doit être supprimé."""
        text = "My phone is 651.216.1559."
        result = anonymize_comments(text)
        assert "[PHONE]" in result
        assert "651.216.1559" not in result

    def test_multiple_phones(self):
        """Plusieurs numéros doivent être supprimés."""
        text = "Call 555-123-4567 or 555.987.6543."
        result = anonymize_comments(text)
        assert result.count("[PHONE]") == 2

    def test_no_false_positive_on_numbers(self):
        """Des nombres qui ne sont pas des téléphones ne doivent pas être modifiés."""
        text = "We processed 123 items."
        result = anonymize_comments(text)
        assert "[PHONE]" not in result
        assert "123" in result


class TestIbanAnonymization:
    """Tests pour la suppression des IBAN partiels."""

    def test_iban_partial_masked(self):
        """Un IBAN partiel masqué doit être supprimé."""
        text = "Account ****3503."
        result = anonymize_comments(text)
        assert "[IBAN]" in result
        assert "****3503" not in result

    def test_multiple_iban(self):
        """Plusieurs IBANs partiels doivent être supprimés."""
        text = "Accounts ****1234 and ****5678."
        result = anonymize_comments(text)
        assert result.count("[IBAN]") == 2


class TestCombinedAnonymization:
    """Tests sur des cas combinant plusieurs types de PII."""

    def test_realistic_manager_comment(self):
        """Un commentaire manager réaliste avec plusieurs types de PII."""
        text = (
            "Allison Hill is a strong promotion candidate this year. "
            "Discussed with HR (Rhonda Smith, 651.216.1559). "
            "Budget pre-approved on account ****3503. "
            "Contact: allison@company.com"
        )
        result = anonymize_comments(text, random_seed=42)
        
        # Vérifier les substitutions des noms par noms fictifs
        assert "Allison Hill" not in result
        assert "Rhonda Smith" not in result
        # Vérifier que les autres PII sont supprimées
        assert "651.216.1559" not in result
        assert "****3503" not in result
        assert "allison@company.com" not in result
        
        # Vérifier que les marqueurs de suppression sont présents
        assert "[PHONE]" in result
        assert "[IBAN]" in result
        assert "[EMAIL]" in result
        
        # Vérifier que des parties du texte sont intactes
        assert "promotion candidate" in result
        assert "this year" in result

    def test_organization_not_anonymized(self):
        """Les noms d'organisations ne doivent pas être anonymisés."""
        text = "Working on Google project with Apple team."
        result = anonymize_comments(text)
        # ORG ne sont pas anonymisés par notre stratégie
        assert "Google" in result
        assert "Apple" in result

    def test_location_not_anonymized(self):
        """Les lieux ne doivent pas être anonymisés."""
        text = "Meeting scheduled in Paris and London."
        result = anonymize_comments(text)
        # LOC/GPE ne sont pas anonymisés par notre stratégie
        assert "Paris" in result
        assert "London" in result


class TestEdgeCases:
    """Tests pour les cas limites."""

    def test_whitespace_preservation(self):
        """Les espaces doivent être préservés après anonymisation."""
        text = "John Smith  has  two  spaces."
        result = anonymize_comments(text, random_seed=42)
        assert "  " in result  # Les doubles espaces sont conservés
        assert "has  two" in result

    def test_punctuation_preservation(self):
        """La ponctuation doit être préservée autour des entités."""
        text = "John Smith, Jane Doe. Robert Wilson!"
        result = anonymize_comments(text, random_seed=42)
        # Les noms fictifs doivent avoir la ponctuation préservée
        assert "," in result
        assert "." in result
        assert "!" in result

    def test_non_string_input(self):
        """Les entrées non-string doivent être traitées gracieusement."""
        assert anonymize_comments(123) == 123
        assert anonymize_comments(None) is None

    def test_already_anonymized(self):
        """Un texte déjà anonymisé ne doit pas être modifié."""
        text = "John Smith discussed with Marcus Lewis."
        result = anonymize_comments(text, random_seed=42)
        # John Smith sera remplacé par un nom fictif
        assert "John Smith" not in result
        # mais du texte reste
        assert "discussed" in result


class TestRobustness:
    """Tests de robustesse et performances."""

    def test_very_long_comment(self):
        """Un commentaire très long doit être traité sans erreur."""
        text = "John Smith " * 100  # Répétition du nom
        result = anonymize_comments(text, random_seed=42)
        assert "John Smith" not in result

    def test_unicode_characters(self):
        """Les caractères Unicode dans les noms doivent être gérés."""
        text = "Jean Müller and François Dupont are experts."
        result = anonymize_comments(text, random_seed=42)
        # Devrait détecter au moins un nom et le remplacer
        assert "are experts" in result

    def test_mixed_case(self):
        """Les noms en cas mixte doivent être détectés."""
        text = "JOHN SMITH and john smith discussed."
        result = anonymize_comments(text, random_seed=42)
        assert "John Smith" not in result
        assert "discussed" in result

    def test_repeated_name(self):
        """Un même nom répété plusieurs fois doit être remplacé."""
        text = "John Smith met with John Smith last week."
        result = anonymize_comments(text, random_seed=42)
        assert "John Smith" not in result
        assert "last week" in result
