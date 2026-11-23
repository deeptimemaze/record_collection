// Opens the newest version when online and falls back to the saved copy offline.
// COVERS must match COVER_CACHE in index.html. The old 'vinyl-covers' cache held unreadable (opaque) responses, including failed ones; activate deletes it.
const CACHE='vinyl-shelf-v55',COVERS='vinyl-covers-2';
const FILES=['./','./index.html','./manifest.webmanifest','./icon-cyber-192.png','./icon-cyber-512.png'];
const COVER_HOST=/(^|\.)(coverartarchive|archive)\.org$/;
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES.map(f=>new Request(f,{cache:'reload'})))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==CACHE&&x!==COVERS).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);
  if(COVER_HOST.test(u.hostname)){
    // album art: keep a copy so covers you have seen still show offline.
    // Covers load with CORS, so failures are visible here and only real images are saved.
    e.respondWith(caches.open(COVERS).then(c=>c.match(e.request).then(hit=>hit||fetch(e.request).then(r=>{if(r.ok&&r.type!=='opaque')c.put(e.request,r.clone()).catch(()=>{});return r}))));
    return;
  }
  if(u.origin!==location.origin)return;
  // network first: new versions show up as soon as the app is opened; the cache is the offline fallback
  e.respondWith((async()=>{
    const c=await caches.open(CACHE);
    try{
      const r=await Promise.race([fetch(e.request,{cache:'no-cache'}),new Promise((_,no)=>setTimeout(no,4000))]);
      if(r.ok)c.put(e.request,r.clone());
      return r;
    }catch(err){
      return (await c.match(e.request,{ignoreSearch:true}))||(await c.match('./index.html'))||Response.error();
    }
  })());
});
