CREATE_NEW_TASKS_TEMPLATE = """
    You must create at most {n_tasks} tasks with the following objective: {objective},
    The last completed task has was {task_description} with this result: {result}
    These are incomplete tasks: {task_list} and new tasks must not overlap.
    Return the tasks in a comma separated list, like: task1, task2, task3, ...
    """

RESCHEDULE_TEMPLATE = """
    You are tasked with prioritizing the following tasks: {task_list}.
    Consider the ultimate objective of these tasks: {objective}.
    Return the tasks in a comma separated list, like: task1, task2, task3, ...
    Clean formatting of the text. Do not remove any task.
    """

EXECUTION_TEMPLATE = """
    You must perform one task based on the following objective: {objective}\n.
    Take into account these previously completed tasks: NOTHING\n.
    Your task: {task}\nResponse:"""
