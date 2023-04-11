# writemore

A library of customizable autonomous agents for common jobs.

## Installation

Make sure you have all the **requirements** above, if not, install/get them.

*The following commands should be executed in a CMD, Bash or Powershell window. To do this, go to a folder on your computer, click in the folder path at the top and type CMD, then press enter.*

Clone the repository and install the requirements (we recommend using a Python virtual environment):

```bash
pip install writemore
```

The library requires the `OPENAI_API_KEY` environment variable to be set with an api key obtained from
the [OpenAI dashboard](https://platform.openai.com/account/api-keys).


## Usage

Run the command line application python script in your terminal:
*(Type this into your CMD window)*

```bash
python -m writemore.cli
```

## Contributing

writemore uses `pre-commit` to run code checks and tests before every commit. To install the pre-commit hooks, run the following commands:

```bash
poetry install --with dev
pre-commit install
```

Or run all the checks manually against all files:

```bash
poetry run pre-commit run --all-files
```

## Development Roadmap

ToDos

- [ ] Add memory, expose at least one local and one thirt party API
- [ ] Expose all LangChain LLM models available
- [ ] Add at least 5 template examples
- [ ] Interactive mode
- [ ] Localhost web-ui
- [ ] Privacy-preserving on-premise workflow (not third party APIs)
