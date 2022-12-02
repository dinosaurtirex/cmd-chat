import json
from websocket import create_connection

ws = create_connection("ws://localhost:1212/update")
while True:
    ws.send(payload="hello baby")#json.dumps({"op":"addr_sub", "addr":"dogecoin_address"}))
    result =  ws.recv()
    print(eval(result))
    print(result)
ws.close()