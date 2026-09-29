import argparse
import sys
from pathlib import Path
from time import time
import json

from openai import OpenAI

from usage import print_usage

def main(model: str, reasoning: str, prompt: str) -> tuple[list, list]:
    client = OpenAI()
    usage = []
    history = [{'role': 'system', 'content': prompt}]
    
    try:
        while True:
            user_msg = input('USER: ')
            if not user_msg:
                break
            history.append({'role': 'user', 'content': user_msg})
            
            start = time()
            response = client.responses.create(
                model=model,
                input=history,
                reasoning={'effort': reasoning}
            )
            print(response.output_text)
            usage.append((model, response.usage))
            history.extend(response.output)
        
            print(f'{round(time()-start, 2)} seconds elapsed', file=sys.stderr)
    except KeyboardInterrupt:
        # catch keyboard interrupts so the history still gets returned (and thus printed)
        pass
    finally:
        print_usage(usage)

    return history, usage

def output_convo_to_json(history: list, out_path: Path) -> None:
    def to_dict(item):
        if isinstance(item, dict):
            return item
        # Pydantic model from response.output (messages, reasoning items, tool calls, etc.)
        return item.model_dump(mode='json', exclude_none=True)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w', encoding='utf-8') as f:
        json.dump([to_dict(item) for item in history], f, indent=2, ensure_ascii=False)


# Launch app
if __name__ == "__main__":
    parser = argparse.ArgumentParser('AI Response')
    parser.add_argument('--prompt_file', type=Path, default="prompts/default.md")
    parser.add_argument('--model', default='gpt-5.6-luna')
    parser.add_argument('--reasoning', default='none')
    parser.add_argument('--out', default=None)

    args = parser.parse_args()
    history = main(args.model, args.reasoning, args.prompt_file.read_text())
    if args.out:
        output_convo_to_json(history, args.out)