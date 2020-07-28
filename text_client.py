import asyncio
import socket


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())
    await writer.drain()
    print('r', await reader.read())
    await asyncio.sleep(4)
    print('Send: %r' % message)
    writer.write(message.encode())
    await writer.drain()
    print(await reader.read())

    print('Close the socket')
    writer.close()


async def main(loop):
    message = 'get_game'
    tasks = []
    for i in range(1):
        tasks.append(asyncio.ensure_future(tcp_echo_client(message.format(str(i)), loop)))
        # await asyncio.sleep(0.1)

    await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()

# sock = socket.socket()
# sock.connect(('localhost', 8888))
# sock.send(b'get_game')
#
# data = sock.recv(1024)
# sock.close()
#
# print('2', data)
