// headerとfooterの表示
$(function () {
  "use strict";
  // $("header").load("./include/header.html");
  $("footer").load("./include/footer.html");
});

// 隠れているメニュー表示
$(document).ready(function () {
  "use strict";
  $(document).on("click", ".el_nav-text", function () {
    if ($(".bl_list-dropdown", this).css("display") == "none") {
      $(".bl_list-dropdown", this).slideDown();
    } else {
      $(".bl_list-dropdown", this).slideUp();
    }
  });
});
