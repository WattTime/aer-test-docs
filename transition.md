We're excited to upgrade our API after about 5 years on the same version. We don't undertake this lightly, and endeavor to avoid breaking changes whenever possible. We think the upgrades we've made available in API v3 will be well worth the effort to update your code, and we're happy to support you as you make the transition. Please contact us with questions, support@WattTime.org.

After an overview including a description of miscellaneous changes, the rest of this guide is meant to help you translate your existing v2 requests into their respective v3 requests and handle any differences in the responses that come back.

# Overview

At a high level, the biggest change between v2 and v3 is a disambiguation of the `/v2/data` endpoint – since these data
are best used in historical analysis rather than real-time optimization, we're now housing these data in the
`/v3/historical` endpoint.


The `/v3/forecast` endpoint continues to provide forecast data for real time optimization, across a number of different signal types. There is now a dedicated `/v3/forecast/historical` endpoint for gathering historical forecasts for retrospective analyses.

WattTime is adding support for a number of new signal types, including: `health_damage` (both forecast and historical), and `co2_aoer` (historical only, for accounting purposes). WattTime's marginal operating emissions rate has been named `co2_moer` to disambiguate from other signals with equivalent units.

Most query responses will now contain two stanzas: `data` and `meta`. The content in `data` includes point times, values, and optional pointwise metadata related to the filtering criteria provided in a request. The content in `meta` describes the returned data, including any potential warnings or issues encountered.

Geographic regions were formerly identified as `abbrev` and `ba` (for balancing authority), and in v3 will be known as `region` (which is inclusive of balancing authorities, subregions, and international nomenclature). `region` is also a unique identifier across all endpoints.

Going forward, new regions will only be added to v3. With the introduction of v3, we're also releasing `co2_moer` data in 12 new countries comprising 21 new regions total.

Where in the past a user could request data from `/v2/data` using GPS lat/long as inputs, the `/v3/historical` endpoint now accepts only the region parameter as input to define the location.

Time zones are now required on all user-provided timestamps. Previously in v2 if timestamps lacked time zone information, UTC was assumed. That must now be made explicit in v3 in the request.

Significantly, our model versioning semantics are now date based. This is a change from the V2 API, where model versioning differed between signal types and endpoints. In the V2 API, model versions for the MOER signal type were represented as decimals (i.e. `2.0`, `3.0`, `3.2`) while forecast model versions were semantically linked to the MOER data they were forecasting (i.e. `3.2-1.0.0`). With the introduction of new signal types and modeling methodologies, WattTime is shifting towards date-based versioning to remove some confusion around the significance of model version names. Model versions across all endpoints in the V3 API are dates (i.e. `2022-12-31`), which represent the approximate end of sample data used to train that model. When a new model version is released, it may indicate that the model was trained on more recent data (which is necessary as the power grid transitions to renewable fuel types), or as WattTime develops new methodologies that improve the accuracy of our signals. To learn more about the various methodologies used in each grid region, see here <link to model types page>.


# v2/register
The URL is the only update to this endpoint.
### v2 URL
`https://api2.watttime.org/v2/register`
### v3 URL
`https://api.watttime.org/register`

# v2/login
The URL is the only update to this endpoint.
### v2 URL
`https://api2.watttime.org/v2/login`
### v3 URL
`https://api.watttime.org/login`

# v2/password
The URL is the only update to this endpoint.
### v2 URL
`https://api2.watttime.org/v2/password`
### v3 URL
`https://api.watttime.org/password`

# v2/ba-from-loc

Formerly known as `ba` and `abbrev`, regions are now identified by the `region` parameter which is also the natural key in API v3 (the `id` in the v2 response has been retired). Accordingly, the URL now reflects that language change (using `.../region-from-loc`). This endpoint now also requires a `signal_type` input parameter as there can be differences in grid regions depending on the type of data you are accessing.


### v2 request:
```python
url = "https://api2.watttime.org/v2/ba-from-loc"
params = {
    "latitude": "42.372",
    "longitude": "-72.519"
}
```

### v2 response:
```json
{
    "id": 169,
    "abbrev": "ISONE_WCMA",
    "name": "ISONE Western/Central Massachusetts"
}
```

