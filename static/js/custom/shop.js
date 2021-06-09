function pixelAddToCart(id, title, quantity_field, price) {
  function cartClick() {
    quantity = Number($(`#${quantity_field}`).val());
    console.log(quantity);
    fbq("track", "AddToCart", {
      content_name: `${title}`,
      content_type: "product",
      contents: [{ id: `${id}`, quantity: quantity }],
      currency: "EUR",
      value: price,
    });
    $(`#cb-${id}`).off("click", cartClick);
  }
  $(`#cb-${id}`).on("click", cartClick);
}

function pixelViewContent(id, title, category, price) {
  fbq("track", "ViewContent", {
    content_category: category,
    content_ids: [id],
    content_name: `${title}`,
    content_type: "product",
    currency: "EUR",
    value: price,
  });
}

/**
 * Receives the like or cart button press, prevents the page reload and runs the function that
 * passes the info to a Python view.
 * On successful response, it receives the data it swaps the icon to indicate a button press.
 * It then deletes the popover content and fires another view which updates the popover templates and page context.
 * Animations are used throughout to smooth the experience.
 * @param {string} likedSvg - location of the SVG for a liked item.
 * @param {string} unlikedSvg - location of the SVG for an unliked item.
 * @param {string} cartedSvg - location of the SVG for a carted item.
 * @param {string} uncartedSvg - location of the SVG for an uncarted item.
 * @param {string} likeUpdate - urls for updating likes
 * @param {string} cartUpdate - url for the view that updates the cart popover.
 * @param {string} cartRefresh - url for the view that updates the cart totals box on the cart_list page.
 */
function buttonToggle(
  likedSvg,
  unlikedSvg,
  cartedSvg,
  uncartedSvg,
  likeUpdate,
  cartUpdate
) {
  /**
   * Switches the SVG icons when a button is pressed.
   * @param {string} btn - Either 'cart' or 'like' depending on which button is pressed.
   * @param {string} id - The specific product id, so other products aren't selected.
   * @param {object} svg - The SVG HTML element.
   */
  function svgSwitch(form, id, svg, formData) {
    var classList = svg.classList;

    if (form === "lf") {
      if (classList.contains("bi-bookmark-heart-fill")) {
        $(`#lb-${id}`).html(unlikedSvg);
      } else if (classList.contains("bi-bookmark-heart")) {
        $(`#lb-${id}`).html(likedSvg);
      }
    }
    if (form === "cf") {
      if (formData.get("special") === "update") {
        if (formData.get("quantity") == 0) {
          $(`#cb-${id}`)
            .html(uncartedSvg)
            .append("&nbsp;&nbsp;&nbsp;Add to Cart");
        } else {
          $(`#cb-${id}`)
            .html(cartedSvg)
            .append("&nbsp;&nbsp;&nbsp;Update Cart");
        }
      } else if (formData.get("special") === null) {
        if (classList.contains("bi-cart-check-fill")) {
          $(`#cb-${id}`).html(uncartedSvg);
        } else if (classList.contains("bi-cart-plus")) {
          $(`#cb-${id}`).html(cartedSvg);
        }
      }
    }
  }

  /**
   * First deletes the popover, then clears the popover html
   * and then fires the view that refreshes the template.
   * @param {array} result - Either 'cart' or 'like' for [0],
   * [1] is used for cart quantity updating depending on which button is pressed.
   */
  function offcanvasUpdate(result, formData, id) {
    if (result[0] === "like") {
      var update = likeUpdate;
    } else if (result[0] === "cart") {
      var update = cartUpdate;
      if (formData.get("special") === "remove") {
        $(`#cart-item-${id}`).slideUp();
      }
      $(`.cart-totals`).fadeTo("fast", 0, function () {
        $("#cart-items").text(`€${result[2]}`);
        $("#cart-delivery").text(`€${result[3]}`);
        $("#cart-grand").text(`€${result[4]}`);
        $(`.cart-totals`).fadeTo("fast", 1);
      });
      if (result[1] > 0) {
        $(`.quantity-badge`).text(result[1]);
      } else {
        $(`.quantity-badge`).text("");
      }
    }

    // Animates the icon before deleting the HTML and loading the template refresh.
    $(`.${result[0]}-offcanvas-container`).fadeTo("fast", 0.6);
    $(`.${result[0]}-offcanvas-content`).fadeTo("fast", 0, function () {
      $(`.${result[0]}-offcanvas-content`)
        .html("")
        // reloads the context and content
        .load(update, function () {
          $(`.${result[0]}-offcanvas-content`).fadeTo("fast", 1);
          $(`.${result[0]}-offcanvas-container`).fadeTo("fast", 1);
        });
    });
  }

  /**
   * The main ajax function. Captures the form data and sends it to the the python view.
   * The response it receives is in JSON format.
   * On success it uses the different variables received in the response to perform logic
   * and decide which action to perform in a specific context.
   * @param {object} object - The captured form element.
   */
  function fetchForm(object) {
    // Cart or like button of the product clicked.
    const formType = object.id.slice(0, 2);

    // The ID of the product clicked.
    const id = object.id.slice(3);

    // Gets svg classes for icon swapping
    var svg = object.firstElementChild.firstElementChild;

    // The data sent in the form POST request.
    const formData = new FormData(object);

    // The URL that the POST data would be sent to.
    const formUrl = object.action;

    if (svg != null) {
      // Swaps svg icons appropriately
      svgSwitch(formType, id, svg, formData);
    }

    // Sends form to Django view
    fetch(formUrl, {
      method: "POST",
      body: formData,
      credentials: "same-origin",
    })
      .then((response) => {
        $(".toggle-submit").prop("disabled", false).removeClass("disabled");
        // if the response is okay, goes switches icons
        if (response.ok) {
          return response.json();
        } else {
          // if there is an error, it fires a message and swaps back the svg icon
          var svg = object.firstElementChild.firstElementChild;
          if (svg != null) {
            svgSwitch(formType, id, svg, formData);
          }
          throw Error(response.status + " " + response.statusText);
        }
      })
      .then((data) => {
        if (data.result === "error") {
          var svg = object.firstElementChild.firstElementChild;
          if (svg != null) {
            svgSwitch(formType, id, svg, formData);
          }
          throw Error(data.message);
          // Refreshes the dropdowns
        } else if (data.result != "error") {
          toastMessage(data.tag, data.tagMessage, data.message);
          offcanvasUpdate(data.result, formData, id);
        }
      })
      .catch((error) => toastMessage("danger", "Error", error));
  }
  $(`.toggle-form`).on("submit", function (ev) {
    // stops form from sending
    ev.preventDefault();
    $(`.toggle-submit`).prop("disabled", true).addClass("disabled");

    // Fires the main fetch function
    fetchForm(this);
  });
}
