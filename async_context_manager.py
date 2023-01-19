import asyncio
import socket
from types import TracebackType
from typing import Optional, Type

class ConnectedSocket:
    
    def __init__(self, server_socket):
        # Setting the connection to None.
        self.connection = None
        # Assigning the server_socket to the self._server_socket.
        self._server_socket = server_socket
    
        
    async def __aenter__(self) -> socket:
        """
        It waits for a connection to be accepted by the server socket, and then returns the connection
        :return: The connection object.
        """
        print('Entering context manager, waiting for connection')
        # Getting the event loop.
        loop = asyncio.get_event_loop()
        # Accepting a connection from the server socket.
        connection, address = await loop.sock_accept(self._server_socket)
        self._connection = connection
        print('Accepted a connection')
        return self._connection
    
    
    async def __aexit__(self,
                        ext_type: Optional[Type[BaseException]],
                        ext_value: Optional[BaseException], 
                        ext_traceback: Optional[TracebackType]) -> None:
        print('Exiting context manager')
        # Closing the connection.
        self._connection.close()
        print('Connection closed')
async def main():
    loop = asyncio.get_event_loop()

    
    # Creating a socket object.
    server_socket = socket.socket()
    # Setting the socket options.
    server_socket.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1',8000)
    server_socket.setblocking(False)
    server_socket.bind (server_address)
    # Listening for connections.
    server_socket.listen ()
    
   
    # Creating a context manager that will wait for a connection to be accepted by the server socket,
    # and then return the connection.
    async with ConnectedSocket(server_socket) as connection:
        # Receiving data from the connection.
        data = await loop.sock_recv(connection, 1024)
        print(data)


asyncio.run(main())

        
