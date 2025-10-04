"""Optional LLM helper: tries to use transformers if installed, otherwise falls back to heuristics."""
from typing import Dict, Any


def analyze_brief_with_llm(text: str) -> Dict[str, Any]:
    """Return a dict with 'entities' and 'actions'.

    If transformers is installed, use a small prompt to extract entities/actions.
    Otherwise return an empty dict so caller falls back to heuristics.
    """
    try:
        from transformers import pipeline
    except Exception:
        return {}

    prompt = (
        "Extract JSON with two keys: entities (list of {name,fields}) and actions (list of strings).\n"
        "Example: {\"entities\": [{\"name\": \"Expense\", \"fields\": [\"date\", \"amount\"]}], \"actions\": [\"upload\", \"categorize\"]}\n\n"
        f"Brief: {text}\n\nRespond with only the JSON."
    )
    try:
        generator = pipeline('text-generation', model='gpt2')
        out = generator(prompt, max_length=256, num_return_sequences=1)
        txt = out[0]['generated_text']
        # try to find the first JSON object in the response
        import re, json
        m = re.search(r"\{.*\}", txt, re.DOTALL)
        if m:
            payload = json.loads(m.group(0))
            return payload
    except Exception:
        return {}
    return {}
