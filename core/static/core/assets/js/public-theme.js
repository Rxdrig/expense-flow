(function () {
  var storageKey = "expenseflow-theme";
  var root = document.documentElement;

  function preferredTheme() {
    var saved = window.localStorage.getItem(storageKey);
    if (saved === "light" || saved === "dark") {
      return saved;
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    root.classList.toggle("light-mode", theme === "light");

    var toggleButtons = document.querySelectorAll("[data-theme-toggle]");
    toggleButtons.forEach(function (button) {
      var icon = button.querySelector("i");
      var text = button.querySelector("span");
      var isDark = theme === "dark";
      if (icon) {
        icon.className = isDark ? "mdi mdi-white-balance-sunny" : "mdi mdi-moon-waning-crescent";
      }
      if (text) {
        text.textContent = isDark ? "Modo claro" : "Modo oscuro";
      }
      button.setAttribute("aria-label", isDark ? "Cambiar a modo claro" : "Cambiar a modo oscuro");
    });
  }

  function saveTheme(theme) {
    window.localStorage.setItem(storageKey, theme);
    // Legacy key used by internal dashboard pages.
    window.localStorage.setItem("theme", theme);
  }

  function toggleTheme() {
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    saveTheme(next);
    applyTheme(next);
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyTheme(preferredTheme());

    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      button.addEventListener("click", toggleTheme);
    });
  });
})();
