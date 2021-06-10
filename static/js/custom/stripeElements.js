function checkoutPage(cart, num_items, item_total, consent) {
  content_list = [];
  const cart_items = Object.keys(cart);
  cart_items.forEach((key, index) => {
    content_list.push({ id: key, quantity: cart[key] });
  });

  function pixelPurchase() {
    fbq("track", "Purchase", {
      content_name: `checkout`,
      content_type: "product",
      contents: content_list,
      currency: "EUR",
      num_items: num_items,
      value: item_total,
    });
  }

  var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
  var clientSecret = $("#id_client_secret").text().slice(1, -1);
  var stripe = Stripe(stripePublicKey);
  var elements = stripe.elements({
    fonts: [
      {
        family: "Montserrat",
        src: "local(Montserrat), url(https://fonts.gstatic.com/s/montserrat/v15/JTUSjIg1_i6t8kCHKm459WlhyyTh89Y.woff2) format('woff2')",
        display: "swap",
      },
    ],
  });
  var style = {
    base: {
      color: "#2b384c",
      fontFamily: "Montserrat, sans-serif",
      fontSize: "16px",
      "::placeholder": {
        color: "#6c757d",
      },
    },
    invalid: {
      color: "#ae1e2c",
      iconColor: "#ae1e2c",
    },
    complete: {
      color: "#2d764a",
      iconColor: "#2d764a",
    },
  };

  var card = elements.create("card", { style: style });
  card.mount("#card-element");

  card.addEventListener("change", function (event) {
    var errorDiv = document.getElementById("card-errors");
    if (event.error) {
      var html = `
            <span>${event.error.message}</span>
        `;
      $(errorDiv).html(html);
    } else {
      errorDiv.textContent = "";
    }
  });

  var form = document.getElementById("payment-form");

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    card.update({ disabled: true });
    $("#payment-submit").attr("disabled", true);
    $("#preloaderMessage").appendTo(".preload-gif").removeClass("d-none");
    $(".preloader").fadeIn("slow");

    var saveInfo = Boolean($("#id-save-info").prop("checked"));
    var billingSame = Boolean($("#billing-same").prop("checked"));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
      csrfmiddlewaretoken: csrfToken,
      client_secret: clientSecret,
      save_info: saveInfo,
      "billing-is-delivery": billingSame,
    };

    if (billingSame == true) {
      form.billing_full_name.value = form.shipping_full_name.value;
      form.billing_phone_number_0.value = form.shipping_phone_number_0.value;
      form.billing_phone_number_1.value = form.shipping_phone_number_1.value;
      form.billing_street_address_1.value =
        form.shipping_street_address_1.value;
      form.billing_street_address_2.value =
        form.shipping_street_address_2.value;
      form.billing_town_or_city.value = form.shipping_town_or_city.value;
      form.billing_county.value = form.shipping_county.value;
      form.billing_postcode.value = form.shipping_postcode.value;
      form.billing_country.value = form.shipping_country.value;
    }

    var url = "/shop/checkout/cache_data/";

    $.post(url, postData)
      .done(function () {
        stripe
          .confirmCardPayment(clientSecret, {
            payment_method: {
              card: card,
              billing_details: {
                address: {
                  city: $.trim(form.billing_town_or_city.value),
                  country: $.trim(form.billing_country.value),
                  line1: $.trim(form.billing_street_address_1.value),
                  line2: $.trim(form.billing_street_address_2.value),
                  postal_code: $.trim(form.billing_postcode.value),
                  state: $.trim(form.billing_county.value),
                },
                email: $.trim(form.email.value),
                name: $.trim(form.billing_full_name.value),
                phone: $.trim(
                  form.billing_phone_number_0.value +
                    form.billing_phone_number_1.value
                ),
              },
            },
            shipping: {
              address: {
                city: $.trim(form.shipping_town_or_city.value),
                country: $.trim(form.shipping_country.value),
                line1: $.trim(form.shipping_street_address_1.value),
                line2: $.trim(form.shipping_street_address_2.value),
                postal_code: $.trim(form.shipping_postcode.value),
                state: $.trim(form.shipping_county.value),
              },
              name: $.trim(form.shipping_full_name.value),
              phone: $.trim(
                form.shipping_phone_number_0.value +
                  form.shipping_phone_number_1.value
              ),
            },
          })
          .then(function (result) {
            if (result.error) {
              var errorDiv = document.getElementById("card-errors");
              var html = `
                <span>${result.error.message}</span>`;
              $(errorDiv).html(html);
              card.update({ disabled: false });
              $("#payment-submit").attr("disabled", false);
              $(".preloader").fadeOut("fast");
            } else {
              if (result.paymentIntent.status === "succeeded") {
                form.submit();
                if (consent == true) {
                  pixelPurchase();
                }
              }
            }
          });
      })
      .fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
      });
  });
}
