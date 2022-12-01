from sanic.response import HTTPResponse
from sanic import Sanic, Request, response 
from cryptography.fernet import Fernet


import rsa

app = Sanic("app")
app.config.OAS = False

# Message structure is:
# [username: message, ...]
actual_messages: list[str] = []
# Users structure is
# {Ip, Username: Public key} 
users: dict[str, str] = {}
key = Fernet.generate_key()


@app.route('/talk', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    actual_messages.append(request.form.get("text"))
    return response.json({"status": "ok"})


@app.route('/update', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    return response.json({
        "status": actual_messages, 
        "users_in_chat": list(users.keys())
    })


@app.route('/get_key', methods=['GET', 'POST'])
async def get_key(request: Request) -> HTTPResponse:
    
    pubkey = rsa.PublicKey.load_pkcs1(request.form.get('pubkey'))
    data = rsa.encrypt(key, pubkey)
    
    if request.ip not in users:
        users[f"{request.ip}, {request.form.get('username')}"] = key
    
    return response.raw(data)