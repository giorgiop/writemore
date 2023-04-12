from langchain.chat_models import ChatOpenAI

from writemore.chains import Executor, Scheduler


def writemore(objective, first_task, verbose):
    """Run writemore."""
    llm = ChatOpenAI(temperature=0, max_tokens=500, verbose=verbose)

    scheduler = Scheduler.from_llm(objective, first_task, llm, verbose=verbose)
    executor = Executor.from_llm(llm, verbose=verbose)

    iter, max_iter = 0, 5
    while scheduler.task_list or iter >= max_iter:
        print(f"\n****Iter {iter}. Current task list****")
        for t in scheduler.task_list:
            print(str(t))

        first_task = scheduler.next_task()
        print("\n****Next task****\n")
        print(first_task)
        result = executor.run(first_task)
        print("\n****Task result****\n")
        print(result)

        new_tasks = scheduler.create_new_tasks()

        if new_tasks:
            scheduler.add(new_tasks)
            scheduler.reschedule()

        iter += 1
