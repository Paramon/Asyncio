import asyncio
import socket
import logging
import signal
from asyncio import AbstractEventLoop
from typing import List

async def echo(connection: socket,loop: AbstractEventLoop) -> None:
    """
    It takes a socket connection and an event loop, and returns nothing
    
    :param connection: The socket object that is connected to the client
    :type connection: socket
    :param loop: The event loop that the server is running on
    :type loop: AbstractEventLoop
    """
    try:
        while data := await loop.sock_recv(connection, 1024):
            print("got data!")
            if data == b'boom\r\n':
                raise Exception("Неожиданная ошибка сети")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


echo_tasks = []


async def connection_listener(server_socket: socket,
                                loop: AbstractEventLoop):
    """
    It listens for new connections on the server socket, and when it gets one, it creates a new socket
    for that connection, and then passes that socket to the `connection_handler` function
    
    :param server_socket: The socket that the server is listening on
    :type server_socket: socket
    :param loop: The event loop that the server is running on
    :type loop: AbstractEventLoop
    """
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Получен запрос на подключение {address}")
        asyncio.create_task(echo(connection, loop))


# It's a subclass of SystemExit that doesn't print a stack trace
class GracefulExit(SystemExit):
    pass

def shutdown():
    """
    It shuts down the script.
    """
    raise GracefulExit()


async def close_echo_task(echo_tasks: List[asyncio.Task]):
    """
    "Wait for all echo tasks to complete, but if they don't complete in 2 seconds, cancel them."
    
    The first line of the function creates a list of tasks that we want to wait for. The second line
    creates a list of waiters. A waiter is a task that waits for another task to complete. In this case,
    we're waiting for each echo task to complete
    
    :param echo_tasks: List[asyncio.Task]
    :type echo_tasks: List[asyncio.Task]
    """
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # We expect a timeout error here
            pass


async def main():
    """
    A function that is asynchronous.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await connection_listener(server_socket, loop)


# It's a common idiom in Python to use this statement to check if the code is being run as a script,
# or if it's being imported as a module.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except GracefulExit:
        loop.run_until_complete(close_echo_task(echo_tasks))
    finally:
        loop.close()