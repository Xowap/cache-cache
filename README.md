# Cache Cache

A simple project to demonstrate how with a Flask app and an Apache Traffic
Server reverse proxy you can leverage ETags in order to keep your cache fresh
and your server cool.

There are two components:

-   `backend` is a very simple Flash application which demonstrates the `ETag`
    functionality. You can run it by its own to check how the browser behaves or
    you can run it behind the cache
-   `cache` is the ATS reverse proxy which will serve as a cache in front of
    your backend.

In order to run the whole thing, you can use Docker Compose:

```
docker-compose up --build
```

Then visit http://localhost:9000 with your browser. You should be able to see a
page giving you both an ETag and a random string. Between refreshes, both values
should be constant:

-   The ETag won't change until you click the button
-   The random string should stay in cache as long as you don't change the ETag

You should be able to visit this URL from different browser and see the same
result out of the cache every single time.

When you click on the "Change ETag" button from any browser, refreshing from any
browser should again show you consistent results across all requests, with the
cache being refreshed for all clients.
