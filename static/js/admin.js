// ============================================================
// CarVerse Admin Panel — matches original admin.html
// Sends BOTH naming styles so it works with any models.py
// ============================================================

const FALLBACK_IMG = "https://placehold.co/140x92/1a1a1a/c5c9c7?text=No+Image";

// ---------------- Admin Key ----------------
function getAdminKey() {
  return localStorage.getItem("adminKey") || "carverse-admin";
}

function adminHeaders() {
  return { "Content-Type": "application/json", "X-Admin-Key": getAdminKey() };
}

document.getElementById("save-key").addEventListener("click", () => {
  const key = document.getElementById("admin-key").value.trim();
  if (key) {
    localStorage.setItem("adminKey", key);
    showToast("🔑 Admin key saved!");
  }
});

// ---------------- Toast ----------------
function showToast(msg, isError = false) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.className = "toast show" + (isError ? " error" : "");
  setTimeout(() => (toast.className = "toast"), 3000);
}

// ---------------- Tabs ----------------
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((t) => t.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
  });
});

// ============================================================
// CARS
// ============================================================
// [form input id, alias column name (or null)]
const CAR_FIELDS = [
  ["brand", null], ["model", null], ["generation", null], ["nickname", null],
  ["category", null], ["status", null], ["production_years", null],
  ["country", null], ["manufacturer", null], ["image_url", null],
  ["horsepower", null],
  ["torque", "torque_nm"],
  ["top_speed", "top_speed_kmh"],
  ["accel_0_100", null], ["quarter_mile", null],
  ["weight", "weight_kg"],
  ["length", "length_mm"], ["width", "width_mm"],
  ["height", "height_mm"], ["wheelbase", "wheelbase_mm"],
  ["engine_name", null], ["engine_code", null], ["engine_layout", null],
  ["displacement", "displacement_l"], ["cylinders", null],
  ["aspiration", null], ["fuel_type", null],
  ["redline", "redline_rpm"],
  ["transmission_type", "transmission"],
  ["gear_count", "gears"],
  ["drivetrain", null],
  ["units_produced", null], ["units_sold", null],
  ["market_availability", null],
  ["msrp", "msrp_usd"],
  ["launch_date", null], ["competitors", null], ["awards", null],
  ["historical_importance", "history"],
];

// Numeric fields (parsed; "+" etc stripped). Units stay as typed.
const INT_FIELDS = new Set([
  "horsepower", "torque", "top_speed", "weight", "length", "width",
  "height", "wheelbase", "cylinders", "redline", "gear_count", "msrp",
]);
const FLOAT_FIELDS = new Set(["accel_0_100", "quarter_mile", "displacement"]);

function collectFormData() {
  const data = {};
  CAR_FIELDS.forEach(([field, alias]) => {
    const el = document.getElementById(field);
    if (!el) return;
    let val = el.value.trim();
    if (INT_FIELDS.has(field)) val = parseInt(val.replace(/[^0-9]/g, "")) || 0;
    else if (FLOAT_FIELDS.has(field)) val = parseFloat(val.replace(/[^0-9.]/g, "")) || 0;
    data[field] = val;
    if (alias) data[alias] = val;   // API keeps whichever column exists
  });
  return data;
}

// ---------------- Save (Create / Update) ----------------
document.getElementById("car-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const carId = document.getElementById("car-id").value;
  const url = carId ? `/api/cars/${carId}` : "/api/cars";
  const method = carId ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: adminHeaders(),
    body: JSON.stringify(collectFormData()),
  });

  if (res.ok) {
    showToast(carId ? "✅ Car updated!" : "✅ Car added!");
    document.getElementById("car-form").reset();
    document.getElementById("car-id").value = "";
    document.getElementById("form-title").textContent = "Add New Car";
    loadCarsList();
  } else if (res.status === 401) {
    showToast("❌ Wrong admin key!", true);
  } else {
    showToast("❌ Save failed!", true);
  }
});

