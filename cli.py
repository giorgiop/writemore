import os
import logging
import getpass
from dotenv import load_dotenv

# Load default environment variables (.env)
load_dotenv()

import click

from writemore.writemore import Writer

logger = logging.getLogger(__name__)


@click.command()
@click.option("-p", "--prompt", required=True, help="Your content description.")
@click.option(
    "-o",
    "--output-path",
    "output_path",
    required=True,
    help="The output path for the generated content.",
)
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
def main(prompt: str, output_path: str, verbose: bool):
    """writemore
    Generates new content following the `prompt` instructions.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass(
            prompt="Enter your OpenAI API key: "
        )

    logger.info(f"Generating content for '{prompt}' at '{output_path}'")

    generator = Writer(
        prompt=prompt, llm=None, output_path=output_path, verbose=verbose
    )
    generator.generate_content_roadmap()

    logger.info(f"You new content is available at {output_path}!")

if __name__ == "__main__":
    main()
