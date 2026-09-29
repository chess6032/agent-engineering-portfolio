# Pricing per 1M tokens (USD) for current OpenAI models, including audio-capable models,
# from the official OpenAI pricing page.
import logging
import sys
import json

from openai.types.responses import ResponseUsage

logger = logging.getLogger(__name__)

PRICING = None

with open('pricing.json') as f:
    try:
        PRICING = json.load(f)
    except Exception as e:
        print("JSON ERR:")
        print(e)
        exit(1)

def _calculate_cost_usd(totals: dict[str, dict]) -> float:
    total = 0
    for model, usage in totals.items():
        rates = PRICING.get(model)
        if not rates:
            logger.warning('No pricing rates configured for model %s', model)
            continue

        audio_input = usage.get('audio_input', 0)
        audio_output = usage.get('audio_output', 0)
        text_input = max(usage['input'] - usage['cached'] - audio_input, 0)
        cached_input = usage['cached']
        text_output = max(usage['output'] - audio_output, 0)

        total += text_input * rates.get('input', 0.0)
        total += cached_input * rates.get('cached', rates.get('input', 0.0))
        total += text_output * rates.get('output', 0.0)
        total += audio_input * rates.get('audio_input', 0.0)
        total += audio_output * rates.get('audio_output', 0.0)
    # Prices are per 1M tokens.
    return total / 1_000_000


def _aggregate_usage(usages: list[tuple[str, ResponseUsage]]):
    total = {}
    for model, usage in usages:
        if model not in total:
            total[model] = {
                'input': 0,
                'cached': 0,
                'output': 0,
                'reasoning': 0,
                'audio_input': 0,
                'audio_output': 0,
            }
        total[model]['input'] += usage.input_tokens
        if hasattr(usage, 'input_tokens_details'):
            total[model]['cached'] += usage.input_tokens_details.cached_tokens
        if hasattr(usage, 'input_token_details'):
            total[model]['audio_input'] += getattr(usage.input_token_details, 'audio_tokens', 0)
        total[model]['output'] += usage.output_tokens
        if hasattr(usage, 'output_tokens_details'):
            total[model]['reasoning'] += usage.output_tokens_details.reasoning_tokens
        if hasattr(usage, 'output_token_details'):
            total[model]['audio_output'] += getattr(usage.output_token_details, 'audio_tokens', 0)
    return total


def print_usage(usages: list[tuple[str, ResponseUsage]], file=sys.stderr):
    print(' Usage '.center(30, '-'), file=file)
    totals = _aggregate_usage(usages)
    for model, total in totals.items():
        print(model.center(30, '~'), file=file)
        for key, value in total.items():
            if value:
                print(f'{key.title()} (tokens):', value, file=file)
        cost = _calculate_cost_usd({model: total})
        print(f'{model} cost (USD): ${cost:.6f}', file=file)

    cost = _calculate_cost_usd(totals)
    print('~'*30, file=file)
    print(f'Total cost (USD): ${cost:.6f}', file=file)


def format_usage_markdown(model: str, usages: list[ResponseUsage]) -> str:
    """Format single-model usage as Markdown for lecture UIs."""
    if not isinstance(usages, list):
        usages = [usages]
    totals = _aggregate_usage([(model, usage) for usage in usages])
    total = totals.get(model, {
        'input': 0,
        'cached': 0,
        'output': 0,
        'reasoning': 0,
        'audio_input': 0,
        'audio_output': 0,
    })
    cost = _calculate_cost_usd({model: total})
    token_table = '\n'.join(
        f"| {key.title()} | {value} |"
        for key, value in total.items()
        if value
    )
    return (
        "# Usage\n\n"
        f"**Model**: `{model}`\n\n"
        "|    | Tokens |\n"
        "|----|--------|\n"
        f"{token_table}\n\n"
        f"**Total cost**: ${cost:.6f}\n"
    )
