#!/bin/bash
OUTFILE="openapi.json"

python generate_openapi.py | jq -c > auth-openapi.json
redocly join --without-x-tag-groups ~/watttime/test-docs/auth-openapi.json ~/watttime/api-maps/openapi.json ~/watttime/apiv3-forecast/openapi.json ~/watttime/apiv3-historical/openapi.json -o "${OUTFILE}"
