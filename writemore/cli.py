from typing import Optional

import click
from pydantic import BaseSettings

from writemore.writemore import writemore


class WriteMoreCLISettings(BaseSettings):
    OPENAI_API_KEY: str

    OBJECTIVE: Optional[str]
    TASK: Optional[str] = "Come up with a plan"
    OPENAI_MODEL_NAME: Optional[str] = "gpt-3.5-turbo"


settings = WriteMoreCLISettings()


@click.command()
@click.option(
    "-o",
    "--objective",
    help="High level objective",
    prompt=True,
    default=lambda: settings.OBJECTIVE,
)
@click.option("-t", "--task", help="Task", prompt=True, default=lambda: settings.TASK)
@click.option("-m", "--model", help="Model", default=lambda: settings.OPENAI_MODEL_NAME)
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
def main(objective: str, task: str, model, verbose: bool):
    print(f"Executing a plan for this objective: {objective}")
    writemore(objective, task, model_name=model, verbose=verbose)


if __name__ == "__main__":
    main()
