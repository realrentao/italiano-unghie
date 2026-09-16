const CACHE = 'ita-audio-v1';
const AUDIO_RE = /\/audio\/[^?]+\.mp3(\?.*)?$/;
self.addEventListener('install', function(e){ self.skipWaiting(); });
self.addEventListener('activate', function(e){
  e.waitUntil((async function(){
    var keys = await caches.keys();
    await Promise.all(keys.filter(function(k){ return k !== CACHE; }).map(function(k){ return caches.delete(k); }));
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', function(e){
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (AUDIO_RE.test(url.pathname)){
    e.respondWith((async function(){
      var cache = await caches.open(CACHE);
      var cached = await cache.match(req);
      if (cached) return cached;
      try {
        var res = await fetch(req);
        if (res && res.ok) cache.put(req, res.clone());
        return res;
      } catch(err){ return cached || Response.error(); }
    })());
  }
});
