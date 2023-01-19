

import asyncio
from util import async_timed, delay


@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    
    # Creating a list of tasks and awaiting each task in the list.
    #[await asyncio.create_task(delay(seconds)) for seconds in delay_times] #  не конкурентно!!!! 

    # Awaiting each task in the list of tasks.
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]
    


# Creating an event loop and running the coroutine until it is complete.
asyncio.run(main())