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
        # Receiving data from the client.
        while data := await loop.sock_recv(connection, 1024):
            print("got data!")
            # Checking if the data that was received from the client is equal to the string
            # 'boom\r\n'.
            if data == b'boom\r\n':
                # It raises an exception.
                raise Exception("Неожиданная ошибка сети")
            # It sends data to the client.
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


echo_tasks = []


async def connection_listener(server_socket: socket,loop: AbstractEventLoop):
    """
    It accepts a socket and an event loop, and then it waits for a connection to be made to the socket.
    When a connection is made, it creates a new task that will handle the connection
    
    :param server_socket: the socket object that will be used to accept incoming connections
    :type server_socket: socket
    :param loop: the event loop that will be used to run the server
    :type loop: AbstractEventLoop
    """
   
    while True:
        # Waiting for a connection to be made to the socket.
        connection, address = await loop.sock_accept(server_socket)
        # It sets the socket to non-blocking mode.
        connection.setblocking(False)
        print(f"Получен запрос на подключение {address}")
        # It creates a new task that will handle the connection.
        asyncio.create_task(echo(connection, loop))



# Это подкласс SystemExit, который не печатает трассировку стека.
class GracefulExit(SystemExit):
    pass

def shutdown():
    raise GracefulExit()


async def close_echo_task(echo_tasks: List[asyncio.Task]):
    """
    «Дождитесь завершения всех эхо-задач, но если они не завершатся в течение 2 секунд, отмените их».
    
    Первая строка функции создает список задач, которые мы хотим дождаться. Вторая строка создает список
    официантов. Официант — это задача, которая ожидает завершения другой задачи. В этом случае мы ждем
    завершения каждой эхо-задачи.
    
    :param echo_tasks: Список[asyncio.Task]
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
    
    # It creates a socket object that will be used to accept incoming connections.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # It sets the socket to reuse the address.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Creating a tuple that contains the IP address and port number that the server will listen on.
    server_address = ('127.0.0.1', 8000)
    # It sets the socket to non-blocking mode.
    server_socket.setblocking(False)
    # It binds the socket to the IP address and port number that the server will listen on.
    server_socket.bind(server_address)
    # It tells the socket to start listening for incoming connections.
    server_socket.listen()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await connection_listener(server_socket, loop)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        # It creates an event loop.
        loop.run_until_complete(main())
    except GracefulExit:
        # Waiting for all the echo tasks to complete, but if they don't complete within 2 seconds, it
        # cancels them.
        loop.run_until_complete(close_echo_task(echo_tasks))
    finally:
        loop.close()