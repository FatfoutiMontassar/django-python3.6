$(function () {

  var scrolled = 0

  $("#btn-upload-picture").click(function () {
    $("#picture-input").click();
  });

  $("#picture-input").change(function() {
    $("#picture-upload-form").submit() ;
  });

  $("#picture-upload-form").submit(function () {
    var csrf = $("#picture-upload-form").attr("csrf");
    var to   = $("#picture-upload-form input[name=to]").val();
    var file = $("#picture-upload-form input[name=picture]").val();
    //alert("it works")
    $.ajax({
      url: '/messenger/send_image/',

      data: new FormData( this ),
      processData: false,
      contentType: false,
      /*
      data:{
        'to':to,
        'image':file,
        'csrfmiddlewaretoken': csrf
      },
      */
      cache: false,
      type: 'post',
      success: function (data) {
        //alert('success');

        $("#list-of-messages").append(data);
        $("input[name='message']").val('');
        $("input[name='message']").focus();

        scrolled=scrolled+10000;
        $("#list-of-messages").animate({
          scrollTop:  scrolled
        });

      }
    });
    return false;
  });

  $.fn.count = function (limit) {
    var length = limit - $(this).val().length;
    var form = $(this).closest("form");
    if (length <= 0) {
      $(".form-group", form).addClass("has-error");
    }
    else {
      $(".form-group", form).removeClass("has-error");
    }
    $(".help-count", form).text(length);
  };

  $(".list-group-item").click(function(){
    if($(this).hasClass("product")){
        if($(this).hasClass("active")){
          $(this).removeClass().addClass('list-group-item').addClass('product')
        }else{
          $(this).removeClass().addClass('list-group-item').addClass('active').addClass('product')
        }
    }
  });
  function fun(str1,str2){
    for(var i = 0 ; i <= str1.length-str2.length ; i++){
      var ret = true
      for(var j = 0 ; j < str2.length ; j++){
        if(str1[i+j] != str2[j]){
          ret = false
          break
        }
      }
      if(ret == true)return true
    }
    return false
  }
  $("#choose-list-search").keyup(function(){
    //alert("The text has been changed.");
    if($("#choose-list-search").val() != "" ){
      var input = $("#choose-list-search").val()
      $("#list-of-selected-products").children('a').each(function(){
        $(this).css('display','')
      });
      $("#list-of-selected-products").children('a').each(function(){
        product_name = $(this).attr("product-name")
        if(!fun(product_name.toLowerCase(),input.toLowerCase()) && !fun(input.toLowerCase(),product_name.toLowerCase())){
          //alert(product_name + "1")
          $(this).css('display','none')
        }else{
          //alert(product_name + "2")
        }
      });
    }else{
      $("#list-of-selected-products").children('a').each(function(){
        $(this).css('display','')
      });
    }
  });


  /*
  var previousVal = "";
  function InputChangeListener()
  {
     if($('#choose-list-search').val() != previousVal)
     {
       previousVal  = $('#choose-list-search').val();
       $('#choose-list-search').change();
     }
  }

  setInterval(InputChangeListener, 500);
  */

});
