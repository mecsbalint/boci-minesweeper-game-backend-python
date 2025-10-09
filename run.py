import os
from typing import cast
from dotenv import load_dotenv
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler  # pyright: ignore[reportMissingTypeStubs]
import sys
from app import create_app

app = create_app()

load_dotenv()
PORT = int(cast(str, os.getenv("PORT")))


if __name__ == "__main__":
    server = pywsgi.WSGIServer(("0.0.0.0", PORT), app, handler_class=WebSocketHandler, log=sys.stdout)

    try:
        print(f"Server is started on port {PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server is stopped by user")
