(function () {
  "use strict";

  var KEY = "promoModalDismissed";
  var modal = document.getElementById("promo-modal");
  if (!modal) return;

  var dismissed = false;
  try {
    dismissed = sessionStorage.getItem(KEY) === "1";
  } catch (e) {}

  if (dismissed) return;

  var lastFocused = null;

  var closeModal = function () {
    modal.hidden = true;
    document.body.classList.remove("no-scroll");
    try {
      sessionStorage.setItem(KEY, "1");
    } catch (e) {}
    if (lastFocused) {
      lastFocused.focus();
    }
  };

  var openModal = function () {
    lastFocused = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("no-scroll");
    modal.querySelector(".promo-modal__close").focus();
  };

  modal.querySelectorAll("[data-promo-close]").forEach(function (el) {
    el.addEventListener("click", closeModal);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !modal.hidden) {
      closeModal();
    }
  });

  openModal();
})();
