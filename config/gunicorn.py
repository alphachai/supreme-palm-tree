import json
import multiprocessing
import os
import pathlib

import decouple

is_development = decouple.config(
    "DEBUG",
    default=bool(
        os.path.exists(pathlib.Path(__file__).parent.parent.absolute() / ".env")
    ),
)
cpu_reservation = decouple.config(
    "CPU_RESERVATION", default=multiprocessing.cpu_count() * 1024, cast=int
)
workers_per_core = decouple.config("WORKERS_PER_CORE", default=4, cast=int)
host = decouple.config("HOST", default="0.0.0.0")
port = decouple.config("PORT", default="80")

workers = int(
    1 if is_development else (cpu_reservation // (1024 / workers_per_core)) + 1
)
bind = [f"{host}:{port}"]
keepalive = 120

# Enable configuration of gunicorn via enviroment variables.
_from_env = {}
for k, v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split("_", 1)[1].lower()
        _from_env[key] = v
        locals()[key] = v

print(
    json.dumps(
        {
            "workers": workers,
            "bind": bind,
            **_from_env,
            # Additional, non-gunicorn variables
            "is_development": is_development,
            "cpu_reservation": cpu_reservation,
            "workers_per_core": workers_per_core,
            "workers": workers,
            "host": host,
            "port": port,
        }
    )
)

loglevel = "info"
errorlog = "-"
accesslog = "-"
