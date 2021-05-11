var controller = new AbortController();
var signal = controller.signal;

var cookieOffcanvas = document.getElementById("offcanvasCookies");
var bsCookieOffcanvas = new bootstrap.Offcanvas(cookieOffcanvas);

cookieOffcanvas.addEventListener("show.bs.offcanvas", function () {
  document.body.addEventListener(
    "click",
    function (e) {
      e.stopPropagation();
    },
    { signal: signal }
  );
});
document.querySelectorAll(".cookie-form").forEach((item) => {
  item.addEventListener("submit", function () {
    bsCookieOffcanvas.hide();
    controller.abort();
  });
});
