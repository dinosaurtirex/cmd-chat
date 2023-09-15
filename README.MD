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
    asyncio.run(
        cmd_chat.run()
    )
```

How does encryption work?

* The client generates a private key.
* The server generates a symmetric key.
* The client sends the public key to the server.
* The server encrypts the symmetric key and sends it to the client.
* The client encrypts the private key.
* After that, communication with the server occurs via the symmetric key.
