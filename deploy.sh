#!/bin/bash

DIST_ID="E30XUKCWOUDBFR"
OUTFILE="openapi.json"

redocly join --without-x-tag-groups ~/watttime/test-docs/auth-openapi.json ~/watttime/api-maps/openapi.json ~/watttime/apiv3-forecast/openapi.json ~/watttime/apiv3-historical/openapi.json -o "${OUTFILE}"
aws s3 cp "${OUTFILE}" "s3://test-docs.watttime.org/openapi.json"
aws s3 cp "index.html" "s3://test-docs.watttime.org/index.html"
aws cloudfront create-invalidation --distribution-id="${DIST_ID}" --paths /openapi.json /index.html
