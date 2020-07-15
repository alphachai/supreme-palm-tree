#!/usr/bin/env bash

cd "$APP_DIR";

wait_for_postgres_ready() {
    #######################################
    # Wait for a postgres database to be available.
    # Arguments:
    #   DATABASE_URL
    #   max_wait (default: 30 seconds)
    #######################################
    local url max_wait n exit_code;
    url="$1";
    max_wait="${2:-30}";
    n=0;
    until [ "$n" -gt "$max_wait" ]; do
        set +e
        python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect("""$url""")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
        exit_code=$?;
        set -e;
        if [ "$exit_code" -eq 0 ]; then
            break;
        fi
        if [ "$n" -eq "$max_wait" ]; then
            break;
        fi
        echo "Postgres is unavailable - sleeping" >&2;
        sleep 1;
        n=$((n + 1));
    done
    if [ $exit_code -eq 0 ]; then
        echo "Postgres is up - continuing..." >&2;
    else
        echo "ERROR: Postgres didn't come up!" >&2;
        exit $exit_code;
    fi
}

cd /app;

# Copy nginx config into position
cp -rf config/nginx/* /etc/nginx/conf.d

if [[ "$DATABASE_URL" = "postgresql"* ]]; then
    # If using a PostgreSQL database, wait for it to be available.
    wait_for_postgres_ready "$DATABASE_URL";
fi

# Do database migrations.
alembic upgrade head;

export GUNICORN_CONF="$APP_DIR/config/gunicorn.py"
export WORKER_CLASS="uvicorn.workers.UvicornWorker"
export APP_MODULE="app.main:app"

exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE" --user nobody --preload "$@";
