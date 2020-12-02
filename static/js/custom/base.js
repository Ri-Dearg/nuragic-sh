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
                return response.json();
            } else {
                console.log(response)
                throw Error(response.statusText);
            }
        })
        // Fires off a toast notification
        .then(data => toastMessage(data.tag, data.message))
        // Catches any errors and displays their text message
        .catch(error => toastMessage("Error", error))
}

// Watches the form for submission, then fires the Fetch function
$("#news-form").on("submit", function (ev) {
    // stops form from sending
    ev.preventDefault();

    // The data sent in the form POST request.
    const formData = new FormData(this);

    // The URL for the form
    const formUrl = this.action;

    // Fires the main fetch function
    newsletterSignup(formData, formUrl);
})