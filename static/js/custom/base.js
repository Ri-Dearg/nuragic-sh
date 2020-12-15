function toastMessage(tag, tagMessage, message) {
    // Sets the toast HTML.
    $(".toast-container").html(
        `<div class="toast" data-bs-delay="5000" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${tag}">
                <strong class="me-auto text-white">${tagMessage}</strong>
                    <button type="button" class="btn-close ms-2 mb-1" data-bs-dismiss="toast" aria-label="Close">
                    </button>
                        </div>
            <div class="toast-body">${message}</div>
        </div>`
    );
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl)
    })
    // Fires the toast.
    var toast;
    for (toast in toastList) {
        console.log(toastList[toast]);
        toastList[toast].show()
    }
}

function newsletterSignup(formData, formUrl) {

    // Sends form to Django view
    fetch(formUrl, {
            method: "POST",
            body: formData,
            credentials: "same-origin",
        })
        .then((response) => {
            if (response.ok) {
                const defHeight = $("#news-col").height()
                const defWidth = defHeight * 1.5
                $("#news-submit").css("max-height", defHeight).css("max-width", defWidth).fadeTo(300, 0, function() {
                    $(this).html('<object class="header-object" type="image/svg+xml" data="/static/icons/check-circle.svg"><img src="/static/icons/check-circle.svg" alt="Account" /></object>')
                        .fadeTo(300, 0.65)
                })

                return response.json();
            }
            else {
                $("#news-submit").prop("disabled", false).removeClass("disabled")
                throw Error(response.status + " " + response.statusText);
            }
        })
        // Fires off a toast notification
        .then(data => toastMessage(data.tag, data.tagMessage, data.message))
        // Catches any errors and displays their text message
        .catch(error => toastMessage("warning", "Error", error));
}

// Watches the form for submission, then fires the Fetch function
$("#news-form").on("submit", function(ev) {
    // stops form from sending
    ev.preventDefault();
    $("#news-submit").prop("disabled", true).addClass("disabled")
    // The data sent in the form POST request.
    const formData = new FormData(this);

    // The URL for the form
    const formUrl = this.action;

    // Fires the main fetch function
    newsletterSignup(formData, formUrl);
})
