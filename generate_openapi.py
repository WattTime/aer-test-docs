#!/usr/bin/env python
import json

from fastapi.openapi.utils import get_openapi

from api import app

new_spec = get_openapi(
    title=app.title,
    servers=app.servers,
    routes=app.routes,
    version=app.version,
    description=app.description,
    tags=app.openapi_tags,
)
print(json.dumps(new_spec))
# with open("openapi.json", "w+") as _f:
# _f.write(json.dumps(new_spec))
