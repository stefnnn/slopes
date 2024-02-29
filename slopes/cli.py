from click import command, option
from mountaineer.cli import handle_runserver, handle_watch, handle_build
from mountaineer.database.cli import handle_createdb
from mountaineer.io import async_to_sync

from slopes import models
from slopes.config import AppConfig


@command()
@option("--port", default=5006, help="Port to run the server on")
def runserver(port: int):
    handle_runserver(
        package="slopes",
        webservice="slopes.main:app",
        webcontroller="slopes.app:controller",
        port=port,
    )


@command()
def watch():
    handle_watch(
        package="slopes",
        webcontroller="slopes.app:controller",
    )


@command()
def build():
    handle_build(
        webcontroller="slopes.app:controller",
    )


@command()
@async_to_sync
async def createdb():
    _ = AppConfig()

    await handle_createdb(models)