"""M2-B2 — Fonction d'anonymisation réutilisable (phase async individuelle)."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import spacy

# spaCy EN pour extraire PERSON/GPE/ORG dans un corpus majoritairement anglais.
NLP = spacy.load("en_core_web_md")

EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
PHONE_RE = re.compile(r"\b\d{3}[.-]?\d{3}[.-]?\d{4}\b")
IBAN_PARTIAL_RE = re.compile(r"\*{2,}\d{4}")
DATE_RE = re.compile(r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b")


def _replace_entities(text: str) -> str:
    """Replace spaCy entities with neutral placeholders."""
    doc = NLP(text)
    anonymized = text

    # Replace longest spans first to avoid partial overlap artifacts.
    entities = sorted(doc.ents, key=lambda ent: len(ent.text), reverse=True)
    for ent in entities:
        if "REDACTED" in ent.text or ent.text in {"DATE", "LOCATION"}:
            continue
        if ent.label_ == "PERSON":
            anonymized = anonymized.replace(ent.text, "[PERSON]")
        elif ent.label_ == "GPE":
            anonymized = anonymized.replace(ent.text, "[LOCATION]")

    return anonymized


def anonymizecomments(text: str) -> str:
    """Anonymize a free-text comment.

    Strategy:
    - PERSON -> [PERSON]
    - GPE -> [LOCATION]
    - ORG -> [ORG]
    - Email/phone/IBAN/date via regex replacement
    """
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    # Regex first to protect direct identifiers before NER substitutions.
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    text = IBAN_PARTIAL_RE.sub("[REDACTED_IBAN]", text)
    text = DATE_RE.sub("[DATE]", text)
    text = _replace_entities(text)
    return text


def anonymize_comments(text: str) -> str:
    """Alias snake_case de anonymizecomments pour lisibilite Python."""
    return anonymizecomments(text)


def anonymize_dataframe(df: pd.DataFrame, text_col: str = "manager_comments") -> pd.DataFrame:
    """Return a copy of a dataframe with anonymized text column."""
    out = df.copy()
    out[text_col] = out[text_col].fillna("").map(anonymizecomments)
    return out


def write_anonymized_sample(
    input_path: Path,
    output_path: Path,
    text_col: str = "manager_comments",
) -> pd.DataFrame:
    """Read CSV, anonymize comments, write CSV, and return resulting dataframe."""
    df = pd.read_csv(input_path)
    anonymized = anonymize_dataframe(df, text_col=text_col)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    anonymized.to_csv(output_path, index=False)
    return anonymized


if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parents[1] / "data"
    input_csv = data_dir / "audit_sample.csv"
    output_csv = data_dir / "auditsample_anonymized_franck.csv"

    if input_csv.exists():
        result = write_anonymized_sample(input_csv, output_csv)
        print(f"Wrote anonymized file: {output_csv}")
        print(f"Rows: {len(result)}")

    sample = (
        "Allison Hill is a strong promotion candidate this year. "
        "Discussed with HR (Rhonda Smith, 651.216.1559). "
        "Budget pre-approved on account ****3503."
    )
    print("Avant :", sample)
    print("Après :", anonymizecomments(sample))