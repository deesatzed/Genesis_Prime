# Prompt-Pack v2.0

## Rationale
Version 1 prompts returned plain text; we now require richer coordination and quantitative metrics. Prompt-Pack v2 introduces:

1. JSON envelope (message schema).
2. Mandatory `valence_tag` & `confidence` for affective + epistemic tracking.
3. ≥250-token responses to promote richer emergent behaviour.
4. Self-repair hook (`"self_patch"`).

## Message Schema
```jsonc
{
  "sender": "<agent_id>",
  "recipient": "<target_id>" | null,
  "broadcast": "*" | null,
  "timestamp": "ISO-8601",
  "valence_tag": -1.0 … +1.0,
  "content": "<rich text>",
  "confidence": 0.0 … 1.0,
  "kpi_anchor": "phi_s" | "phi_c" | null,
  "self_patch": { /* optional */ }
}
```

## Template Changes
```jinja2
{% raw %}
## RESPONSE GUIDELINES
1. Reply **only** with a JSON object following the schema above.
2. Write at least 3 paragraphs (~250 tokens).
3. Choose `valence_tag` to reflect emotional weight; choose `confidence` to reflect certainty.
4. If recommending a code or parameter change, include `self_patch`.
{% endraw %}
```

## Hot-Reload Workflow
* Set `PROMPT_VERSION=2` in `.env`.
* Backend will reload template on next agent action.
