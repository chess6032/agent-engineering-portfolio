import json
from pathlib import Path

def _dump(item):
    """Normalize a plain dict or Pydantic object into a JSON-safe dict."""
    if isinstance(item, dict):
        return item
    return item.model_dump(mode='json', exclude_none=True)

def model_dump_history(history: list) -> list[dict]:
    return [_dump(item) for item in history]


def model_dump_usage(usage: list) -> dict:
    requests = [{'model': model, **_dump(u)} for model, u in usage]
    totals = {
        key: sum(getattr(u, key) for _, u in usage)
        for key in ('input_tokens', 'output_tokens', 'total_tokens')
    }
    return {'requests': requests, 'totals': totals}


def output_to_json(history: list, usage: list, out_path: Path) -> None:
    data = {
        'history': model_dump_history(history),
        'usage': model_dump_usage(usage),
    }

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
