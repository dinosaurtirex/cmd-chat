import json
from websocket import create_connection

ws = create_connection("ws://192.168.1.1/update")
ws.send()#json.dumps({"op":"addr_sub", "addr":"dogecoin_address"}))
result =  ws.recv()
print(result)
ws.close()