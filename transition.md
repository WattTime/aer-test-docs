# High level notes
At a high level, the biggest change between v2 and v3 is a disambiguation of the `/v2/data` endpoint – since these data
are best used in historical analysis rather than real time optimization, we’re now housing these data in the
`/v3/historical` endpoint.


The `/v3/forecast` endpoint continues to provide forecast data for real time optimization, across a number of different signal types.

WattTime is adding support for a number of new signal types, including: health_damage (both forecasted and historical), and co2_aoer (historical only, for accounting purposes). WattTime’s marginal operating emissions rate has been named co2_moer to disambiguate from other signals with equivalent units.


As a generalization, most query responses will now contain two stanzas: data and meta. data contains point times, values and optional pointwise metadata related to the filtering criteria provided in an array, and meta is a map/dictionary describing the returned data, including any potential warnings or issues encountered.


Where in the past a user could request data from `/v2/data` and `/v2/index` using GPS lat/long as inputs, these
endpoints `/v3/historical` and `/v3/forecast/index` now accept only the region parameter as input to define the location.

In order to avoid potential ambiguity and confusion, timezones are now required on all user-provided timestamps. Previously if timestamps lacked timezone information, UTC was assumed. That must now be made explicit at request time.

There are fairly significant changes to how model versions are expressed in both historical data and forecasted data. WattTime is shifting towards date-based modeling to remove some confusion around the significance of model versions. WattTime uses a set of models depending on what data is available for a given region, and the model type is now expressed in the meta stanza of a response. See (here)[#section/Marginal-Operating-Emissions-Rate-(MOER)-Model-Hierarchy] for more information.

# /v2/forecast → /v3/forecast
## Notes:

The `/v3/forecast` endpoint provides the currently applicable forecast. The response has been simplified compared to v2.

The first point of a forecast in the v3 schema holds data that applies to the current time period, aka the real-time data point. This endpoint is guaranteed to return data in all cases, including if data is missing upstream, and therefore should be relied on exclusively for real-time services like optimization.

Historical forecasts (forecasts generated at times in the past) are accessible via the `/v3/forecast/historical` endpoint, which is described in further detail below.
### From (v2 schema):
```json
[
  {
    "generated_at": "2022-12-19T18:50:00+00:00",
    "forecast":
      [
        {
          "point_time": "2022-12-19T18:55:00+00:00",
          "ba": "CAISO_NORTH",
          "value": 1048.4131919701972,
          "version": "3.2-1.0.0"
        },
        {
          "point_time": "2022-12-19T19:00:00+00:00",
          "ba": "CAISO_NORTH",
          "value": 1051.0880801214637,
          "version": "3.2-1.0.0"},
         ...<24/72 hours worth of datapoints>...
      ]
  }
]
```
### To (v3 schema):
#### Real time forecasts (`/v3/forecast`):
```json
{
    "data": [
       {
          "point_time": "2022-07-15T00:00:00+00:00",
          "value": 1048.4131919701972
        },
        {
          "point_time": "2022-07-15T00:05:00+00:00",
          "value": 1051.0880801214637
         },
         ...<1-72 hours worth of datapoints>...
    ],
 "meta": {
   "data_point_period_seconds": 300,
    "region": "CAISO_NORTH",
    "warnings":
       [
        {
          "type": "EXAMPLE_WARNING",
          "message": "This is just an example"
        }
       ],
     "signal_type": "co2_moer",
     "model":
       {
        "date": "2023-03-01"
       },
     "units": "lbs_co2_per_mwh",
     "generated_at_period_seconds": 300,
     "generated_at": "2022-07-15T00:00:00+00:00"
 }
}
```

#### Historical forecasts (`/v3/forecast/historical`):

```json
{
  "data": [
    {
            "generated_at": "2022-07-15T00:00:00+00:00",
            "forecast": [
        {
                   "point_time": "2022-07-15T00:00:00+00:00",
                   "value": 870
              },
                 ...<24/72 hours worth of datapoints>...
              {
                   "point_time": "2022-07-15T23:55:00+00:00",
                   "value": 870
              }
             ]
    },
    ...<other requested forecasts>...
 ],
  "meta": {
        "data_point_period_seconds": 300,
        "region": "CAISO_NORTH",
        "warnings": [
              {
                  "type": "EXAMPLE_WARNING",
                  "message": "This is just an example"
              }
        ],
        "signal_type": "co2_moer",
        "model": {
              "date": "2023-03-01"
        },
        "units": "lbs_co2_per_mwh",
        "generated_at_period_seconds": 300
  }
}
```

# /v2/data (or /v2/index style: ‘moer’) → /v3/historical
## Notes:
Historical data can be updated post-hoc if WattTime receives higher quality upstream data, and correspondingly is not guaranteed to be produced without delay like forecasts. These data points should be used primarily for historical analysis and not for real time optimization.

### From (`/v2/data` schema):
```json
[
    {"point_time": "2022-11-17T04:45:00.000Z", "value": 937.0, "frequency": 300, "market": "RTM", "ba": "CAISO_NORTH", "datatype": "MOER", "version": "3.2"},
    {"point_time": "2022-11-17T04:40:00.000Z", "value": 937.0, "frequency": 300, "market": "RTM", "ba": "CAISO_NORTH", "datatype": "MOER", "version": "3.2"},
    {"point_time": "2022-11-17T04:35:00.000Z", "value": 937.0, "frequency": 300, "market": "RTM", "ba": "CAISO_NORTH", "datatype": "MOER", "version": "3.2"},
    {"point_time": "2022-11-17T04:30:00.000Z", "value": 937.0, "frequency": 300, "market": "RTM", "ba": "CAISO_NORTH", "datatype": "MOER", "version": "3.2"}
]
```


### To (v3 schema):
```json
{
  "data": [
        {
            "point_time": "2022-07-15T00:00:00+00:00",
            "value": 870
        },
        {
            "point_time": "2022-07-15T00:05:00+00:00",
            "value": 860
        }
  ],
  "meta": {
        "data_point_period_seconds": 300,
        "region": "CAISO_NORTH",
        "warnings": [
            {
                "type": "EXAMPLE_WARNING",
                "message": "This is just an example"
            }
        ],
        "signal_type": "co2_moer",
        "model": {
            "type": "binned_regression",
            "date": "2023-03-01"
        },
        "units": "lbs_co2_per_mwh"
  }
}
```

# /v2/avgemissions → /v3/historical
## Notes:
Average emissions have been rolled into the standard data path under the signal_type `co2_aoer`. The schema matches the above schema for `/v3/historical` data. In order to distinguish between true and modeled data points, there is a new query parameter include_imputed_marker that will distinguish point-wise between data points that were generated with imputed data (imputed_data_used=true, equivalent to the old 3.0-modeled version).

### From (v2 schema):
```json
[
  {
     "point_time": "2023-10-26T14:00:00+00:00",
          "datatype": "AOER",
          "frequency": 3600,
          "ba": "IT",
          "value": 1267.717268507,
          "version": "3.0"
    },
  {
     "point_time": "2023-10-26T15:00:00+00:00",
          "datatype": "AOER",
          "frequency": 3600,
          "ba": "IT",
          "value": 1267.717268507,
          "version": "3.0-modeled"
    }
]
```

### To (v3 schema):
```
{
  "data": [
        {
            "point_time": "2023-10-26T14:00:00+00:00",
            "value": 1267.717268507,
            "imputed_data_used": false
        },
        {
            "point_time": "2023-10-26T14:00:00+00:00",
            "value": 1267.717268507,
            "imputed_data_used": true
        }
  ],
  "meta": {
        "data_point_period_seconds": 3600,
        "region": "CAISO_NORTH",
        "warnings": [
            {
                "type": "EXAMPLE_WARNING",
                "message": "This is just an example"
            }
        ],
        "signal_type": "co2_aoer",
        "model": {
            "type": "average",
            "date": "2023-03-01"
        },
        "units": "lbs_co2_per_mwh"
  }
}
```

# /index → /v3/forecast/index
## Notes:
Previously, the index value was the statistical percentile value of the current MOER relative to the last 30 days of MOER values for the specified location (100=dirtiest, 0=cleanest). In the v3 API, the index values are now calculated using a 24h lookahead (based on the forecast, rather than historical values). This is a more impactful metric for decision-making. Parameters for the index schema are equivalent to the `/v3/forecast` schema.

### From (v2 schema):
```json
{
    "freq": "300",
    "ba": "CAISO_NORTH",
    "percent": "53",
    "moer": "850.743982",
    "point_time": "2019-01-29T14:55:00.00Z"
}
```

### To (v3 schema):


```json
{
  "data": [
        {
            "point_time": "2022-07-15T00:00:00+00:00",
            "value": 50
        },
        {
            "point_time": "2022-07-15T00:05:00+00:00",
            "value": 100
        }
  ],
  "meta": {
        "data_point_period_seconds": 300,
        "region": "CAISO_NORTH",
        "warnings": [
            {
                "type": "EXAMPLE_WARNING",
                "message": "This is just an example"
            }
        ],
        "signal_type": "co2_moer",
        "model": {
            "type": "binned_regression",
            "date": "2023-03-01"
        },
        "units": "percentile"
  }
}
```

# /v2/ba-from-loc → /v3/region-from-loc
## Notes:
Region requests from latitude/longitude pairs are also now specific to a `signal_type` (and require this parameter in each query).


Example (python):
```python
import requests
from requests.auth import HTTPBasicAuth


lat, lon = 41.5, -104  # SPP_WESTNE
SIGNAL = 'co2_moer'


region_url = 'https://api.watttime.org/v3/region-from-loc'
headers = {'Authorization': f'Bearer {token}'}
params = {'latitude': f'{lat}',
          'longitude': f'{lon}',
          'signal_type': SIGNAL
         }
rsp=requests.get(region_url, headers=headers, params=params)
print(rsp)
print(rsp.text)


Response:
<Response [200]>
{"abbrev":"SPP_WESTNE","name":"SPP Western Nebraska"}
```

# /v2/maps → /v3/maps
## Notes:
Maps are now specific to a `signal_type` (and require this parameter in each query). The associated `signal_type` is included in the meta field in the response.


Example (python)
```python
import requests
from os import path

SIGNAL = 'co2_moer'

params = {'signal_type': SIGNAL}
url = 'https://api.watttime.org/v3/maps'
headers = {'Authorization': 'Bearer {}'.format(token)}
rsp=requests.get(url, headers=headers, params=params)


cur_dir = path.dirname(path.realpath('__file__'))
file_path = path.join(cur_dir, f'wt_map_{SIGNAL}.geojson')
with open(file_path, 'wb') as fp:
    fp.write(rsp.content)


print(rsp)
print(f'Wrote /maps geojson to {file_path}')
```


# /v2/ba-access → /v3/my-access
## Notes:
This endpoint is a guide to what is available to your account on the API. It provides a hierarchical JSON output that describes the signals, regions, endpoints, and model-dates and any available associated meta data for available data (in that hierarchical order).


Example (python)
```python
myaccess_url = 'https://api.watttime.org/v3/my-access'
headers = {'Authorization': 'Bearer {}'.format(token)}
rsp = requests.get(myaccess_url, headers=headers)


# print(rsp.text)
from IPython.display import JSON
JSON(rsp.text)
```
