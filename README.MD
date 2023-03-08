```
 ██████╗███╗   ███╗██████╗  ██████╗██╗  ██╗ █████╗ ████████╗
██╔════╝████╗ ████║██╔══██╗██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██║     ██╔████╔██║██║  ██║██║     ███████║███████║   ██║   
██║     ██║╚██╔╝██║██║  ██║██║     ██╔══██║██╔══██║   ██║   
╚██████╗██║ ╚═╝ ██║██████╔╝╚██████╗██║  ██║██║  ██║   ██║   
 ╚═════╝╚═╝     ╚═╝╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                                            
```

![Alt Text](example.gif)

# How it works?

All you need it's to run web-server and connect to them via client

# Server run 

## Linux 

For linux its required to have python3.10 

```
chmod +x run_server.sh
```

```
./run_server.sh <port>
```

## Windows 

```
python -m venv venv
```

```
venv/scripts/Activate
```

```
pip install -r requirements.txt
```

```
sanic server.server.app -H 0.0.0.0 -p <port>
```

# Client run 

## Linux 

For linux its required to have python3.10 

```
chmod +x run_client.sh
```
```
./run_client.sh
```

## Windows 

```
python -m venv venv
```

```
venv/scripts/Activate
```

```
pip install -r requirements.txt
```

```
python client/client.py
```

## How crypting works? 

* Client making priv key
* Server making symmetric key 
* Client sending public key to server
* Server crypting symmetric key and sending to client 
* Client encrypting private key 
* And than communicate with server via symmetric key
