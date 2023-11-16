We're excited to upgrade our API after about 5 years on the same version. We don't undertake this lightly, and endeavor to avoid breaking changes whenever possible. We think the upgrades we've made available in API v3 will be well worth the effort to update your code, and we’re happy to support you as you make the transition. Please contact us with questions, support@WattTime.org.

After an overview including a description of miscellaneous changes, the rest of this guide is meant to help you translate your existing v2 requests into their respective v3 requests and handle any differences in the responses that come back.

# Overview

At a high level, the biggest change between v2 and v3 is a disambiguation of the `/v2/data` endpoint – since these data
are best used in historical analysis rather than real-time optimization, we’re now housing these data in the
`/v3/historical` endpoint.


The `/v3/forecast` endpoint continues to provide forecast data for real time optimization, across a number of different signal types. There is now a dedicated `/v3/forecast/historical` endpoint for gathering historical forecasts for retrospective analyses.

WattTime is adding support for a number of new signal types, including: `health_damage` (both forecast and historical), and `co2_aoer` (historical only, for accounting purposes). WattTime’s marginal operating emissions rate has been named `co2_moer` to disambiguate from other signals with equivalent units.

Most query responses will now contain two stanzas: `data` and `meta`. The content in `data` includes point times, values, and optional pointwise metadata related to the filtering criteria provided in an array. The content in `meta` describes the returned data, including any potential warnings or issues encountered.

Geographic regions were formerly identified as `abbrev` and `ba` (for balancing authority), and in v3 will be known as `region` (which is inclusive of balancing authorities and subregions). `region` is also a unique identifier across all endpoints.

Where in the past a user could request data from `/v2/data` using GPS lat/long as inputs, the `/v3/historical` endpoint now accepts only the region parameter as input to define the location.

Time zones are now required on all user-provided timestamps. Previously in v2 if timestamps lacked time zone information, UTC was assumed. That must now be made explicit in v3 in the request.

There are fairly significant changes to how model versions are expressed in both historical data and forecasted data. WattTime is shifting towards date-based modeling to remove some confusion around the significance of model versions. WattTime uses one of a set of models depending on what data is available for a given region, and the model type is now expressed in the meta stanza of a response. Learn more about the various model types here <link to model types page>.

# Forecast
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

# Data
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

# Avgemissions
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

# ba-from-loc
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
{"region":"SPP_WESTNE","region_full_name":"SPP Western Nebraska"}
```

# maps
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


# access
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
