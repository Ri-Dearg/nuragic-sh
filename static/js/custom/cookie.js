var cookieOffcanvas = document.getElementById("offcanvasCookies");
var bsCookieOffcanvas = new bootstrap.Offcanvas(cookieOffcanvas);

cookieOffcanvas.addEventListener("shown.bs.offcanvas", function () {
  var bsModal = document.getElementsByClassName("modal-backdrop")[0];
  var myModal = bsModal.cloneNode(true);
  bsModal.parentNode.replaceChild(myModal, bsModal);
});

bsCookieOffcanvas.show();

document.querySelectorAll(".cookie-form").forEach((item) => {
  item.addEventListener("submit", function () {
    bsCookieOffcanvas.hide();
  });
});
