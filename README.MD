# Welcome to command line chat project [CMD CHAT]

![Alt Text](https://static.wikia.nocookie.net/listofdeaths/images/b/b3/Tyler_Durden.webp/revision/latest?cb=20220909010337)

# What is this?

It is a console chat with message encryption.

# How does it work?

All you need to do is run a web server and connect to it via a client.

# Run 

### Create and activate a virtual environment in Python

```
pip install secured_console_chat
```

```
import asyncio 
import cmd_chat

if __name__ == '__main__':
    asyncio.run(cmd_chat.run())
```


### Or 

Start server:

```
cmd_chat serve localhost 5000 
```

Connect to server:

```
cmd_chat connect localhost 5000 tyler
```

How does encryption work?

* The client generates a private key.
* The server generates a symmetric key.
* The client sends the public key to the server.
* The server encrypts the symmetric key and sends it to the client.
* The client encrypts the private key.
* After that, communication with the server occurs via the symmetric key.

# Example

![Alt Text](example.gif)

# Known bugs 

* Sometime WS just drop connection
* Client input message problem. To start input, you need to press enter first, only after that you got pop up with message. Tried to fix, but nothing worked.

# 1.1.22

- Renderer logics have been separated
- A new renderer have been implemented  
- Thread closing logics have been changed. Now, it is easy to quit from the client without any unexpected behavior
- Now, displaying messages is limited to the last N messages. The default value is 5
- WS dropped connection, probably fixed 