### v3 request
```python
url = "https://api.watttime.org/v3/region-from-loc"
params = {
    "latitude": "42.372",
    "longitude": "-72.519",
    "signal_type": "co2_moer"
}
```

### v3 response:
```json
{
    "region": "ISONE_WCMA",
    "region_full_name": "ISONE Western/Central Massachusetts",
    "signal_type": "co2_moer"
}
```

# v2/ba-access

This endpoint provided a list of available regions and could be filtered to the subset accessible by the authenticated account. The new v3 endpoint provides a more comprehensive guide to what is available for your account on the API. It provides a hierarchical JSON output that describes the signals, regions, endpoints, models and any available associated metadata for available data (in that hierarchical order).

### v2 request:
```python
url = "https://api2.watttime.org/v2/ba-access"
params = {
    "all": "false"
}
```

### v2 response:
```json
{
  "ba": "CAISO_NORTH",
  "name": "California ISO Northern",
  "access": true,
  "datatype": "MOER"
}
```

### v3 request
```python
url = "https://api.watttime.org/v3/my-access"
params = {}
```

### v3 response:
```json
{
  "signal_types": [
    {
      "signal_type": "co2_moer",
      "regions": [
        {
          "region": "PJM_NJ",
          "region_full_name": "PJM New Jersey",
          "parent": "PJM",
          "data_point_period_seconds": 300,
          "endpoints": [
            {
              "endpoint": "v3/forecast",
              "models": [
                {
                  "model": "2023-08-24",
                  "data_start": "2021-08-24",
                  "train_start": "2021-08-24",
                  "train_end": "2021-08-24"
                }
              ]
            },
            {
              "endpoint": "v3/historical",
              "models": [
                {
                  "model": "2023-08-24",
                  "data_start": "2021-08-24",
                  "train_start": "2021-08-24",
                  "train_end": "2021-08-24",
                  "type": "binned_regression"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```


# v2/index
This endpoint provides the most recent marginal carbon intensity value for the local grid. It provided either a percentile value, a raw MOER value, or both, depending on the request parameters. Since there are two types of data available from this endpoint, we'll address the differences for each separately.

## v2/index, "style": "percent"
WattTime is still gathering input on how this feature might be included in v3.

## v2/index, "style": "moer"
`"style": "moer"` is replaced by `"signal_type": "co2_moer"` in the request parameters.

### v2/index request for MOER value:

```python
url = "https://api2.watttime.org/index"
params = {
    "ba": "CAISO_NORTH",
    "style": "moer"
}
```
There are two options for how you translate this v2 request to v3. You can get recent data from the /historical endpoint (higher accuracy, slightly older), or you can request the first point of the forecast (guaranteed to be less than 5 minutes old for `co2_moer`, lower accuracy).

### v3 request for MOER value from v3/historical:

```python
url = "https://api.watttime.org/v3/historical"
params = {
    "region": "CAISO_NORTH",
    "start": "2022-07-15T00:00+00:00",
    "end": "2022-07-15T00:05+00:00",
    "signal_type": "co2_moer",
}
```

### v3 request for MOER value from v3/forecast:

```python
url = "https://api.watttime.org/v3/forecast"
params = {
    "region": "CAISO_NORTH",
    "signal_type": "co2_moer",
    "horizon_hours: 0,
}
```

# v2/data
This endpoint was used to obtain historical MOER data (e.g. CO2 lbs/MWh) for a specified grid region or location (latitude & longitude pair). Since this request was meant for historical data, in v3 we're making all “historical” data available from an endpoint called `historical`. Also, in v3, we've eliminated the option to use lat/lon here, so you'll need to first determine the region and use that as an input parameter here. In v2, if the optional parameters `starttime` and `endtime` were omitted, the response would contain the latest available value. In v3, the `start` and `end` parameters are required.

### v2 request
```python
url = "https://api2.watttime.org/v2/data"
params = {
    "ba": "CAISO_NORTH",
    "starttime": "2022-11-16T20:30:00-0800",
    "endtime": "2022-11-16T20:45:00-0800"
}
```

### v3 request
```python
url = "https://api.watttime.org/v3/historical"
params = {
    "region": "CAISO_NORTH",
    "start": "2022-07-15T00:00+00:00",
    "end": "2022-07-15T00:05+00:00",
    "signal_type": "co2_moer",
}
```

