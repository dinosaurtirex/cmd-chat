#! /bin/bash

if [ -d venv ]; then 
  source venv/bin/activate;
  python client/client.py
else:
  python3.10 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python client.py
fi

