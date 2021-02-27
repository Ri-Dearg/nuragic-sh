// Code from : https://www.jujens.eu/posts/en/2020/Feb/29/django-pwa
const VERSION = "{{ version }}";
const staticCachePrefix = "static";
const staticCacheName = `${staticCachePrefix}-${VERSION}`;
const dynamicCacheName = "dynamic";

self.addEventListener("install", (event) => {
  console.log("[SW] Installing SW version:", VERSION);
  event.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      console.log("[SW] Caching app shell");
      cache.addAll(["/static/manifest.json", "/"]);
    })
  );
});

self.addEventListener("fetch", (event) => {
  // Let the browser do its default thing
  // for non-GET requests.
  if (event.request.method !== "GET") {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      console.log(`[SW] Requesting ${event.request.url}.`);
      // If we have the response in the cache, we return it.
      // If not, we try to fetch it.
      if (response) {
        console.log(
          `[SW] Served response to ${event.request.url} from the cache.`
        );
        return response;
      }

      return fetch(event.request)
        .then((res) => {
          return caches.open(dynamicCacheName).then((cache) => {
            // We can read a response only once. So if we don't clone it here,
            // we won't be able to see anything in the browser.
            cache.put(event.request.url, res.clone());
            return res;
          });
        })
        .catch((err) => {
          console.warn(
            "[SW] Network request failed, app is probably offline",
            err
          );
          return caches.open(staticCacheName);
        })
        .then((cache) => {
          // If the request expects an HTML response, we display the offline page.
          if (event.request.headers.get("accept").includes("text/html")) {
            return cache.match("/offline/");
          }

          return Promise.reject();
        })
        .catch((err) =>
          console.warn(
            "[SW] failed to get response from network and cache.",
            err
          )
        );
    })
  );
});
