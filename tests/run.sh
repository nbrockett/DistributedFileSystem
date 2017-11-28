#!/usr/bin/env bash

cd ../dfs

echo 'starting directory server'
cd ../dfs && python ./directory_server.py --host='127.0.0.1' --port=8002 &

echo 'starting file server 1'
cd ../dfs && python ./file_server.py --host='127.0.0.1' --port=8001 --config=fs1.json&

echo 'starting file server 2'
cd ../dfs && python ./file_server.py --host='127.0.0.1' --port=8003 --config=fs2.json&