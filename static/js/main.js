// ============================================================
// CarVerse — main.js (stats counter + mobile menu)
// ============================================================
(function () {
  "use strict";

  // ---------------- Stats Counter (1 se target tak) ----------------
  var statCars = document.getElementById("stat-cars");
  if (statCars) {
    fetch("/api/stats")
      .then(function (r) {
        if (!r.ok) throw new Error("stats " + r.status);
        return r.json();
      })
      .then(function (s) {
        animateNum("stat-cars", s.cars);
        animateNum("stat-brands", s.brands);
        animateNum("stat-engines", s.engines);
        animateNum("stat-categories", s.categories);
      })
      .catch(function (e) { console.error("Stats error:", e); });
  }

  function animateNum(id, target) {
    var el = document.getElementById(id);
    if (!el) return;
    target = parseInt(target) || 0;
    if (target <= 0) { el.textContent = 0; return; }
    var current = 1;                 // ⭐ 1 se shuru
    el.textContent = current;
    var timer = setInterval(function () {
      current += 1;                  // ⭐ 1-1 karke badhega
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = current;
    }, Math.max(20, Math.floor(800 / target)));  // total ~0.8 sec animation
  }

  // ---------------- Hamburger Menu (mobile) ----------------
  var hamburger = document.getElementById("hamburger");
  var navLinks = document.querySelector(".nav-links");
  if (hamburger && navLinks) {
    hamburger.addEventListener("click", function () {
      navLinks.classList.toggle("open");
    });
  }
})();
