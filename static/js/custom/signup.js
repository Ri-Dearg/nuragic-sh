$(document).ready(function () {
  $("#id_tnc").click(function () {
    if ($(this).prop("checked") == true) {
      $("#submit_register").attr("disabled", false);
    } else if ($(this).prop("checked") == false) {
      $("#submit_register").attr("disabled", true);
    }
  });
});
