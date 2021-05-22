$(document).ready(function () {
  // Once the DOM is loaded, it auto hides the billing
  $("#hidden-form-details").hide();
  // Removes the required attribute from billing fields.
  $(".billing-field").prop("required", false);
  // When the box is checked required is removed from certain field.
  // Else required is added to the billing fields.
  $("#billing-same").change(function () {
    if (this.checked) {
      $("#hidden-form-details").slideUp("slow");
      $(".billing-field").prop("required", false);
    } else {
      $("#hidden-form-details").slideDown("slow");
      $(".billing-field").prop("required", true);
    }
  });
});
