import json
from websocket import create_connection

ws = create_connection("wss://ws.dogechain.info/inv")
ws.send(json.dumps({"op":"addr_sub", "addr":"dogecoin_address"}))
result =  ws.recv()
print (result)
ws.close()