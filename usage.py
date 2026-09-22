# My professor(s) provided this. Thanks Dr. Bean and Dr. Jones!
# They probably used AI to write it though, so don't give them
# too much thanks ;)

# Pricing per 1M tokens (USD) for recent OpenAI models, fetched March 6, 2026 from https://developers.openai.com/api/docs/pricing.
import sys
import json

PRICING = None

with open('pricing.json') as f:
    try:
        PRICING = json.load(f)
    except Exception as e:
        print("JSON ERR:")
        print(e)
        exit(1)

print(PRICING.get('gpt-5.6-luna'))

def _calculate_cost_usd(model, usage) -> float:
    rates = PRICING.get(model)
    if not rates:
        return 0.0
    input_cost = usage['input'] * rates['input']
    cached_cost = usage['cached'] * rates.get('cached', rates['input'])
    output_cost = usage['output'] * rates['output']
    # Prices are per 1M tokens.
    return (input_cost + cached_cost + output_cost) / 1_000_000


def _aggregate_usage(usages):
    total = {'input': 0, 'cached': 0, 'output': 0, 'reasoning': 0}
    for usage in usages:
        total['input'] += usage.input_tokens
        total['cached'] += usage.input_tokens_details.cached_tokens
        total['output'] += usage.output_tokens
        total['reasoning'] += usage.output_tokens_details.reasoning_tokens
    return total


def print_usage(model, usage, file=sys.stderr):
    print(' Usage '.center(30, '-'), file=file)
    print('Model:', model, file=file)

    if not isinstance(usage, list):
        usage = [usage]
    total = _aggregate_usage(usage)

    for key, value in total.items():
        print(f'{key.title()} (tokens):', value, file=file)

    cost = _calculate_cost_usd(model, total)
    if cost is not None:
        print(f'Total cost (USD): ${cost:.6f}', file=file)
    else:
        print('Total cost: n/a (pricing unavailable for model)', file=file)


def format_usage_markdown(model, usage) -> str:
    if not isinstance(usage, list):
        usage = [usage]
    total_usage = _aggregate_usage(usage)
    cost = _calculate_cost_usd(model, total_usage)
    token_table = '\n'.join(
        f"| {key.title()} | {value} |"
        for key, value in total_usage.items()
    )

    out = (
        "# Usage\n\n"
        f"**Model**: `{model}`\n\n"
        "|    | Tokens |\n"
        "|----|--------|\n"
        + token_table +
        f"\n\n**Total cost**: ${cost:.6f}\n"
    )
    print(out)
    return out
