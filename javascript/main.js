// headerとfooterの表示
$(function () {
  "use strict";
  $("header").load("./include/header.html");
  $(".overlay").load("./include/overlay.html");
  $("footer").load("./include/footer.html");
});

// グローバルメニュー内の隠れている項目表示
$(document).on("click", ".el_nav-text", function () {
  "use strict";
  if ($(".bl_list-dropdown", this).css("display") == "none") {
    $(".bl_list-dropdown", this).slideDown();
  } else {
    $(".bl_list-dropdown", this).slideUp();
  }
});

// ページ最上部に戻るためのボタン機能
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

// ハンバーガーメニューをクリックしてメニュー表示機能
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

// サムネイルをクリックするとメイン画像を切り替える機能
$(function () {
  "use strict";
  // どのサムネイルがクリックされたか分別
  $(".bl_chimg-item").each(function (i, image) {
    $(image).on("click", function () {
      // console.log(image);
      // クリックした画像のパスを取得
      let fig = $(image).find("img").attr("src");
      // console.log(fig);
      // console.log($(image).parent().find(".bl_chimg-item"));
      // 新たにメインとするcurrentクラスを付け替え
      let img_p = $(image).parent();
      $(img_p).find(".bl_chimg-item").removeClass("current");
      $(image).addClass("current");

      // 既存のメイン画像を消して新たなメイン画像を設置
      // console.log($(img_p).prev().find("img"));
      let img_main = $(img_p).prev().find("img");
      $(img_main).fadeOut(50, function () {
        $(img_main)
          .attr("src", fig)
          .on("load", function () {
            // console.log(img_main);
            // $(this).fadeIn();
            $(img_main).fadeIn();
          });
      });
    });
  });

  //
  // });
});
