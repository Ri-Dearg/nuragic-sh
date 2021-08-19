// Inputs special values that are used for ajax logic processing to declare quantity update.
$(".update-button").on("click", function () {
  var id = this.id.slice(3);
  $(`#${id}-special-info`).remove();
  $(`#af-${id}`).append(
    `<input id="${id}-special-info" type="hidden" name="special" value="update"/>`
  );
});
// Inputs special values that are used for ajax logic processing to remove the product.
$(".remove-button").on("click", function () {
  var id = this.id.slice(3);
  $(`#${id}-special-info`).remove();
  $(`#af-${id}`).append(
    `<input id="${id}-special-info" type="hidden" name="special" value="remove"/>`
  );
});
