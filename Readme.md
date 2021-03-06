# Event Target
A simple Python/Django based API to accept events with data and geolocate their source.

## Running
To run, clone the repo and `docker-compose up --build` The rest should be done automatically.

## Interacting with Event Target
You'll find the API under `127.0.0.1:8000/api/` There is a swagger based schema for the API at `127.0.0.1:8000/api/redoc/` or `127.0.0.1:8000/swagger/`

To send an event at the API you need to send a POST request to `127.0.0.1:8000/api/events/` with a JSON body following this schema

```json
{
  "name": "Signup",
  "data": {
    "any": "old",
    "thing": {
      "you": ["like"]
    },
    "as": ["long", "as", "It's", "JSON"]
  }
}
```

You should then get back immediately the saved representation of your event, with a UUID as the primary key, the data you filled in and the creation date. Nothing else at this point will be filled in as the Geo location part works via celery and is filled in shortly after saving.

If the application was deployed so that it could get a public IP with some location data, you would be able to make a GET request to `127.0.0.1:8000/api/events/<uuid>/` and see the filled in location data. The API will accept and continue to process requests with/without the API resolving.

## Limitations
Running under docker-compose, the IP address that is presented to the geolocation API is always private, and therefore doesn't end up with a location. A deployed instance wouldn't suffer this problem as it would either receive a public IP directly, or via upstream proxies and by using ipware it should be figured out automagically which IP to use.

There is no CI/CD setup, no pre-built docker image to pull and no terraform config. I'd want all of these for any deployment usually. 

Not everything is 12 factor, just whatever I added or needed to modify. A proper project would have any reasonably variable settings loaded as environment variables, with potential for defaults.

The tests are pretty limited, only covering a subsection of the API and I'd typically like to set up property based testing with Hypothesis, but I ran out of free time.

The solution to avoid overloading the API is kinda dependant on a single celery worker per instance of the location API. It's using exponential backoff and jitter based on the response from the geolocation API to avoid thundering herd. My preferred solution to this would be to work out why the API has random latency spikes and why it can't handle more requests, while also reducing repeated calls to the service for repeat IP addresses using caching.

The API docs are automatically generated and the output isn't the best. Typically you'd configure it a lot more, giving explanations for the various viewsets and more details on each method and what they do and why.

We don't currently use GeoDjango or any GIS functionality. Adding that would allow much more interesting searches than a square area inside a given lat/long range.

Lat/Long searches are currently not validated. GeoDjango could help there, but it's low priority as giving a nonsense lat/long for filtering doesn't harm anything.

If the Geo Location API is offline for a considerable amount of time, there could be legitimate events that could be geolocated which are missed. This can happen because Celery has a default cap on reties of 3. Resolution would be another task who would be scheduled to iterate over any fields that are missing location data. I would also add a short circuit for private IP addresses for the regular task and the batch task in such a way that they'd not come up again and don't waste calls to the Geo Location API

There is no Sentry, Datadog or other runtime error or profiling tools attached which I'd like to have

No KPI metrics are currently tracked, although the main ones could probably be retroactively generated if needed. I'd probably look to prometheus or riemann for that, although I've never used the latter before I have seen just how powerful it can be.

## Deployment
To deploy this application, I'd recommend sticking with docker, probably using either Kubes or AWS ECS, with an ALB or Nginx Sidecar container with public IP. I personally like using a combination of Terraform, Packer, a CI service like CircleCI or whatever to build and deploy everything.
