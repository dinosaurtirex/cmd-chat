#! /bin/bash

if [ -d venv ]; then 
  source venv/bin/activate;
  python client.py
else:
  python3.10 -m venv venv
  source venv/bin/activate
  pip install -r reqs.txt
  python client.py
fi

