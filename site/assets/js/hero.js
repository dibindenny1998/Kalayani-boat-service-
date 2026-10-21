/* Home page hero: the sun dial.
   The sun travels the dial from 5 am to 8 pm on its own (about 36 seconds). Visitors can drag it,
   use the arrow keys, pause it, or jump to the real time in Alleppey. The photo, the light and the
   departure under the dial change with the hour. */
(() => {
  const K = window.KALYANI;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const dial = document.getElementById("dial");
  if (!dial) return;
  const $ = id => document.getElementById(id);
  const sun = $("sun"), halo = $("halo"), done = $("dialdone"), ticks = $("ticks");
  const rt = $("rt"), rn = $("rn"), rf = $("rf"), rplay = $("rplay"), rnow = $("rnow");
  const pics = [...document.querySelectorAll("#hour .pics img")], tint = document.querySelector("#hour .tint");
  const hh = v => { const H = Math.floor(v), M = Math.floor((v - H) * 60 + 1e-6); return String(H).padStart(2, "0") + ":" + String(M).padStart(2, "0"); };
  const inr = v => "₹" + v.toLocaleString("en-IN");

  const MIN = 5, MAX = 20, CX = 500, CY = 290, RX = 440, RY = 260, LOOP = 36;
  const pt = h => { const a = Math.PI * (1 - (h - MIN) / (MAX - MIN)); return [CX + RX * Math.cos(a), CY - RY * Math.sin(a)]; };

  /* hour ticks, labels and a red dot at each departure */
  let svg = "";
  for (let h = MIN; h <= MAX; h++) {
    const a = Math.PI * (1 - (h - MIN) / (MAX - MIN)), c = Math.cos(a), s = Math.sin(a);
    const big = h % 3 === 0;
    svg += `<line class="tick" x1="${CX + (RX + 8) * c}" y1="${CY - (RY + 8) * s}" x2="${CX + (RX + (big ? 22 : 14)) * c}" y2="${CY - (RY + (big ? 22 : 14)) * s}"/>`;
    if (big) svg += `<text class="hr" x="${CX + (RX + 46) * c}" y="${CY - (RY + 40) * s + 5}">${String(h).padStart(2, "0")}</text>`;
  }
  K.tours.filter(t => t.start !== null).forEach(t => { const [x, y] = pt(t.start); svg += `<circle class="dep" cx="${x}" cy="${y}" r="6"><title>${hh(t.start)} ${t.name}</title></circle>`; });
  ticks.innerHTML = svg;

  /* light over the photo through the day: [hour, colour] */
  const TINT = [[5, "rgba(70,80,190,.75)"], [6.3, "rgba(255,120,150,.6)"], [8, "rgba(255,200,150,.25)"], [11, "rgba(255,255,255,0)"], [15, "rgba(255,190,90,.25)"], [17.5, "rgba(255,110,60,.55)"], [18.8, "rgba(120,60,150,.6)"], [20, "rgba(40,50,140,.8)"]];
  const tintAt = h => (TINT.filter(t => t[0] <= h).pop() || TINT[0])[1];

  let hour = 5.6, playing = !still, resumeAt = 0, last = performance.now();
  function render() {
    const [x, y] = pt(hour);
    sun.setAttribute("cx", x); sun.setAttribute("cy", y); halo.setAttribute("cx", x); halo.setAttribute("cy", y);
    done.setAttribute("d", `M60 290 A440 260 0 0 1 ${x.toFixed(1)} ${y.toFixed(1)}`);
    dial.setAttribute("aria-valuenow", hour.toFixed(2)); dial.setAttribute("aria-valuetext", hh(hour));
    rt.textContent = hh(hour);
    const tours = K.tours.filter(t => t.start !== null);
    const on = tours.filter(t => hour >= t.start && hour < t.end).sort((a, b) => b.start - a.start)[0];
    const next = tours.filter(t => t.start > hour).sort((a, b) => a.start - b.start)[0] || tours[0];
    const t = on || next;
    rn.textContent = t.name; rn.href = t.slug + ".html";
    rf.textContent = on ? `On the water · ${inr(t.price)} for two` : `Next out ${hh(t.start)} · ${inr(t.price)} for two`;
    pics.forEach(p => { const a = +p.dataset.from, b = +p.dataset.to; p.classList.toggle("on", hour >= a && hour < b); });
    if (tint) tint.style.setProperty("--tint", tintAt(hour));
  }
  function frame(now) {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    if (!playing && resumeAt && now > resumeAt) setPlay(true);
    if (playing) { hour += dt * (MAX - MIN) / LOOP; if (hour > MAX) hour = MIN; render(); }
    halo.setAttribute("r", (28 + 5 * Math.sin(now / 400)).toFixed(1));
    requestAnimationFrame(frame);
  }
  function setPlay(v) { playing = v; resumeAt = 0; rplay.textContent = v ? "Pause" : "Play the day"; }
  const hold = () => { setPlay(false); resumeAt = performance.now() + 7000; };

  /* drag the sun */
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
  rplay.onclick = () => setPlay(!playing);
  rnow.onclick = () => { const h = window.KALYANI_IST ? window.KALYANI_IST() : new Date().getHours(); hour = Math.min(MAX, Math.max(MIN, h)); setPlay(false); render(); };

  render();
  if (still) setPlay(false); else requestAnimationFrame(frame);
})();
