"""
sampler.py  – pick a balanced subset of Thousand-Questions
"""

import random
import psycopg
from typing import List, Dict

# tweak weights if you want to emphasise certain categories
MIN_PER_CATEGORY = 1

def sample_questions(user_id: str, n: int) -> List[Dict]:
    """
    Return `n` distinct tq_questions rows, stratified so we get
    at least MIN_PER_CATEGORY from as many categories as possible.
    """
    conn = psycopg.connect("postgresql://postgres:pass@localhost:5432/sentient", autocommit=True)
    cur = conn.cursor(row_factory=psycopg.rows.dict_row)

    # grab all questions & group by category
    cur.execute("SELECT id, text, category FROM tq_questions;")
    rows = cur.fetchall()
    by_cat: Dict[str, list] = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)

    # step 1 – guarantee diversity
    sample: list = []
    for cat_rows in by_cat.values():
        if len(sample) >= n:
            break
        pick = random.choice(cat_rows)
        sample.append(pick)
        cat_rows.remove(pick)

    # step 2 – fill remaining slots at random
    remaining_pool = [r for cat_rows in by_cat.values() for r in cat_rows]
    sample.extend(random.sample(remaining_pool, k=n - len(sample)))

    random.shuffle(sample)
    conn.close()
    return sample
