"""
builder.py – very first-pass personality profiler

Given a user_id, fetch their answered sample questions from
`tq_answers` and derive a naive Big-Five trait vector (0-1 floats).

You can improve the heuristics later; this gets Option 1 moving.
"""

from __future__ import annotations

import math
import re
from typing import Dict, Any

import psycopg
from psycopg.rows import dict_row

BIG_FIVE = [
    "openness",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "neuroticism",
]


def _count_keywords(text: str, keywords: list[str]) -> int:
    return sum(1 for kw in keywords if kw in text.lower())


def _normalise(value: float, max_val: float = 5.0) -> float:
    return round(min(value / max_val, 1.0), 2)


def extract_traits(user_id: str) -> Dict[str, Any]:
    """
    VERY SIMPLE heuristic:
      • looks at user answers already in tq_answers (is_user_answer = true)
      • counts thematic keywords to map into Big-Five 0-1 range
    """

    conn = psycopg.connect(
        "postgresql://postgres:pass@localhost:5432/sentient",
        row_factory=dict_row,
    )
    cur = conn.cursor()
    cur.execute(
        """
        SELECT answer_text
        FROM tq_answers
        WHERE user_id = %s
          AND is_user_answer = true
        """,
        (user_id,),
    )
    answers = [row["answer_text"] or "" for row in cur.fetchall()]
    conn.close()

    if not answers:  # safeguard
        return {trait: 0.5 for trait in BIG_FIVE}

    joined = " ".join(answers)

    score = {
        # incredibly naive word buckets:
        "openness": _count_keywords(joined, ["imagine", "dream", "create", "explore"]),
        "conscientiousness": _count_keywords(
            joined, ["plan", "organize", "schedule", "goal"]
        ),
        "extraversion": _count_keywords(joined, ["friend", "party", "social", "talk"]),
        "agreeableness": _count_keywords(joined, ["kind", "help", "care", "empathy"]),
        "neuroticism": _count_keywords(joined, ["worry", "anxious", "nervous", "fear"]),
    }

    # map raw counts to 0-1
    traits = {k: _normalise(v) for k, v in score.items()}
    traits["sample_size"] = len(answers)
    return traits
