#!/usr/bin/env python3

from alembic.config import Config
from alembic import command
from uvicorn import Config as UvicornConfig, Server

# Запуск миграций Alembic
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

# Запуск Uvicorn
config = UvicornConfig("src.main:app", host="0.0.0.0", port=8000, reload=True)
server = Server(config)

if __name__ == "__main__":
    server.run()
