@echo off

echo -------------------------------------------
echo copyright SLIIT research 2020-159 group
echo -------------------------------------------

goto startServer

:startServer

echo server starting
start chrome http://localhost:5002/api
echo server started
echo server running on http://localhost:5002/api

echo -------------------------------------------

python App.py