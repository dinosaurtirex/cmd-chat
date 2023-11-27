import asyncio 

import rsa
from cryptography.fernet import Fernet

from functools import partial

from sanic.worker.loader import AppLoader

from sanic.response import HTTPResponse
from sanic import Sanic, Request, response, Websocket

from cmd_chat.server.models import Message
from cmd_chat.server.services import (
    _get_bytes_and_serialize,
    _check_ws_for_close_status,
    _generate_new_message,
    _generate_update_payload
)


app = Sanic("app")
app.config.OAS = False


# Message structure is:
# [username: message, ...]
MESSAGES_MEMORY_DB: list[Message] = []


# Users structure is
# {Ip, Username: Public key} 
USERS: dict[str, str] = {}
PUBLIC_KEY = Fernet.generate_key()


def attach_endpoints(app: Sanic):

    @app.websocket("/talk")
    async def talk_ws_view(request: Request, ws: Websocket) -> HTTPResponse:
        while True:
            serialized_message: dict = await _get_bytes_and_serialize(ws)
            await _check_ws_for_close_status(
                serialized_message,
                ws
            )
            new_message = await _generate_new_message(
                serialized_message.get("text")
            )
            MESSAGES_MEMORY_DB.append(new_message)
            await ws.send(
                str({"status": "ok"})
            )
            await asyncio.sleep(0.2)


    @app.websocket("/update")
    async def update_ws_view(request: Request, ws: Websocket) -> HTTPResponse:
        while True:
            payload = await _generate_update_payload(
                MESSAGES_MEMORY_DB,
                USERS
            )
            await ws.send(payload.encode())
            await asyncio.sleep(0.2)


    @app.route('/get_key', methods=['GET', 'POST'])
    async def get_key_view(request: Request) -> HTTPResponse:
        public_key = rsa.PublicKey.load_pkcs1(request.form.get('pubkey'))
        encrypted_data = rsa.encrypt(PUBLIC_KEY, public_key)
        if request.ip not in USERS:
            USERS[f"{request.ip}, {request.form.get('username')}"] = PUBLIC_KEY
        return response.raw(encrypted_data)


def create_app(app_name: str) -> Sanic:
    app = Sanic(app_name)
    attach_endpoints(app)
    return app 


def run_server(host: str, port: int, dev: bool=False) -> None:
    loader = AppLoader(factory=partial(create_app, "CMD_SERVER"))
    app = loader.load()
    app.prepare(host=host, port=port, dev=dev)
    Sanic.serve(primary=app, app_loader=loader)
