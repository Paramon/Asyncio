import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    """
    It fetches the status code of a URL
    
    :param session: ClientSession - the session object that we created earlier
    :type session: ClientSession
    :param url: The URL to fetch the status from
    :type url: str
    :return: The status code of the url
    """
    # Creating a timeout object that will be used to set the timeout for the request.
    ten_milliseconds = aiohttp.ClientTimeout(total=.1)
    async with session.get(url, timeout=ten_milliseconds) as result:
        return result.status


@async_timed()
async def main():
    # Creating a session object that we can use to make requests.
    # Setting the timeout for the session to 1 second.
    session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = 'http://www.example.com'
        # Calling the `fetch_status` function and waiting for it to finish.
        status = await fetch_status(session, url)
        print(f'Status for {url} was {status}')


asyncio.run(main())