#!/bin/bash
python generate_openapi.py | jq -c > auth-openapi.json
