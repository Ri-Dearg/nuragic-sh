// Confirms email address deletion
(function profileActions() {
  var message = "Do you really want to remove the selected email address?";
  var actions = document.getElementsByName("action_remove");
  if (actions.length) {
    actions[0].addEventListener("click", function (e) {
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  }
})();
