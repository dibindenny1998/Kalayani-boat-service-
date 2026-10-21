/* Home page hero: the sky over the backwater follows the time in Alleppey.
   The sun rises and sets, the Kalyani shikara glides across, and the line under the hero names the tour on the water now or next. */
(() => {
  const K = window.KALYANI;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const cv = document.getElementById("sky"), stage = document.getElementById("stage"), now = document.getElementById("now");
  if (!cv) return;
  const cx = cv.getContext("2d");
  const hh = v => { const H = Math.floor(v), M = Math.round((v - H) * 60); return String(H).padStart(2, "0") + ":" + String(M % 60).padStart(2, "0"); };

  /* time in Alleppey (IST), whatever the visitor's own time zone */
  const istHour = () => { const p = new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Kolkata", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date());
    const g = t => +p.find(x => x.type === t).value; return (g("hour") % 24) + g("minute") / 60; };
  let real = istHour();
  /* overnight the scene waits at first light, ready for the Sunrise Cruise */
  const sceneHour = h => (h >= 5 && h <= 19.6) ? h : 5.4;
  let hour = sceneHour(real);

  function label() {
    if (!now) return;
    const tours = K.tours.filter(t => t.start !== null);
    const on = tours.filter(t => real >= t.start && real < t.end);
    const next = tours.filter(t => t.start > real).sort((a, b) => a.start - b.start)[0];
    const link = t => `<a href="${t.slug}.html">${t.name}</a>`;
    now.innerHTML = `<b>${hh(real)}</b><span>in Alleppey.</span> ` + (on.length ? `<span>On the water now: ${on.map(link).join(", ")}.</span>` : "")
      + (next ? ` <span>Next out: ${link(next)} at ${hh(next.start)}.</span>` : ` <span>Tomorrow: ${link(tours[0])} at ${hh(tours[0].start)}.</span>`);
  }

  const SKY = [[4.5,"#0f1424","#1d2238","#2a2c48"],[6,"#3c3a66","#b77a8e","#f3b48a"],[7.5,"#7f9fc0","#e9c3a8","#f8dcc0"],[11,"#5f97bb","#a9cbd8","#dfeceb"],[15,"#6f9cba","#c6d3c9","#f2dfb8"],[17.6,"#3b2f52","#b2475a","#f28a3c"],[18.6,"#1b1630","#4a2540","#a8433c"],[19.6,"#0f1424","#1d2238","#2a2c48"],[20,"#0f1424","#1d2238","#2a2c48"]];
  const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  const css = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  function skyAt(h) { let i = 0; while (i < SKY.length - 2 && h > SKY[i + 1][0]) i++; const a = SKY[i], b = SKY[i + 1], t = Math.min(1, Math.max(0, (h - a[0]) / (b[0] - a[0]))); return [1, 2, 3].map(j => mix(rgb(a[j]), rgb(b[j]), t)); }

  let W = 0, H = 0;
  function size() { const dpr = Math.min(2, devicePixelRatio || 1); W = stage.clientWidth; H = stage.clientHeight; cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  const trees = []; for (let i = 0; i <= 60; i++) trees.push(.5 + .5 * Math.sin(i * 1.7) + .35 * Math.sin(i * .53 + 1) + ((i * 37) % 10) / 33);

  function palm(x, y, s, c) {
    cx.strokeStyle = c; cx.lineWidth = 2.2 * s; cx.beginPath(); cx.moveTo(x, y); cx.quadraticCurveTo(x + 8 * s, y - 60 * s, x + 2 * s, y - 110 * s); cx.stroke();
    const tx = x + 2 * s, ty = y - 110 * s; cx.lineWidth = 1.6 * s;
    for (let k = 0; k < 7; k++) { const a = -Math.PI * .95 + k * Math.PI / 6.2; cx.beginPath(); cx.moveTo(tx, ty); cx.quadraticCurveTo(tx + Math.cos(a) * 30 * s, ty + Math.sin(a) * 22 * s - 6 * s, tx + Math.cos(a) * 48 * s, ty + Math.sin(a) * 12 * s + 16 * s); cx.stroke(); }
  }

  /* the Kalyani shikara, facing right: tall curled bow with its gold border, black hull with orange trim, coir canopy on turned teak pillars */
  function shikara(x, y, s, sky) {
    const tone = (h, k = .3) => css(mix(rgb(h), sky, k)), P = (px, py) => [x + px * s, y + py * s];
    const M = (px, py) => cx.moveTo(...P(px, py)), L = (px, py) => cx.lineTo(...P(px, py)), Q = (a, b, c, d) => cx.quadraticCurveTo(...P(a, b), ...P(c, d));
    cx.lineCap = "round"; cx.lineJoin = "round";
    cx.fillStyle = tone("#15130f", .2); cx.beginPath();
    M(-76, -13); Q(-70, 3, -46, 5); L(44, 5); Q(70, 4, 78, -20); Q(84, -42, 74, -54); Q(62, -50, 58, -36); Q(56, -22, 50, -9); L(-64, -9); Q(-71, -10, -76, -13); cx.closePath(); cx.fill();
    cx.strokeStyle = tone("#d9a52e"); cx.lineWidth = 2.6 * s; cx.beginPath(); M(51, -10); Q(56, -22, 58, -36); Q(62, -50, 74, -54); Q(84, -42, 78, -20); Q(72, -4, 58, 1); cx.stroke();
    cx.lineWidth = 1 * s; cx.setLineDash([1.5 * s, 2.5 * s]); cx.beginPath(); M(57, -12); Q(61, -30, 64, -40); Q(68, -48, 74, -49); cx.stroke(); cx.setLineDash([]);
    cx.strokeStyle = tone("#e8622c"); cx.lineWidth = 2.6 * s; cx.beginPath(); M(-68, -8); L(57, -8); cx.stroke();
    cx.lineWidth = 1.2 * s; cx.beginPath(); M(-64, -4); L(54, -4); cx.stroke();
    cx.strokeStyle = tone("#d8dcdc", .35); cx.lineWidth = 1 * s; cx.beginPath(); M(30, -17); Q(46, -19, 58, -14); cx.stroke();
    for (let i = 32; i <= 56; i += 4) { cx.beginPath(); M(i, -9); L(i, -17 + (i > 48 ? 2 : 0)); cx.stroke(); }
    cx.strokeStyle = tone("#7a4a24"); cx.lineWidth = 2.4 * s;
    for (const px of [-50, -32, -14, 4, 22]) { cx.beginPath(); M(px, -9); L(px, -33); cx.stroke(); }
    cx.fillStyle = tone("#b98a55"); cx.beginPath(); M(-58, -31); Q(-18, -46, 30, -31); L(30, -35); Q(-18, -52, -58, -35); cx.closePath(); cx.fill();
    cx.strokeStyle = tone("#e8622c"); cx.lineWidth = 1.4 * s; cx.setLineDash([2 * s, 2 * s]); cx.beginPath(); M(-56, -29); Q(-18, -43, 28, -29); cx.stroke(); cx.setLineDash([]);
    cx.fillStyle = tone("#ffc21a"); cx.fillRect(...P(-40, -14), 14 * s, 4 * s); cx.fillRect(...P(-6, -14), 14 * s, 4 * s);
  }

  let boatX = .62, t0 = performance.now(), visible = true, lastClock = 0;
  function draw(time) {
    /* keep the horizon and the boat above the headline, which takes more of the frame on tall phone screens */
    const [top, mid, hor] = skyAt(hour), hz = H * (W < H ? .36 : .44), tt = time / 1000;
    let g = cx.createLinearGradient(0, 0, 0, hz); g.addColorStop(0, css(top)); g.addColorStop(.6, css(mid)); g.addColorStop(1, css(hor)); cx.fillStyle = g; cx.fillRect(0, 0, W, hz);
    const p = (hour - 6) / (18.4 - 6), up = p > -.05 && p < 1.05, sx = W * (.12 + .76 * p), sy = hz - Math.sin(Math.PI * Math.min(1, Math.max(0, p))) * hz * .78 + (p < 0 || p > 1 ? 30 : 0), sr = Math.max(14, W * .028);
    if (up) {
      const halo = cx.createRadialGradient(sx, sy, 0, sx, sy, sr * 6); halo.addColorStop(0, "rgba(255,236,190,.55)"); halo.addColorStop(1, "rgba(255,236,190,0)"); cx.fillStyle = halo; cx.fillRect(0, 0, W, hz);
      cx.save(); cx.beginPath(); cx.rect(0, 0, W, hz); cx.clip(); cx.fillStyle = "#FFF1CF"; cx.beginPath(); cx.arc(sx, sy, sr, 0, 7); cx.fill(); cx.restore();
    }
    if (hour < 5.8 || hour > 18.9) { cx.fillStyle = "rgba(255,255,255,.7)"; for (let i = 0; i < 40; i++) { const x = (i * 97.3) % W, y = (i * 53.7) % (hz * .7); cx.globalAlpha = .3 + .5 * Math.abs(Math.sin(tt + i)); cx.fillRect(x, y, 1.4, 1.4); } cx.globalAlpha = 1; }
    const land = css(mix(top, [18, 22, 19], .82));
    cx.fillStyle = land; cx.fillRect(0, hz - 4, W, 4);
    for (let i = 0; i <= 60; i++) { cx.beginPath(); cx.arc(i / 60 * W, hz - 2, H * .01 + trees[i] * H * .014, Math.PI, 0); cx.fill(); }
    palm(W * .07, hz, Math.max(.7, H / 520), land); palm(W * .15, hz, Math.max(.55, H / 700), land); palm(W * .9, hz, Math.max(.6, H / 620), land);
    g = cx.createLinearGradient(0, hz, 0, H); g.addColorStop(0, css(mix(hor, [18, 22, 19], .35))); g.addColorStop(1, css(mix(top, [12, 15, 13], .75))); cx.fillStyle = g; cx.fillRect(0, hz, W, H - hz);
    if (up && sy < hz + 10) for (let y = hz + 2; y < H; y += 3) { const d = (y - hz) / (H - hz), w = sr * (1.2 + d * 5) * (.6 + .4 * Math.sin(y * .21 + tt * 2.2)), o = Math.sin(y * .13 + tt * 1.6) * 6 * d; cx.fillStyle = `rgba(255,226,170,${.42 * (1 - d)})`; cx.fillRect(sx - w / 2 + o, y, w, 1.6); }
    cx.fillStyle = "rgba(255,255,255,.08)"; for (let i = 0; i < 26; i++) { const y = hz + ((i * 37) % (H - hz)), x = ((i * 211 + tt * 12 * (1 + i % 3)) % (W + 80)) - 40; cx.fillRect(x, y, 30 + (i % 4) * 14, 1); }
    const by = hz + (H - hz) * .08, bs = Math.max(.7, W / 820), bx = boatX * W, bob = Math.sin(tt * 1.4) * 1.5;
    shikara(bx, by + bob, bs, top);
    cx.save(); cx.translate(0, 2 * (by + bob) + 10 * bs); cx.scale(1, -1); cx.globalAlpha = .2; shikara(bx + Math.sin(tt * 3) * 2, by + bob, bs, top); cx.restore();
  }
  function loop(time) {
    const dt = Math.min(.05, (time - t0) / 1000); t0 = time;
    if (time - lastClock > 30000) { lastClock = time; real = istHour(); hour = sceneHour(real); label(); }
    boatX += dt * .012; if (boatX > 1.15) boatX = -.15;
    if (visible) draw(time);
    requestAnimationFrame(loop);
  }
  size(); label();
  if (still) draw(0); else requestAnimationFrame(loop);
  addEventListener("resize", () => { size(); if (still) draw(0); });
  new IntersectionObserver(e => { visible = e[0].isIntersecting; }).observe(stage);
})();