// ---------------- Edit ----------------
async function editCar(id) {
  const car = await (await fetch(`/api/cars/${id}`)).json();
  document.getElementById("car-id").value = car.id;
  CAR_FIELDS.forEach(([field, alias]) => {
    const el = document.getElementById(field);
    if (!el) return;
    let v = car[field];
    if ((v === undefined || v === null || v === "") && alias) v = car[alias];
    if (v !== undefined && v !== null) el.value = v;
  });
  document.getElementById("form-title").textContent = `Edit: ${car.brand} ${car.model}`;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ---------------- Delete ----------------
async function deleteCar(id) {
  const car = allCars.find((c) => c.id === id);
  if (!confirm(`Delete "${car ? car.full_name : "this car"}"? This cannot be undone.`)) return;
  const res = await fetch(`/api/cars/${id}`, { method: "DELETE", headers: adminHeaders() });
  if (res.ok) {
    showToast("🗑️ Car deleted!");
    loadCarsList();
  } else {
    showToast("❌ Delete failed — check admin key!", true);
  }
}

// Clear button
document.getElementById("clear-form").addEventListener("click", () => {
  document.getElementById("car-form").reset();
  document.getElementById("car-id").value = "";
  document.getElementById("form-title").textContent = "Add New Car";
});

// ---------------- Cars list ----------------
let allCars = [];
async function loadCarsList() {
  const data = await (await fetch("/api/cars?per_page=100")).json();
  allCars = data.cars || [];
  renderCarsList(allCars);
}

function renderCarsList(cars) {
  document.getElementById("admin-cars-list").innerHTML = cars.map((c) => `
    <div class="admin-list-item">
      <img src="${c.image_url || FALLBACK_IMG}" referrerpolicy="no-referrer"
           onerror="this.onerror=null;this.src='${FALLBACK_IMG}'" alt="car">
      <div class="item-info">
        <strong>${c.full_name}</strong>
        <small>${c.category} · ${c.horsepower} hp · ${c.status}</small>
      </div>
      <div class="item-actions">
        <button type="button" class="btn-small edit-btn" data-id="${c.id}">✏️ Edit</button>
        <button type="button" class="btn-small danger delete-btn" data-id="${c.id}">🗑️</button>
      </div>
    </div>
  `).join("");
}

// Event delegation — Edit/Delete always work (tap-safe)
document.getElementById("admin-cars-list").addEventListener("click", (e) => {
  const editBtn = e.target.closest(".edit-btn");
  const delBtn = e.target.closest(".delete-btn");
  if (editBtn) editCar(parseInt(editBtn.dataset.id));
  else if (delBtn) deleteCar(parseInt(delBtn.dataset.id));
});

// Filter
document.getElementById("admin-car-filter").addEventListener("input", (e) => {
  const q = e.target.value.toLowerCase();
  renderCarsList(allCars.filter((c) => c.full_name.toLowerCase().includes(q)));
});

// ============================================================
// ENGINES (Types + Variants)
// ============================================================
document.getElementById("engine-type-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const res = await fetch("/api/engine-types", {
    method: "POST",
    headers: adminHeaders(),
    body: JSON.stringify({
      name: document.getElementById("etype-name").value.trim(),
      image_url: document.getElementById("etype-image").value.trim(),
    }),
  });
  if (res.ok) { showToast("✅ Engine type added!"); e.target.reset(); loadEngines(); }
  else showToast("❌ Error — check admin key!", true);
});

document.getElementById("variant-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const typeId = parseInt(document.getElementById("var-type-id").value);
  if (!typeId) { showToast("❌ Select an engine type first!", true); return; }
  const res = await fetch("/api/engine-variants", {
    method: "POST",
    headers: adminHeaders(),
    body: JSON.stringify({
      engine_type_id: typeId,
      name: document.getElementById("var-name").value.trim(),
      power_hp: parseInt(document.getElementById("var-power").value.replace(/[^0-9]/g, "")) || 0,
      torque_nm: parseInt(document.getElementById("var-torque").value.replace(/[^0-9]/g, "")) || 0,
      weight_kg: parseInt(document.getElementById("var-weight").value.replace(/[^0-9]/g, "")) || 0,
      image_url: document.getElementById("var-image").value.trim(),
    }),
  });
  if (res.ok) { showToast("✅ Variant added!"); e.target.reset(); loadEngines(); }
  else showToast("❌ Error — check admin key!", true);
});

let allEngineTypes = [];

function computeRange(variants, key) {
  const vals = (variants || []).map((v) => v[key] || 0).filter((n) => n > 0);
  if (!vals.length) return null;
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  return min === max ? `${min}` : `${min}-${max}`;
}

