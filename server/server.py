from aiohttp import web
import jinja2
import aiohttp_jinja2
import asyncio

from handles.handles import *
from config.conf import cfg

main_loop = asyncio.get_event_loop()

app = web.Application(loop=main_loop)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))


for listener in cfg["server"].values():
    for method in listener.values():
        calable = method["handle"]
        app.router.add_route(method["method"],
                             method["endpoint"],
                             eval(method["handle"]))

app.router.add_static("/js/", "templates/js")
app.router.add_static("/css/", "templates/css")

web.run_app(app, host=cfg["service"]["home"]["host"],
            port=cfg["service"]["home"]["port"][1:5])
