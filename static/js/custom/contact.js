function captchaCallback(token) {
  const url = $("#recap-url").val();
  const formData = new FormData();
  formData.append("g-recaptcha-response", token);

  fetch(url, {
    method: "POST",
    body: formData,
    credentials: "same-origin",
  })
    .then((response) => {
      // if the response is okay, goes switches icons
      if (response.ok) {
        return response.json();
      } else {
        throw Error(response.status + " " + response.statusText);
      }
    })
    .then((data) => {
      if (data.result === "error") {
        throw Error(data.message);
      } else if (data.result === "success") {
        $("#contact-submit").prop("disabled", false);
      }
    })
    .catch((error) => toastMessage("danger", "Error", error));
}
