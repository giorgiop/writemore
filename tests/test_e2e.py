import os

from langchain.llms.fake import FakeListLLM

from writemore.writemore import Writer

os.environ["OPENAI_API_KEY"] = ""

responses = ["Something something"]
llm = FakeListLLM(responses=responses)

prompt = "test"
writer = Writer(prompt, output_path="", llm=llm, verbose=False)
