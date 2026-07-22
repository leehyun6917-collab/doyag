(function () {
  "use strict";

  var lightbox = document.getElementById("doc-lightbox");
  var image = document.getElementById("doc-lightbox-image");
  var caption = document.getElementById("doc-lightbox-title");
  var cards = document.querySelectorAll(".doc-card");

  if (!lightbox || !image || !caption || !cards.length) {
    return;
  }

  var lastFocused = null;

  var openLightbox = function (card) {
    var src = card.getAttribute("data-doc-image");
    var title = card.getAttribute("data-doc-title") || "";
    if (!src) {
      return;
    }

    lastFocused = document.activeElement;
    image.src = src;
    image.alt = title + " 샘플 확대 이미지";
    caption.textContent = title;
    lightbox.hidden = false;
    document.body.classList.add("no-scroll");
    lightbox.querySelector(".doc-lightbox__close").focus();
  };

  var closeLightbox = function () {
    lightbox.hidden = true;
    image.src = "";
    document.body.classList.remove("no-scroll");
    if (lastFocused) {
      lastFocused.focus();
    }
  };

  cards.forEach(function (card) {
    card.addEventListener("click", function () {
      openLightbox(card);
    });
  });

  lightbox.querySelectorAll("[data-doc-close]").forEach(function (el) {
    el.addEventListener("click", closeLightbox);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !lightbox.hidden) {
      closeLightbox();
    }
  });
})();
