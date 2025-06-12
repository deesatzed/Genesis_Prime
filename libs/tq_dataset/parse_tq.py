"""
parse_tq.py  –  Convert the raw Thousand_Questions.txt into structured data.

Usage (from repo root):
    python -m libs.tq_dataset.parse_tq \
        --infile  libs/tq_dataset/Thousand_Questions.txt \
        --sql-out libs/tq_dataset/tq_questions.sql

Optional:
    --json-out libs/tq_dataset/tq_questions.json
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from datetime import timezone

# ────────────────────────────────────────────────────────────────────────────────
# Heuristic helpers – you can swap these for smarter NLP later
# ────────────────────────────────────────────────────────────────────────────────
_THEMES_LOOKUP = {
    "child": ["childhood", "raise", "parent", "kid"],
    "value": ["value", "belief", "principle", "purpose"],
    "relationship": ["friend", "partner", "family", "love"],
    "legacy": ["legacy", "remember", "impact"],
    "growth": ["grow", "mature", "change", "learn"],
    "mind": ["mindful", "present", "aware", "reflection"],
}


def extract_themes(text: str, category: str) -> List[str]:
    text_low = text.lower()
    hits = {cat for cat, kws in _THEMES_LOOKUP.items() if any(k in text_low for k in kws)}
    # Always include the raw category as a theme anchor
    hits.add(category)
    return sorted(hits)


def estimate_complexity(text: str) -> int:
    # Complexity on 1–5: a naive proxy based on length & punctuation
    tokens = text.split()
    length_score = min(len(tokens) // 8 + 1, 5)
    qmarks = text.count("?")
    comma_bonus = text.count(",") // 2
    return min(length_score + qmarks + comma_bonus, 5)


def identify_knowledge_dependencies(text: str, category: str) -> List[str]:
    deps = []
    if "memory" in text.lower():
        deps.append("personal_memory")
    if "value" in text.lower():
        deps.append("core_values")
    if "relationship" in text.lower() or "friend" in text.lower():
        deps.append("relationships")
    if category in {"wisdom", "mindfulness"}:
        deps.append("introspection")
    return deps


def identify_personality_dimensions(text: str) -> List[str]:
    dims = []
    text_low = text.lower()
    if any(w in text_low for w in ("imagine", "creative", "dream")):
        dims.append("openness")
    if any(w in text_low for w in ("plan", "organize", "goal")):
        dims.append("conscientiousness")
    if any(w in text_low for w in ("friend", "party", "social")):
        dims.append("extraversion")
    if any(w in text_low for w in ("feel", "care", "empath")):
        dims.append("agreeableness")
    if any(w in text_low for w in ("worry", "fear", "anxious")):
        dims.append("neuroticism")
    return dims


# After all questions are loaded, we’ll relate similar ones by Levenshtein on stem;
# for speed we keep a simple substring relation here.
def establish_question_relationships(questions: List[Dict]) -> List[Dict]:
    for q in questions:
        rel = [
            other["id"]
            for other in questions
            if other["id"] != q["id"]
            and q["category"] == other["category"]
            and any(tok in other["text"].lower() for tok in q["text"].lower().split()[:2])
        ][:4]  # cap at 4 related items
        q["related_questions"] = rel
    return questions


# ────────────────────────────────────────────────────────────────────────────────
# Core parser
# ────────────────────────────────────────────────────────────────────────────────
def parse_raw_file(path: Path) -> List[Dict]:
    questions: List[Dict] = []
    current_cat = "uncategorized"

    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue  # skip blank lines

            # Category lines have no leading whitespace and often have '&' or capitalised words
            if re.match(r"^[^ \t].+", line):
                current_cat = (
                    line.strip().lower()
                    .replace(" & ", "_")
                    .replace(" ", "_")
                    .replace("&", "_")
                )
                continue

            # Question lines (indent with spaces or bullet)
            question_text = line.lstrip(" -\t").rstrip()
            q_id = f"q_{len(questions):04d}"

            question = {
                "id": q_id,
                "text": question_text,
                "category": current_cat,
                "themes": extract_themes(question_text, current_cat),
                "complexity": estimate_complexity(question_text),
                "related_questions": [],  # filled later
                "knowledge_dependencies": identify_knowledge_dependencies(
                    question_text, current_cat
                ),
                "personality_dimensions": identify_personality_dimensions(question_text),
            }
            questions.append(question)

    questions = establish_question_relationships(questions)
    return questions


# ────────────────────────────────────────────────────────────────────────────────
# Output helpers
# ────────────────────────────────────────────────────────────────────────────────
def dump_sql(questions: List[Dict], outfile: Path):
    """Write INSERT statements for tq_questions into outfile."""
    header = textwrap.dedent(
        f"""\
        -- Auto-generated from Thousand_Questions.txt
        -- Generated at {datetime.now(timezone.utc).isoformat()}
        BEGIN;
        """
    )

    rows: list[str] = []
    for q in questions:
        # Postgres wants ARRAY[...] literal without extra quotes        
        themes_literal = (
            "ARRAY[]::text[]" if not q["themes"] else "ARRAY" + str(q["themes"])
        )
        related_literal = (
            "ARRAY[]::text[]" if not q["related_questions"] else "ARRAY" + str(q["related_questions"])
        )
        # Use $$...$$ to avoid escaping quotes inside the question text
        rows.append(
            "INSERT INTO tq_questions "
            "(id, text, category, themes, complexity, related_ids) VALUES "
            f"('{q['id']}', $$ {q['text']} $$, '{q['category']}', "
            f"{themes_literal}, {q['complexity']}, {related_literal}) "
            "ON CONFLICT (id) DO NOTHING;"
        )

    footer = "\nCOMMIT;\n"
    outfile.write_text(header + "\n".join(rows) + footer, encoding="utf-8")

def get_question_statistics(questions: List[Dict]) -> Dict:
    """Get statistics about the question set"""
    categories = {}
    themes = {}
    complexities = {}
    
    for q in questions:
        # Category stats
        cat = q['category']
        categories[cat] = categories.get(cat, 0) + 1
        
        # Theme stats
        for theme in q['themes']:
            themes[theme] = themes.get(theme, 0) + 1
            
        # Complexity stats
        comp = q['complexity']
        complexities[comp] = complexities.get(comp, 0) + 1
    
    return {
        'total_questions': len(questions),
        'categories': dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)),
        'themes': dict(sorted(themes.items(), key=lambda x: x[1], reverse=True)),
        'complexities': dict(sorted(complexities.items()))
    }

# ────────────────────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Parse Thousand Questions dataset.")
    parser.add_argument("--infile", required=True, type=Path, help="Raw txt file")
    parser.add_argument("--sql-out", type=Path, help="Write INSERTs to .sql")
    parser.add_argument("--json-out", type=Path, help="Write structured JSON")

    args = parser.parse_args()

    questions = parse_raw_file(args.infile)
    print(f"Parsed {len(questions)} questions across {len(set(q['category'] for q in questions))} categories.")

    if args.sql_out:
        dump_sql(questions, args.sql_out)
        print(f"SQL written → {args.sql_out}")

    if args.json_out:
        args.json_out.write_text(json.dumps(questions, indent=2), encoding="utf-8")
        print(f"JSON written → {args.json_out}")


if __name__ == "__main__":
    main()
