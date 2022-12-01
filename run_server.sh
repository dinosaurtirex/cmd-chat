#! /bin/bash

port=$1

if [ -d venv ]; then
  source venv/bin/activate
  sanic server.server.app -H 0.0.0.0 -p $port
else
  python3.10 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  sanic server.server.app -H 0.0.0.0 -p $port
fi
