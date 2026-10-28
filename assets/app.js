(function () {
  document.addEventListener("toggle", function (event) {
    var drawer = event.target;
    if (!drawer || !drawer.classList || !drawer.classList.contains("math-drawer")) return;
    if (!drawer.open) return;
    document.querySelectorAll("details.math-drawer[open]").forEach(function (other) {
      if (other !== drawer) other.open = false;
    });
  }, true);

  document.addEventListener("click", function (event) {
    document.querySelectorAll("details.math-drawer[open]").forEach(function (drawer) {
      if (!drawer.contains(event.target)) drawer.open = false;
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    document.querySelectorAll("details.math-drawer[open]").forEach(function (drawer) {
      drawer.open = false;
    });
  });
})();
