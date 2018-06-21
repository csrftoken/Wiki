$(document).ready(function () {
  bindToolBarEvent();
  bindSummaryActive();
});


function isPc() {
  var userAgent = navigator.userAgent.toLowerCase();
  var bIsIpad = userAgent.match(/ipad/i) == "ipad";
  var bIsIphoneOs = userAgent.match(/iphone os/i) == "iphone os";
  var bIsMidp = userAgent.match(/midp/i) == "midp";
  var bIsUc7 = userAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
  var bIsUc = userAgent.match(/ucweb/i) == "ucweb";
  var bIsAndroid = userAgent.match(/android/i) == "android";
  var bIsCE = userAgent.match(/windows ce/i) == "windows ce";
  var bIsWM = userAgent.match(/windows mobile/i) == "windows mobile";

  if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
    return false;
  } else {
    return true;
  }
}

/*
 *  菜单栏拉伸效果
 */
function bindToolBarEvent() {

  $("img.js-toolbar-action").click(function () {
    var toggleClassEle = $(".book-summary");

    if (isPc()) {
      toggleClassEle.toggleClass("left");

      if (toggleClassEle.hasClass("left")) {
        $(".book-body").css({"left": "0"});
      } else {
        $(".book-body").css({"left": "300px"});
      }
    }else {
      toggleClassEle.parent().toggleClass("with-summary");

      if (toggleClassEle.parent().hasClass("with-summary")) {
        $(".book-body").css({"left": "300px"});
      } else {
        $(".book-body").css({"left": "0"});
      }
    }
  });

}

/*
 *  选中效果添加 `active`
 */
function bindSummaryActive() {
  $(".chapter a").each(function () {
    const pathName = window.location.pathname;
    const elePath = $(this).attr("href");
    if (pathName === elePath) {
      $(this).parent().addClass("active");
    }
  })
}