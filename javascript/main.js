"use strict";
{
  // headerとfooterの表示
  $(function () {
    $("header").load("./include/header.html");
    $("footer").load("./include/footer.html");
  });

  // 隠れているメニュー表示
  $(document).ready(function () {
    $(".el_nav-item").hover(
      function () {
        // $("ul:not(:animated)", this).slideDown();
        $(".bl_list-dropdown", this).slideDown();
      },
      function () {
        $(".bl_list-dropdown", this).slideUp();
      }
    );
  });
}
