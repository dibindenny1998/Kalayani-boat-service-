/* Home hero: the sun dial.
   The sun travels the arc from 5 am to 7:30 pm on its own (about 30 seconds), and a gold line pulls
   along behind it. The photo, the colour wash and the tour shown under the arc follow the hour.
   Visitors can drag the sun, use the arrow keys, or pause. */
(() => {
  const K = window.KALYANI;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = id => document.getElementById(id);
  const hero = $("hero"), dial = $("dial"); if (!hero || !dial) return;
  const sun = $("dsun"), halo = $("dhalo"), pull = $("dpull"), ticks = $("dticks");
  const play = $("dplay"), clock = $("dclock"), name = $("dname"), link = $("dnow");
  const pics = [...hero.querySelectorAll(".hero__pics img")], wash = hero.querySelector(".hero__wash");
  const MIN = 5, MAX = 19.5, LOOP = 30, CX = 300, CY = 300, RX = 270, RY = 250;
  const hh = v => { const H = Math.floor(v), M = Math.floor((v - H) * 60 + 1e-6); return String(H).padStart(2, "0") + ":" + String(M).padStart(2, "0"); };
  const ang = h => Math.PI * (1 - (h - MIN) / (MAX - MIN));
  const pt = (h, gx = 0, gy = 0) => { const a = ang(h); return [CX + (RX + gx) * Math.cos(a), CY - (RY + gy) * Math.sin(a)]; };
  const tours = K.tours.filter(t => t.start !== null);

  /* hour ticks, labels and a dot at each departure time */
  let svg = "";
  for (let h = 6; h <= 19; h++) {
    const big = h % 3 === 0, [x1, y1] = pt(h, 8, 8), [x2, y2] = pt(h, big ? 18 : 13, big ? 18 : 13);
    svg += `<line class="dial__tick" x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"/>`;
    if (big) { const [tx, ty] = pt(h, 36, 34); svg += `<text class="dial__hr" x="${tx.toFixed(1)}" y="${(ty + 5).toFixed(1)}">${String(h).padStart(2, "0")}</text>`; }
  }
  tours.forEach(t => { const [x, y] = pt(t.start); svg += `<circle class="dial__dep" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="5"><title>${hh(t.start)} ${t.name}</title></circle>`; });
  ticks.innerHTML = svg;

  /* colour wash: one colour family at each part of the day */
  const WASH = [[5, "linear-gradient(180deg,#FF8FB0,#FFD3E1)"], [7.5, "linear-gradient(180deg,#FFD36E,#FFF1C9)"], [10.5, "linear-gradient(180deg,#7FC8F2,#D5EEFC)"],
    [15, "linear-gradient(180deg,#FFC94A,#FFE7A8)"], [17, "linear-gradient(180deg,#F2542D,#FF9A80)"], [18.8, "linear-gradient(180deg,#5A3D9A,#9C83D6)"]];

  let hour = 5.6, playing = !still, resumeAt = 0, last = performance.now();
  function render() {
    const [x, y] = pt(hour);
    sun.setAttribute("cx", x); sun.setAttribute("cy", y); halo.setAttribute("cx", x); halo.setAttribute("cy", y);
    pull.setAttribute("d", `M30 300 A${RX} ${RY} 0 0 1 ${x.toFixed(1)} ${y.toFixed(1)}`);
    dial.setAttribute("aria-valuenow", hour.toFixed(2)); dial.setAttribute("aria-valuetext", hh(hour));
    clock.textContent = hh(hour);
    const on = tours.filter(t => hour >= t.start && hour < t.end).sort((a, b) => b.start - a.start)[0];
    const t = on || tours.filter(t => t.start > hour).sort((a, b) => a.start - b.start)[0] || tours[0];
    name.textContent = (on ? "" : "Next: ") + t.name; link.href = t.slug + ".html";
    pics.forEach(img => img.classList.toggle("on", hour >= +img.dataset.from && hour < +img.dataset.to));
    wash.style.setProperty("--wash", (WASH.filter(w => w[0] <= hour).pop() || WASH[0])[1]);
  }
  function setPlay(v) { playing = v; resumeAt = 0; play.textContent = v ? "❚❚" : "▶"; play.setAttribute("aria-label", v ? "Pause" : "Play"); }
  const hold = () => { setPlay(false); resumeAt = performance.now() + 6000; };
  function frame(now) {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    if (!playing && resumeAt && now > resumeAt) setPlay(true);
    if (playing) { hour += dt * (MAX - MIN) / LOOP; if (hour > MAX) hour = MIN; render(); }
    halo.setAttribute("r", (22 + 4 * Math.sin(now / 380)).toFixed(1));
    requestAnimationFrame(frame);
  }

  /* drag the sun along the arc */
  const fromPointer = e => {
    const p = dial.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
    const q = p.matrixTransform(dial.getScreenCTM().inverse());
    const a = Math.atan2(Math.max(0, (CY - q.y) / RY), (q.x - CX) / RX);
    hour = Math.min(MAX, Math.max(MIN, MIN + (MAX - MIN) * (1 - a / Math.PI))); render();
  };
  let dragging = false;
  dial.addEventListener("pointerdown", e => { dragging = true; dial.setPointerCapture(e.pointerId); hold(); fromPointer(e); });
  dial.addEventListener("pointermove", e => { if (dragging) { hold(); fromPointer(e); } });
  dial.addEventListener("pointerup", () => { dragging = false; });
  dial.addEventListener("keydown", e => {
    const d = { ArrowRight: .25, ArrowUp: .25, ArrowLeft: -.25, ArrowDown: -.25 }[e.key]; if (!d) return;
    e.preventDefault(); hold(); hour = Math.min(MAX, Math.max(MIN, hour + d)); render();
  });
  play.onclick = () => setPlay(!playing);

  render();
  if (still) setPlay(false); else requestAnimationFrame(frame);
})();
