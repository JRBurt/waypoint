# Waypoint

A small Redis-backed service that sits in front of geocoding providers (Mapbox, OpenRouteService). Built to learn Redis properly: cache-aside with TTL, a rate limiter shared across callers, and a distributed lock to stop cache-stampedes when a hot key expires under load.

## Why

Geocoding and routing keep showing up as the shared need across a few other projects of mine - a TEU calculator for intermodal shipping, a bike route/commute calculator. Each one ends up needing the same thing: cache provider lookups, respect rate limits, don't let a stampede of concurrent requests hammer the API. Waypoint pulls that into its own service, built deliberately against Redis instead of improvised per-project.

## Running it locally

```bash
cp .configs.example.json .configs.json   # fill in your Mapbox/ORS tokens
docker-compose up
```

Then:

```
GET http://localhost:8080/geocode?provider=mapbox&q=900+Washington+Ave,+Golden,+CO
```

Without Docker: `pip install -r requirements.txt`, run a local Redis, then `python -m server`.

## Stack

Python stdlib (`http.server`), `redis-py`, `requests`. No framework, no ORM, no auth - deliberately minimal so the Redis patterns stay the point.
