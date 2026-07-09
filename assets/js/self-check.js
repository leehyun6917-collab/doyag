(function () {
  "use strict";

  var root = document.getElementById("self-check");
  if (!root) return;

  var steps = root.querySelectorAll(".self-check__step");
  var results = root.querySelectorAll(".self-check__result");
  var liveRegion = document.getElementById("self-check-live");

  function showStep(stepNumber) {
    steps.forEach(function (step) {
      step.hidden = step.getAttribute("data-step") !== String(stepNumber);
    });
    results.forEach(function (result) {
      result.hidden = true;
    });
  }

  function showResult(name) {
    steps.forEach(function (step) {
      step.hidden = true;
    });
    results.forEach(function (result) {
      var match = result.getAttribute("data-result") === name;
      result.hidden = !match;
      if (match && liveRegion) {
        liveRegion.textContent = result.querySelector("h3")
          ? result.querySelector("h3").textContent
          : "진단 결과가 표시되었습니다.";
      }
    });
  }

  root.addEventListener("click", function (event) {
    var option = event.target.closest(".self-check__option");
    if (option) {
      var step = option.closest(".self-check__step");
      var stepNumber = step ? step.getAttribute("data-step") : null;
      var value = option.getAttribute("data-value");

      if (stepNumber === "1") {
        if (value === "under") {
          showResult("not-yet");
        } else {
          showStep(2);
        }
      } else if (stepNumber === "2") {
        showResult("eligible");
      }
      return;
    }

    var restart = event.target.closest(".self-check__restart");
    if (restart) {
      showStep(1);
    }
  });
})();
