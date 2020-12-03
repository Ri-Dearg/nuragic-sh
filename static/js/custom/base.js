function toastMessage(tag, message) {
    // Sets the toast HTML.
    $(".toast-wrapper").html(
        `<div class="toast" data-delay="5000">
            <div class="toast-header bg-${tag}">
                <strong class="mr-auto text-white">${tag.charAt(0).toUpperCase() + tag.slice(1)}</strong>
                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="toast-body">${message}</div>
        </div>`
    );
    // Fires the toast.
    $(".toast").toast("show");
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
            } else {
                $("#news-submit").prop("disabled", false).removeClass("disabled")
                throw Error(response.status + " " + response.statusText);
            }
        })
        // Fires off a toast notification
        .then(data => toastMessage(data.tag, data.message))
        // Catches any errors and displays their text message
        .catch(error => toastMessage("error", error))
}

// Watches the form for submission, then fires the Fetch function
$("#news-form").on("submit", function (ev) {
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