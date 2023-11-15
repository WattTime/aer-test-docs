#!/bin/bash
python generate_openapi.py | jq > auth-openapi.json
