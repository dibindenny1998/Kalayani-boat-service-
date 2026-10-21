/* Home hero: the day plays on its own, sunrise to sunset (about 30 seconds).
   The photo, the colour wash and the tour shown in the time bar follow the hour.
   Visitors can pause or drag the sun along the bar. */
(() => {
  const K = window.KALYANI;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = id => document.getElementById(id);
  const hero = $("hero"); if (!hero) return;
  const bar = $("timebar"), input = $("thour"), play = $("tplay"), clock = $("tclock"), name = $("tname"), link = $("tnow");
  const pics = [...hero.querySelectorAll(".hero__pics img")], wash = hero.querySelector(".hero__wash");
  const MIN = +input.min, MAX = +input.max, LOOP = 30;
  const hh = v => { const H = Math.floor(v), M = Math.floor((v - H) * 60 + 1e-6); return String(H).padStart(2, "0") + ":" + String(M).padStart(2, "0"); };
  /* colour wash through the day, from the four skies */
  const WASH = [[5, "linear-gradient(180deg,#5B5BB8,#FF9EC0)"], [6.5, "linear-gradient(180deg,#FF9EC0,#FFB38A)"], [8.5, "linear-gradient(180deg,#FFE29A,transparent)"],
    [10.5, "linear-gradient(180deg,#7FD0FF,transparent)"], [15, "linear-gradient(180deg,#FFD24A,transparent)"], [17, "linear-gradient(180deg,#FF8A4C,#FF4E6A)"], [18.8, "linear-gradient(180deg,#3A2A7A,#E8418A)"]];
  let hour = 5.6, playing = !still, resumeAt = 0, last = performance.now();
  const tours = K.tours.filter(t => t.start !== null);

  function render() {
    const p = ((hour - MIN) / (MAX - MIN)) * 100;
    bar.style.setProperty("--p", p.toFixed(2) + "%"); input.value = hour;
    clock.textContent = hh(hour);
    const on = tours.filter(t => hour >= t.start && hour < t.end).sort((a, b) => b.start - a.start)[0];
    const t = on || tours.filter(t => t.start > hour).sort((a, b) => a.start - b.start)[0] || tours[0];
    name.textContent = (on ? "" : "Next: ") + t.name; link.href = t.slug + ".html";
    pics.forEach(img => img.classList.toggle("on", hour >= +img.dataset.from && hour < +img.dataset.to));
    wash.style.setProperty("--wash", (WASH.filter(w => w[0] <= hour).pop() || WASH[0])[1]);
  }
  function setPlay(v) { playing = v; resumeAt = 0; play.textContent = v ? "❚❚" : "▶"; play.setAttribute("aria-label", v ? "Pause" : "Play"); }
  function frame(now) {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    if (!playing && resumeAt && now > resumeAt) setPlay(true);
    if (playing) { hour += dt * (MAX - MIN) / LOOP; if (hour > MAX) hour = MIN; render(); }
    requestAnimationFrame(frame);
  }
  play.onclick = () => setPlay(!playing);
  input.addEventListener("input", () => { hour = +input.value; setPlay(false); resumeAt = performance.now() + 6000; render(); });
  render();
  if (still) setPlay(false); else requestAnimationFrame(frame);
})();
