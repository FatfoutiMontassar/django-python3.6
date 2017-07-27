$(document).ready(function(){
  $(".reaction").on("click",function(){   // like click
    var span = $(this).closest(".like-btn");
    var id = $(span).attr("product-id");
    var csrf = $(span).attr("csrf");
    //alert("product id : " + id)
    var data_reaction = $(this).attr("data-reaction");
    var function2call ;
    if(data_reaction == "Like")function2call = "/shop/reactionLike/" ;
    if(data_reaction == "Love")function2call = "/shop/reactionLove/" ;
    if(data_reaction == "Wow" )function2call = "/shop/reactionWow/"  ;


    $.ajax({
      url: function2call+id+'/',
      data: {
        'id': id,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $(".like-btn-emo" , span).removeClass().addClass('like-btn-emo').addClass('like-btn-'+data_reaction.toLowerCase());
      	$(".like-btn-text" , span).text(data_reaction).removeClass().addClass('like-btn-text').addClass('like-btn-text-'+data_reaction.toLowerCase()).addClass("active");;
        $(".like-count", span).text(data);
      	if(data_reaction == "Like")
      	  $(".like-emo" , span).html('<span class="like-btn-like"></span>');
      	else
      	  $(".like-emo" , span).html('<span class="like-btn-like"></span><span class="like-btn-'+data_reaction.toLowerCase()+'"></span>');

      }
    });
    return false ;
  });

  $(".like-btn-text").on("click",function(){ // undo like click
	  if($(this).hasClass("active")){
      var span = $(this).closest(".like-btn");
      var id = $(span).attr("product-id");
      var csrf = $(span).attr("csrf");
      //alert(id + " -- " + csrf )
      $.ajax({
        url: '/shop/reactionRemove/'+id+'/',
        data: {
          'id': id,
          'csrfmiddlewaretoken': csrf
        },
        type: 'post',
        cache: false,
        success: function (data) {
          $(".like-btn-text", span).text("Like").removeClass().addClass('like-btn-text');
    		  $(".like-btn-emo" , span).removeClass().addClass('like-btn-emo').addClass("like-btn-default");
    		  $(".like-emo" , span ).html('<span class="like-btn-like"></span>');
          $(".like-count", span).text(data);
        }
      });
      return false ;
	  }
  })





  $('.testOfJquery').on("click",function(){
    window.alert("ok!!")
    return false ;
  });
  $("ul.thumbnails").on("click", ".like", function () {
    var li = $(this).closest("li");
    var id = $(li).attr("product-id");
    var csrf = $(li).attr("csrf");
    //window.alert("like !!" + id)
    $.ajax({
      url: '/shop/likeProduct/'+id+'/',
      data: {
        'id': id,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        //window.alert("success :D")
        if ($(".like", li).hasClass("unlike")) {
          $(".like", li).removeClass("unlike");
          $(".like .text", li).css("color","black");
          $(".like .like-icon", li).attr("src","/static/themes/images/thumb-up.png");
        }
        else {
          $(".like", li).addClass("unlike");
          $(".like .text", li).css("color","blue");
          $(".like .like-icon", li).attr("src","/static/themes/images/thumb-up-blue.png");
        }
        $(".like-count", li).text(data);
      }
    });
    return false;
  });

  $("ul.thumbnails").on("click", ".smile", function () {
    var li = $(this).closest("li");
    var id = $(li).attr("product-id");
    var csrf = $(li).attr("csrf");
    //window.alert("like !!" + id)
    $.ajax({
      url: '/shop/smileProduct/'+id+'/',
      data: {
        'id': id,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        //window.alert("success :D")
        if ($(".smile", li).hasClass("unsmile")) {
          $(".smile", li).removeClass("unsmile");
          $(".smile .text", li).text("S");
        }
        else {
          $(".smile", li).addClass("unsmile");
          $(".smile .text", li).text("U");
        }
        $(".smile-count", li).text(data);
      }
    });
    return false;
  });

  $("ul.thumbnails").on("click", ".wish", function () {
    var li = $(this).closest("li");
    var id = $(li).attr("product-id");
    var csrf = $(li).attr("csrf");
    //window.alert("like !!" + id)
    $.ajax({
      url: '/shop/wishProduct/'+id+'/',
      data: {
        'id': id,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        //window.alert("success :D")
        if ($(".wish", li).hasClass("unwish")) {
          $(".wish", li).removeClass("unwish");
          $(".wish .text", li).text("W");
        }
        else {
          $(".wish", li).addClass("unwish");
          $(".wish .text", li).text("U");
        }
        $(".wish-count", li).text(data);
      }
    });
    return false;
  });
});
