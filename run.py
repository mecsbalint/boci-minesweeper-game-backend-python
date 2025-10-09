from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler  # pyright: ignore[reportMissingTypeStubs]
import sys
from app import create_app

app = create_app()

if __name__ == "__main__":
    server = pywsgi.WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler, log=sys.stdout)

    try:
        print(f"Server is started on port {5000}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server is stopped by user")
