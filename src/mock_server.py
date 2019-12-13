import http.server
import socketserver
import time
import os
import numpy as np
from json import dumps
from threading import Thread

def server():
    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

def updating():
    print("Started html updater")
    path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "index.html")
    print(path)
    while True:
        ts = float(time.time())
        file = {"time": ts, "current_weight": {"time": ts, "value": float(4.1*np.random.random_sample())}, "valid_weight": {"time": ts, "value": float(6.7*np.random.random_sample())}}
        with open(path, "w") as f:
            f.write(dumps(file, indent=4))
        time.sleep(2)
        
t_server = Thread(target=server)
t_updating = Thread(target=updating)

t_server.start()
t_updating.start()
    
while True:
    pass
