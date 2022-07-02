from typing import Any, Coroutine
from sanic import Sanic, Request, response 
from sanic.response import HTTPResponse
from sanic.server.websockets.impl import WebsocketImplProtocol


app = Sanic("app")
app.config.OAS = False

actual_messages = []


@app.route('/talk', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    actual_messages.append(request.form["text"])
    return response.json({"status": "ok"})


@app.route('/update', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    return response.json({"status": actual_messages})