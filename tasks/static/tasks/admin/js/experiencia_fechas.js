(function () {
  function getSelect(name) {
    return {
      y: document.querySelector(`select[name="${name}_year"]`),
      m: document.querySelector(`select[name="${name}_month"]`),
      d: document.querySelector(`select[name="${name}_day"]`),
    };
  }

  function readDate(parts) {
    if (!parts.y || !parts.m || !parts.d) return null;

    const y = parseInt(parts.y.value, 10);
    const m = parseInt(parts.m.value, 10);
    const d = parseInt(parts.d.value, 10);

    if (!y || !m || !d) return null;
    return new Date(y, m - 1, d);
  }

  function setDate(parts, date) {
    parts.y.value = date.getFullYear();
    parts.m.value = date.getMonth() + 1;
    parts.d.value = date.getDate();

    parts.y.dispatchEvent(new Event("change", { bubbles: true }));
    parts.m.dispatchEvent(new Event("change", { bubbles: true }));
    parts.d.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function enforce() {
    const inicio = getSelect("fecha_de_inicio_de_gestion");
    const fin = getSelect("fecha_fin_de_gestion");

    if (!inicio.y || !fin.y) return;

    const di = readDate(inicio);
    const df = readDate(fin);

    if (!di || !df) return;

    if (df < di) {
      // 🔒 no permite error lógico
      setDate(fin, di);
    }
  }

  function bind() {
    const inicio = getSelect("fecha_de_inicio_de_gestion");
    const fin = getSelect("fecha_fin_de_gestion");

    if (!inicio.y || !fin.y) return;

    [...Object.values(inicio), ...Object.values(fin)].forEach((el) => {
      if (el) el.addEventListener("change", enforce);
    });
  }

  document.addEventListener("DOMContentLoaded", bind);
})();