async function loadEngines() {
  allEngineTypes = await (await fetch("/api/engine-types")).json();

  const typeSelect = document.getElementById("var-type-id");
  const prevVal = typeSelect.value;
  typeSelect.innerHTML = '<option value="">— Select Engine Type —</option>' +
    allEngineTypes.map((t) => `<option value="${t.id}">${t.name}</option>`).join("");
  typeSelect.value = prevVal;

  document.getElementById("admin-engines-list").innerHTML = allEngineTypes.map((t) => {
    const hpRange = computeRange(t.variants, "power_hp");
    const tqRange = computeRange(t.variants, "torque_nm");
    const rangeLine = (hpRange || tqRange)
      ? `<small class="etype-range">${hpRange ? "Horsepower: " + hpRange + " hp" : ""}${hpRange && tqRange ? " · " : ""}${tqRange ? "Torque: " + tqRange + " Nm" : ""}</small>`
      : "";
    return `
    <div class="etype-admin-block">
      <div class="etype-admin-head">
        <div><strong>${t.name}</strong>${rangeLine}</div>
        <button type="button" class="btn-small danger" data-type="engine-types" data-id="${t.id}">🗑️ Delete Type</button>
      </div>
      ${(t.variants || []).map((v) => `
        <div class="variant-admin-item">
          <img src="${v.image_url || FALLBACK_IMG}" referrerpolicy="no-referrer"
               onerror="this.onerror=null;this.src='${FALLBACK_IMG}'" alt="">
          <div class="item-info">
            <strong>${v.name}</strong>
            <small>${v.power_hp} hp · ${v.torque_nm} Nm · ${v.weight_kg} kg</small>
          </div>
          <button type="button" class="btn-small danger" data-type="engine-variants" data-id="${v.id}">🗑️</button>
        </div>
      `).join("") || '<small style="color:#666">No variants yet.</small>'}
    </div>
  `;
  }).join("");
}

// ============================================================
// MATERIALS
// ============================================================
document.getElementById("material-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const res = await fetch("/api/materials", {
    method: "POST",
    headers: adminHeaders(),
    body: JSON.stringify({
      name: document.getElementById("mat-name").value.trim(),
      weight_factor: parseFloat(document.getElementById("mat-weight").value.replace(/[^0-9.]/g, "")) || 1.0,
      strength_factor: parseFloat(document.getElementById("mat-strength").value.replace(/[^0-9.]/g, "")) || 1.0,
      description: document.getElementById("mat-desc").value.trim(),
      image_url: document.getElementById("mat-image").value.trim(),
    }),
  });
  if (res.ok) { showToast("✅ Material added!"); e.target.reset(); loadMaterials(); }
  else showToast("❌ Error — check admin key!", true);
});

async function loadMaterials() {
  const mats = await (await fetch("/api/materials")).json();
  document.getElementById("admin-materials-list").innerHTML = mats.map((m) => `
    <div class="admin-list-item">
      <div class="item-info">
        <strong>${m.name}</strong>
        <small>Weight: ${m.weight_factor}× · Strength: ${m.strength_factor}×</small>
      </div>
      <div class="item-actions">
        <button type="button" class="btn-small danger" data-type="materials" data-id="${m.id}">🗑️</button>
      </div>
    </div>
  `).join("");
}

// ============================================================
// COLORS
// ============================================================
document.getElementById("col-picker").addEventListener("input", (e) => {
  document.getElementById("col-hex").value = e.target.value.toUpperCase();
});

document.getElementById("color-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const res = await fetch("/api/colors", {
    method: "POST",
    headers: adminHeaders(),
    body: JSON.stringify({
      name: document.getElementById("col-name").value.trim(),
      hex_code: document.getElementById("col-hex").value.trim() ||
                document.getElementById("col-picker").value,
    }),
  });
  if (res.ok) { showToast("✅ Color added!"); e.target.reset(); loadColors(); }
  else showToast("❌ Error — check admin key!", true);
});

async function loadColors() {
  const colors = await (await fetch("/api/colors")).json();
  document.getElementById("admin-colors-list").innerHTML = colors.map((c) => `
    <div class="color-chip">
      <span class="swatch" style="background:${c.hex_code}"></span>
      <div class="item-info">
        <strong>${c.name}</strong>
        <small>${c.hex_code}</small>
      </div>
      <button type="button" class="btn-small danger" data-type="colors" data-id="${c.id}">🗑️</button>
    </div>
  `).join("");
}

// ============================================================
// Generic delete (engines / materials / colors)
// ============================================================
async function deleteItem(type, id) {
  if (!confirm("Delete this item?")) return;
  const res = await fetch(`/api/${type}/${id}`, { method: "DELETE", headers: adminHeaders() });
  if (res.ok) {
    showToast("🗑️ Deleted!");
    if (type === "engine-types" || type === "engine-variants") loadEngines();
    if (type === "materials") loadMaterials();
    if (type === "colors") loadColors();
  } else showToast("❌ Delete failed!", true);
}

["admin-engines-list", "admin-materials-list", "admin-colors-list"].forEach((listId) => {
  document.getElementById(listId).addEventListener("click", (e) => {
    const btn = e.target.closest("[data-type]");
    if (btn) deleteItem(btn.dataset.type, parseInt(btn.dataset.id));
  });
});

// ============================================================
// Init
// ============================================================
loadCarsList();
loadEngines();
loadMaterials();
loadColors();