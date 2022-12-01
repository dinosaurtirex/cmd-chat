from sanic.response import HTTPResponse
from sanic import Sanic, Request, response 
from cryptography.fernet import Fernet

import rsa

app = Sanic("app")
app.config.OAS = False

actual_messages = []
users = {}
key = Fernet.generate_key()


@app.route('/talk', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    actual_messages.append(request.form["text"][0])
    return response.json({"status": "ok"})


@app.route('/update', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    print("users_in_chat", [[username, ip] for username, ip in zip(users.keys(),users.values())])
    return response.json({
        "status": actual_messages, 
        "users_in_chat": [[username, ip] for username, ip in zip(
            users.keys(),users.values()
        )]
    })


@app.route('/get_key', methods=['GET', 'POST'])
async def get_key(request: Request) -> HTTPResponse:
    
    pubkey = rsa.PublicKey.load_pkcs1(request.form['pubkey'][0])
    data = rsa.encrypt(key, pubkey)
    
    if request.ip not in users:
        users[request.form['username'][0]] = key
    
    return response.raw(data)