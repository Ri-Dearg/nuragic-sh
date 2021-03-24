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
 * @param {string} likeUpdate - url for the view that updates the like popover.
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
  //   cartRefresh
) {
  /**
   * Switches the SVG icons when a button is pressed.
   * @param {string} btn - Either 'cart' or 'like' depending on which button is pressed.
   * @param {string} id - The specific product id, so other products aren't selected.
   * @param {object} svg - The SVG HTML element.
   */
  function svgSwitch(form, id, svg) {
    var classList = svg.classList;

    if (form === "lf") {
      if (classList.contains("bi-bookmark-heart-fill")) {
        $(`#lb-${id}`).html(unlikedSvg);
      } else if (classList.contains("bi-bookmark-heart")) {
        $(`#lb-${id}`).html(likedSvg);
      }
    }
    if (form === "cf") {
      if (classList.contains("bi-cart-check-fill")) {
        $(`#cb-${id}`).html(uncartedSvg);
      } else if (classList.contains("bi-cart-plus")) {
        $(`#cb-${id}`).html(cartedSvg);
      }
    }
  }

  /**
   * First deletes the popover, then clears the popover html
   * and then fires the view that refreshes the template.
   * @param {string} result - Either 'cart' or 'like' depending on which button is pressed.
   */
  function dropdownUpdate(result) {
    if (result === "like") {
      var update = likeUpdate;
    } else if (result === "cart") {
      var update = cartUpdate;
    }
    // Deletes the popover instance, necessary in bootstrap otherwise the new one won't load.
    var dropdownElList = [].slice.call(
      document.querySelectorAll(`.${result}-dropdown`)
    );
    var dropdownList = dropdownElList.map(function (dropdownEl) {
      return new bootstrap.Dropdown(dropdownEl);
    });
    for (dropdown in dropdownList) {
      if (dropdownList.hasOwnProperty(dropdown)) {
        dropdownList[dropdown].dispose();
      }
    }
    // Animates the icon before deleting the HTML and loading the template refresh.
    $(`.${result}-dropdown-container`).fadeTo("fast", 0, function () {
      $(`.${result}-dropdown-container`).html("").load(update);
      // Animates the icon, then initialises the popover.
      $(`.${result}-dropdown-container`)
        .delay(400)
        .fadeTo("slow", 1, function () {
          dropdownElList.map(function (dropdownEl) {
            return new bootstrap.Dropdown(dropdownEl);
          });
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

    // Swaps svg icons appropriately
    svgSwitch(formType, id, svg);

    // Sends form to Django view
    fetch(formUrl, {
      method: "POST",
      body: formData,
      credentials: "same-origin",
    })
      .then((response) => {
        // if the response is okay, goes switches icons
        if (response.ok) {
          return response.json();
        } else {
          // if there is an error, it fires a message and swaps back the svg icon
          var svg = object.firstElementChild.firstElementChild;
          svgSwitch(formType, id, svg);
          throw Error(response.status + " " + response.statusText);
        }
      })
      .then((data) => {
        if (data.result === "error") {
          var svg = object.firstElementChild.firstElementChild;
          svgSwitch(formType, id, svg);
          throw Error(data.message);
          // Refreshes the dropdowns
        } else if (data.result != "error") {
          toastMessage(data.tag, data.tagMessage, data.message);
          dropdownUpdate(data.result);
        }
      })

      // // Used on the product_detail.html template.
      // // If the product does not have multiple stock the button text switches.
      // if (data.special != "stocked") {
      //     if ($(`#btn-${id}`).length > 0) {
      //     $(`#btn-${id}`).contents().last()[0].textContent =
      //         "  Remove from Cart";
      //     }
      // }

      // // Used on the product_detail.html template o change button text.
      // if ($(`#btn-${id}`).length > 0) {
      //     $(`#btn-${id}`).contents().last()[0].textContent = "  Add to Cart";
      // }
      // //Used on the cart list page to remove items from view after being uncarted.
      // if (window.location.pathname == "/cart/") {
      //     if (data.special != "update") {
      //     $(`#cart-item-${id}`).fadeOut("slow");
      //     }
      //     // Refreshes the totals box. Works for both removing items and updating quantity.
      //     $("#totals-box").fadeTo("slow", 0, function () {
      //     $(`#totals-box`).html("").load(cartRefresh);
      //     $(`#totals-box`).delay(400).fadeTo("slow", 1);
      //     });
      // }
      // Send the message if anything else occurs.
      // } else {
      // toastMessage(data.tag, data.message);
      // }
      //     }
      //   })
      .catch((error) => toastMessage("danger", "Error", error));
  }
  $(`.toggle-form`).on("submit", function (ev) {
    // stops form from sending
    ev.preventDefault();

    // Fires the main fetch function
    fetchForm(this);
  });
}
