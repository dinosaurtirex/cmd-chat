import json
from websocket import create_connection

ws = create_connection("ws://localhost:1212/talk")
while True:
    ws.send(payload=b"{'text': 123, 'username': 'bob'}")#json.dumps({"op":"addr_sub", "addr":"dogecoin_address"}))
    result =  ws.recv()
    print(result)
    #print(eval(result))
    #print(result)
ws.close()