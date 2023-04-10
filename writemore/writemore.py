from collections import deque

from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser

from writemore.templates import (
    CREATE_NEW_TASKS_TEMPLATE,
    EXECUTION_TEMPLATE,
    RESCHEDULE_TEMPLATE,
)

VERBOSE = False


class Executor:
    def __init__(self, objective, memory, llm):
        self.objective = objective
        # self.memory = memory
        self.llm = llm

    def run(self, task):
        """Call LLM to execute the task"""

        # context = context_agent(query=objective, n=5)

        prompt = PromptTemplate(
            template=EXECUTION_TEMPLATE,
            input_variables=["objective", "task"],
        )
        self.chain = LLMChain(prompt=prompt, llm=self.llm, verbose=VERBOSE)
        response = self.chain.run(objective=self.objective, task=task)
        print(response)
        return response


class Scheduler:
    def __init__(self, objective, first_task, memory, llm):
        self.objective = objective
        # self.memory = memory
        self.llm = llm
        self.task_list = deque([first_task])
        self.output_parser = CommaSeparatedListOutputParser()

    def next_task(self):
        self.task_list.popleft()

    def add(self, task):
        self.task_list.append(task)

    def create_new_tasks(self):
        """Check task_list. Call LLM to decide if new tasks must be added"""

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
        self.chain = LLMChain(prompt=prompt, llm=self.llm, verbose=VERBOSE)
        response = self.chain.run(
            objective=self.objective,
            result="None",
            task_description="None",
            task_list={", ".join([str(t) for t in self.task_list])},
            n_tasks=5,
        )
        print(response)
        new_tasks = self.output_parser.parse(response)
        self.task_list.extend(new_tasks)
        return self.task_list

    def reschedule(self):
        """Check task_list. Call LLM to decide if task priority is ok"""

        prompt = PromptTemplate(
            template=RESCHEDULE_TEMPLATE,
            input_variables=["objective", "task_list"],
        )
        self.chain = LLMChain(prompt=prompt, llm=self.llm, verbose=VERBOSE)
        response = self.chain.run(
            objective=self.objective,
            task_list={", ".join([str(t) for t in self.task_list])},
        )

        print(response)
        self.task_list = deque()
        new_tasks = self.output_parser.parse(response)
        self.task_list.extend(new_tasks)
        return self.task_list


# class Memory():

#     def __init__(self, objective):
#         self.objective = objective

#     def fetch_context(self, n):
#         context = context_agent(query=self.objective, n=n)


def writemore(objective, task, verbose):
    if verbose:
        pass

    llm = ChatOpenAI(temperature=0, max_tokens=500)
    # memory = Memory()
    memory = []
    scheduler = Scheduler(objective, task, memory, llm)
    executor = Executor(objective, memory, llm)

    iter, max_iter = 0, 5
    while scheduler.task_list or iter >= max_iter:
        print(f"Iter {iter}. \nCurrent task list: {scheduler.task_list}")

        task = scheduler.next_task()
        result = executor.run(task)
        memory.append(result)
        print(f"Task: {task} \nResult: {result}")

        new_tasks = scheduler.create_new_tasks()

        if new_tasks:
            scheduler.add(new_tasks)
            scheduler.reschedule()

        iter += 1
