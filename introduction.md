The WattTime API provides access to real-time, forecast, and historical data for electric grids around the world, including marginal emissions data. For the different signals we provide, see the [data signals page](https://www.watttime.org/data-signals).

If you’re curious about what you can do with this data, [see the solutions we support](https://www.watttime.org/), where you can dive into the various use cases. A common example of how to use the MOER value is to schedule load at the cleanest times of day.

You can access the API by sending standard HTTP requests to the endpoints listed below. The `/v3/historical`, `/v3/forecast`, and `/v3/maps` endpoints are only available to subscribers. However, if you don’t yet have a subscription, you can preview all of the available region-specific data by providing `CAISO_NORTH` as the region for your requests. A comparison of the different available data plans can be found [here](https://www.watttime.org/docs-dev/data-plans/).

Python3 example code is provided in the right pane of this documentation which shows how to interact with the API endpoints. You can kick start your development by using our [python client/SDK](https://github.com/WattTime/watttime-python-client).

## Restrictions

There is a strict limit on the rate at which you may query the API. From any user, we allow a maximum of 3,000 requests in any 5-minute rolling window (an average of 10 requests per second). There is also a lower limit specific to the `/login` endpoint, which is 100 requests in 5 minutes. If requests exceed this, an `HTTP 429` error code is returned.

**The API rate limit is a total of 3,000 requests in 5 minutes (an average of 10 per second). The limit for /login is 100 requests in 5 minutes.**

## API Status Page and User Alerts

WattTime publishes the current and historical uptime on the [API Status Page](https://status.watttime.org/). This page shows upcoming scheduled maintenance and provides updates during outages or maintenance. Users should subscribe to alerts via the status page to be kept up to date. This page is our method of communicating updates to our users related to maintenance, outages, and announcements related to version upgrades. Follow these instructions to subscribe to alerts:
1. Navigate to the [WattTime API Status Page](https://status.watttime.org/)
1. Click the 'subscribe to updates' button in the top right corner
1. Select your preferred means of notification (email, SMS, Slack, webhook)
1. Enter your contact information (this will not be used for any other purpose)

## Best Practices for API Usage
If using this API to control many smart devices in different locations, we suggest the following protocol. For each device location, use GPS lat/lon to query `/v3/region-from-loc` in order to determine the region for the desired `signal_type`. Then, query the other endpoints (e.g. `/v3/forecast`, `/v3/historical`, etc.) with the resulting region to receive signal data.

Because grid region boundaries are occasionally updated, it is important to re-query `/v3/region-from-loc` at least once a month to ensure devices are receiving the signal corresponding to their location. The `/v3/maps` endpoint provides a GeoJSON that can be used for offline geocoding. The GeoJSON file includes a `last_updated` field that changes whenever the grid regions change.
