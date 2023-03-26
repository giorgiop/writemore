import logging
from pathlib import Path

from langchain.chat_models import ChatOpenAI
from langchain.llms.base import LLM
from langchain import LLMChain, PromptTemplate
from langchain.schema import BaseLanguageModel

from templates import WRITEMORE_DESCRIPTION, CONTENT_ROADMAP_TEMPLATE, CONTENT_TEMPLATE

logger = logging.getLogger(__name__)


def load_content_roadmap_chain(llm: BaseLanguageModel, verbose: bool = False):
    """Loads the content roadmap chain."""
    prompt = PromptTemplate(
        template=CONTENT_ROADMAP_TEMPLATE,
        input_variables=["writemore_project"],
        partial_variables={"writemore_description": WRITEMORE_DESCRIPTION},
    )
    return LLMChain(prompt=prompt, llm=llm, verbose=verbose)


def load_content_chain(llm: BaseLanguageModel, verbose: bool = False):
    """Loads the content chain."""
    prompt = PromptTemplate(
        template=CONTENT_TEMPLATE,
        input_variables=["writemore_project", "content_roadmap", "content_element"],
        partial_variables={
            "writemore_description": WRITEMORE_DESCRIPTION,
        },
    )
    return LLMChain(prompt=prompt, llm=llm, verbose=verbose)


class Writer:
    """The Writer is in charge of writing new content"""

    def __init__(self, prompt: str, output_path: str,
                 llm: LLM, verbose: bool) -> None:
        """Constructor.
        Args:
            prompt: a description of the project topic or idea
            output_path: The output path for the generated project template.
        """
        self.prompt = prompt
        self.output_path = output_path
        self.verbose = verbose

        if not llm:
            self.llm = ChatOpenAI(temperature=0, max_tokens=2048)
        else:
            self.llm = llm

        self.content_roadmap_chain = load_content_roadmap_chain(
            self.llm, self.verbose
        )
        self.content_chain = load_content_chain(self.llm, self.verbose)

    def generate_content_roadmap(self) -> None:
        """Generates the content roadmap."""
        logger.info("Generating content roadmap...")
        self.roadmap_content_str = \
            self.content_roadmap_chain.predict(writemore_project=self.prompt)
        self.write_file("roadmap.txt", self.roadmap_content_str.strip())

    def generate_content_element(self, step: int) -> None:
        """Generates one element of content."""

        content_roadmap_str = self.read_file("roadmap.txt")
        file_name = f"content_{step}.txt"
        logger.info(f"Generating content: {file_name}...")
        content = self.content_chain.predict(
            writemore_project=self.prompt,
            content_roadmap=content_roadmap_str,
            content_element=step,
        )
        self.write_file(file_name, content)

    def read_file(self, file_name: str) -> str:
        """Read the file from the output path."""
        file_path = Path(self.output_path) / file_name
        return file_path.read_text()

    def write_file(self, file_name: str, file_content: str):
        """Writes the file to the output path."""
        file_path = Path(self.output_path) / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file_content)
