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
new_spec["info"]["x-logo"] = {
        "url": "https://staging-watttimemigration-staging.kinsta.cloud/wp-content/uploads/2023/01/WattTime-logo-2023-black-1920px.png",
        "backgroundColor": "#DAD9D9",
        "altText": "WattTime Logo",
    }
print(json.dumps(new_spec))
# with open("openapi.json", "w+") as _f:
# _f.write(json.dumps(new_spec))
