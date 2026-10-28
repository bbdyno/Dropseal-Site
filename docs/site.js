// Dropseal site motion: a wax seal that melts as you scroll, phone screens that follow the
// story, and videos that play when they come into view. Same seal math as the app
// (WaxSealShape.swift), so the site and the app melt the same way.
(() => {
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const svgNS = "http://www.w3.org/2000/svg";

  // ---- Seal geometry -------------------------------------------------------------------

  function sealPath(size, melt, scale = 1) {
    const radius = (size / 2) * 0.82 * scale;
    const cx = size / 2, cy = size / 2 - (size / 2) * 0.82 * 0.08 * melt;
    const scallop = 0.045 * (1 - melt * 0.8);
    const samples = 180;
    let d = "";
    for (let i = 0; i <= samples; i++) {
      const a = (i / samples) * Math.PI * 2;
      const r = radius * (1 + scallop * Math.cos(9 * a));
      let x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
      const lower = Math.max(0, Math.sin(a)), upper = Math.max(0, -Math.sin(a));
      y += melt * radius * 0.30 * lower ** 3;
      x += melt * radius * 0.12 * Math.cos(a) * lower;
      y += melt * radius * 0.10 * upper;
      d += (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1);
    }
    return d + "Z";
  }

  function dripPaths(size, melt) {
    const amount = Math.max(0, (melt - 0.3) / 0.7);
    if (!amount) return [];
    const radius = (size / 2) * 0.82, centerY = size / 2 - radius * 0.08 * melt;
    return [[0.40, 0.10, 0.30], [0.58, 0.08, 0.20], [0.49, 0.06, 0.12]].map(([turn, width, reach]) => {
      const a = turn * Math.PI;
      const x = size / 2 + radius * Math.cos(a) * (1 + 0.12 * melt);
      const rimY = centerY + radius * Math.sin(a) + melt * radius * 0.30 * Math.sin(a) ** 3;
      const w = radius * width, end = rimY + radius * reach * amount, top = rimY - w * 2;
      const bead = w * 0.58;
      return `M${x - w} ${top}Q${x - w * 0.42} ${rimY + w * 0.4} ${x - w * 0.42} ${end}` +
        `L${x + w * 0.42} ${end}Q${x + w * 0.42} ${rimY + w * 0.4} ${x + w} ${top}Z` +
        `M${x - bead} ${end}a${bead} ${bead} 0 1 0 ${bead * 2} 0a${bead} ${bead} 0 1 0 ${-bead * 2} 0Z`;
    });
  }

  const dropPath = (cx, cy, w, h) => {
    const r = w / 2, by = cy + h / 2 - r, top = cy - h / 2;
    return `M${cx} ${top}C${cx + w * 0.18} ${top + h * 0.22} ${cx + r} ${by - r * 0.55} ${cx + r} ${by}` +
      `A${r} ${r} 0 0 1 ${cx - r} ${by}C${cx - r} ${by - r * 0.55} ${cx - w * 0.18} ${top + h * 0.22} ${cx} ${top}Z`;
  };

  // Builds a seal into an <svg>; returns update(progress) for 0…1.
  function makeSeal(svg, size) {
    svg.setAttribute("viewBox", `0 0 ${size} ${size * 1.12}`);
    const el = (name, attrs) => {
      const node = document.createElementNS(svgNS, name);
      for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
      return node;
    };
    const halves = ["left", "right"].map((side) => {
      const g = el("g", { class: `seal-half seal-${side}`, "clip-path": `url(#crack-${side}-${size})` });
      svg.appendChild(g);
      return g;
    });
    const defs = el("defs", {});
    const zig = [0.02, -0.05, 0.04, -0.03, 0.06, -0.02, 0.03, -0.04, 0.01];
    const crack = zig.map((dx, i) => [size / 2 + size * dx, (size * 1.12 * i) / (zig.length - 1)]);
    for (const side of ["left", "right"]) {
      const edge = side === "left" ? -size : size * 2;
      const pts = [[edge, -size], [crack[0][0], -size], ...crack, [crack.at(-1)[0], size * 3], [edge, size * 3]];
      const cp = el("clipPath", { id: `crack-${side}-${size}` });
      cp.appendChild(el("polygon", { points: pts.map((p) => p.join(",")).join(" ") }));
      defs.appendChild(cp);
    }
    svg.prepend(defs);

    const parts = halves.map((g) => {
      const drips = el("g", { class: "wax" });
      const body = el("path", { class: "wax" });
      const lip = el("path", { class: "lip" });
      const ring = el("ellipse", { class: "mark-ring" });
      const drop = el("path", { class: "mark" });
      g.append(drips, body, lip, ring, drop);
      return { drips, body, lip, ring, drop };
    });

    return (progress) => {
      const melt = Math.pow(Math.min(Math.max(progress, 0), 1), 0.6);
      const dripsD = dripPaths(size, melt);
      const cx = size / 2, cy = size / 2 + size * 0.06 * melt;
      for (const p of parts) {
        p.body.setAttribute("d", sealPath(size, melt));
        p.lip.setAttribute("d", sealPath(size, melt, 0.84));
        p.drips.replaceChildren(...dripsD.map((d) => el("path", { d })));
        p.ring.setAttribute("cx", cx); p.ring.setAttribute("cy", cy);
        p.ring.setAttribute("rx", size * 0.24 * (1 + 0.1 * melt)); p.ring.setAttribute("ry", size * 0.24 * (1 - 0.16 * melt));
        p.ring.setAttribute("opacity", 1 - 0.8 * melt);
        p.drop.setAttribute("d", dropPath(cx, cy, size * 0.075 * (1 + 0.1 * melt), size * 0.105 * (1 - 0.16 * melt)));
        p.drop.setAttribute("opacity", 1 - 0.8 * melt);
      }
    };
  }

  // ---- Hero: melt with scroll ----------------------------------------------------------

  const hero = document.querySelector(".hero");
  if (hero) {
    const svg = hero.querySelector(".hero-seal");
    const update = makeSeal(svg, 320);
    const count = hero.querySelector(".hero-count");
    const goal = Number(count.dataset.goal);
    const format = new Intl.NumberFormat(document.documentElement.lang);
    let last = -1;
    const frame = () => {
      const rect = hero.getBoundingClientRect();
      const travel = hero.offsetHeight - innerHeight;
      const p = reduceMotion ? 0.4 : Math.min(Math.max(-rect.top / (travel * 0.82), 0), 1);
      if (Math.abs(p - last) > 0.001) {
        last = p;
        update(p);
        count.textContent = format.format(Math.round(goal * p));
        hero.classList.toggle("is-open", p >= 1);
        hero.style.setProperty("--p", p.toFixed(3));
      }
      if (!reduceMotion) requestAnimationFrame(frame);
    };
    frame();
  }

  // Small static seals (price section, footer mark).
  document.querySelectorAll("svg.seal-static").forEach((svg) => makeSeal(svg, 200)(Number(svg.dataset.progress || 0)));

  // ---- Story: phone follows the step in view -------------------------------------------

  const story = document.querySelector(".story");
  if (story) {
    const screens = [...story.querySelectorAll(".phone .screen")];
    const steps = [...story.querySelectorAll(".story-step")];
    const show = (i) => {
      screens.forEach((s, j) => {
        s.classList.toggle("is-active", i === j);
        if (s.tagName === "VIDEO") {
          if (i === j) { s.currentTime = 0; s.play().catch(() => {}); } else s.pause();
        }
      });
      steps.forEach((s, j) => s.classList.toggle("is-active", i === j));
    };
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) show(steps.indexOf(e.target));
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach((s) => io.observe(s));
    show(0);

    const toggle = story.querySelector(".sound-toggle");
    toggle?.addEventListener("click", () => {
      const on = toggle.getAttribute("aria-pressed") !== "true";
      toggle.setAttribute("aria-pressed", String(on));
      toggle.textContent = on ? toggle.dataset.off : toggle.dataset.on;
      story.querySelectorAll("video").forEach((v) => { v.muted = !on; });
      const active = story.querySelector("video.is-active");
      if (active && on) { active.currentTime = 0; active.play().catch(() => {}); }
    });
  }

  // ---- Reveal on scroll and counting numbers ---------------------------------------------

  const reveal = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("is-in");
      reveal.unobserve(e.target);
      e.target.querySelectorAll("[data-count]").forEach((n) => {
        const to = Number(n.dataset.count), fmt = new Intl.NumberFormat(document.documentElement.lang);
        if (reduceMotion) { n.textContent = fmt.format(to); return; }
        const start = performance.now();
        const tick = (t) => {
          const k = Math.min((t - start) / 1200, 1), eased = 1 - (1 - k) ** 3;
          n.textContent = fmt.format(Math.round(to * eased));
          if (k < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }
  }, { threshold: 0.2 });
  document.querySelectorAll(".reveal").forEach((el) => reveal.observe(el));
})();
