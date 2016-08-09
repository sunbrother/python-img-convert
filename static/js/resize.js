//图片加载成功
function loadSuccess(obj){
imgHW(obj.target);
}

//调整图片高宽
function imgHW(obj){
  var imgWidth, imgHeight;
  //var docRatio = mySwiper.width / mySwiper.height;
  //  var docRatio=document.body.clientWidth/document.body.clientHeight;
    var docRatio=window.innerWidth/window.innerHeight;
  //$('.img-wrapper img').each(function() {
    //alert("width:" + $(this).width() + "  height:" + $(this).height());
    var img = new Image();
    img.src = obj.src;
    /*img.onload=function(){*/
      imgWidth = img.naturalWidth;
      imgHeight = img.naturalHeight;
      //imgWidth = img.width;
      //imgHeight = img.height;
      var ratio = imgWidth / imgHeight;
      if (docRatio <= 1) {
        if (ratio >= 1) {
          $(obj).width("100%");
          $(obj).height("auto");
          //var top=(document.body.clientHeight-document.body.clientWidth*imgHeight/imgWidth)/2;
          var top=(window.innerHeight-window.innerWidth*imgHeight/imgWidth)/2;
          $(obj).css("margin-top",top+"px");
        } else {
          if (ratio >= docRatio) {
            $(obj).css("width", "100%");
            $(obj).css("height", "auto");
            //var top=(document.body.clientHeight-document.body.clientWidth*imgHeight/imgWidth)/2;
            var top=(window.innerHeight-window.innerWidth*imgHeight/imgWidth)/2;
            $(obj).css("margin-top",top+"px");
          } else {
            $(obj).width("auto");
            $(obj).height("100%");
          }
        }
      } else {
        if (ratio <= 1) {
          $(obj).width("auto");
          $(obj).height("100%");
        } else {
          if (ratio >= docRatio) {
            $(obj).css("width", "100%");
            $(obj).css("height", "auto");
            //var top=(document.body.clientHeight-document.body.clientWidth*imgHeight/imgWidth)/2;
            var top=(window.innerHeight-window.innerWidth*imgHeight/imgWidth)/2;
            $(obj).css("margin-top",top+"px");
          } else {
            $(obj).width("auto");
            $(obj).height("100%");
          }
        }
      }
}