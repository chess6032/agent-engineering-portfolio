# Agent Engineering

This is a portfolio of all the agent engineering stuff I worked on CS 301R, taught by Gordon Bean and Mike Jones at BYU (Fall 2026 semester).

## OpenAI Key

I'm using an OpenAI key provided by my professor (it's like for students or smth idk).

The `openai` library reads its api key from an `OPENAI_API_KEY` environment variable. If you've saved said API key in a .env file (e.g., `openai.env`), you can load it into your current shell like this.

```sh
set -a
source openai.env
set +a
```

- `$ set -a` sets the terminal to export every env var created hereonout.
- `$ source openai.env` executes `openai.env` as a script.
- `$ set +a` disables `set -a`.

You can check if that worked with `$ echo OPENAI_API_KEY`.
