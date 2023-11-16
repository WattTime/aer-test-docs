# V3 Docs Deploy

All openapi.json schemas are automatically generated and compiled into comprehensive docs. Sections like Introduction
are markdown files that get sourced at compile-time.

The following repos have openapi.json schemas that are used to compile these docs:

* [APIv3 data](https://github.com/WattTime/watttime-apiv3-data/)
* [APIv3 forecast](https://github.com/WattTime/watttime-apiv3-forecast/)
* [API maps](https://github.com/WattTime/watttime-api-maps)
* [test docs](./auth-openapi.json)

To join all the openapi.json files:

```
redocly join --without-x-tag-groups ./path/to/test-docs/auth-openapi.json ./path/to/watttime-api-maps/openapi.json ./path/to/watttime-apiv3-forecast/openapi.json ./path/to/watttime-apiv3-data/openapi.json -o openapi.json
```

To deploy to S3 and invalidate the cache:

```
./deploy.sh
```
