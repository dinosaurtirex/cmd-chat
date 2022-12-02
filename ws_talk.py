import json
from websocket import create_connection

ws = create_connection("ws://localhost:1212/update")
while True:
    ws.send(payload="")#json.dumps({"op":"addr_sub", "addr":"dogecoin_address"}))
    result =  ws.recv()
    print(result)
ws.close()