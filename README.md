# writemore

A library of customizable autonomous agents for common jobs.

## Installation

`writemore` is a command line application written in Python.
*The following commands should be executed in a CMD, Bash or Powershell window. 

To do this in Microsoft Windows, go to a folder on your computer, click in the folder path at the top and type CMD, then press enter.*

Install Python 3.10 or later from [python.org](https://www.python.org/downloads/) if not already installed, then install the `writemore` library using `pip`:

```bash
pip install writemore
```

## Usage

The library requires the `OPENAI_API_KEY` environment variable to be set. An api key can be obtained from
the [OpenAI dashboard](https://platform.openai.com/account/api-keys).

To set an environment variable in Windows, run the following command in a CMD or Powershell window:

```
setx OPENAI_API_KEY "your_api_key_here"
```

Replace `your_api_key_here` with your actual API key from the OpenAI dashboard!

For macOS or Linux users, you can set the environment variable in the terminal by running:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

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

- [ ] Add memory, expose at least one local and one third party API
- [ ] Expose all LangChain LLM models available
- [ ] Add at least 5 template examples
- [ ] Interactive mode
- [ ] Localhost web-ui
- [ ] Privacy-preserving on-premise workflow (not third party APIs)
