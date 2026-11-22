/* LittleSprout service worker.
   Strategy:
     - shell (all top-level pages, manifest, icons) precached on install
     - game pages, their backgrounds and their character sprites precached on install
     - everything else (books, sprites) cached the first time it is opened,
       so a book a child has read once will still open with no connection.
   Bump CACHE_VERSION whenever site files change, so old copies are cleared. */

const CACHE_VERSION = 'littlesprout-v45';

const SHELL = [
  './',
  './index.html',
  './characters.html',
  './privacy.html',
  './grants.html',
  './resources.html',
  './stats.html',
  './rewards.html',
  './shop.html',
  './book-nook.html',
  './book-nook-bookplate.html',
  './reading-passport.html',
  './board.html',
  './manifest.json',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png'
];

// Games pick characters and poses at random, so a game can ask for any sprite
// in these sets on its first draw. Cache them all at install so the games open
// offline before the child has ever seen a given pose.
const GAME_PAGES = [
  './games/feelings_faces.html',
  './games/pose_parade.html',
  './games/rhyme_time.html',
  './games/sentence_builder.html',
  './games/sound_it_out.html',
  './games/whos_missing.html',
  './games/word_dash.html',
  './games/helper_detective.html',
  './games/garden_harvest.html',
  './games/block_balance.html',
  './games/bug_safari.html',
  './games/river_hop.html'
];

const GAME_BACKGROUNDS = [
  './assets/backgrounds/classroom_2.jpg',
  './assets/backgrounds/firestation_2.jpg',
  './assets/backgrounds/library_2.jpg',
  './assets/backgrounds/police_2.jpg',
  './assets/backgrounds/garden_2.jpg',
  './assets/backgrounds/bakery_2.jpg',
  './assets/backgrounds/repair.jpg',
  './assets/backgrounds/center.jpg',
  './assets/backgrounds/garden_3.jpg',
  './assets/backgrounds/garden_4.jpg',
  './assets/backgrounds/classroom_3.jpg',
  './assets/backgrounds/school_3.jpg',
  './assets/games/garden_harvest_bad.jpg',
  './assets/games/garden_harvest_bg.jpg',
  './assets/games/garden_harvest_item1.jpg',
  './assets/games/garden_harvest_item2.jpg'
];

const SPRITE_CHARACTERS = ['maya', 'marcus', 'sophie', 'james'];
const SPRITE_MOODS = ['happy', 'sad', 'surprised', 'frustrated', 'neutral'];
const HAPPY_POSES = ['standing', 'waving', 'hands', 'looking', 'jumping', 'pointing', 'kneeling', 'running', 'sitting'];
const OTHER_POSES = ['standing', 'waving', 'hands', 'looking'];

function gameSpriteUrls() {
  var urls = [];
  SPRITE_CHARACTERS.forEach(function (id) {
    SPRITE_MOODS.forEach(function (mood) {
      var poses = mood === 'happy' ? HAPPY_POSES : OTHER_POSES;
      poses.forEach(function (pose) {
        urls.push('./assets/sprites/' + id + '_' + mood + '_' + pose + '.png');
      });
    });
  });
  return urls;
}

const PRECACHE = SHELL.concat(GAME_PAGES, GAME_BACKGROUNDS, gameSpriteUrls());

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then(function (cache) {
        // addAll is all-or-nothing; add individually so one miss can't break install
        return Promise.all(PRECACHE.map(function (url) {
          return cache.add(url).catch(function () { return null; });
        }));
      })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE_VERSION) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

function putInCache(req, res) {
  if (res && res.status === 200 && res.type === 'basic') {
    var copy = res.clone();
    caches.open(CACHE_VERSION).then(function (cache) { cache.put(req, copy); });
  }
  return res;
}

self.addEventListener('fetch', function (event) {
  var req = event.request;

  // only handle same-origin GETs; let fonts/CDNs go straight to network
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== self.location.origin) return;

  // HTML pages (navigations): network-first. A page that's already cached
  // used to be served instantly and stale -- CACHE_VERSION bumping only
  // helps from the SECOND visit onward, since the first post-deploy load
  // still hit the old cache entry before the background refresh finished.
  // Network-first means anyone online always sees the current page; the
  // cache is only the fallback when there's no connection at all.
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').indexOf('text/html') !== -1) {
    event.respondWith(
      // 'reload' bypasses the browser's own HTTP cache, not just the SW
      // cache above it -- fetch(req) alone can still return a
      // browser-cached response for a page with no explicit Cache-Control
      // header (GitHub Pages doesn't set one), which would silently
      // defeat network-first the same way cache-first did.
      fetch(req, { cache: 'reload' }).then(function (res) {
        return putInCache(req, res);
      }).catch(function () {
        return caches.match(req).then(function (cached) {
          return cached || caches.match('./index.html');
        });
      })
    );
    return;
  }

  // Everything else (sprites, backgrounds, icons, manifest): cache-first
  // with a background refresh. These are content-addressed by filename
  // and change rarely relative to page markup, so instant-from-cache is
  // the right tradeoff -- especially for offline reading of a book a
  // child has already opened once.
  event.respondWith(
    caches.match(req).then(function (cached) {
      var network = fetch(req).then(function (res) {
        return putInCache(req, res);
      }).catch(function () {
        return cached;
      });
      return cached || network;
    })
  );
});
