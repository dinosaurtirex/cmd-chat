from email.policy import HTTP
from typing import Any, Coroutine
from sanic import Sanic, Request, response 
from sanic.response import HTTPResponse
from sanic.server.websockets.impl import WebsocketImplProtocol
import rsa

app = Sanic("app")
app.config.OAS = False

actual_messages = []

(pubkey, privkey) = rsa.newkeys(512)

with open("private.pem", "wb") as f:
    f.write(privkey.save_pkcs1())
    
with open("public.pem", "wb") as f:
    f.write(pubkey.save_pkcs1())


@app.route('/talk', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    actual_messages.append(request.form["text"][0])
    return response.json({"status": "ok"})


@app.route('/update', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    return response.json({"status": [rsa.encrypt(k.encode('utf8'), pubkey) for k in actual_messages]})


@app.route('/get_key', methods=['GET', 'POST'])
async def get_key(request: Request) -> HTTPResponse:
    return await response.file("public.pem", status=200)