from aiohttp import web
import jinja2
import aiohttp_jinja2
import asyncio
import socket
import os

from handles.handles import *
from config.conf import cfg


# Override 'config/conf.py' setting for listening IP -> current IP is selected
cfg["service"]["home"]["host"] = socket.gethostbyname(socket.gethostname())

# Full path to 'server' directory
server_dir = os.path.abspath(__file__ + "/../")

# Initialisation asyncio loop and fetch it to web server
main_loop = asyncio.get_event_loop()
app = web.Application(loop=main_loop)

# Initialisation jinja templates location
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(server_dir + '/templates'))

# Initialisation of server endpoints based on 'config/conf.py' settings
for listener in cfg["server"].values():
    for method in listener.values():
        calable = method["handle"]
        app.router.add_route(method["method"],
                             method["endpoint"],
                             eval(method["handle"]))

# Initialisation of server static resources... Use NGINX on production!
app.router.add_static("/js/", server_dir + "/templates/js")
app.router.add_static("/css/", server_dir + "/templates/css")

# Server start
web.run_app(app, host=cfg["service"]["home"]["host"],
            port=cfg["service"]["home"]["port"])
