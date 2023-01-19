

import asyncio
from util import async_timed, delay


@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    
    # Creating a list of tasks and awaiting each task in the list.
    # [await asyncio.create_task(delay(seconds)) for seconds in delay_times] #  Wrong!!!! 
    '''
    starting <function main at 0x108d189a0> with args () {}
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    finished <function main at 0x108d189a0> in 9.0057 second(s)
    '''

    # Awaiting each task in the list of tasks.
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]
    '''
    starting <function main at 0x108ffc9a0> with args () {}
    sleeping for 3 second(s)
    sleeping for 3 second(s)
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    finished <function main at 0x108ffc9a0> in 3.0022 second(s)
    '''
    


# Creating an event loop and running the coroutine until it is complete.
asyncio.run(main())