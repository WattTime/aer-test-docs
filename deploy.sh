#!/bin/bash

STAGING_DIST_ID="E30XUKCWOUDBFR"
STAGING_BUCKET="s3://test-docs.watttime.org"
PROD_DIST_ID="E12XPRKTUDNALL"
PROD_BUCKET="s3://docs.watttime.org"

BUCKET=${PROD_BUCKET}
DIST_ID=${PROD_DIST_ID}

OUTFILE="openapi.json"

./build_docs.sh
aws s3 cp "${OUTFILE}" "${BUCKET}/openapi.json"
aws s3 cp "index.html" "${BUCKET}/index.html"
aws s3 cp "WattTime-logo-2023-black-1920px_wpad.png" "${BUCKET}/WattTime-logo-2023-black-1920px_wpad.png"
aws s3 cp "favicon.ico" "${BUCKET}/favicon.ico"
aws cloudfront create-invalidation --distribution-id="${DIST_ID}" --paths /openapi.json /index.html
