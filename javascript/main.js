// headerとfooterの表示
$(function () {
  "use strict";
  $("header").load("./include/header.html");
  $(".overlay").load("./include/overlay.html");
  $("footer").load("./include/footer.html");
});

// 隠れているメニュー表示
$(document).on("click", ".el_nav-text", function () {
  "use strict";
  if ($(".bl_list-dropdown", this).css("display") == "none") {
    $(".bl_list-dropdown", this).slideDown();
  } else {
    $(".bl_list-dropdown", this).slideUp();
  }
});

$(function () {
  "use strict";
  let topBtn = $(".el_top-btn");
  topBtn.hide();
  //スクロールが150に達したらボタン表示
  $(window).scroll(function () {
    if ($(this).scrollTop() > 150) {
      topBtn.fadeIn();
    } else {
      topBtn.fadeOut();
    }
  });
  //スクロールしてトップ
  topBtn.click(function () {
    $("body,html").animate(
      {
        scrollTop: 0,
      },
      500
    );
    return false;
  });
});

$(function () {
  "use strict";
  $(document).on("click", ".el_btn-nav", function () {
    $(".bl_overlay").fadeToggle();
    $(".el_btn-hm i").toggleClass("fa-bars").toggleClass("fa-times");
  });
});

$(function () {
  "use strict";

  $(document).on("click", ".bl_over-navItem", function () {
    if ($(".bl_over-acc", this).css("display") == "none") {
      $(".bl_over-acc", this).slideDown();
      $(".bl_over-navTxt .el_icon-toggle", this)
        .toggleClass("fa-plus")
        .toggleClass("fa-minus");
    } else {
      $(".bl_over-acc", this).slideUp();
      $(".bl_over-navTxt .el_icon-toggle", this)
        .toggleClass("fa-plus")
        .toggleClass("fa-minus");
    }
  });
});

// $(function () {
//   "use strict";
//   $(document).on("click", ".bl_overlay", function () {
//     $(".bl_overlay").fadeToggle(200);
//     $(".el_btn-hm i").toggleClass("fa-bars").toggleClass("fa-times");
//   });
// });
