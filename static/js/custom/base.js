/**
 * Fades the preloader once content is loaded.
 */
function fadePreload() {
  $(".preloader").fadeOut(1000);
}

/**
 * Fades in the preloader when a link is clicked.
 * Then you are sent to the link address.
 */
function smoothFade() {
  $(".smooth-click")
    .unbind("click")
    .on("click", function (ev) {
      ev.preventDefault();
      var goTo = this.getAttribute("href");
      $(".preloader").fadeIn(1000);
      setTimeout(function () {
        window.location = goTo;
      }, 800);
    });
}

/**
 * Fires any toasts on the page
 */
function showToast() {
  var toastElList = [].slice.call(document.querySelectorAll(".toast"));
  var toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl);
  });
  // Fires the toast.
  var toast;
  for (toast in toastList) {
    if (toastList.hasOwnProperty(toast)) {
      toastList[toast].show();
    }
    $(".toast").on("hidden.bs.toast", function () {
      $(this).remove();
    });
  }
}

/**
 * Creates a toast message after the parameters are passed from the Fetch function.
 * Is fired by the 'like' function.
 * @param {string} tag - Used as a header and a color class
 * @param {string} tagMessage - Header for the message
 * @param {string} message - The message to display in the toast
 */
function toastMessage(tag, tagMessage, message) {
  // Sets the toast HTML.
  $(".toast-container").prepend(
    `<div class="toast my-2" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${tag}">
                <strong class="me-auto text-white">${tagMessage}</strong>
                    <button type="button" class="btn-close ms-2 mb-1" data-bs-dismiss="toast" aria-label="Close">
                    </button>
                        </div>
            <div class="toast-body">${message}</div>
        </div>`
  );
  // Shows the toast
  showToast();
}

/**
 * Adds an email to the newsletter list. CHanges the icon
 * and disables the button if successful. If not, throws an erro notificaation.
 * Fires toast as feedback
 * @param {object} formData - Formdata from the request
 * @param {string} formUrl - url to send the data
 */
function newsletterSignup(formData, formUrl) {
  // Sends form to Django view
  fetch(formUrl, {
    method: "POST",
    body: formData,
    credentials: "same-origin",
  })
    .then((response) => {
      // if the response is okay, changes the icon and returns the data
      if (response.ok) {
        const defHeight = $("#news-col").height();
        const defWidth = defHeight * 1.5;
        $("#news-submit")
          .css("max-height", defHeight)
          .css("max-width", defWidth)
          .fadeTo(300, 0, function () {
            $(this)
              .html(
                `<svg class="bi" width="32"height="32" fill="currentColor"><use xlink:href="/static/icons/bootstrap-icons.svg#check-circle"></svg>`
              )
              .fadeTo(300, 0.65);
          });

        return response.json();
      } else {
        // if there is an error, it fires a message and removes the disabled class
        // from the submission button
        $("#news-submit").prop("disabled", false).removeClass("disabled");
        throw Error(response.status + " " + response.statusText);
      }
    })
    // Fires off a toast notification
    .then((data) => toastMessage(data.tag, data.tagMessage, data.message))
    // Catches any errors and displays their text message
    .catch((error) => toastMessage("warning", "Error", error));
}

// Watches the form for submission, then fires the Fetch function
$("#news-form").on("submit", function (ev) {
  // stops form from sending
  ev.preventDefault();
  $("#news-submit").prop("disabled", true).addClass("disabled");
  // The data sent in the form POST request.
  const formData = new FormData(this);

  // The URL for the form
  const formUrl = this.action;

  // Fires the main fetch function
  newsletterSignup(formData, formUrl);
});

// Runs the fade for the preloader once content has loaded.
window.onload = function () {
  window.document.body.onload = fadePreload();
  smoothFade();
};
