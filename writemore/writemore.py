from collections import deque

from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser

from writemore.templates import (
    CREATE_NEW_TASKS_TEMPLATE,
    EXECUTION_TEMPLATE,
    RESCHEDULE_TEMPLATE,
)


class Executor:
    def __init__(self, objective, memory, llm, verbose=False):
        self.objective = objective
        # self.memory = memory
        self.llm = llm
        self.verbose = verbose

    def run(self, task):
        """Call LLM to execute the task"""

        # context = context_agent(query=objective, n=5)

        prompt = PromptTemplate(
            template=EXECUTION_TEMPLATE,
            input_variables=["objective", "task"],
        )
        self.chain = LLMChain(prompt=prompt, llm=self.llm, verbose=self.verbose)
        response = self.chain.run(objective=self.objective, task=task)
        return response


class Scheduler:
    def __init__(self, objective, first_task, memory, llm, verbose=False):
        self.objective = objective
        self.memory = memory
        self.llm = llm
        self.task_list = deque([first_task])
        self.output_parser = CommaSeparatedListOutputParser()
        self.verbose = verbose

    def next_task(self):
        return self.task_list.popleft()

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
        self.chain = LLMChain(prompt=prompt, llm=self.llm, verbose=self.verbose)
        response = self.chain.run(
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

        prompt = PromptTemplate(
            template=RESCHEDULE_TEMPLATE,
            input_variables=["objective", "task_list"],
        )
        self.chain = LLMChain(prompt=prompt, llm=self.llm, verbose=self.verbose)
        response = self.chain.run(
            objective=self.objective,
            task_list={", ".join([str(t) for t in self.task_list])},
        )

        self.task_list = deque()
        new_tasks = self.output_parser.parse(response)
        self.task_list.extend(new_tasks)
        return self.task_list


# class Memory():

#     def __init__(self, objective):
#         self.objective = objective

#     def fetch_context(self, n):
#         context = context_agent(query=self.objective, n=n)


def writemore(objective, task, verbose: bool = False):
    llm = ChatOpenAI(temperature=0, max_tokens=500, verbose=verbose)
    # memory = Memory()
    memory = []
    scheduler = Scheduler(objective, task, memory, llm)
    executor = Executor(objective, memory, llm)

    iter, max_iter = 0, 5
    while scheduler.task_list or iter >= max_iter:
        print(f"\n****Iter {iter}. Current task list****")
        for t in scheduler.task_list:
            print(str(t))

        task = scheduler.next_task()
        print("\n****Next task****\n")
        print(task)
        result = executor.run(task)
        # memory.append(result)
        print("\n****Task result****\n")
        print(result)

        new_tasks = scheduler.create_new_tasks()

        if new_tasks:
            scheduler.add(new_tasks)
            scheduler.reschedule()

        iter += 1
