import argparse
import sys
from pathlib import Path
from time import time
import json

from openai import OpenAI

from usage import print_usage
from dumper import output_to_json

def get_user_input() -> str:
    print('USER: ', end='')
    text = ''
    while (line := input()):
        text += line
    return text

def div(div_type: str) -> str:
    if div_type == 'user':
        return '. . . \n'
    elif div_type == 'agent':
        return '\n-----------\n'
    else: raise ValueError()

def print_div(div_type: str) -> None:
    d = div(div_type)
    print(d, end='')

def main(model: str, reasoning: str, prompt: str) -> tuple[list, list]:
    client = OpenAI()
    usage = []
    history = [{'role': 'system', 'content': prompt}]
    
    try:
        while True:
            user_msg = get_user_input()
            print_div('user')
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
            print_div('agent')
    except KeyboardInterrupt:
        # catch keyboard interrupts so the history still gets returned (and thus printed)
        pass
    finally:
        print_usage(usage)

    return history, usage

# Launch app
if __name__ == "__main__":
    parser = argparse.ArgumentParser('AI Response')
    parser.add_argument('--prompt_file', type=Path, default="prompts/default.md")
    parser.add_argument('--model', default='gpt-5.6-luna')
    parser.add_argument('--reasoning', default='none')
    parser.add_argument('--out', default=None)

    args = parser.parse_args()
    history, usage = main(args.model, args.reasoning, args.prompt_file.read_text())
    if args.out:
        output_to_json(history, usage, args.out)