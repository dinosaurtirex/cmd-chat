import asyncio 
import argparse

from cmd_chat.server.server import run_server
from cmd_chat.client.client import Client


def run_http_server(
    ip: str,
    port: int
) -> None:
    run_server(ip, port, False)


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
    parser = argparse.ArgumentParser(
        description='Command-line chat application'
    )
    parser.add_argument(
        'command', 
        choices=['serve', 'connect'], 
        help='Command to execute'
    )
    parser.add_argument(
        'ip_address', 
        help='IP address to serve or connect'
    )
    parser.add_argument(
        'port', 
        help='PORT of server'
    )
    parser.add_argument(
        'username', 
        nargs='?', 
        default='', 
        help='Username for connection (required for connect command)'
    )
    args = parser.parse_args()
    if args.command == 'serve':
        run_http_server(args.ip_address, int(args.port))
    elif args.command == 'connect':
        if not args.username:
            parser.error("Username is required for 'connect' command")
        await run_client(args.username, args.ip_address, int(args.port))


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()