# v2/historical
This endpoint provided a zip file containing monthly .csv files with the MOER values (e.g. CO2 lbs/MWh) and timestamps for a requested region for the past two years or more. You can still get historical data using the new historical endpoint, and using the required parameters `start`, `end`, and `signal_type`.

The response is the biggest difference here. We've retired this csv output feature in favor of standardizing on the JSON response type. The request to `/v3/historical` is limited to 32 days per request. We've developed an SDK that you can use to pull data in larger chunks than just one month at a time, and translate the data into various formats. If you're still having trouble getting the data in the format you'd like, please contact support@watttime.org for assistance.

### v2 request
```python
url = "https://api2.watttime.org/v2/historical"
params = {
    "ba": "CAISO_NORTH",
}
```

### v3 request
```python
url = "https://api.watttime.org/v3/historical"
params = {
    "region": "CAISO_NORTH",
    "start": "2022-07-15T00:00+00:00",
    "end": "2022-07-15T00:05+00:00",
    "signal_type": "co2_moer",
}
```

# v2/forecast

This endpoint provided a forecast of the MOERs (e.g. CO2 lbs/MWh) for a specified region, by default the latest forecast was returned. The `/v3/forecast` endpoint is now used solely to get the most recent available forecast, the response is simplified because it only returns one set of forecast values. In v2, a 72-hour forecast could be requested using the optional parameter `extended_forecast` and in v3 you can request the specific length of `forecast_horizon` that you'd like from 0-72 hours.

### v2 request (latest forecast)
```python
url = "https://api2.watttime.org/v2/forecast"
params = {
    "ba": "CAISO_NORTH",
    "extended_forecast": "True",
}
```

### v3 request (latest forecast)
```python
url = "https://api.watttime.org/v3/forecast"
params = {
    "region": "CAISO_NORTH",
    "signal_type": "co2_moer",
    "horizon_hours": 72,
}
```

In v2, a batch of historical forecasts could be requested using the optional parameters `starttime` and `endtime` to bound the `generated_at` time. In v3, we've moved this request to a new endpoint and the response is a similar but nested version of the v3/forecast response since it is designed for returning multiple sets of forecasts, one for each `generated_at` time.

### v2 request (historical forecast)
```python
url = "https://api2.watttime.org/v2/forecast"
params = {
    "ba": "CAISO_NORTH",
    "starttime": "2023-07-15T00:00+00:00",
    "endtime": "2023-07-15T00:05+00:00",
}
```

### v3 request (historical forecast)
```python
url = "https://api.watttime.org/v3/forecast/historical"
params = {
    "region": "CAISO_NORTH",
    "signal_type": "co2_moer",
    "start": "2023-07-15T00:00+00:00",
    "end": "2023-07-15T00:05+00:00",
}
```

# v2/maps
This endpoint provided a GeoJSON of the grid region boundary for all regions that WattTime covers globally. The biggest change here besides the URL, is that a `signal_type` is now required in the request since there are different maps for each. The response also includes the `signal_type` and is otherwise identical to the v2 response.

### v2 request
```python
url = "https://api2.watttime.org/v2/maps"
```

### v3 request
```python
url = "https://api.watttime.org/v3/maps"
params = {
    "signal_type": "co2_moer",
}
```

# v2/avgemissions

Average emissions have been rolled into the standard data path under the signal_type `co2_aoer`. The request and response schema otherwise matches the above schema for v3/historical data. In order to distinguish between the default model (full quality) and the backup model (imputed, lower quality) data points, there is a new query parameter `include_imputed_marker` that will provide a point-wise indication in the response of data points that were generated with imputed data (`imputed_data_used=true`, equivalent to the old `3.0-modeled` version).

### v2 request
```python
url = "https://api2.watttime.org/v2/avgemissions"
params = {
    "ba": "CAISO_NORTH",
}
```

### v3 request
```python
url = "https://api.watttime.org/v3/historical"
params = {
    "region": "CAISO",
    "signal_type": "co2_aoer",
    "start": "2023-07-15T00:00+00:00",
    "end": "2023-07-15T00:05+00:00",
    "include_imputed_marker": True,
}
```
