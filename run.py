from app import create_app
import eventlet  # pyright: ignore[reportMissingTypeStubs]
import eventlet.wsgi  # pyright: ignore[reportMissingTypeStubs]

app = create_app()

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
