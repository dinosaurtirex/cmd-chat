```
 ██████╗███╗   ███╗██████╗  ██████╗██╗  ██╗ █████╗ ████████╗
██╔════╝████╗ ████║██╔══██╗██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██║     ██╔████╔██║██║  ██║██║     ███████║███████║   ██║   
██║     ██║╚██╔╝██║██║  ██║██║     ██╔══██║██╔══██║   ██║   
╚██████╗██║ ╚═╝ ██║██████╔╝╚██████╗██║  ██║██║  ██║   ██║   
 ╚═════╝╚═╝     ╚═╝╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                                            
```

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
pip install -r reqs.txt
```

```
sanic server.app -H 0.0.0.0 -p <port>
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
pip install -r reqs.txt 
```

```
python client.py
```

## How crypting works? 

* Client making priv key
* Server making symmetric key 
* Client sending public key to server
* Server crypting symmetric key and sending to client 
* Client encrypting private key 
* And than communicate with server via
* symmetric key

## To do

* interface for choosing server in client 
* double password user verification
* white list

![preview](preview.png)
