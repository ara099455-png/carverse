// ============================================================
// CarVerse — search.js (live search: navbar + hero)
// Silver highlight on matching letters
// ============================================================
(function () {
  "use strict";

  var PLACEHOLDER = "https://placehold.co/128x84/141414/c5c9c7?text=Car";

  function setupSearch(inputId, resultsId) {
    var input = document.getElementById(inputId);
    var box = document.getElementById(resultsId);
    if (!input || !box) return;

    var debounce = null;

    input.addEventListener("input", function () {
      var q = input.value.trim();
      clearTimeout(debounce);
      if (!q) { box.classList.remove("open"); box.innerHTML = ""; return; }
      debounce = setTimeout(function () { doSearch(q, box); }, 180);
    });

    box.addEventListener("click", function (e) {
      var item = e.target.closest(".search-item");
      if (item) window.location.href = "/car/" + item.dataset.id;
    });

    document.addEventListener("click", function (e) {
      if (!e.target.closest("#" + inputId) && !e.target.closest("#" + resultsId)) {
        box.classList.remove("open");
      }
    });
  }

  function doSearch(q, box) {
    fetch("/api/search?q=" + encodeURIComponent(q))
      .then(function (r) { return r.json(); })
      .then(function (cars) {
        if (!cars.length) {
          box.innerHTML = '<div class="search-empty">No cars found</div>';
          box.classList.add("open");
          return;
        }
        var html = "";
        cars.forEach(function (c) {
          html += '<div class="search-item" data-id="' + c.id + '">' +
            '<img src="' + (c.image_url || PLACEHOLDER) + '"' +
            ' referrerpolicy="no-referrer"' +
            ' onerror="this.onerror=null;this.src=\'' + PLACEHOLDER + '\'">' +
            '<span class="s-name">' + highlight(c.full_name, q) + '</span>' +
            '</div>';
        });
        box.innerHTML = html;
        box.classList.add("open");
      })
      .catch(function () {});
  }

  // Matching letters = metallic silver, rest = dark gray
  function highlight(name, q) {
    var idx = name.toLowerCase().indexOf(q.toLowerCase());
    if (idx === -1) return name;
    return name.slice(0, idx) +
      '<span class="hl">' + name.slice(idx, idx + q.length) + '</span>' +
      name.slice(idx + q.length);
  }

  // Navbar search (base.html)
  setupSearch("nav-search-input", "nav-search-results");
  // Hero search (index.html)
  setupSearch("hero-search", "hero-search-results");
})();