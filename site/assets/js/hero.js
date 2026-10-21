/* Home page hero: a whole day on the backwater.
   The sky plays from sunrise to sunset on a loop (about 40 seconds), the Kalyani shikara glides across,
   and the headline and the player show which tour is on the water at that hour.
   Visitors can pause, scrub the time, or jump to the real time in Alleppey. */
(() => {
  const K = window.KALYANI;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const cv = document.getElementById("sky"), stage = document.getElementById("stage");
  if (!cv) return;
  const cx = cv.getContext("2d");
  const $ = id => document.getElementById(id);
  const slider = $("hour"), clockEl = $("clock"), now = $("now"), playBtn = $("playbtn"), liveBtn = $("livebtn"), rot = $("rotator");
  const hh = v => { v = ((v % 24) + 24) % 24; const H = Math.floor(v), M = Math.floor((v - H) * 60); return String(H).padStart(2, "0") + ":" + String(M).padStart(2, "0"); };
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  const START = 5, END = 19.6, LOOP_SECONDS = 40;
  const istHour = () => { const p = new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Kolkata", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date());
    const g = t => +p.find(x => x.type === t).value; return (g("hour") % 24) + g("minute") / 60; };

  let hour = 5.6, playing = !still, resumeAt = 0;

  /* ---- words and labels that follow the hour ---- */
  const PHASES = [[8, "at sunrise"], [11.5, "over breakfast"], [15.3, "after lunch"], [18.8, "at sunset"], [99, "under the stars"]];
  let phase = "";
  function labels() {
    clockEl.textContent = hh(hour);
    slider.value = clamp(hour, START, END);
    const word = (PHASES.find(p => hour < p[0]) || PHASES[0])[1];
    if (rot && word !== phase) { phase = word; rot.innerHTML = `<span class="swap">${word}</span>`; }
    const tours = K.tours.filter(t => t.start !== null);
    const on = tours.filter(t => hour >= t.start && hour < t.end);
    const next = tours.filter(t => t.start > hour).sort((a, b) => a.start - b.start)[0];
    const link = t => `<a href="${t.slug}.html">${t.name}</a>`;
    now.innerHTML = on.length ? `On the water: ${on.slice(0, 2).map(link).join(" & ")}` : next ? `Next out: ${link(next)} at ${hh(next.start)}` : `Tomorrow: ${link(tours[0])} at 06:00`;
  }

  /* ---- the sky through the day: [hour, top, middle, horizon] ---- */
  const SKY = [[4.5,"#1d2257","#3b3778","#6a5aa0"],[5.8,"#5a5bb8","#ff8fab","#ffc48a"],[7,"#4fb0f0","#ffc4ae","#ffe4c2"],[10,"#2f9ff0","#7fcff5","#e2f6ff"],[14,"#3aa6ec","#9fdcf2","#fff0c4"],[16.6,"#5b7fd0","#ffb08a","#ffd27a"],[17.8,"#5b4aa6","#ff5e62","#ffa447"],[18.6,"#3b2a72","#c23b6b","#ff7a45"],[19.6,"#1d2257","#3b3778","#6a5aa0"],[20,"#1d2257","#3b3778","#6a5aa0"]];
  const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  const css = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  function skyAt(h) { let i = 0; while (i < SKY.length - 2 && h > SKY[i + 1][0]) i++; const a = SKY[i], b = SKY[i + 1], t = clamp((h - a[0]) / (b[0] - a[0]), 0, 1); return [1, 2, 3].map(j => mix(rgb(a[j]), rgb(b[j]), t)); }

  let W = 0, H = 0;
  function size() { const dpr = Math.min(2, devicePixelRatio || 1); W = stage.clientWidth; H = stage.clientHeight; cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  const bumps = []; for (let i = 0; i <= 70; i++) bumps.push(.5 + .5 * Math.sin(i * 1.7) + .35 * Math.sin(i * .53 + 1) + ((i * 37) % 10) / 33);

  function palm(x, y, s, trunk, leaf, sway) {
    cx.strokeStyle = trunk; cx.lineWidth = 4 * s; cx.lineCap = "round"; cx.beginPath(); cx.moveTo(x, y); cx.quadraticCurveTo(x + 14 * s, y - 70 * s, x + 6 * s, y - 130 * s); cx.stroke();
    const tx = x + 6 * s, ty = y - 130 * s; cx.strokeStyle = leaf; cx.lineWidth = 5 * s;
    for (let k = 0; k < 8; k++) { const a = -Math.PI * .98 + k * Math.PI / 7 + sway * .06; cx.beginPath(); cx.moveTo(tx, ty); cx.quadraticCurveTo(tx + Math.cos(a) * 34 * s, ty + Math.sin(a) * 26 * s - 10 * s, tx + Math.cos(a) * 62 * s, ty + Math.sin(a) * 14 * s + 24 * s); cx.stroke(); }
  }

  /* the Kalyani shikara, facing right: tall curled bow with its gold border, black hull with orange trim, coir canopy on teak pillars */
  function shikara(x, y, s, sky) {
    const tone = (h, k = .2) => css(mix(rgb(h), sky, k)), P = (px, py) => [x + px * s, y + py * s];
    const M = (px, py) => cx.moveTo(...P(px, py)), L = (px, py) => cx.lineTo(...P(px, py)), Q = (a, b, c, d) => cx.quadraticCurveTo(...P(a, b), ...P(c, d));
    cx.lineCap = "round"; cx.lineJoin = "round";
    cx.fillStyle = tone("#15130f", .12); cx.beginPath();
    M(-76, -13); Q(-70, 3, -46, 5); L(44, 5); Q(70, 4, 78, -20); Q(84, -42, 74, -54); Q(62, -50, 58, -36); Q(56, -22, 50, -9); L(-64, -9); Q(-71, -10, -76, -13); cx.closePath(); cx.fill();
    cx.strokeStyle = tone("#f0b62e"); cx.lineWidth = 2.8 * s; cx.beginPath(); M(51, -10); Q(56, -22, 58, -36); Q(62, -50, 74, -54); Q(84, -42, 78, -20); Q(72, -4, 58, 1); cx.stroke();
    cx.lineWidth = 1 * s; cx.setLineDash([1.5 * s, 2.5 * s]); cx.beginPath(); M(57, -12); Q(61, -30, 64, -40); Q(68, -48, 74, -49); cx.stroke(); cx.setLineDash([]);
    cx.strokeStyle = tone("#ff6a2c"); cx.lineWidth = 2.8 * s; cx.beginPath(); M(-68, -8); L(57, -8); cx.stroke();
    cx.lineWidth = 1.2 * s; cx.beginPath(); M(-64, -4); L(54, -4); cx.stroke();
    cx.strokeStyle = tone("#e6eaea", .25); cx.lineWidth = 1 * s; cx.beginPath(); M(30, -17); Q(46, -19, 58, -14); cx.stroke();
    for (let i = 32; i <= 56; i += 4) { cx.beginPath(); M(i, -9); L(i, -17 + (i > 48 ? 2 : 0)); cx.stroke(); }
    cx.strokeStyle = tone("#8a5226"); cx.lineWidth = 2.6 * s;
    for (const px of [-50, -32, -14, 4, 22]) { cx.beginPath(); M(px, -9); L(px, -33); cx.stroke(); }
    cx.fillStyle = tone("#c99a5e"); cx.beginPath(); M(-58, -31); Q(-18, -46, 30, -31); L(30, -35); Q(-18, -52, -58, -35); cx.closePath(); cx.fill();
    cx.strokeStyle = tone("#ff6a2c"); cx.lineWidth = 1.4 * s; cx.setLineDash([2 * s, 2 * s]); cx.beginPath(); M(-56, -29); Q(-18, -43, 28, -29); cx.stroke(); cx.setLineDash([]);
    cx.fillStyle = tone("#ffc21a"); cx.fillRect(...P(-40, -14), 14 * s, 4 * s); cx.fillRect(...P(-6, -14), 14 * s, 4 * s);
  }

  let boatX = .5, t0 = performance.now(), visible = true;
  function draw(time) {
    const [top, mid, hor] = skyAt(hour), narrow = W < H, hz = H * (narrow ? .5 : .6), tt = time / 1000;
    let g = cx.createLinearGradient(0, 0, 0, hz); g.addColorStop(0, css(top)); g.addColorStop(.62, css(mid)); g.addColorStop(1, css(hor)); cx.fillStyle = g; cx.fillRect(0, 0, W, hz);
    /* sun (or moon) on its arc across the sky */
    const p = (hour - 6.1) / (18.5 - 6.1), up = p > -.06 && p < 1.06;
    const sx = W * (.08 + .84 * clamp(p, 0, 1)), sy = hz - Math.sin(Math.PI * clamp(p, 0, 1)) * hz * .8 + (p < 0 || p > 1 ? 40 : 0), sr = Math.max(26, W * .042);
    const night = hour < 5.6 || hour > 19;
    if (night) { cx.fillStyle = "rgba(255,255,255,.85)"; for (let i = 0; i < 60; i++) { const x = (i * 97.3) % W, y = (i * 53.7) % (hz * .75); cx.globalAlpha = .25 + .6 * Math.abs(Math.sin(tt * .8 + i)); cx.fillRect(x, y, 1.6, 1.6); } cx.globalAlpha = 1;
      cx.fillStyle = "#FFF6DA"; cx.beginPath(); cx.arc(W * .78, hz * .26, sr * .7, 0, 7); cx.fill(); cx.fillStyle = css(top); cx.beginPath(); cx.arc(W * .78 + sr * .28, hz * .26 - sr * .1, sr * .62, 0, 7); cx.fill(); }
    if (up) {
      const warm = clamp(1 - Math.abs(p - .5) * 2.2, 0, 1), sun = mix([255, 140, 70], [255, 222, 90], warm);
      const halo = cx.createRadialGradient(sx, sy, 0, sx, sy, sr * 7); halo.addColorStop(0, css(sun, .5)); halo.addColorStop(1, css(sun, 0)); cx.fillStyle = halo; cx.fillRect(0, 0, W, hz);
      cx.save(); cx.beginPath(); cx.rect(0, 0, W, hz); cx.clip(); cx.fillStyle = css(sun); cx.beginPath(); cx.arc(sx, sy, sr, 0, 7); cx.fill(); cx.restore();
    }
    /* soft clouds drifting */
    cx.fillStyle = css(mix([255, 255, 255], mid, .2), night ? .06 : .32);
    for (let i = 0; i < 3; i++) { const x = ((i * 520 + tt * (6 + i * 2)) % (W + 400)) - 200, y = hz * (.12 + i * .12), w = 120 + i * 40; cx.beginPath(); cx.ellipse(x, y, w, 9 + i * 2, 0, 0, 7); cx.fill(); cx.beginPath(); cx.ellipse(x + w * .3, y - 8, w * .5, 8, 0, 0, 7); cx.fill(); }
    /* far tree line */
    const land = css(mix(top, [24, 104, 66], .72)), landFar = css(mix(hor, [40, 120, 80], .55));
    cx.fillStyle = landFar; for (let i = 0; i <= 70; i++) { cx.beginPath(); cx.arc(i / 70 * W, hz - 3, H * .012 + bumps[(i + 9) % 70] * H * .012, Math.PI, 0); cx.fill(); }
    cx.fillStyle = land; cx.fillRect(0, hz - 3, W, 5); for (let i = 0; i <= 70; i++) { cx.beginPath(); cx.arc(i / 70 * W + 7, hz, H * .008 + bumps[i] * H * .01, Math.PI, 0); cx.fill(); }
    /* water */
    const water = mix(hor, [15, 163, 163], .55), deep = mix(top, [11, 110, 112], .6);
    g = cx.createLinearGradient(0, hz, 0, H); g.addColorStop(0, css(water)); g.addColorStop(1, css(deep)); cx.fillStyle = g; cx.fillRect(0, hz, W, H - hz);
    if (up && sy < hz + 20) { const glint = mix([255, 210, 140], hor, .2); for (let y = hz + 2; y < H; y += 3) { const d = (y - hz) / (H - hz), w = sr * (1.4 + d * 6) * (.6 + .4 * Math.sin(y * .21 + tt * 2.2)), o = Math.sin(y * .13 + tt * 1.6) * 8 * d; cx.fillStyle = css(glint, .5 * (1 - d)); cx.fillRect(sx - w / 2 + o, y, w, 1.8); } }
    cx.fillStyle = "rgba(255,255,255,.14)"; for (let i = 0; i < 34; i++) { const y = hz + 6 + ((i * 37) % (H - hz)), x = ((i * 211 + tt * 14 * (1 + i % 3)) % (W + 80)) - 40; cx.fillRect(x, y, 26 + (i % 4) * 16, 1.4); }
    /* palms on the bank, big and close */
    const sway = Math.sin(tt * .8), ps = clamp(Math.min(W, H) / 560, .7, 1.35), leaf = css(mix([28, 128, 72], top, .35)), trunk = css(mix([70, 48, 30], top, .3));
    palm(W * .04, hz + 6, ps * 1.15, trunk, leaf, sway); palm(W * .13, hz + 4, ps * .85, trunk, leaf, -sway);
    if (!narrow) { palm(W * .9, hz + 6, ps * 1.05, trunk, leaf, sway); palm(W * .97, hz + 8, ps * .8, trunk, leaf, -sway); }
    /* the boat and its reflection */
    const by = hz + (H - hz) * (narrow ? .1 : .14), bs = Math.max(.85, W / 700), bx = boatX * W, bob = Math.sin(tt * 1.4) * 1.6;
    shikara(bx, by + bob, bs, top);
    cx.save(); cx.translate(0, 2 * (by + bob) + 10 * bs); cx.scale(1, -1); cx.globalAlpha = .22; shikara(bx + Math.sin(tt * 3) * 2, by + bob, bs, top); cx.restore();
  }

  function loop(time) {
    const dt = Math.min(.05, (time - t0) / 1000); t0 = time;
    if (!playing && resumeAt && time > resumeAt) { setPlaying(true); }
    if (playing) { hour += dt * (END - START) / LOOP_SECONDS; if (hour > END) hour = START; labels(); }
    boatX += dt * .018; if (boatX > 1.15) boatX = -.15;
    if (visible) draw(time);
    requestAnimationFrame(loop);
  }
  function setPlaying(v) { playing = v; resumeAt = 0; playBtn.textContent = v ? "❚❚" : "▶"; playBtn.setAttribute("aria-label", v ? "Pause the day" : "Play the day"); }
  playBtn.onclick = () => setPlaying(!playing);
  slider.addEventListener("input", () => { hour = +slider.value; setPlaying(false); resumeAt = performance.now() + 6000; labels(); if (still) draw(0); });
  liveBtn.onclick = () => { const h = istHour(); hour = (h >= START && h <= END) ? h : 5.4; setPlaying(false); labels(); if (still) draw(0); };

  size(); labels();
  if (still) { setPlaying(false); draw(0); } else requestAnimationFrame(loop);
  addEventListener("resize", () => { size(); if (still) draw(0); });
  new IntersectionObserver(e => { visible = e[0].isIntersecting; }).observe(stage);
})();
