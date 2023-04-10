import getpass
import os

import click
from dotenv import load_dotenv

from writemore.writemore import writemore

# Load default environment variables (.env)
load_dotenv()


@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
def main(verbose: bool):
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass(
            prompt="Enter your OpenAI API key: "
        )
    if not os.environ.get("OBJECTIVE"):
        os.environ["OBJECTIVE"] = getpass.getpass(
            prompt="Describe your objective for the AI: "
        )
    if not os.environ.get("TASK"):
        os.environ["TASK"] = getpass.getpass(
            prompt="Describe the first task to be executed towards the objective: "
        )
    objective, task = os.environ.get("OBJECTIVE"), os.environ.get("TASK")

    print(f"Executing a plan for this objective: {objective}")
    writemore(objective, task, verbose)


if __name__ == "__main__":
    main()
