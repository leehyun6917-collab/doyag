/* 부정클릭 방지: 네이버 광고로 들어온 방문만 기록합니다(쿠키 사용 안 함, 90일 후 자동 삭제). */
(function () {
  var URL_ = "https://click-guard.yediconsult.workers.dev/v";
  try {
    var q = new URLSearchParams(location.search);
    var keys = ["n_media", "n_query", "n_keyword", "n_rank", "n_ad_group", "n_keyword_id", "NaPm"];
    if (!navigator.sendBeacon || !keys.some(function (k) { return q.has(k); })) return;
    var sid = "";
    try {
      sid = sessionStorage.getItem("cg_sid") || "";
      if (!sid) { sid = Math.random().toString(36).slice(2, 12); sessionStorage.setItem("cg_sid", sid); }
    } catch (e) { sid = Math.random().toString(36).slice(2, 12); }
    var t0 = Date.now(), acts = 0, left = false;
    var send = function (o) {
      try { navigator.sendBeacon(URL_, new Blob([JSON.stringify(o)], { type: "text/plain" })); } catch (e) {}
    };
    send({ t: "land", sid: sid, path: location.pathname, p: {
      media: q.get("n_media"), query: q.get("n_query"), keyword: q.get("n_keyword"), rank: q.get("n_rank"),
      adgroup: q.get("n_ad_group"), keyword_id: q.get("n_keyword_id"), napm: q.has("NaPm") ? 1 : 0 } });
    ["scroll", "touchstart", "click", "keydown"].forEach(function (e) {
      addEventListener(e, function () { acts++; }, { passive: true });
    });
    var leave = function () {
      if (left) return;
      left = true;
      send({ t: "leave", sid: sid, dwell: Date.now() - t0, acts: acts });
    };
    addEventListener("pagehide", leave);
    document.addEventListener("visibilitychange", function () { if (document.visibilityState === "hidden") leave(); });
  } catch (e) {}
})();
