import asyncio


async def delay(delay_seconds: int) -> int:
    """
    It sleeps for a given number of seconds and then returns that number of seconds
    
    :param delay_seconds: the number of seconds to sleep
    :type delay_seconds: int
    :return: The return value of the coroutine.
    """
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds