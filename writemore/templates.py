CREATE_NEW_TASKS_TEMPLATE = """
    You must create new tasks with the following objective: {objective},
    The last completed task has this result: {result}
    The last completed task was based on this description: {task_description}.
    These are incomplete tasks: {task_list}.
    Based on the result, return in a comma separated list of no
    more than {n_tasks} tasks to be completed.
    They must not overlap with incomplete tasks.
    """

RESCHEDULE_TEMPLATE = """
    You are tasked with prioritizing the following tasks: {task_list}.
    Consider the ultimate objective of these tasks: {objective}.
    Reorder in a comma separated list these tasks, in order of priority.
    Clean formatting of the text. Do not remove any task.
    """

EXECUTION_TEMPLATE = """
    You must perform one task based on the following objective: {objective}\n.
    Take into account these previously completed tasks: NOTHING\n.
    Your task: {task}\nResponse:"""
