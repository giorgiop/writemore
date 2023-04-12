from collections import deque

from langchain import LLMChain, PromptTemplate
from langchain.chains.base import Chain
from langchain.llms import BaseLLM
from langchain.output_parsers import CommaSeparatedListOutputParser
from pydantic import BaseModel, Field

from writemore.templates import (
    CREATE_NEW_TASKS_TEMPLATE,
    EXECUTION_TEMPLATE,
    RESCHEDULE_TASKS_TEMPLATE,
)


class TaskCreator(LLMChain):
    """Chain to create tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        prompt = PromptTemplate(
            template=CREATE_NEW_TASKS_TEMPLATE,
            input_variables=[
                "objective",
                "result",
                "task_description",
                "task_list",
                "n_tasks",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class TaskRescheduler(LLMChain):
    """Chain to reschedule tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        prompt = PromptTemplate(
            template=RESCHEDULE_TASKS_TEMPLATE,
            input_variables=["objective", "task_list"],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class Executor(LLMChain):
    """Chain to execute tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        prompt = PromptTemplate(
            template=EXECUTION_TEMPLATE,
            input_variables=["objective", "task"],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class Scheduler(Chain, BaseModel):
    objective: str = Field(...)
    first_task: str = Field(...)
    task_creator: TaskCreator = Field(...)
    task_rescheduler: TaskRescheduler = Field(...)
    output_parser: CommaSeparatedListOutputParser = Field(
        default_factory=CommaSeparatedListOutputParser
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.task_list = deque([self.first_task])

    def next_task(self):
        return self.task_list.popleft()

    def add(self, task):
        self.task_list.append(task)

    def create_new_tasks(self):
        """Check task_list. Call LLM to decide if new tasks must be added"""

        response = self.task_creator.run(
            objective=self.objective,
            result="None",
            task_description="None",
            task_list={", ".join([str(t) for t in self.task_list])},
            n_tasks=5,
        )
        new_tasks = self.output_parser.parse(response)
        self.task_list.extend(new_tasks)
        return self.task_list

    def reschedule(self):
        """Check task_list. Call LLM to decide if task priority is ok"""

        response = self.task_rescheduler.run(
            objective=self.objective,
            task_list={", ".join([str(t) for t in self.task_list])},
        )

        self.task_list = deque()
        new_tasks = self.output_parser.parse(response)
        self.task_list.extend(new_tasks)
        return self.task_list

    @classmethod
    def from_llm(
        cls,
        objective: str,
        first_task: str,
        llm: BaseLLM,
        verbose: bool = False,
        **kwargs,
    ) -> "Scheduler":
        return cls(
            objective=objective,
            first_task=first_task,
            task_creator=TaskCreator.from_llm(llm, verbose=verbose),
            task_rescheduler=TaskRescheduler.from_llm(llm, verbose=verbose),
            **kwargs,
        )
