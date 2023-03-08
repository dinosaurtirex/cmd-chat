import asyncio 

from cmd_chat.server.server import app
from cmd_chat.client.client import Client


async def run_server(
    ip: str,
    port: int
) -> None:
    app.run(
        host=ip,
        port=port,
        dev=False
    )


async def run_client(
    username: str,
    server: str,
    port: int
) -> None:
    Client(
        server = server,
        port = port,
        username = username
    ).run()


async def run() -> None:
    action: int = int(input("Choose action:\n1. Run server\n2. Run client\nAction: "))
    if action == 1:
        await run_server(
            input("IP: "),
            int(input("PORT: "))
        )
    if action == 2:
        await run_client(
            input("USERNAME: "),
            input("IP: "),
            int(input("PORT: "))
        )


if __name__ == '__main__':
    asyncio.run(
        run()
    )