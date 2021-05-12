var cookieOffcanvas = document.getElementById("offcanvasCookies");
var bsCookieOffcanvas = new bootstrap.Offcanvas(cookieOffcanvas);

function cookieForm(object) {
  // The data sent in the form POST request.
  const formData = new FormData(object);
  // The URL that the POST data would be sent to.
  const formUrl = object.action;
  // Sends form to Django view
  fetch(formUrl, {
    method: "POST",
    body: formData,
    credentials: "same-origin",
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw Error(response.status + " " + response.statusText);
      }
    })
    .then((data) => {
      toastMessage(data.tag, data.tagMessage, data.message);
    })
    .catch((error) => toastMessage("danger", "Error", error));
}

cookieOffcanvas.addEventListener("shown.bs.offcanvas", function () {
  var bsModal = document.getElementsByClassName("modal-backdrop")[0];
  var myModal = bsModal.cloneNode(true);
  bsModal.classList.replace("show", "hide");
  bsModal.parentNode.appendChild(myModal);
});

bsCookieOffcanvas.show();

document.querySelectorAll(".cookie-form").forEach((item) => {
  item.addEventListener("submit", function (ev) {
    ev.preventDefault();
    cookieForm(this);
    bsCookieOffcanvas.hide();

    var backdrop = document.getElementsByClassName("modal-backdrop")[1];
    backdrop.classList.remove("show");
    backdrop.remove();
  });
});
